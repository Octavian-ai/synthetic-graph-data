from neo4j.v1 import GraphDatabase, Driver
from .classes import CypherQuery, QueryParams, DatasetName
from config import config
from lazy import lazy
from queue import Queue
from multiprocessing.pool import ThreadPool
from more_itertools import chunked
import uuid
from tqdm import tqdm

class NodeClient(object):
    class_singleton = None

    def __init__(self, uri, user, password):
        self._driver: Driver = GraphDatabase.driver(uri, auth=(user, password))
        self.instance = None
        self.batch = Queue(maxsize=100)
        self.count = 0
        self.executor = ThreadPool(1)
        self.in_flight = None

    @lazy
    def _session(self):
        return self._driver.session().__enter__()

    def execute_cypher(self, cypher: CypherQuery, query_params: QueryParams):
        # TODO: If you use this for writes then bad things can happen
        for x in self._session.run(cypher.value, **query_params.cypher_query_parameters):
            yield x

    def execute_cypher_once_per_id(self, cypher: CypherQuery, query_params: QueryParams, dataset_name, batch_size=8, id_limit=None, id_type="Node"):
        # TODO: If you use this for writes then bad things can happen
        total = id_limit/batch_size if id_limit is not None else None
        for node_ids in tqdm(chunked(self.get_node_ids(dataset_name, id_limit, id_type), batch_size), total=total):

            def read_tx(tx):
                queries = []
                for node_id in node_ids:
                    temp_query_params = QueryParams(id=node_id)
                    temp_query_params.update(query_params)
                    queries.append(tx.run(cypher.value, **temp_query_params.cypher_query_parameters))

                results = []
                for query in queries:
                    for x in query:
                        results.append(x)
                return results

            for x in self._session.read_transaction(read_tx):
                yield x

    def run(self, cypher: CypherQuery, query_params: QueryParams):
        # TODO: If you use this for writes then bad things can happen
        return self._session.run(cypher.value, **query_params.cypher_query_parameters)

    def get_node_ids(self, dataset_name, limit=None, tpe="NODE"):
        qy = "MATCH (n:" + tpe + " {dataset_name:{dataset_name}}) RETURN n.id" + (f" LIMIT {limit}" if limit is not None else "")
        get_node_cypher = CypherQuery(qy)
        for n in self.run(get_node_cypher, QueryParams(dataset_name=dataset_name)):
            yield uuid.UUID(n.value())

    def add_to_batch(self, cypher: CypherQuery, query_params: QueryParams):
        if not self.in_flight and not self.batch.empty():
            self.run_batch()
        elif self.batch.full():
            self.run_batch()

        self.batch.put((cypher, query_params), block=True)

    def run_batch(self):
        if self.in_flight:
            result = self.in_flight.get(timeout=60)
            assert result
            self.in_flight = None

        def execute_cypher(tx):
            batch = []
            while not self.batch.empty():
                cypher, query_params = self.batch.get(block=True, timeout=10)
                batch.append(tx.run(cypher.value, **query_params.cypher_query_parameters))
                self.count+=1
            return batch

        def run():
            session = self._session
            count_before = self.count
            result = session.write_transaction(execute_cypher)
            return result

        self.in_flight = self.executor.apply_async(run)
        return self.in_flight

    def execute_cypher_write(self, cypher: CypherQuery, query_params: QueryParams):
        execute_cypher = lambda tx: tx.run(cypher.value, **query_params.cypher_query_parameters)

        session = self._session
        result = session.write_transaction(execute_cypher)
        self.count+=1
        return result

    @staticmethod
    def get_client():
        if NodeClient.class_singleton is None:
            NodeClient.class_singleton = NodeClient(config.neo4j_url, config.neo4j_user, config.neo4j_password)
        return NodeClient.class_singleton

    @staticmethod
    def close_client():
        NodeClient.class_singleton._session.__exit__(None, None, None)
        NodeClient.class_singleton.executor.close()
        NodeClient.class_singleton._driver.close()

    @property
    def _nuke_db_query(self):
        return CypherQuery("MATCH (n) DETACH DELETE n")

    def nuke_db(self):
        self.instance.execute_cypher(self._nuke_db_query, QueryParams())


class SimpleNodeClient(NodeClient):
    def __init__(self):
        self.instance: NodeClient = None
        # deliberately not calling super

    def __enter__(self) -> NodeClient:
        self.instance = NodeClient.get_client()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.batch.empty():
            self.run_batch()
        NodeClient.close_client()
        self.instance = None
        return

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def __setattr__(self, name, value):
        if name == 'instance':
            super(SimpleNodeClient, self).__setattr__(name, value)
            return
        return setattr(self.instance, name, value)

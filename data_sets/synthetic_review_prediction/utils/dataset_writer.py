from graph_io import SimpleNodeClient, CypherQuery, QueryParams
from ..classes import GraphNode, GraphEdge, IsGoldenFlag
from graph_io.classes.dataset_name import DatasetName
from typing import Set, AnyStr
from multiprocessing.pool import ThreadPool
from multiprocessing.queues import Queue
from uuid import UUID


class DatasetWriter(object):
    ADDITIONAL_NODE_PROPERTIES: Set[AnyStr] = {'id'}

    def __init__(self,
                 client: SimpleNodeClient,
                 dataset_name: DatasetName,
                 properties_to_ignore: Set[str] = set()
                 ):
        self.properties_to_ignore = properties_to_ignore
        self.dataset_name = dataset_name
        self._client = client
        self.pool = ThreadPool(1)

    def __enter__(self):
        # TODO: do query batching with a buffer etc. to increase performance
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.run_batch()
        # TODO: on non error exits wait until the buffer has all flushed
        pass

    def nuke_dataset(self):
        query = CypherQuery("""
            MATCH (n:NODE {dataset_name: $dataset_name})
            WITH n LIMIT 1000
            DETACH DELETE n
            RETURN count(*);
            """)
        self._client.execute_cypher_write(query, QueryParams(dataset_name=self.dataset_name))

    def create_node_if_not_exists(self, node: GraphNode, properties: Set[AnyStr]):  # TODO: define properties on the node entity itself?
        properties = properties.union(self.ADDITIONAL_NODE_PROPERTIES)

        query_params = self._get_properties_for_query(node, properties)

        create_query = CypherQuery(f"MERGE (n:{node.label_string} {query_params.query_string} )")

        result = self._client.add_to_batch(create_query, query_params)
        # TODO: check that result wasn't an error

    def create_edge_if_not_exists(self, edge: GraphEdge, properties: Set[AnyStr]):
        _from = edge._from
        _to = edge._to

        query_params = self._get_properties_for_query(edge, properties)

        match = f"MATCH (from:{_from.label_string} {{ id: $from_id }}), (to:{_to.label_string} {{ id: $to_id }})"
        merge = f"MERGE (from)-[r:{edge.relationship} {query_params.query_string} ]->(to)"

        create_query = CypherQuery(match + "\n" + merge)
        query_params = query_params.union(QueryParams(from_id=str(_from.id.value), to_id=str(_to.id.value)))

        result = self._client.add_to_batch(create_query, query_params)

    def _get_properties_for_query(self, node, properties, prefix=None):
        properties.add('is_golden')

        properties_dict = {
            name if not prefix else f"{prefix}_{name}": getattr(node, name) for name in properties if name not in self.properties_to_ignore
        }

        query_params = QueryParams(dataset_name=self.dataset_name, **properties_dict)
        return query_params

from ..classes import PersonWroteReview, ReviewOfProduct, IsGoldenFlag
from typing import Set, AnyStr
import random

from ..meta_classes import DataSetProperties
from .simple_data_set import SimpleDataSet
from ..utils import DatasetWriter
from graph_io import QueryParams, CypherQuery
from uuid import UUID
from tqdm import tqdm


def run(client, data_set_properties: DataSetProperties):

    with DatasetWriter(client, data_set_properties.dataset_name) as writer:

        writer.nuke_dataset()
        print("Deleted previous data")

        data_set: SimpleDataSet = SimpleDataSet(data_set_properties)

        def create_indexes():
            client.execute_cypher_write(CypherQuery("CREATE INDEX ON :NODE(id)"), QueryParams())
            #client.execute_cypher_write(CypherQuery("CREATE INDEX ON :NODE(id, dataset_name)"), QueryParams())
            pass

        create_indexes()

        print("Created indices")

        for i, product in enumerate(tqdm(data_set.generate_public_products())):
            writer.create_node_if_not_exists(product, {"style"})

        print("Created product nodes")

        for i, person in enumerate(tqdm(data_set.generate_public_people())):
            writer.create_node_if_not_exists(person, {"style_preference"})

            for review in data_set.generate_reviews(person):
                review.test = random.random() <= 0.1
                writer.create_node_if_not_exists(review, {"score", "test"})
                writer.create_edge_if_not_exists(PersonWroteReview(review.by_person, review.id, IsGoldenFlag(False)), set())
                writer.create_edge_if_not_exists(ReviewOfProduct(review.id, review.of_product, IsGoldenFlag(False)), set())



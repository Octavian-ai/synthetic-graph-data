from .configure import create_data_set_properties
from ..experiment_1.generate import run
from graph_io.classes.dataset_name import DatasetName

DATASET_NAME = DatasetName('synthetic_review_prediction_experiment_5')


def gen_run(n):
	DATASET_NAME = DatasetName('review_hidden_real_'+str(n))
	return DATASET_NAME, lambda client: run(client, create_data_set_properties(DATASET_NAME, n))


runner = dict([gen_run(i) for i in range(1,7)])

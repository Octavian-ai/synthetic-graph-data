from .configure import create_data_set_properties
from ..experiment_1.generate import run as _run
from .configure import DATASET_NAME

def run(client):
    return _run(client, create_data_set_properties())

runner = {
	DATASET_NAME: run
}

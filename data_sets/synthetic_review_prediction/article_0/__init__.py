from .configure import DATASET_NAME, create_data_set_properties
from .generate import run as _run


def run(client):
    print(DATASET_NAME)
    return _run(client, create_data_set_properties())

runner = {
	DATASET_NAME: run
}

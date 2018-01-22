from collections import defaultdict
from .environment import Environment

# There are too many layers and too many files to this config system
default_values = {
    'neo4j_url': 'bolt://localhost',
    'neo4j_user': 'neo4j',
    'neo4j_password': 'local neo hates security!'
}

environment_box = Environment(None)


def set_environment(environment_name):
    environment_box.name = environment_name


def get(config_variable_name):
    # don't execute code in overrides till necessary
    from .overrides import overrides
    return overrides[environment_box.name].get(config_variable_name, default_values[config_variable_name])


class Config(object):
    @property
    def neo4j_url(self):
        return get('neo4j_url')

    @property
    def neo4j_user(self):
        return get('neo4j_user')

    @property
    def neo4j_password(self):
        return get('neo4j_password')


config: Config = Config()

import os

if 'ENVIRONMENT' not in os.environ:
    raise Exception("You must set an ENVIRONMENT variable. Sorry, I am very opinionated that we should not have a default value because it will mask misconfiguration issues later.")
set_environment(os.environ['ENVIRONMENT'])
import json
overrides = dict()

# There are too many layers and too many files to this config system
overrides.update(**{
    'remote': {
        'neo4j_url': 'bolt://796bafef-staging.databases.neo4j.io',
        'neo4j_user': 'readonly',
        'neo4j_password': '0s3DGA6Zq'
    },
    'floyd': { # Todo: implement me?
        'neo4j_url': 'bolt://796bafef-staging.databases.neo4j.io',
        'neo4j_user': 'readonly',
        'neo4j_password': '0s3DGA6Zq'
    },
    'local': { # Just uses defaults

    }
})

with open('./config/local_overrides.json') as f:
    overrides.update(json.load(f))
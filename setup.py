from setuptools import setup
from setuptools import find_packages


setup(name='generate-data',
      version='1.0.0',
      description='Generate data for graph ML experiments',
      author='Andrew Jefferson',
      author_email='andy@octavian.ai',
      url='https://github.com/Octavian-ai/generate-data',
      download_url='https://github.com/Octavian-ai/generate-data',
      license='MIT',
      install_requires=['numpy', 'neo4j-driver', 'lazy', 'tqdm', 'more-itertools'],
      packages=find_packages())
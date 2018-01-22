#!/usr/bin/env python3

if __name__ == '__main__':
	from graph_io import SimpleNodeClient
	import argparse

	from data_sets import runner

	parser = argparse.ArgumentParser()
	parser.add_argument('--dataset', type=str, choices=runner.keys())
	FLAGS = parser.parse_args()

	if FLAGS.dataset is None:
		print("Please select an experiment with --dataset. Available datasets:")
		for i in runner.keys():
			print(i)
		exit()

	with SimpleNodeClient() as client:
		run = runner[FLAGS.dataset]
		print("Generating...")
		run(client)
		print("... complete!")
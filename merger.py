#!/usr/bin/python3

import argparse
import json
import sys

parser = argparse.ArgumentParser(description="Merging the json files for easing the use of ./vassals_power.py")
parser.add_argument("--liege", nargs=1, help="Liege's JSON file")
parser.add_argument("--output", nargs=1, help="Liege of the vassals to merge")
parser.add_argument("vassals", nargs="+", help="Vassals' JSON files")

args = parser.parse_args()

with open(args.liege[0], "r") as l_file:
	root = json.load(l_file)

for vassal in args.vassals:
	with open(vassal, "r") as v_file:
		v = json.load(v_file)
		root['vassals'].append(v)

with open(args.output[0], "w") as out:
	json.dump(root, out, indent=4)

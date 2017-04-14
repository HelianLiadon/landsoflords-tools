#!/usr/bin/python3

import argparse
import json

# This function is the only thing you should need to edit


def process_domain_strength(population, army, activity):
	if 'halberdiers' in army: #Advanced mode
		army_strength = army['knights'] * 3 \
				+ army['catapults'] \
				+ army['crossbowmen'] \
				+ (army['battering_rams'] + army['archers'] \
					+ army['coutiliers'] + army['pikemen'] \
					+ army['halberdiers']) \
					/ 2. \
				+ army['rest'] / 4 

	else: #Simple mode
		army_strength = army['knights'] * 3 \
				+ army['catapults'] \
				+ army['rest'] / 2 \

	domain_raw = (population / 1000. + army_strength) / 2

	return domain_raw * activity


def ask_for(conversion_funct, request_str, exceptions=None):
	"""
	@exceptions: List of exceptions, each exception being a list composed
			of two elements: the value to match to be in the
			exception case, and the value to return in this
			situation.
	"""
	value = input(request_str)
	if exceptions is not None:
		for exception in exceptions:
			if value == exception[0]:
				return exception[1]

	try:
		return conversion_funct(value)
	except ValueError as ve:
		print("Invalid input ({})".format(ve))
		return ask_for(conversion_funct, request_str,
				exceptions=exceptions)


class Domain():
	def __init__(self, liege=None):
		self.vassals = []
		self.owner = ""
		self.liege = liege
		self.population = 0
		self.army = {}
		self.name = ""
		self.strength = 0
		self.t_strength = 0
		self.activity = 1

	def register(self, advanced=False):
		self.name = input("Domain name: ")
		self.owner = input("Owner: ")
		self.population = ask_for(int, "Population: ")
		
		self.army['knights'] = ask_for(int, "Number of knights: ")

		self.army['catapults'] = ask_for(int, "Number of catapults: ")
		if advanced:
			self.army['pikemen'] = ask_for(int, "Number of pikemen: ")
			self.army['halberdiers'] = ask_for(int, "Number of halberdiers: ")
			self.army['crossbowmen'] = ask_for(int, "Number of crossbowmen: ")
			self.army['archers'] = ask_for(int, "Number of archers: ")
			self.army['battering_rams'] = ask_for(int, "Number of battering_rams: ")
			self.army['coutiliers'] = ask_for(int, "Number of coutiliers: ")
		self.army['rest'] = ask_for(int, "Number of other military/auxiliary units: ")
		
		if advanced:
			activity = ask_for(float, "Owner's activity (multiplier, default=1): ",
				exceptions=[["", 1]])
		
		self.process_strength()

	def process_strength(self):
		self.strength = process_domain_strength(
			self.population, self.army, self.activity)
	
	def printer(self):
		print(self)
		for vassal in self.vassals:
			vassal.printer()
	
	def total_strength(self):
		if self.t_strength:
			return self.t_strength
		
		total = self.strength
		for vassal in self.vassals:
			total += vassal.total_strength()
		
		self.t_strength = total
		return total

	def __str__(self):
		value = "{} has {} inhabitants, {} army points.\n".format(
			self.name, self.population, self.army)
		value += "Its vassals are: {}".format(
			str([i.name + " " for i in self.vassals]))
		return value
	

def to_jsonable(liege):
	l = {'population': liege.population,
		'army': liege.army,
		'name': liege.name,
		'owner': liege.owner,
		'vassals': [],
		'activity': liege.activity,
	}
	for vassal in liege.vassals:
		v = to_jsonable(vassal)
		l['vassals'].append(v)
	return l
			
def from_json(json, liege=None):
	l = Domain(liege=liege)
	l.population = json['population']
	l.name = json['name']
	if 'owner' in json:
		l.owner = json['owner']
	l.activity = json['activity']
	l.army = json['army']
	l.process_strength()
	for vassal_json in json['vassals']:
		l.vassals.append(from_json(vassal_json, liege=l))
		
	return l

def add_vassals(liege, advanced=False):
	if liege is None:
		return

	response = input("Add a vassal for {} ? [Y/n] ".format(liege.name))
	if response.lower() != "n" and response.lower() != "no":
		vassal = Domain(liege=liege)
		vassal.register(advanced=advanced)
		liege.vassals.append(vassal)
		add_vassals(vassal, advanced=advanced)
	else:
		print("")
		add_vassals(liege.liege, advanced=advanced)


def get_domains(advanced=False):
	print("Starting with highest liege:")
	root_domain = Domain()
	root_domain.register(advanced=advanced)
	
	add_vassals(root_domain, advanced=advanced)

	return root_domain


def sort_vassals(liege):
	liege.vassals = sorted(liege.vassals, key=lambda e: e.total_strength(), reverse=True)
	for vassal in liege.vassals:
		if len(vassal.vassals):
			sort_vassals(vassal)
	

def pretty_print(liege, indent=0):
	relat_str = ""
	if liege.liege is not None:
		relat_str = ": {}%".format(round(100 * liege.total_strength() / liege.liege.total_strength(), 2))
	
	tab = ""
	for i in range(indent):
		tab += "\t"

	owner = ""
	if liege.owner:
		owner = " ({})".format(liege.owner)
	
	print("{}{}{} {}".format(tab, liege.name, owner, strength))

	for vassal in liege.vassals:
		pretty_print(vassal, indent=indent+1)


parser = argparse.ArgumentParser(description="Calculating relative strength of a domain's vassals, recursively.")
parser.add_argument("--input", nargs='?', help="Input JSON file")
parser.add_argument("--output", nargs='?', help="Output JSON file")
parser.add_argument("--advanced", action='store_true', help="Advanced mode for input (more detailed army command-line input)")
args = parser.parse_args()

if args.input is None:
	root = get_domains(args.advanced)
else:
	with open(args.input, "r") as f:
		root = from_json(json.load(f))

sort_vassals(root)
pretty_print(root)

if args.output is not None:
	with open(args.output, "w") as f:
		json.dump(to_jsonable(root), f, indent=4)

input("\nPress Enter to exit")

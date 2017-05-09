#!/usr/bin/python3

import argparse
import json

import vassals_power

def get_military(json, army):
	for key in json['army']:
		if key not in army:
			army[key] = 0
		army[key] += json['army'][key]
	for vassal in json['vassals']:
		get_military(vassal, army)


def print_military(json):
	army = {}
	get_military(json, army)
	for troop in army:
		print("Number of {} : {}".format(troop, army[troop]))


def get_population(json):
	population = json['population']
	for vassal in json['vassals']:
		population += get_population(vassal)
	return population

def print_population(json):
	print("Total population : {}".format(get_population(json)))

def get_owners_and_nbr_domains(json):
	nbr_domains = 1
	owners = {json['owner']}
	for vassal in json['vassals']:
		dom, own = get_owners_and_nbr_domains(vassal)
		nbr_domains += dom
		owners |= own
	return nbr_domains, owners

def print_ratio_owners(json):
	if 'owner' not in json:
		return
	nbr_domains, owners = get_owners_and_nbr_domains(json)
	print("{} domains, {} owners : ratio of {}".format(nbr_domains,
			len(owners), round(nbr_domains / len(owners), 2)))

def get_owners(json, owners):
	if json['owner'] not in owners:
		owners[json['owner']] = 0
	owners[json['owner']] += \
		vassals_power.process_domain_strength(json['population'],
					json['army'], json['activity'])
	for vassal in json['vassals']:
		get_owners(vassal, owners)

def print_owners_strengths(json, nbr_owners):
	print("\nRelative strength of owners:")
	owners_dict = {}
	get_owners(json, owners_dict)
	owners = [(a, b) for a, b in owners_dict.items()]
	owners = sorted(owners, key=lambda e:e[1], reverse=True)
	t_strength = 0
	for owner in owners:
		t_strength += owner[1]
	position = 1
	for owner in owners[:nbr_owners]:
		print("{}- {} : {}%".format(position, owner[0],
				round(100 * owner[1] / t_strength, 2)))
		position += 1

def get_militarism(json, militarism):
	total_soldiers = 0
	for troop, nbr in json['army'].items():
		total_soldiers += nbr
	militarism[json['name']] = round(100 * total_soldiers
					/ (json['population'] / 50), 2)
	for vassal in json['vassals']:
		get_militarism(vassal, militarism)

def print_militarism(json, nbr_domains):
	print("\nMilitarism of domains:")
	militarism = {}
	get_militarism(json, militarism)
	domains = [(a, b) for a, b in militarism.items()]
	domains = sorted(domains, key=lambda e:e[1], reverse=True)
	position = 1
	for domain in domains[:nbr_domains]:
		print("{}- {} : {}%".format(position, domain[0], domain[1]))
		position += 1

parser = argparse.ArgumentParser(description="Getting some stats on a domain\
						and its vassals.")
parser.add_argument("--owners", nargs='?', help="Outputs a given number of\
		owners in the owners' strength ranking", default=15, type=int)
parser.add_argument("--militarism", nargs='?', help="Outputs a given number of\
		domains for the militarism ranking", default=15, type=int)
parser.add_argument("file", nargs=1, help="Path to input file")
args = parser.parse_args()

with open(args.file[0], "r") as f:
	root = json.load(f)
print_military(root)
print_population(root)
print_ratio_owners(root)
print_owners_strengths(root, args.owners)
print_militarism(root, args.militarism)

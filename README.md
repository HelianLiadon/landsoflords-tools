# Introduction

This repository is dedicated to tools for the browser game Lands of Lords. I do not own anything, blah blah. Just do what you want with it.

# Vassal's power

## Concept

This script is made to get the relative strength of all the vassals of
a domain, recursively. The scripts prompts for the data in input on the
command-line (a JSON file can as well be provided in replacement, in
order to allow users to share the effort of entering all the data) and
outputs the vassals sorted by strength, with the % of the liege's
strength they hold.

Typically, if you have such an output :
```
DomainA
	DomainB: 23%
	DomainC: 20%
		DomainD: 30%
		DomainE: 20%
	DomainF : 10%
```

DomainA has here 3 vassalS (B, C, F). B holds 23% of the strength of A,
C 20%, and F 10%. The sum isn't 100% since this is the % of the
strength of a domain and its vassals, so it includes the strength of
the domain in itself. A is in this case rather powerful, since it has
the same strength as all of its vassals combined.

The % are only concerning the direct liege. D owns 30% of the strength
of C, so it only owns `0.3 * 0.2 = 6%` of A's strength.


The way to measure the strength of a domain can vary from one user to
another, so the script is designed to allow the user to easily edit the
function used for computing the strength.


## Usage

`./vassals_power.py [--advanced] [--input <JSON_input_file_path>]
 	[--output <JSON_output_file_path>]`

`--advanced` is only useful when `--input` isn't used, and allows the
user to asks for more detailed input for the army. Without this option,
the only requested informations for the army are the number of knights,
catapults and the sum of the rest. With this option, the other military
units (halberdiers, pikemen, ...) will be asked for as well. This means
the user-defined function `process_domain_strength` (at the beginning
of `vassals_power.py`) will have to deal with both cases.

`--output` allows the user to dump the data he gave to the prompt into
a JSON file that will be then usable by `--input`. When using `--input`
the prompt will be disabled and all the required data will be taken
from the file. The strength will be recalculated according to the
user-defined function of this script (and not the one used by the
script that generated the JSON file).

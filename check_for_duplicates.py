"""
Usage:
	check_for_duplicates.py --target_file <target_file>

Options:
	--target_file <target_file> Path to the target dataset
"""
from docopt import docopt
from fasttext_test import read_label
import os

if __name__ == "__main__":
	arguments = docopt(__doc__)
	
	target_path = arguments["<target_file>"]

	s = set()
	c = 0
	with open(target_path, 'r', encoding='UTF-8') as f:
		for index, line in enumerate(f):
			if line in s:
				label = int(read_label(line))
				[4, 9, 2]
				if label not in [4, 9, 2, 10, 1]:
					c+=1
					print(line)
			else:
				s.add(line)


	print("Duplicates: " + str(c))
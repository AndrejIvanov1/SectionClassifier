"""
Usage:
	author_convert_data.py --source_file <source_file> --train_file <train_file> --test_file <test_file>

Options:
	--source_file <source_file> Path to file to convert
	--train_file <train_file> Path to the train dataset
	--test_file <test_file> Path to test dataset
"""
from docopt import docopt
import pandas as pd
"""
	Converts the data to a format the fastText library can work with
"""
if __name__ == "__main__":
	arguments = docopt(__doc__)
	train_dataset_path = arguments["<train_file>"]
	test_dataset_path = arguments["<test_file>"]
	source_file_path = arguments["<source_file>"]

	df = pd.read_csv(source_file_path)

	# Drop rows with missing abstract
	df.dropna(inplace=True) 

	#Get rid of newlines
	df['abstract'] = df['abstract'].apply(lambda abstract: abstract.replace('\n', ' '))
	df = df[['author_id', 'abstract']]

	df.to_csv(train_dataset_path, sep=' ', index=False, header=False)
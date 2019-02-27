"""

Usage:
	author_convert_data.py --source_file <source_file> --train_file <train_file> --test_file <test_file>

Options:
	--source_file <source_file> Path to file to convert
	--train_file <train_file> Path to the train dataset
	--test_file <test_file> Path to test dataset
"""
from docopt import docopt
from sklearn.model_selection import train_test_split
import pandas as pd
"""
	Input: a csv file of abstracts labeled with authors
	Output: the same file in a format fasttext can work with
"""

def save_df(df, path):
	df.to_csv(path, sep=' ', index=False, header=False)

if __name__ == "__main__":
	arguments = docopt(__doc__)
	train_dataset_path = arguments["<train_file>"]
	test_dataset_path = arguments["<test_file>"]
	source_file_path = arguments["<source_file>"]
	min_num_samples = 100
	max_num_samples = 200

	df = pd.read_csv(source_file_path)

	# Drop rows with missing abstract
	df.dropna(inplace=True) 

	#Get rid of newlines
	df['abstract'] = df['abstract'].apply(lambda abstract: abstract.replace('\n', ' '))
	df = df[['author_id', 'abstract']]
	df['author_id'] = df['author_id'].apply(lambda x: "__label__{}".format(x))
	cnt = df['author_id'].value_counts()
	df = df[df.isin(cnt.index[cnt > min_num_samples]).values]
	df = df[df.isin(cnt.index[cnt < max_num_samples]).values]
	#print(df['author_id'].value_counts())

	print("Number of labels: ", df['author_id'].nunique())

	df_train, df_test = train_test_split(df, test_size=0.2, shuffle=True, stratify=df['author_id'])

	print(train_dataset_path, test_dataset_path)
	save_df(df_train, train_dataset_path)
	save_df(df_test, test_dataset_path)
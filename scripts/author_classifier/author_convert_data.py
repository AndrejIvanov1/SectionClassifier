"""

Usage:
	author_convert_data.py --source_file <source_file> --train_file <train_file> --test_file <test_file> [--equalize] [--binary]

Options:
	--source_file <source_file> Path to file to convert
	--train_file <train_file> Path to the train dataset
	--test_file <test_file> Path to test dataset
	--binary True if we want to save only 2 classes
	--equalize True if we want the same number of samples for each author
"""
from docopt import docopt
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt
"""
	Input: a csv file of abstracts labeled with authors
	Output: the same file in a format fasttext can work with
"""

def save_df(df, path):
	df.to_csv(path, sep=' ', index=False, header=False)


def plot_cnt(df):
	temp = df.groupby(['author_id']).size().reset_index(name='counts').groupby(['counts']).size()
	temp.plot(kind='line', 
			  xticks=[5, 10, 50, 100, 150, 200, 300, 400],
			  ylim=(0, 200)).invert_xaxis()

	plt.show()

def authors_with_low_cnt(counts):
	for count in counts:
		print("Authors, < {} abstracts: {}".format(count, cnt.index[cnt < count].size))

if __name__ == "__main__":
	arguments = docopt(__doc__)
	train_dataset_path = arguments["<train_file>"]
	test_dataset_path = arguments["<test_file>"]
	source_file_path = arguments["<source_file>"]
	binary = arguments["--binary"]
	equalize = arguments["--equalize"]
	min_num_samples = 150
	max_num_samples = 200

	df = pd.read_csv(source_file_path)

	# Drop rows with missing abstract
	df.dropna(inplace=True) 

	print("Number of samples: {}".format(df.shape[0]))
	#Get rid of newlines
	df['abstract'] = df['abstract'].apply(lambda abstract: abstract.replace('\n', ' '))
	df = df[['author_id', 'abstract']]

	plot_cnt(df)
	cnt = df['author_id'].value_counts()
	print("Total number of authors: {}".format(cnt.size))
	authors_with_low_cnt([5, 10, 20, 50])

	df = df[df.isin(cnt.index[cnt > min_num_samples]).values]
	df = df[df.isin(cnt.index[cnt < max_num_samples]).values]

	if binary:
		df = df.loc[(df['author_id'] == 675) | (df['author_id'] == 587)]

	if equalize:
		df = df.groupby('author_id').head(min_num_samples)

	df['author_id'] = df['author_id'].apply(lambda x: "__label__{}".format(x))
	print("Number of labels: {}".format(df['author_id'].nunique()))

	df_train, df_test = train_test_split(df, test_size=0.2, shuffle=True, stratify=df['author_id'])

	print("Train counts: ", df_train['author_id'].value_counts())
	print("Test counts: ", df_test['author_id'].value_counts())
	print(train_dataset_path, test_dataset_path)
	save_df(df_train, train_dataset_path)
	save_df(df_test, test_dataset_path)
"""

Usage:
	author_convert_data.py --source_file <source_file> --train_file <train_file> --test_file <test_file> [--equalize] [--binary] [--first_author] [--preprocess] [--pad] [--plot]

Options:
	--source_file <source_file> Path to file to convert
	--train_file <train_file> Path to the train dataset
	--test_file <test_file> Path to test dataset
	--binary True if we want to save only 2 classes
	--equalize True if we want the same number of samples for each author
	--first_author True if we want only papers where the author is first
	--pad True if we want to equalize number of samples per author by duplicating sample
	--plot
"""
from preprocessing import preprocess
from docopt import docopt
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt
"""
	Input: a csv file of abstracts labeled with authors
	Output: the same file in a format fasttext can work with
"""

def save_df(df, path):
	df.to_csv(path, sep=' ', index=False, header=False, encoding='utf-8')


def plot_cnt(df):
	temp = df.groupby(['author_id']).size().reset_index(name='counts').groupby(['counts']).size()
	temp.plot(kind='line', 
			  xticks=[5, 10, 50, 100, 150, 200, 300, 400],
			  ylim=(0, 200)).invert_xaxis()

	plt.show()

def authors_with_low_cnt(counts):
	for count in counts:
		print("Authors, < {} abstracts: {}".format(count, cnt.index[cnt < count].size))

def pad_df(df):
	#temp = df.groupby(['author_id']).size().reset_index(name='counts')
	for author_id in df.author_id.unique():
		for i in range(4):
			df = df.append(df[df.author_id == author_id])

	df = df.groupby('author_id').head(max_num_samples)
	
	return df

if __name__ == "__main__":
	arguments = docopt(__doc__)
	train_dataset_path = arguments["<train_file>"]
	test_dataset_path = arguments["<test_file>"]
	source_file_path = arguments["<source_file>"]
	binary = arguments["--binary"]
	equalize = arguments["--equalize"]
	first_author = arguments["--first_author"]
	do_preprocess = arguments["--preprocess"]
	pad = arguments["--pad"]
	plot = arguments["--plot"]
	min_num_samples = 50
	max_num_samples = 200

	df = pd.read_csv(source_file_path, encoding='utf-8')

	# Drop rows with missing abstract
	df.dropna(inplace=True) 

	print("Number of samples: {}".format(df.shape[0]))
	#Get rid of newlines
	df['abstract'] = df['abstract'].apply(lambda abstract: abstract.replace('\n', ' '))

	if do_preprocess:
		df['abstract'] = df['abstract'].apply(lambda abstract: preprocess(abstract, 
																		  remove_stopwords=True,
																		  do_stem=True))

	if first_author:
		df = df.loc[df['is_a_first_author'] == '1']
		print("Number of first author samples: {}".format(df.shape[0]))
	
	df = df[['author_id', 'abstract']]

	if plot:
		plot_cnt(df)

	cnt = df['author_id'].value_counts()
	print("Total number of authors: {}".format(cnt.size))
	authors_with_low_cnt([5, 10, 20, 50])

	df = df[df.isin(cnt.index[cnt >= min_num_samples]).values]
	df = df[df.isin(cnt.index[cnt <= max_num_samples]).values]

	if binary:
		df = df.loc[(df['author_id'] == 675) | (df['author_id'] == 587)]

	if equalize:
		df = df.groupby('author_id').head(min_num_samples)

	if pad:
		df = pad_df(df)

	df['author_id'] = df['author_id'].apply(lambda x: "__label__{}".format(x))
	print("Number of labels: {}".format(df['author_id'].nunique()))

	df_train, df_test = train_test_split(df, test_size=0.2, shuffle=True, stratify=df['author_id'])

	print("Train counts: ", df_train['author_id'].value_counts())
	print("Test counts: ", df_test['author_id'].value_counts())
	print(train_dataset_path, test_dataset_path)
	save_df(df_train, train_dataset_path)
	save_df(df_test, test_dataset_path)
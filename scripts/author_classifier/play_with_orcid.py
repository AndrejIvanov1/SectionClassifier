import pandas as pd
import os 

filepath =  os.path.join("..", "..", "data", "orcid", "orcids.csv")
output_path = os.path.join("..", "..", "data", "orcid", "duplicate_names.csv")

def authors_with_duplicates(df):
	print("Total number of samples: {}".format(df.shape[0]))
	print("Number of authors: {}".format(df["orcid"].nunique()))

	df_duplicates = pd.concat(g.drop_duplicates(subset=["orcid"], keep="first") \
					for _, g in df.groupby(["firstname", "lastname"]) if len(g) > 1)
	df_duplicates = pd.concat(g for _, g in df_duplicates.groupby(["firstname", "lastname"]) if len(g) > 1)
	#print(df[['firstname', 'lastname', 'orcid']])

	return df_duplicates

def samples_from_duplicates(df):
	df_duplicates = authors_with_duplicates(df)
	print("Authors with duplicates: {}".format(df_duplicates['orcid'].nunique()))
	df_duplicates = df.loc[df['orcid'].isin(df_duplicates.orcid.values)]
	print("Samples of authors with duplicates: {}".format(df_duplicates.shape[0]))
	df_duplicates = df_duplicates[['firstname', 'lastname', 'orcid']].sort_values(by=["firstname", "lastname"])

	return df_duplicates

if __name__ == "__main__":
	df = pd.read_csv(filepath)
	df['orcid'] = df['orcid'].apply(lambda orcid: orcid.replace('https', 'http'))
	df['orcid'] = df['orcid'].apply(lambda orcid: orcid if orcid.startswith('http://') else 'http://' + orcid)
	
	df_duplicates = samples_from_duplicates(df)
	df_duplicates.to_csv(output_path, encoding='utf-8', index=False)

import pandas as pd
import os 

if __name__ == "__main__":
	filepath =  os.path.join("..", "..", "data", "orcid", "orcids.csv")
	df = pd.read_csv(filepath)

	print("Total number of samples: {}".format(df.shape[0]))
	print("Number of authors: {}".format(df["orcid"].nunique()))
	
	df = df.drop_duplicates(subset=["orcid"], keep="first")
	df = pd.concat(g for _, g in df.groupby(["firstname", "lastname"]) if len(g) > 1)

	print(df)


import pandas as pd

def augment_df(df, labeled_authors):
    for firstname, lastname, orcid, url in labeled_authors:
        if not contains(df, orcid, url):
            print("Adding ", firstname, lastname, orcid, url)
            df = add_author_entry(df, firstname, lastname, orcid, url)

    return df


def add_author_entry(df, firstname, lastname, orcid, url):
    new_row = pd.DataFrame([[firstname, lastname, orcid, url]], columns=list(df))
    df = df.append(new_row, ignore_index=True)

    return df

def contains(df, orcid, url):
    row = df[(df.orcid == orcid) & (df.url == url)]
    
    return row.shape[0] > 0

def has_pmc_id(df, pmc_id):
    return any([True for url in df.url.values if pmc_id in url])


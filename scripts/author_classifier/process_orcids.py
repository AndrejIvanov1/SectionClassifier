"""
Usage:
    process_orcids.py --target_file <target_file> 

Options:
    --target_file <target_file> File to process
"""
from docopt import docopt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import time

if __name__ == "__main__":
    arguments = docopt(__doc__)
    filepath = arguments["--target_file"]

    df = pd.read_csv(filepath)

    """
    print("Entries per unique author")
    print(df['orcid'].value_counts())"""

    df = df.sort_values(by=['firstname', 'lastname'])
    bool_series = df['lastname'].duplicated(keep=False)

    print(df[bool_series].head(100))


    
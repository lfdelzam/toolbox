#!/usr/bin/env python
"""A script to create a concoct input table from khmer abundance.txt output files"""

import argparse
import pandas as pd
import os
import sys

def samplenames_from_file(name_file):
    if name_file:
        with open(name_file, 'r') as name_file_h:
            return [l.strip() for l in name_file_h]
    else:
        return None

def main(args):
    sample_dfs = []

    samplenames = samplenames_from_file(args.samplenames)
    for i, sample in enumerate(args.quantfiles):
        if samplenames:
            samplename = samplenames[i]
        else:
            samplename = os.path.basename(sample)        
        sample_df = pd.read_table(sample, index_col=0, sep=',')
        
        sample_dfs.append((samplename, sample_df[args.column]))
    khmer_df = pd.DataFrame(index=sample_df.index)

    for sample, sample_df in sample_dfs:
        khmer_df['khmer_{0}_{1}'.format(args.column, sample)] = sample_df

    khmer_df.to_csv(sys.stdout, sep="\t", float_format="%.6f")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("quantfiles", nargs='+', help="Khmer abundance.csv files")
    parser.add_argument("--samplenames", default=None, help="File with sample names, one line each, Should be the same order and the same number as the abundance.txt files")
    parser.add_argument("--column", default='median', help="Column to use for abundance, default is median")
    args = parser.parse_args()
    
    main(args)

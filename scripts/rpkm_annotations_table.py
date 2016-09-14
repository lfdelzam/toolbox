#!/usr/bin/env python
"""A script to sum the rpkm values for all genes for each annotation."""

import pandas as pd
import argparse
import sys

def main(args):
    rpkm_table =pd.read_table(args.rpkm_table, index_col=0)
    annotations = pd.read_table(args.annotation_table, header=None, names=["gene_id", "annotation", "evalue"])

    annotation_rpkm = {}
    for annotation, annotation_df in annotations.groupby('annotation'):
        annotation_rpkm[annotation] = rpkm_table.ix[annotation_df.gene_id].sum()

    annotation_rpkm_df = pd.DataFrame.from_dict(annotation_rpkm, orient='index')
    # sort the columns of the dataframe
    annotation_rpkm_df = annotation_rpkm_df.reindex(columns=sorted(rpkm_table.columns))
    annotation_rpkm_df.to_csv(sys.stdout, sep='\t')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rpkm_table")
    parser.add_argument("annotation_table")
    args = parser.parse_args()
    main(args)

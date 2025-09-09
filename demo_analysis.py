#!/usr/bin/env python3
"""
Quick analysis script for quotes.csv
Produces:
 - printed top authors
 - printed top tags
 - saves simple plots to an output directory (requires matplotlib)
Usage:
    python demo_analysis.py --input quotes.csv --outdir assets
"""
import argparse
import os
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt


def load_csv(path):
    return pd.read_csv(path)


def top_authors(df, n=10):
    return df["author"].value_counts().head(n)


def top_tags(df, n=20):
    # tags column stores comma-separated tags
    tags_series = df["tags"].fillna("").apply(lambda s: [t.strip() for t in s.split(",") if t.strip()])
    flat = [t for sub in tags_series for t in sub]
    return Counter(flat).most_common(n)


def save_bar(counter_items, outpath, title):
    labels, values = zip(*counter_items)
    plt.figure(figsize=(8, 4))
    plt.barh(labels, values, color="tab:blue")
    plt.gca().invert_yaxis()
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="Path to quotes.csv")
    p.add_argument("--outdir", default="assets", help="Directory to save charts")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    df = load_csv(args.input)
    print(f"Loaded {len(df)} rows.")

    authors = top_authors(df, n=10)
    print("\nTop authors:")
    print(authors)

    tags = top_tags(df, n=20)
    print("\nTop tags (top 20):")
    for tag, cnt in tags:
        print(f"{tag}: {cnt}")

    # Save simple charts
    save_bar(list(authors.items()), os.path.join(args.outdir, "top_authors.png"), "Top Authors")
    save_bar(tags[:10], os.path.join(args.outdir, "top_tags.png"), "Top Tags (top 10)")
    print(f"Saved charts to {args.outdir}/")
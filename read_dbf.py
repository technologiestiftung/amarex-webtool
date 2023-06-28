import argparse

import geopandas as gpd
import pandas as pd


def read_file():
    """
    Read and print the contents of a DBF file.
    """
    # Convert DBF file to Pandas dataframe
    df = gpd.read_file(args.input_file).drop("geometry", axis=1)

    # Configure display
    df.index += 1
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)
    if args.n_rows:
        print(df.head(args.n_rows))
    else:
        print(df)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read a DBF file and print the contents to the console."
    )

    parser.add_argument("input_file", help="Path to the DBF file to read")
    parser.add_argument("--n_rows", type=int, help="Print only the first N rows")

    args = parser.parse_args()

    read_file()

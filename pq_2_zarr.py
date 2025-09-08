#!/bin/python3

import argparse
import pandas as pd
import xarray as xr
import zarr
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Convert a Parquet file into a zipped Zarr store (.zarr.zip)"
    )
    parser.add_argument("input", help="Input Parquet file")
    parser.add_argument("output", help="Output .zarr.zip filename")
    args = parser.parse_args()

    try:
        # Read parquet
        df = pd.read_parquet(args.input)

        # Convert to xarray Dataset
        ds = df.to_xarray()

        # Save to zipped Zarr
        ds.to_zarr(args.output, mode="w", consolidated=True)

        print(f"✅ Converted {args.input} → {args.output}")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

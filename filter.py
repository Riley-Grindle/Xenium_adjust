#!/opt/bitnami/python/bin/python3

import argparse
import sys

import polars as pl


def main():
    # Parse input arguments.
    args = parse_args()

    data_frame: pl.LazyFrame = pl.scan_parquet(args.transcript)  # type: ignore
    x_col = pl.col("x_location")
    y_col = pl.col("y_location")
    f_col = pl.col("feature_name")

    high_quality = pl.col("qv").gt(args.min_qv)

    x_in_bounds = (x_col >= args.min_x) & (x_col <= args.max_x)
    y_in_bounds = (y_col >= args.min_y) & (y_col <= args.max_y)

    not_control = (
        f_col.str.starts_with("NegControlProbe_").not_()
        & f_col.str.starts_with("antisense_").not_()
        & f_col.str.starts_with("UnassignedCodeword_").not_()
        & f_col.str.starts_with("NegControlCodeword_").not_()
        & f_col.str.starts_with("BLANK_").not_()
    )

    # Filter transcripts. Ignore negative controls
    data_frame = data_frame.filter(
        high_quality & x_in_bounds & y_in_bounds & not_control
    ).with_columns(
        # Change cell_id to number
        rank=pl.col("cell_id").rank("dense")
        - 1
    )
    # drop string cell_id and replace with numeric cell ID
    data_frame = data_frame.drop("cell_id").rename({"rank": "cell_id"})

    # Output filtered transcripts to CSV
    data_frame.collect().write_csv("filtered_transcripts.csv")


def parse_args():
    """Parses command-line options for main()."""
    summary = "Filter transcripts from transcripts.csv based on Q-Score threshold \
               and upper bounds on x and y coordinates. Remove negative controls."

    parser = argparse.ArgumentParser(description=summary)
    required_named = parser.add_argument_group("required named arguments")
    required_named.add_argument(
        "--transcript",
        required=True,
        help="The path to the transcripts.parquet file produced " + "by Xenium.",
    )
    parser.add_argument(
        "--min_qv",
        default="20.0",
        type=float,
        help="The minimum Q-Score to pass filtering. (default: 20.0)",
    )
    parser.add_argument(
        "--min_x",
        default="0.0",
        type=float,
        help=(
            "Only keep transcripts whose x-coordinate is greater than specified limit. "
            + "If no limit is specified, the default minimum value will be 0.0"
        ),
    )
    parser.add_argument(
        "--max_x",
        default="24000.0",
        type=float,
        help=(
            "Only keep transcripts whose x-coordinate is less than specified limit. "
            + "If no limit is specified, the default value will retain all "
            + "transcripts since Xenium slide is <24000 microns in x and y. "
            + "(default: 24000.0)"
        ),
    )
    parser.add_argument(
        "--min_y",
        default="0.0",
        type=float,
        help=(
            "Only keep transcripts whose y-coordinate is greater than specified limit. "
            + "If no limit is specified, the default minimum value will be 0.0"
        ),
    )
    parser.add_argument(
        "--max_y",
        default="24000.0",
        type=float,
        help=(
            "Only keep transcripts whose y-coordinate is less than specified limit. "
            + "If no limit is specified, the default value will retain all "
            + "transcripts since Xenium slide is <24000 microns in x and y. "
            + "(default: 24000.0)"
        ),
    )

    try:
        opts = parser.parse_args()
    except:
        sys.exit(0)

    return opts


if __name__ == "__main__":
    main()

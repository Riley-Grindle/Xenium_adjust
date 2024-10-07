import pandas as pd
import sys

def csv_to_parquet(csv_file, parquet_file):
    try:
        # Load CSV into a DataFrame
        df = pd.read_csv(csv_file)
        
        # Convert to Parquet format
        df.to_parquet(parquet_file, index=False)
        print(f"Conversion successful! File saved as {parquet_file}")
        
    except Exception as e:
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python csv_to_parquet.py <input_csv> <output_parquet>")
    else:
        input_csv = sys.argv[1]
        output_parquet = sys.argv[2]
        csv_to_parquet(input_csv, output_parquet)


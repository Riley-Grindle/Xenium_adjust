#!/bin/bash

for file in ./*.parquet; do
    python3 -c "
import pandas as pd
df = pd.read_parquet('$file')
df.to_csv('${file%.parquet}.csv', index=False)
"
    echo "Converted $file to CSV."
done

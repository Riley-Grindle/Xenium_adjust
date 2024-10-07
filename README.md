## Xenium_adjust

#Necessary Input Files

- config.toml (baysor params)
	- scale (number of pixels expected by largest cell radius, recommend: manual meeasurment)
	- scale_std (amount of variability allowed in cell radius, recommend: 0.8)
        - min_molecules_per_cell (use histogram of tx per cell from original xenium output, recommend: Median value)  
	- prior_segmentation_confidence (conservation of xenium segmentation in new calculation, recommend: 0.8)
	- n_cells_init (number of cells initially identified)
- custom_features.tsv (format: current_id \t replacement_id)
- subset_cells.csv (only if subsetting a ROI) 
- Xenium Sample Directory (output from XeniumRanger)

#Workflow

- pq_2_csv.sh <transcripts.parquet>
	`output : trandcripts.csv`

- subset_transcripts.py <transcripts.csv> <subset_cells.csv>
	`output : subset_transcripts.csv`

- csv_2_pq.py <subset_transcripts.csv>
	`output : transcripts.parquet (replace orig transcripts.parquet)`

- xenium_adjust.sh <work_dir_with_samples>
	`params : --baysor (run baysor segmentation) --rename (rename xenium probes)`
	`output : sample_dir (containing either baysor dir, or relabeled dir)` 

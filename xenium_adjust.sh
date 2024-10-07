#!/usr/bin/bash

data_directory=$1
rename=0
baysor=0

if [[ $2 == '--rename' ]] || [[ $3 == '--rename' ]] ; then
    rename=1
fi

if [[ $2 == '--baysor' ]] || [[ $3 == '--baysor' ]] ; then
    baysor=1
fi

if [[ $baysor == 1 ]]; then
    for dir in $data_directory/*; do
        if ! [ -e "$dir/filtered_transcripts.csv" ]; then
            if [ $(find "$dir/" -name "transcripts.parquet" 2>/dev/null) ]; then
                echo "Filtering transcripts : $dir"
                docker run -v $dir:/mnt/ quay.io/rgrindle/filter_transcripts_xenium:v.2.0
            fi
        fi
    done


    for dir in $data_directory/*; do
        if ! [ -e "$dir/segmentation_polygons.json" ]; then
            if [ $(find "$dir/" -name "filtered_transcripts.csv" 2>/dev/null) ]; then
                if [ $(ls $dir| grep config.toml) ]; then
                    echo "Baysor Segmenting : $dir"
                    docker run -v $dir:/mnt/ quay.io/rgrindle/baysor:v0.6.1
                else
                    echo "ERROR: config.toml does not exist in $dir"
                fi
            fi
        fi
    done
fi

if [[ $rename == 1 ]]; then
    for dir in $data_directory/*; do
        if [ $(find "$dir/" -name "gene_panel.json" 2>/dev/null) ] && [ $(find "$dir/" -name "custom_features.tsv" 2>/dev/null) ]; then
            echo "Xenium Relableling : $dir"
            docker run -v $dir:/mnt/ quay.io/rgrindle/xenium_relabel_tx:v2.0.0
        else
            if [ -d $dir ]; then
                echo "ERROR: custom_features.tsv or gene_panel.json do not exist"
            fi
        fi
    done
fi

if [[ $baysor == 1 ]]; then
    for dir in $data_directory/*; do

        if [ $(find "$dir/" -name "segmentation.csv" 2>/dev/null) ] && [ $(find "$dir/" -name "segmentation_polygons.json" 2>/dev/null) ] && [ $(find "$dir/" -name "relabled" 2>/dev/null) ]; then
            echo "Xenium Reconstruction : $dir"
            docker run -v $dir/relabled:/mnt/ quay.io/rgrindle/xenium_import_segmentation:v1.1.0
        elif [ $(find "$dir/" -name "segmentation.csv" 2>/dev/null) ] && [ $(find "$dir/" -name "segmentation_polygons.json" 2>/dev/null) ]; then
            docker run -v $dir:/mnt/ quay.io/rgrindle/xenium_import_segmentation:v1.1.0
        else
            echo "ERROR: segmentation.csv or segmentation_polygons.csv do not exist"
        fi
    done
fi

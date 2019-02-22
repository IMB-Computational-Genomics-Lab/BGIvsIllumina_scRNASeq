#!/bin/bash

# This script reformats filenames from the MGISEQ-2000 to 10x 
# Genomics Cell Ranger-compatible names.

# File inputs
WORKING_DIR=$(dirname $PWD)
INPUT_CSV=${WORKING_DIR}/metadata/samplesheet.csv
INDEX_CSV=${WORKING_DIR}/metadata/chromium-shared-sample-indexes-plate.csv

# Define output path
OUTPUT_DIR=/shares/powell/data/experimental_data/PROCESSING/BGISeq_scRNA

for N in 2 3 4 5; do
    # Read elements from INPUT_CSV
    LINE=$(sed -n ${N}p  "$INPUT_CSV")
    IFS="," read -r SAMPLE INDEX FASTQ_DIR <<< "$LINE"
    SAMPLE_NUMBER=$(( $N - 1 ))
    # Define paths to write files out to
    SAMPLE_OUTPUT_DIR=$OUTPUT_DIR/$SAMPLE
    # mkdir -p $SAMPLE_OUTPUT_DIR
    echo $SAMPLE $INDEX $FASTQ_DIR $SAMPLE_OUTPUT_DIR

    # Retrieve line that matches the sample index
    INDEX_LINE=$(grep '^'${INDEX} $INDEX_CSV)

    # Parse line into an array so we can access them by number
    IFS="," read -r -a INDEX_ARRAY <<< "$INDEX_LINE"

    # For every set of indices, build a new name
    for X in 1 2 3 4; do
        SEQ="${INDEX_ARRAY[${X}]}"
        SAMPLE_NAME=${SAMPLE}_${SEQ}_S${SAMPLE_NUMBER}

        # For every Lane, get the filename and rename it
        for Y in 1 2 3 4; do
            FILE_R1=$( ls ${FASTQ_DIR}/*L0${Y}_*_${X}_1.fq.gz )
            FILE_R2=$( ls ${FASTQ_DIR}/*L0${Y}_*_${X}_2.fq.gz )

            NEW_FILE_R1=${SAMPLE_NAME}_L00${Y}_R1_001.fastq.gz
            NEW_FILE_R2=${SAMPLE_NAME}_L00${Y}_R2_001.fastq.gz
            RENAME1_CMD="""cp "${FILE_R1[1]}" ${OUTPUT_DIR}/${NEW_FILE_R1}"""
            RENAME2_CMD="""cp "${FILE_R2[2]}" ${OUTPUT_DIR}/${NEW_FILE_R2}"""

            echo $RENAME1_CMD
            echo $RENAME2_CMD
        done
    done
done

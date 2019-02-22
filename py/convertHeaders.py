#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import argparse
import re
import gzip
import itertools
import multiprocessing as mp

# Fastq.gz module by Guillaume Filion
import gzopen

# Worker function to perform task over list of reads
def worker(chunk):
    return len(chunk)

# Retrieves arguments inputted by user
def parseArguments(args):
    # Retrieve from parser
    input_file = args.input
    output_file = args.output
    
    # Extract barcode from filename
    sample_index = input_file.split("_")[3]
    return input_file, output_file, sample_index


# Sets up arguments for user input
def setupParser():
    # Set up argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", action = "store", help = "fastq.gz file you want to convert", type = str)
    parser.add_argument("-o", "--output", action = "store", help = "Name of the file you want the converted file.", type = str)
    args = parser.parse_args()

    return(args)


# Code starts here
if __name__ == "__main__":
    args = setupParser()
    input_file, output_file, sample_index = parseArguments(args)
    
    with gzopen.gzopen(input_file) as input_fastq:
        for chunk in itertools.islice(input_fastq, 1e6):
            print chunk
        #worker_pool = mp.Pool(4)
        #processed = worker_pool.map(worker, input_fastq, chunksize = 1e6)
        #worker_pool.close()
        #worker_pool.join()
  
        #print processed
        #with gzip.open(output_file, "wb") as output_fastq:
        #    for line in input_fastq:
        #        parsed_line = parseLine(line, sample_index = sample_index)
        #        output_fastq.write(parsed_line)

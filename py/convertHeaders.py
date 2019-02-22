#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import argparse
import re
import gzip
import itertools
import multiprocessing as mp

# Fastq.gz module by Guillaume Filion
import gzopen

# Rewrite as illumina header
def convertIllumina(elements_dict, sample_index):
    template_str = "@{instrument}:{run_number}:{flowcell_id}:{lane}:{tile}:{x_pos}:{y_pos} {read}:N:0:{sample_number}\n"
    formatted_string = template_str.format(instrument = "MGISEQ2000",
                                           run_number = 1,
                                           flowcell_id = elements_dict["flowcell-id"],
                                           lane = elements_dict["lane"],
                                           tile = elements_dict["tile"],
                                           x_pos = elements_dict["x-pos"],
                                           y_pos = elements_dict["y-pos"],
                                           read = elements_dict["read_no"],
                                           sample_number = sample_index)
    return(formatted_string)


# Collect elements from BGI format
def parseBGI(header):
    # Get basic information from split
    header_split1 = header.split("_")
    sample_id = header_split1[0]
    sample_id = sample_id.replace("@", "")
    header_split2 = header_split1[1].split("/")
    paired_read_direction = (header_split2[1]).strip()
    seq_header = header_split2[0]

    # Get location of L (Lane number)
    lane_id = re.search("L\d+", seq_header).group(0)
    lane_id = int(lane_id.replace("L", ""))

    # Get location of C (x location)
    x_id = re.search("C\d+", seq_header).group(0)
    x_id = x_id[:4]
    x_id = int(x_id.replace("C", ""))

    # Get location of R (y location)
    y_id = re.search("R\d+", seq_header).group(0)
    # Shorten incase it's trailing
    y_id = y_id[:4]
    y_id = int(y_id.replace("R", ""))

    # Get run number (last part of the string)
    tile_number = seq_header[seq_header.index("R")+4:]

    # Get the device ID from the first part of the script
    flowcell_id = seq_header[:seq_header.index("L")]

    # Pack into dictionary
    elements_dict = {"sample-id": sample_id,
                     "lane": lane_id,
                     "x-pos": x_id,
                     "y-pos": y_id,
                     "tile": int(tile_number),
                     "flowcell-id": flowcell_id,
                     "read_no": paired_read_direction}
    return elements_dict

# Parses the entry
def parseLine(x, sample_index = ""):
    if x.startswith("@") and ("_" in x):
        elements_dict = parseBGI(x)
        converted_header = convertIllumina(elements_dict, sample_index)
        return(converted_header)
    else:
        return(x)


# Retrieves arguments inputted by user
def parseArguments(args):
    # Retrieve from parser
    input_file = args.input
    output_file = args.output
    
    # Extract barcode from filename
    sample_index = "AAGACGGA"
    #sample_index = input_file.split("_")[3]
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
        line_chunk =  islice(input_fastq, 1e6)

        for line in line_chunk:
            parsed_line = parseLine(line, sample_index = sample_index)
            print parsed_line
    #with gzopen.gzopen(input_file) as input_fastq:
    #    with gzip.open(output_file, "wb") as output_fastq:
            # This opens the fastq file as a datastream
            # Light on memory, takes forever though

    #        line_chunk =  islice(input_fastq, 24)
            
    #        for line in line_chunk:
    #            parsed_line = parseLine(line, sample_index = sample_index)
    #            output_fastq.write(parsed_line)
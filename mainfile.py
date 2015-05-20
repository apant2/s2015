#To Do:
#Output should have same name as input file, say what it does and what is next step.
#Miscanthus and maize files
#Comment every function in very basic words

# Look for others as well. Also offer them the choice of outputting as a tab delimited file or csv.

#To run script in terminal:
#  python mainfile.py [-i arg] [-d arg] [-f arg] [-c arg] [-o arg] [-t arg]


import pandas as pd
import numpy as np
import os

#Imports and cleans data for easy manipulation and usage.
def import_data(datafile):
    data = pd.read_csv(datafile, sep=" ", header=None, delim_whitespace=True)
    data = data[pd.notnull(data[0])]

    return(data)

#Taking in the data and the depth value, does the following for each block: returns the start position and end position in one array,
# and the depths for the individual components of the block
def desired_values(data, depth):
    blocks=[[[],[]]]
    j=0

    for i in range(len(data)-1):
        if(data[3].iloc[i]>=depth):
            blocks[j][1].append(data[3].iloc[i])
            try:
                if(data[3].iloc[i-1]<5):
                    blocks[j][0].append(data[1].iloc[i])
            except:
                pass
            if(data[3].iloc[i+1]<depth):
                blocks[j][0].append(data[2].iloc[i])
                blocks.append([[],[]])
                j+=1
    del blocks[-1]
    return(blocks)

#Taking in the blocks, desired filename, and desired output filetype, create a file in the specified directory
def statistics(blocks, name, iscsv=True):
    out_table = pd.DataFrame(columns=['Start','End', 'Std_Dev', 'Avg', 'Median'])
    i=0
    for block in blocks:
        vals=[]
        vals_np = np.array(block[1])

        start_pos = block[0][0]
        end_pos =block[0][1]
        std_dev = np.std(vals_np)
        avg = np.average(vals_np)
        med = np.median(vals_np)

        out_table.loc[i] = [start_pos, end_pos, std_dev, avg, med]
        i+=1

    name = datafile.replace(".bedCov", "outputval.csv")

    if not iscsv:
        out_table.to_csv(name, sep='\t')
    if iscsv:
        out_table.to_csv(name)

#Function to run for one file
def create_file(datafile, depth, iscsv):
    data = import_data(datafile)
    blocks = desired_values(data, depth)
    statistics(blocks, datafile, iscsv)

#Main function to run the script
def main(input_directory, depth, iscsv, filetype):
    files = os.listdir(input_directory)
    for f in files:
        if(f[-len(filetype):-1]+f[-1] == filetype):
            create_file(f, depth, iscsv)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='something')
    parser.add_argument("-i", "--inputdirectory", dest="input", default=os.getcwd(), type=string, help="The input directory of the files")
    parser.add_argument("-d", "--depth", dest="depth", default=5, type=int, help="Minimum depth of window")
    parser.add_argument("-f", "--filename", dest="filename", default="window_depth", help="name of the output file")
    parser.add_argument("-c", "--iscsv", dest="iscsv", default=True, help="If set to true, the output files will be csv files")
    parser.add_argument("-o", "--outputdirectory", dest="output", default=os.getcwd()+"/output", type=string, help="The output directory of the files")
    parser.add_argument("-t", "--filetype", dest="filetype", default='.bedCov', type=string, help="The input file extension")

    args=parser.parse_args()
    main(args.input, args.depth, args.iscsv, args.filetype)



#Don't hardcode anything.
# Let user choose depth of cutoff
# name of output file, but set a default for both (5, inputgroup.[depth]).
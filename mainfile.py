#To Do:
#Find and replace var_name 'hey' to something more meaningful
#Output should have same name as input file, say what it does and what is next step.
#Miscanthus and maize files
#Usage- comment out exactly how to execute file in terminal
#Comment every function in very basic words
#Don't hardcode anything. Let user choose depth of cutoff, name of output file, but set a default for both (5, inputgroup.[depth]). Look for others as well. Also offer them the choice of outputting as a tab delimited file or csv.


import pandas as pd
import numpy as np
#import warnings
import os
#import sys
import argparse

#warnings.simplefilter("error")

#To execute the entire script, execute the function whole_script_run() at the end of this script

#Import into pandas datatable and remove all nan values, reset row indices
def import_clean(datafile):
    data = pd.read_csv(datafile, sep=" ", header = None, delim_whitespace=True)
    #data = data.drop([1,2,3,4,5,7,8,10,11], axis=1)
    data = data[pd.notnull(data[0])]

    return(data)

#Creates a 3-D Array. Returns array of arrays, with each sub-array consisting of two arrays: (1) the start and end positions, and
# (2) the values in there
def desired_values(data, depth):
    hey=[[[],[]]]
    j=0

    for i in range(len(data)-1):
        if(data[3].iloc[i]>=depth):
            hey[j][1].append(data[3].iloc[i])
            try:
                if(data[3].iloc[i-1]<5):
                    hey[j][0].append(data[1].iloc[i])
            except:
                pass
            if(data[3].iloc[i+1]<depth):
                hey[j][0].append(data[2].iloc[i])
                hey.append([[],[]])
                j+=1
    del hey[-1]
    return(hey)

#Return std. dev,
def statistics(hey, datafile, iscsv):
    out_table = pd.DataFrame(columns=['Start','End', 'Std_Dev', 'Avg', 'Median'])
    i=0
    for elem in hey:
        vals=[]
        vals_np = np.array(elem[1])

        start_pos = elem[0][0]
        end_pos = elem[0][1]
        std_dev = np.std(vals_np)
        avg = np.average(vals_np)
        med = np.median(vals_np)

        out_table.loc[i] = [start_pos, end_pos, std_dev, avg, med]
        i+=1

    name = datafile.replace(".bedCov", "outputval.csv")

    if not csv:
        out_table.to_csv(name, sep='\t')
    if csv:
        out_table.to_csv(name)

#Function to run for one file
def wrapper_fn(datafile, depth, iscsv):
    data = import_clean(datafile)
    hey = desired_values(data, depth)
    statistics(hey, datafile, iscsv)

#Main function to run the script
def main(depth, iscsv):
    files = os.listdir(os.getcwd())
    for f in files:
        if(f[-6:-1]+f[-1] == 'bedCov'):
            wrapper_fn(f, depth, iscsv)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='something')
    parser.add_argument("-d", "--depth", dest="depth", default=5, type=int, help="Minimum depth of window")
    parser.add_argument("-f", "--filename", dest="filename", default="window_depth", help="name of the output file")
    parser.add_argument("-c", "--iscsv", dest="iscsv", default=TRUE, help="If set to true, the output files will be csv files")

    args=parser.parse_args()
    main(args.depth, args.iscsv)
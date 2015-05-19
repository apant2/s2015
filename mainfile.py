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
def desired_values(data):
    hey=[[[],[]]]
    j=0

    for i in range(len(data)-1):
        if(data[3].iloc[i]>=5):
            hey[j][1].append(data[3].iloc[i])
            try:
                if(data[3].iloc[i-1]<5):
                    hey[j][0].append(data[1].iloc[i])
            except:
                pass
            if(data[3].iloc[i+1]<5):
                hey[j][0].append(data[2].iloc[i])
                hey.append([[],[]])
                j+=1
    del hey[-1]
    return(hey)

#Return std. dev,
def statistics(hey, datafile):
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
    out_table.to_csv(name)

#Function to run for one file
def wrapper_fn(datafile):
    data = import_clean(datafile)
    hey = desired_values(data)
    statistics(hey, datafile)

#Run this funtion to execute this script for the directory it is placed in
def whole_script_run():
    files = os.listdir(os.getcwd())
    for f in files:
        if(f[-6:-1]+f[-1] == 'bedCov'):
            wrapper_fn(f)

#ALL FUNCITONS BELOW ARE OLD VERSIONS OF FUNCTIONSS!!!! ~~SAVE FOR FUTURE USE IF NEEDED

#For each block of rows that contains values greater than or equal to 5, places their star positions, end positions and values in a tuple, then
#combines each tuple in a block, then puts every block in a different array
def old_fn_2(data):
    hey=[[]]
    j=0

    for i in range(len(data)-1):
        if(data[12].iloc[i]>=5):
            hey[j].append((data[6].iloc[i], data[9].iloc[i], data[12].iloc[i]))
            if(data[12].iloc[i+1]<5):
                hey.append([])
                j+=1
    return(hey)

#Copute mean, standard deviation and -- for each block
def old_fn_3(hey):
    for elem in hey:
        vals=[]
        for elem1 in elem:
            vals.append(elem1[2])
        vals_np = np.array(vals)
        print(np.std(vals_np))
        print(np.average(vals_np))



whole_script_run()
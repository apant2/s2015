#To Do:
#Miscanthus and maize files
#Comment every function in very basic words

#For help on how to run this script in bash, run the following:
#  python mainfile.py --help

import pandas as pd
import numpy as np
import csv
import os

#Cleans and returns data for easy usage by this script
def import_data(datafile):
    array=[]
    with open(datafile, 'r') as f:
        for line in f:
            words = line.split()
            if words:
                array.append(words)
    return array
    print(array)

#Taking in the cleaned data and the depth value, does the following for each block that it finds: returns the start position, end position,
# and all the depths for the individual components of the block
def desired_values(data, depth):
    blocks=[[[],[]]]
    j=0
    index = 0
    
    for row in data:
        if row:
            if(int(row[3])>=depth):
                blocks[j][1].append(int(row[3]))
                try:
                    if(int(data[index-1][3])<depth):
                        blocks[j][0].append(row[1])
                except:
                    if(index==0):
                        blocks[j][0].append(int(row[1]))
                    pass
                if(int(data[index+1][3])<depth or index == len(data)-1):
                    blocks[j][0].append(int(row[2]))
                    blocks.append([[],[]])
                    j+=1
            index+=1
    del blocks[-1]
    return(blocks)

def average(values):
    sum=0
    for elem in values:
        sum+=float(elem)
    
    return(sum/len(values))

def std_dev(values):
    var=0
    avg=average(values)
    for num in values:
        var+=((num-avg)**2)
    stdev=(var/len(values))**.5
    
    return stdev

def median(numericValues):
    theValues = sorted(numericValues)
    if len(theValues) % 2 == 1:
        return theValues[(len(theValues)+1)/2-1]
    else:
        lower = theValues[len(theValues)/2-1]
        upper = theValues[len(theValues)/2]
        return (float(lower + upper)) / 2


#Taking in the blocks, the name of the file being analyzed, the is CSV option, and the desired output filetype, this function creates an output file in the specified directory.
def statistics(blocks, name, depth, iscsv, outputdirectory):
    
    (root, ext) = os.path.splitext(name)
    exit_name = outputdirectory+root+str(depth)+".bedCov"
    
    #If the desired output directory does not exist, it is created
    if not os.path.exists(outputdirectory):
        os.makedirs(outputdirectory)
    
    out=[]
    i=0
    for block in blocks:
        vals=[]
        values = block[1]
        
        start_pos = int(block[0][0])
        end_pos = int(block[0][1])
        stddev = std_dev(values)
        avg = average(values)
        med = median(values)
        out.append((start_pos,end_pos,stddev,avg,med))
    
    if iscsv:
        f=open(exit_name, 'wt')
        try:
            writer = csv.writer(f)
            writer.writerow( ('Start','End', 'Std_Dev', 'Avg', 'Median') )
            for row in out:
                writer.writerow( (row[0], row[1], row[2], row[3],row[4]) )
        finally:
            f.close()

    if not iscsv:
        f=open(exit_name, 'wt')
        try:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow( ('Start','End', 'Std_Dev', 'Avg', 'Median') )
            for row in out:
                writer.writerow( (str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4])) )
        finally:
            f.close()

#Creates a file for one dataset
def create_file(datafile, depth, iscsv, outputdirectory):
    data = import_data(datafile)
    blocks = desired_values(data, depth)
    statistics(blocks, datafile, depth, iscsv, outputdirectory)

#converts some string version of the word "true" to its boolean expression; if the string inputted is not a form of 'true', returns false. Used in another function.
def isTrue(bool_statement):
    if bool_statement.lower()=='true':
        return True
    else:
        return False

#Main function to run the script
def main(input_directory, depth, iscsv, fileid, outputdirectory):
    files = os.listdir(input_directory)
    for f in files:
        if(fileid in f):
            create_file(f, depth, iscsv, outputdirectory)

#The below code will run only when this file is executed as the main file. When this file is imported as a module the code below will not execute.
if __name__ == '__main__':
    import argparse
    import time
    
    #Records the time before we start the script
    start_time = time.time()

    #Create the optional parameters this script can take in terminal
    parser = argparse.ArgumentParser(description='something')
    parser.add_argument("-i", "--inputdirectory", dest="input", default=os.getcwd(), help="The location of the files you want to run the script on.")
    parser.add_argument("-d", "--depth", dest="depth", default=5, type=int, help="The minimum depth of window you want to select.")
    parser.add_argument("-c", "--iscsv", dest="iscsv", default="True", help="If set to true, the output files will be comma separated value files. If false, they will be tsv files.")
    parser.add_argument("-o", "--outputdirectory", dest="outputdirectory", default=os.getcwd()+"/output/", help="The absolute output directory of the files this program creates.")
    parser.add_argument("-f", "--fileid", dest="fileid", default=".bedCov", help="The piece of text that identifies which files we want to run through this script.")
    args=parser.parse_args()
    
    #The running of the actual program; takes in the inputs from the user in the terminal.
    main(args.input, args.depth, isTrue(args.iscsv), args.fileid, args.outputdirectory)
    
    #Prints out how long it took for the script to run
    print("--- %s seconds ---" % (time.time() - start_time))


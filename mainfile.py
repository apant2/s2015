#To Do:
#Miscanthus and maize files
#Comment every function in very basic words

#For help on how to run this script in bash, run the following:
#  python mainfile.py --help

import pandas as pd
import numpy as np
import os

#Cleans and returns data for easy usage.
def import_data(datafile):
    data = pd.read_csv(datafile, header=None, delim_whitespace=True)
    data = data[pd.notnull(data[0])]

    return(data)

#Taking in the cleaned data and the depth value, does the following for each block that it finds: returns the start position, end position,
# and all the depths for the individual components of the block
def desired_values(data, depth):
    blocks=[[[],[]]]
    j=0

    for i in range(len(data)-1):
        if(data[3].iloc[i]>=depth):
            blocks[j][1].append(data[3].iloc[i])
            try:
                if(data[3].iloc[i-1]<depth):
                    blocks[j][0].append(data[1].iloc[i])
            except:
                if(i==0):
                    blocks[j][0].append(data[1].iloc[i])
                pass
            if(data[3].iloc[i+1]<depth or i == len(data)-2):
                blocks[j][0].append(data[2].iloc[i])
                blocks.append([[],[]])
                j+=1
    del blocks[-1]
    return(blocks)

#Taking in the blocks, the name of the file being analyzed, the is CSV option, and the desired output filetype, this function creates an output file in the specified directory.
def statistics(blocks, name, depth, iscsv, outputdirectory):
    out_table = pd.DataFrame(columns=['Start','End', 'Std_Dev', 'Avg', 'Median'])
    i=0
    for block in blocks:
        vals=[]
        vals_np = np.array(block[1])

        start_pos = int(block[0][0])
        end_pos = int(block[0][1])
        std_dev = np.std(vals_np)
        avg = np.average(vals_np)
        med = np.median(vals_np)

        out_table.loc[i] = [start_pos, end_pos, std_dev, avg, med]
        i+=1

    (root, ext) = os.path.splitext(name)
    exit_name = root+str(depth)+".bedCov"

    #If the desired output directory does not exist, it is created
    if not os.path.exists(outputdirectory):
        os.makedirs(outputdirectory)
    
    # If iscsv is false, creates the output file as a tsv file. IF true, creates the output file as a csv.
    if not iscsv:
        out_table.to_csv(outputdirectory+exit_name, sep='\t', index=False)
    if iscsv:
        out_table.to_csv(outputdirectory+exit_name, index=False)

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
    parser.add_argument("-c", "--iscsv", dest="iscsv", help="If set to true, the output files will be comma separated value files. If false, they will be tsv files.")
    parser.add_argument("-o", "--outputdirectory", dest="outputdirectory", default=os.getcwd()+"/output/", help="The output directory of the files this program creates.")
    parser.add_argument("-t", "--filetype", dest="fileid", default='.bedCov', help="The piece of text that identifies which files we want to run through this script.")    
    args=parser.parse_args()
    
    #The running of the actual program; takes in the inputs from the user in the terminal.
    main(args.input, args.depth, isTrue(args.iscsv), args.fileid, args.outputdirectory)
    
    #Prints out how long it took for the script to run
    print("--- %s seconds ---" % (time.time() - start_time))


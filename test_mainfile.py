#!/usr/local/bin/python
#/usr/lib/python2.7

#For help on how to run this script in bash, run the following:
#  python mainfile.py --help

#For proper output, all input files must be in the format as the block of text below:
#
#Scaffold810	132577	133699	0
#Scaffold810	133699	133703	4
#Scaffold810	133703	133706	7
#Scaffold810	133706	133707	8
#Scaffold810	133707	133709	10
#Scaffold810	133709	133710	16
#Scaffold810	133710	133714	17
#Scaffold810	133714	133723	18
#Scaffold810	133723	133724	16
#Scaffold810	133724	133725	13
#Scaffold810	133725	133730	12
#Scaffold810	133730	133731	11
#Scaffold810	133731	133734	3
#Scaffold810	133734	133736	2
#Scaffold810	133736	133738	1
#Scaffold810	133738	133753	11
#Scaffold810	133753	133761	10
#Scaffold810	133761	133798	0
#Scaffold810	133798	133819	1
#Scaffold810	133819	133969	0
#Scaffold810	133969	133990	1
#Scaffold810	133990	134039	0
#Scaffold810	134039	134043	1
#Scaffold810	134043	134044	2
#Scaffold810	134044	134046	3
#Scaffold810	134046	134047	7
#Scaffold810	134047	134054	10
#Scaffold810	134054	134061	11
#Scaffold810	134061	134068	10

#When this script is run from terminal with default values on the above data, the following is what the output file will contain:
#Scaffold,Start,End,Window Size,Std_Dev,Avg,Median
#Scaffold810,133703,133731,28,3.6551333764994136,12.8,12.5
#Scaffold810,133738,133761,23,0.5,10.5,10.5
#Scaffold810,134046,134068,22,1.5,9.5,10.0


import csv
import os

#Cleans and returns data in the above format for easy usage by this script
def import_data(datafile):
    data=[]
    with open(datafile, 'r') as f:
        for line in f:
            words = line.split()
            if words:
                data.append(words)
    return data


# Taking in the cleaned data (data) and the depth value (depth), does the following for every block of rows with depth greater than or equal to depth:
# Returns the start position, end position, and all the depths for the individual components of the block in an array
def desired_values(data, depth):
    blocks=[[[],[]]]
    j=0
    index = 0

    for row in data:
        if row:
            if(int(row[3])>=depth):
                blocks[j][1].append(int(row[3]))
                if(index==0):
                    blocks[j][0].append(row[0])
                    blocks[j][0].append(int(row[1]))
                elif(int(data[index-1][3])<depth):
                    blocks[j][0].append(row[0])
                    blocks[j][0].append(row[1])
                
                if(index == len(data)-1):
                    blocks[j][0].append(int(row[2]))
                    blocks.append([[],[]])
                elif(int(data[index+1][3])<depth):
                    blocks[j][0].append(int(row[2]))
                    blocks.append([[],[]])
                    j+=1
            index+=1
    del blocks[-1]

    return(blocks)

#Taking an array or list of values, returns the average of the values
def average(values):
    sum=0
    for elem in values:
        sum+=float(elem)
    
    return(sum/len(values))

#Taking an array or list of values, returns the standard deviation of the values
def std_dev(values):
    var=0
    avg=average(values)
    for num in values:
        var+=((num-avg)**2)
    stdev=(var/len(values))**.5
    
    return stdev

#Taking an array or list of values, returns the median of the values
def median(numericValues):
    theValues = sorted(numericValues)
    if len(theValues) % 2 == 1:
        return theValues[(len(theValues)+1)/2-1]
    else:
        lower = theValues[len(theValues)/2-1]
        upper = theValues[len(theValues)/2]
        return (float(lower + upper)) / 2


#Function input: array returned from desired_values, the name of the file being analyzed, the is CSV option, and the desired output directory
#What is returned by the function: A delimitered file with each row having the following information-
#Name of Scaffold, Start Position , End Position,Window Size (Difference of End and Start Position), Standard Deviation of the depths in each block, Average of the depths, Median of the depths

def statistics(blocks, name, depth, iscsv, outputdirectory):
    
    (root, ext) = os.path.splitext(name)
    exit_name = outputdirectory+root+".depth"+str(depth)+".bedCov"
    
    #If the desired output directory does not exist, it is created
    if not os.path.exists(outputdirectory):
        os.makedirs(outputdirectory)
    
    out=[]
    i=0
    for block in blocks:
        vals=[]
        values = block[1]
        
        scaffold=block[0][0]
        start_pos = int(block[0][1])
        end_pos = int(block[0][2])
        window_size = end_pos-start_pos
        stddev = std_dev(values)
        avg = average(values)
        med = median(values)
        out.append((scaffold,start_pos,end_pos,window_size,stddev,avg,med))
    
    d=","
    if not iscsv:
        d="\t"
    
    f=open(exit_name, 'wt')
    try:
        writer = csv.writer(f, delimiter=d)
        writer.writerow( ('Scaffold','Start','End','Window Size','Std_Dev', 'Avg', 'Median') )
        for row in out:
            writer.writerow( (row[0], row[1], row[2], row[3],row[4],row[5],row[6]) )
    finally:
        f.close()

#Creates a file for one dataset
#Function input: An input file in the above format, the cutoff value of the depth, whether the file is a csv (true) or tsv (false), and the output file's directory
#Function output: An output file
def create_file(datafile, depth, iscsv, outputdirectory):
    data = import_data(datafile)
    blocks = desired_values(data, depth)
    statistics(blocks, datafile, depth, iscsv, outputdirectory)

#Converts a string to a boolean value
#Function input: A string
#Function output: If it is some version of the word "true", returns boolean value True. Else, returns boolean value false
def isTrue(bool_statement):
    if bool_statement.lower()=='true':
        return True
    else:
        return False

#The main function of the script
#Function input: A directory that contains files with the format shown at the start of this script, the cutoff value of the depth, whether the file is a csv (true) or tsv (false), the slice of text which identifies the files we want to run through this script, and the directory of the output files
#Function output: In the directory outputdirectory, creates output files for each input file
def main(input_directory, depth, iscsv, fileid, outputdirectory):
    files = os.listdir(input_directory)
    for f in files:
        if(fileid in f):
            create_file(f, depth, iscsv, outputdirectory)

#The below code will run only when this file is executed as the main file. When this file is imported as a module into another the code below will not execute.
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


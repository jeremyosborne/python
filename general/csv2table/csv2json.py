"""Convert a csv file to a JSON data structure."""

import sys
import csv
import json
import os
import re

# pointer to our csv file descriptor
csvFile = None
columnNames = None
columnTypes = None
columnComments = None
validDataTypes = ["String", "Number"]
outfileName = None
outfileExtension = ".json"

def confirm(default=True):
    """Waits for user input, and exits on anything other than a string
    that begins with "Y" or "y".
    
    @param [default=True] {Boolean} Default response displayed to the user.
    Either "[Y/n]:" (if True) for a default affirmative or "[y/N]:" (if False)
    for a default negative.
    
    @return {Boolean} True if the user typed in an affirmative response, 
    False if not.
    """
    if default == True:
        print "[Y/n]: ",
    else:
        print "[n/Y]: ",
    
    response = raw_input()
    if len(response) == 0:
        return default
    elif len(response) and (response.lower()[0] == "y"):
        return True
    else:
        return False 

def createJSON():
    """Create the JSON data structure and output to file."""
    global columnNames, columnTypes, columnComments, outfileName

    print "\033[1;43m--Building JSON file--\033[1;m"
    
    # The resulting JSON structure will have two top level keys:
    #   "describe": an object describing the contents of each of the
    #   records in the "table rows".
    #   "data": an array of 1 to N number of objects, ordered in the
    #   same fashion as the underlying csv file.
    jsonStruct = {"describe":{}, "data":[]}
    
    # Build the describe structure
    for i in range(len(columnNames)):
        jsonStruct["describe"][columnNames[i]] = "{"+columnTypes[i]+"} "+columnComments[i]

    # Build each data field
    # Insert Data
    csvFile.seek(0)
    dataReader = csv.reader(csvFile)
    # skip the header rows
    counter = 0
    for row in dataReader:
        if counter < 3:
            counter += 1
            continue
        else:
            # Build the object
            dataObject = {}
            for columnNum in range(len(row)):
                if columnTypes[columnNum] == "String":
                    dataObject[columnNames[columnNum]] = row[columnNum]
                elif columnTypes[columnNum] == "Number":
                    # TODO: Do a simple conversion for numbers
                    # If the number has a decimal, it's a float.
                    # If the number has no decimal, it's an int.
                    if re.search("\.", row[columnNum]):
                        #print "Treating as a float"
                        dataObject[columnNames[columnNum]] = float(row[columnNum])
                    else:
                        #print "Treating as an int"
                        dataObject[columnNames[columnNum]] = int(row[columnNum])
            # add the "row" to our JSON "table"
            jsonStruct["data"].append(dataObject)
    
    print "The json that will be output to the file:"
    print json.dumps(jsonStruct)
    out = open(outfileName, "w")
    out.write(json.dumps(jsonStruct))
    out.close()

def computeSchema():
    """Determines the table schema for our csv file."""
    global csvFile, columnNames, columnTypes, columnComments
    
    print "\033[1;43m--Computing schema--\033[1;m"
    csvFile.seek(0)
    schema = csv.reader(csvFile)
    counter = 0
    for row in schema:
        if counter == 0:
            columnNames = row
        elif counter == 1:
            columnTypes = row
        elif counter == 2:
            columnComments = row
            break
        counter += 1
                
    print "We assume the first three rows in your csv file contain header info."
    print "If the information looks incorrect, you will have an opportunity"
    print "to exit and fix the csv file before creating the output table."
    print "--------------------------------------------------------------------"    
    print "Your column equivalents will be named (from the first row of data):"
    for column in range(len(columnNames)):
        print "{0:>5}: {1}".format(column, columnNames[column]) 
    
    print "The data types for the columns (from the second row of data):"
    for column in range(len(columnTypes)):
        print "{0:>5}: {1}".format(column, columnTypes[column])
    
    print "The descriptions of each column (from the third row of data):"
    for column in range(len(columnComments)):
        print "{0:>5}: {1}".format(column, columnComments[column])
    print ""

def reportFileStats():
    """Report any stats about the csv file."""
    # I think we need a new csv reader every time we want to view
    # the file.
    global csvFile, validDataTypes
    
    print "\033[1;43m--Computing file stats, checking integrity--\033[1;m"
    print "Number of columns in your table (determined from the first row):"
    csvFile.seek(0)
    columncount = 0
    counter = csv.reader(csvFile)
    for row in counter:
        columncount = len(row)
        break    
    print "    {0}".format(columncount)

    print "Number of rows in the csv file:"
    csvFile.seek(0)    
    counter = csv.reader(csvFile)
    rowcount = 0
    for row in counter:
        rowcount += 1
    print "    {0}".format(rowcount)
    
    print "Check table integrity: expected number of columns per row?"
    csvFile.seek(0)
    counter = csv.reader(csvFile)
    rowcount = 0
    isBadTable = False
    for row in counter:
        if len(row) != columncount:
            print "Error: row {0} has {1} columns, expected {2}".format(rowcount, len(row), columncount)
            isBadTable = True
        rowcount += 1
    if isBadTable == False:
        print "\033[1;32mTable integrity check PASS: expected dimensions.\033[1;m"
        print ""
    else:
        print "\033[1;31mTable integrity check FAIL: unexpected dimensions.\033[1;m"
        print ""
        sys.exit(1)

    print "Check table integrity: expected data types for each column?"
    print "Valid datatypes are:"
    for validType in validDataTypes:
        print "    {0}".format(validType)
    csvFile.seek(0)
    counter = csv.reader(csvFile)
    rowcount = 0
    isBadTable = False
    for row in counter:
        # data types are in the second row
        if rowcount == 1:
            columncount = 0
            for column in row:
                if column not in validDataTypes:
                    print "Error: column {0} has unexpected type {1}".format(columncount, column)
                    isBadTable = True
                columncount += 1
            # Only process the data type row
            break
        else:
            rowcount += 1
    if isBadTable == False:
        print "\033[1;32mTable integrity check PASS: expected datatypes.\033[1;m"
        print ""
    else:
        print "\033[1;31mTable integrity check FAIL: unexpected datatypes.\033[1;m"
        print ""
        sys.exit(1)

def init(filepath):
    """Kicks off the program by attempting to open the csv file."""
    global csvFile, outfileName
    
    # read stocks data, print status messages
    try:
        print "\033[1;43m--Opening csv file--\033[1;m"
        csvFile = open(filepath, "rb")
        print "\033[1;32mOpened csv file:", filepath,"\033[1;m"
        # Figure out output file name
        outfileMatches = re.match(r"([\w\S]*)(\.[^.]+$)", os.path.basename(filepath))
        if outfileMatches == None:
            # Handle the case where we don't have something that qualifies
            # as an extension to the file
            outfileName = filepath+outfileExtension
        else:
            outfileName = outfileMatches.group(1)+outfileExtension
                
        print "The JSON file will be named:", outfileName
        print "Is this correct?"
        if not confirm():
            print "Please input the complete output file name and path: "
            outfileName = raw_input()
            print "We will attempt to use the file at:", outfileName
            print "Is this okay?"
            if not confirm():
                print "We need an output file."
                print ""
                sys.exit()
        # TODO: choose a base table name, and inform the user that we will
        # attempt to use this name as the table name in the database.
        #
        # TODO: prompt for okayness from the user, default yes
        print ""
    except IOError:
        print "\033[1;31mFailed to open csv file:", sys.exc_info()[1],"\033[1;m"    
        print ""
        sys.exit(1)
    

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print "Usage:"
            print "python", sys.argv[0], "file2convert.csv"
            sys.exit(1)
        else:
            # process the file
            init(sys.argv[1]) 
            reportFileStats()
            computeSchema()
            createJSON()
            # natural exit
            sys.exit(0)
    except SystemExit:
        if csvFile:
            # Make sure to close the file
            csvFile.close()
        print "Exiting program."

import csv
import json

def getLastNames(csvReader):
    lastNames = {}
    dupNames = {}
    for row in csvReader:
        currName = row[2]
        #If dup found:
	    #add to dup name
 	#else:
	    #add to lastNames


def test():
    csvFileString = input("Enter name of CSV file")
    with open(csvFileString as csvFile:
        csvReader = csv.DictReader(csvFile, delimiter = ',')
        #answer = getLastNames(csvReader)
             

def main():
    print("Initial Commit")

if __name__ == "__main__":
    main()
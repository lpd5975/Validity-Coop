import csv
import json

def leven(str_one, str_two):
    str_one_len = len(str_one)
    str_two_len = len(str_two)
    if str_one_len == 0:
        return str_two_len        # If either string is empty, no need to create matrix
    elif str_two_len == 0:
        return str_one_len        # Same as previous note     
    else:
        matrix = [[0 for x in range(str_two_len + 1)] for y in range(str_one_len + 1)]
        for i in range(0, str_one_len + 1):
            for t in range(0, str_two_len + 1):
                if i == 0:
                    matrix[i][t] = t           # Fills up the first row and first col
                elif t == 0:
                    matrix[i][t] = i
                else:
                    cost = 1
                    if str_one[i-1] == str_two[t-1]:
                        cost = 0                        # Cost to edit char
                    insert = matrix[i][t-1] + 1         # If they are the same, no incr
                    delete = matrix[i-1][t] + 1         #  from previous cost
                    substitue = matrix[i-1][t-1] + cost
                    matrix[i][t] = min(insert, delete, substitue)
    return matrix[str_one_len][str_two_len]

def probablyTypo(str_one, str_two):
    return leven(str_one.lower(), str_two.lower()) < 3       # A typo/duplicate name will
                                                             #  most likely be below 3 edits

def findTypos(currName, lastNames):
    for key in lastNames:
        if probablyTypo(currName, key):
            return (True, key)
    return (False, "False") 

def getLastNames(csvReader):
    lastNames = {}
    dupNames = {}
    for row in csvReader:
        currName = row[2]
        If currName in lastNames:
            dupNames[currName] = row
            lastNames.pop(currName)
 	else:
	    lastNames[currName] = row


def test():
    csvFileString = input("Enter name of CSV file")
    with open(csvFileString) as csvFile:
        csvReader = csv.DictReader(csvFile, delimiter = ',')
        lastNames = getLastNames(csvReader)
        
                     

def main():
    print(leven("sun", "sunny"))

if __name__ == "__main__":
    main()
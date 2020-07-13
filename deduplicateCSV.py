import csv
import json

def leven(str_one, str_two):
    str_one_len = len(str_one)
    str_two_len = len(str_two)
    if str_one_len == 0:
        return str_two_len
    elif str_two_len == 0:
        return str_one_len
    else:
        matrix = [[0 for x in range(str_one_len + 1)] for y in range(str_one_len + 1)]
        for i in range(0, str_one_len + 1):
            for t in range(0, str_two_len + 1):
                if i == 0:
                    matrix[i][t] = t
                elif t == 0:
                    matrix[i][t] = i
                else:
                    cost = 1
                    if str_one[i-1] == str_two[t-1]:
                        cost = 0
                    insert = matrix[i][t-1] + 1
                    delete = matrix[i-1][t] + 1
                    substitue = matrix[i-1][t-1] + cost
                    matrix[i][t] = min(insert, delete, substitue)
    return matrix[str_one_len][str_two_len]

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
    with open(csvFileString) as csvFile:
        csvReader = csv.DictReader(csvFile, delimiter = ',')
        #answer = getLastNames(csvReader)
             

def main():
    print(leven("sun", "sunny"))

if __name__ == "__main__":
    main()
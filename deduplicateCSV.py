from itertools import combinations
import csv
import json

LAST_NAME_COL = 2
FIRST_NAME_COL = 1
STATE_COL = 10
PHONE_COL = 11


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

def dictManipulator(key, currName, row, dupNames, uniqueNames, allNames):
    if currName != key:
        if currName not in dupNames:
            dupNames[currName] = [row]
        else:
            dupNames[currName].append(row)
        if key not in dupNames:
            dupNames[key] = [allNames[key]]
        if key in uniqueNames:
            uniqueNames.pop(key)
        allNames[currName] = row
    else:
        if currName in dupNames:
            dupNames[currName].append(row)
        else:
            dupNames[currName] = [row]
            dupNames[currName].append(uniqueNames[currName])
        if currName in uniqueNames:
            uniqueNames.pop(currName)

def getLastNames(csvReader):
    uniqueNames = {}
    dupNames = {}
    allNames = {}
    for row in csvReader:
        currName = row[LAST_NAME_COL]
        (found, key) = findTypos(currName, allNames)
        #print("\n",found, currName, key)
        if found:
            dictManipulator(key, currName, row, dupNames, uniqueNames, allNames)
        else:
            allNames[currName] = row
            uniqueNames[currName] = row
        #print()
    return (uniqueNames, dupNames)

def isMatch(entry, dupList, dupNamesBool, entry_num):
    answer = dupNamesBool[entry_num]
    entry_num = entry_num + 1
    for entry2 in dupList:
        count = 0
        if probablyTypo(entry[FIRST_NAME_COL], entry2[FIRST_NAME_COL]):
            count += 1
        if entry[STATE_COL] == entry2[STATE_COL]:
            count += 1
        if probablyTypo(entry[PHONE_COL], entry2[PHONE_COL]):
            count += 1
        if count >= 2:
            dupNamesBool[entry_num] = True
            answer = True
        entry_num += 1
    return answer
        

def validateDuplicate(dupNames, uniqueNames):
    dupNamesList = []
    dupNamesBool = []
    entry_num = 0
    for key in dupNames:
        for val in dupNames[key]:
            dupNamesList.append(val)
            dupNamesBool.append(False)
    for entry in dupNamesList:
        if isMatch(entry, dupNamesList[entry_num+1:], dupNamesBool, entry_num):
            dupNamesBool[entry_num] = True
        entry_num += 1
    counter = 0
    for i in range(0, len(dupNamesBool)):
        if not dupNamesBool[i]:
            dupNamesList.pop(counter)
        else:
            counter = counter + 1
    uniqueNamesList = []
    for key in uniqueNames:
        uniqueNamesList.append(uniqueNames[key])
    return (uniqueNamesList, dupNamesList)        

def readCSV():
    csvFileString = input("Enter name of CSV file")
    with open(csvFileString) as csvFile:
        csvReader = csv.reader(csvFile, delimiter = ',')
        (uniqueNames, dupNames) = getLastNames(csvReader)
        (uniqueNamesList, dupNamesList) = validateDuplicate(dupNames, uniqueNames)
        print("\nDuplicate Names")
        for x in dupNamesList:
            print(x)
"""
        print()
        for x in dupNames:
            print(dupNames[x])
"""



def main():
    readCSV()    

if __name__ == "__main__":
    main()
from itertools import combinations
import csv
import json

"""
FileName: deduplicateCSV.py
Author: Liam Dougherty
Description: Reads a CSV file and outputs a JSON object listing
 duplicate and unique rows seperately.
"""


LAST_NAME_COL = 2       # Column numbers for the specified data
FIRST_NAME_COL = 1
STATE_COL = 10
PHONE_COL = 11

NUM_OF_COLS = 12       # Total Columns


"""
Dynamic Programming Implementaion of Levenshtein Algorithm.
Finds how similar two strings are from each other by the number of "edits" 
 (inserts, deletions, substitutions).

str_one (string): first string to be compared
str_two (string): second string to be compared

returns (int): the edit distacne between str_one and str_two
"""
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
                    insert = matrix[i][t-1] + 1         
                    delete = matrix[i-1][t] + 1        
                    substitue = matrix[i-1][t-1] + cost
                    matrix[i][t] = min(insert, delete, substitue)
    return matrix[str_one_len][str_two_len]


"""
Helper Fucntion to determine if two words are most likely typos or duplicates.

str_one (string): first string to be compared
str_two (string): second string to be compared

returns (bool): Whether or not two words are most likely typos
"""
def probablyTypo(str_one, str_two):
    return leven(str_one.lower(), str_two.lower()) < 3       # A typo/duplicate name will
        
                                                     #  most likely be below 3 edits
"""
Helper Function to find typos. Loops through a dictionary for keys and compares
  the current name to them with levenshtein algorithm.

currName (string): The current name to be compared
nameDict (dict): Dictionary with keys being last names and values being rows.

return ( (bool, string) ): Tuple containing whether or not a match was found and if so, the key of the match.
"""
def findTypos(currName, nameDict):
    for key in nameDict:
        if probablyTypo(currName, key):
            return (True, key)
    return (False, "False") 


"""
Manipulates the several dictionaries and places the found duplicate
  into the appropriate dictionaries. Goal is to seperate the unique names from the 
  possibly duplicate entries.

key (string): The key found in the allNames to match currName
currName (string): The current last name attempting to be placed in a dictionary
row ([string]): List of strings representing the entry in the CSV file
dupNames (dict): Contains all of the most likely duplicate entries
uniqueNames (dict): Contains all of the most likely unique entries
allNames (dict): COntains all of the names in the CSV file for refernce and comparison

return: VOID
"""
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


"""
Iterates through the CSV file to create dictionaries 
  containing the last names as keys and the values as CSV file entries.

csvReader (csv.reader): Class that allows for reading and manipulation of CSV files.

returns ( (dict, dict) ): Two dictionaries in a Tuple. One contians the unique entries,
  the other contains the most likely duplicate entries.
"""
def getLastNames(csvReader):
    uniqueNames = {}
    dupNames = {}
    allNames = {}
    for row in csvReader:
        currName = row[LAST_NAME_COL]
        (found, key) = findTypos(currName, allNames)
        if found:
            dictManipulator(key, currName, row, dupNames, uniqueNames, allNames)
        else:
            allNames[currName] = row
            uniqueNames[currName] = row
    return (uniqueNames, dupNames)


"""
Last resort function.
Used to compare two entries entirely if there is too little data to conclusively
  determine a possible duplciate or not. Goes through every item in each list and 
  compares each to determine duplication.

entry ([string]): List of strings representing a row in a CSV file
entry2 ([string]): List of strings representing a row in a CSV file

return (bool): Whether or not the two entries are duplicates.
"""
def checkEveryCell(entry, entry2):
    matches = 0
    empties = 0
    for i in range(0, NUM_OF_COLS):
        if len(entry2[i]) == 0 or len(entry[i]) == 0:
            empties += 1
        else:
            if probablyTypo(entry[i], entry2[i]):
                matches += 1
    if NUM_OF_COLS - empties == matches:
        return True
    else:
        return False


"""
Compares first names, state abbreviation, and phone number. If two
  of three are matching (given leven algo leeway), it is considered a duplicate.
If there is too much missing data and at least one piece of data matches, the 
  two entries will be sent to checkEveryCell.

entry ([string]): List of strings representing a row in a CSV file
dupList ([[string]]): List contaning all of the CSV file entries that are most likely duplicates
dupNamesBool ([bool]): List of bools corresponding with dupList. The index matching dupList
  is set to True if that entry is truly a duplciate.
entry_num (int): the entry index in dupList

return (bool): Whether or not the entry has found a duplicate
"""
def isMatch(entry, dupList, dupNamesBool, entry_num):
    answer = dupNamesBool[entry_num]
    entry_num = entry_num + 1
    for entry2 in dupList:
        count = 0
        missing_data = 0
        if len(entry2[FIRST_NAME_COL]) == 0 or len(entry[FIRST_NAME_COL]) == 0:
            missing_data += 1
        else:
            if probablyTypo(entry[FIRST_NAME_COL], entry2[FIRST_NAME_COL]):
                count += 1

        if len(entry2[STATE_COL]) == 0 or len(entry[STATE_COL]) == 0:
            missing_data += 1
        else:
            if entry[STATE_COL] == entry2[STATE_COL]:
                count += 1

        if len(entry2[PHONE_COL]) == 0 or len(entry[PHONE_COL]) == 0:
            missing_data += 1
        else:
            if probablyTypo(entry[PHONE_COL], entry2[PHONE_COL]):
                count += 1

        if missing_data >= 2 and count > 0:
            if checkEveryCell(entry, entry2):
                count = 3
        if count >= 2:
            dupNamesBool[entry_num] = True
            answer = True
        entry_num += 1
    return answer


"""
Takes the two dictionaries and first unwraps the values into lists, then it
  confirms the duplicate entries are actually duplciates by calling isMatch(). Removes
  the entry from the list if found to not be a true duplicate.

dupNames (dict): The dictioanry containing most likely duplicates.

return ([]): A list of duplciate entries.
"""
def validateDuplicate(dupNames):
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
    return dupNamesList       

      
"""
Prints combined dictionary in a readable format.
combinedDict (dict): Contains both the unique and duplciate entries.
return: VOID
"""              
def printNames(combinedDict):
    for key in combinedDict:
        print(key)
        for val in combinedDict[key]:
            print("\t",combinedDict[key][val])
        print()


"""
Takes two dictionaries, combines them into one and outputs a JSON Object.

unique (dict): A dictionary containing the unique entries in the original CSV file
duplciate (dict): A dictionary containing the duplicate entries in the original CSV file

return (string): A string representing a JSON Object.
"""
def dictsToJSON(unique, duplicate):
    combinedDict = { "Unique Entries": unique,
                     "Duplicate Entries": duplicate}
    printNames(combinedDict)
    return json.dumps(combinedDict)


"""
Takes a list and creates a dictionary with the last names as the keys.

namesList ([[string]]): List contaning all of the CSV file entries that are duplicates

returns (dict): A dictionary containing all of the CSV file entries that are duplciates
"""
def listToDict(namesList):
    namesDict = {}
    for entry in namesList:
      if entry[LAST_NAME_COL] not in namesDict:
          namesDict[entry[LAST_NAME_COL]] = entry
      else:
          namesDict[entry[LAST_NAME_COL]].append(entry)
    return namesDict


"""
Opens and iterates through the CSV file given by the user. Seperates the entries into duplciates
  and unique entries.

returns ( [], [] ): A tuple holding lists containing the unique entires and the duplicate entries, respectively.
"""
def readCSV():
    csvFileString = input("Enter name of CSV file")
    with open(csvFileString) as csvFile:
        csvReader = csv.reader(csvFile, delimiter = ',')
        next(csvReader)
        (uniqueNames, dupNames) = getLastNames(csvReader)
        dupNamesList = validateDuplicate(dupNames)
    return (uniqueNames, dupNamesList)


"""
Main Function.
Iterates through CSV file and converts the entries into a JSON output.
"""
def main():
    (uniqueEntries, dupEntriesList) = readCSV()    
    dupEntries = listToDict(dupEntriesList)
    jsonEntries = dictsToJSON(uniqueEntries, dupEntries)

if __name__ == "__main__":
    main()
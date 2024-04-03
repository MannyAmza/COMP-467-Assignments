import csv
import argparse
import pandas as pd
import pymongo

#Create the connection
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
print("Connected to MongoDB!")

#Create the database
mydb= myclient["EGDB"]

#Create the first collection
col1 = mydb["Weekly Reports"]

#Create the second collection
col2 = mydb["DB Dump"]

#Create the parser to read the file and insert it into the first collection using the function
parser = argparse.ArgumentParser(description='Dump csv files and xlsx files to MongoDB.')
parser.add_argument('-f', '--file',type=str, help='The name of the csv file')
parser.add_argument('-f2', '--file2',type=str, help='The name of the xlsx file')
parser.add_argument('-dba', '--dbanswers', help = 'Run all four functions', action = 'store_true')
parser.add_argument('-o', '--output',type=str, help='The name of the output file')
args = parser.parse_args()



#Create a function to read the csv file and add it into the first collection
#The first row of the csv file is the header, so we skip it
def read_csv(filename):
    global header
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for i, row in enumerate(csvreader):
            if i == 0:
                header = row
            else:
                col1.insert_one(dict(zip(header, row)))

#Create a function to read the xlsx file and add it into the second collection
#The first row of the xlsx file is the header, so we skip it
def read_xlsx(filename):
    global header
    df = pd.read_excel(filename, engine='openpyxl')
    header = list(df.columns)
    for i, row in df.iterrows():
        col2.insert_one(row.to_dict())

#Creating 4 total functions that the assignment asks for

#1. List all work done by Your user - from both collections(No duplicates)​
#My user is Mansoor Amza
#In both collections the column name to check is called Test Owner
def list_all_by_mansoor():
    query = {'Test Owner': 'Mansoor Amza'}
    results = list(col1.find(query, {'_id': 0}))
    results2 = list(col2.find(query, {'_id': 0}))
    
    all_results = set()
    for result in results:
        all_results.add(tuple(result.items()))
    for result in results2:
        all_results.add(tuple(result.items()))
    
    unique_results = [dict(item) for item in all_results]
    print(unique_results)

#2. All repeatable bugs- from both collections(No duplicates)
#Repeatable bugs were given as yes or no, so check for the yes in the column
#In both collections the column name to check is called Repeatable?
#Don't display duplicates
def list_all_repeatable_bugs():
    query = {'Repeatable?': 'Yes'}
    results = list(col1.find(query, {'_id': 0}))
    results2 = list(col2.find(query, {'_id': 0}))
    
    all_results = set()
    for result in results:
        all_results.add(tuple(result.items()))
    for result in results2:
        all_results.add(tuple(result.items()))
    
    unique_results = [dict(item) for item in all_results]
    print(unique_results)

#3.All Blocker bugs- from both collections(No duplicates)
#Blocker bugs were given as yes or no, so check for the yes in the column
#In both collections the column name to check is called Blocker?
#Don't display duplicates
def list_all_blocker_bugs():
    query = {'Blocker?': 'Yes'}
    results = list(col1.find(query, {'_id': 0}))
    results2 = list(col2.find(query, {'_id': 0}))
    
    all_results = set()
    for result in results:
        all_results.add(tuple(result.items()))
    for result in results2:
        all_results.add(tuple(result.items()))
    
    unique_results = [dict(item) for item in all_results]
    print(unique_results)

#4. All reports on build 3/19/2024 - from both collections(No duplicates)
#In both collections the column name to check is called Build #
#The date is displayed in many ways. The different ways are: 
# 3/19/2024(as type String) and 2024-03-19T00:00:00.000+00:00(as type Date)
#Don't display duplicates
def list_all_build_3_19_2024():
    query = {'Build #': '3/19/2024'}
    query2 = {'$or': [{'Build #': '3/19/2024'}, {'Build #': '2024-03-19T00:00:00.000+00:00'}]}
    
    results1 = list(col1.find(query, {'_id': 0}))
    results2 = list(col2.find(query2, {'_id': 0}))
    
    unique_results = set([tuple(result.items()) for result in results1] + [tuple(result.items()) for result in results2])
    unique_results = [dict(item) for item in unique_results]
    
    print(unique_results)

#5.Report back the very 1st test case (Test #1), the middle test case (you determine that), 
#and the final test case of your database - from collection 2
def first_middle_last_test_case():
    first = col2.find_one()
    length = col2.count_documents({})
    middle = col2.find().skip(length // 2).limit(1).next()
    last = col2.find().skip(length - 1).limit(1).next()
    
    print("First Test Case:")
    print(first)
    print("\nMiddle Test Case:")
    print(middle)
    print("\nLast Test Case:")
    print(last)

#Write a csv file from collection 2 where the user is Kevin Chaja
#To find the user, the column name to check is called Test Owner
#The file name is kevin_chaja.csv
def write_kevin_chaja(filename):
    query = {'Test Owner': 'Kevin Chaja'}
    df = pd.DataFrame(list(col2.find(query)))
    df.to_csv(filename)


if __name__ == '__main__':
    if args.file:
        read_csv(args.file)
    if args.file2:
        read_xlsx(args.file2)
    if args.dbanswers:
        list_all_by_mansoor()
        list_all_repeatable_bugs()
        list_all_blocker_bugs()
        list_all_build_3_19_2024()
        first_middle_last_test_case()
    if args.output:
        write_kevin_chaja(args.output)



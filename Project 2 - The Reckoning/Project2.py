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
    #Using the find function to find the query in collection 1
    results = col1.find(query)
    #Using the find function to find the query in collection 2
    results2 = col2.find(query)
    #Check for duplicates
    all_results = results.copy()
    all_results.update(results2)
    print(all_results)

    

if __name__ == '__main__':
    if args.file:
        read_csv(args.file)
    if args.file2:
        read_xlsx(args.file2)

    list_all_by_mansoor()

import csv
import argparse
import pymongo

#Create the connection
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

#Create the database
mydb= myclient["EGDB"]

#Create the first collection
mycol1 = mydb["Weekly Reports"]

#Create the second collection
mycol2 = mydb["DB Dump"]

#Create a function to read the csv file and add it into the first collection
#The first row of the csv file is the header, so we use it to





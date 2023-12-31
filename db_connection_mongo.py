#-------------------------------------------------------------------------
# AUTHOR: Janista Gitbumrungsin
# FILENAME: db_connection_mongo
# SPECIFICATION: Connects to database and allows updating of database for documents in an inverted index
# FOR: CS 4250- Assignment #2
# TIME SPENT: 2.5 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
from pymongo import MongoClient
import re
import datetime

def connectDataBase():

    # Create a database connection object using pymongo
    # --> add your Python code here
    client = MongoClient(host="localhost", port=27017)
    db = client.library
    return db

def createDocument(col, docId, docText, docTitle, docDate, docCat):

    # create a dictionary to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
    # --> add your Python code here
    termCount = {}
    newText = re.sub(r'[^\w\s]', '', docText)
    newText = newText.lower()
    words = newText.split()

    for x in words:
        if x not in termCount.keys():
            termCount.update({x : words.count(x)})

    # create a list of dictionaries to include term objects.
    # --> add your Python code here
    termList = []
    for k,v in termCount.items():
        temp = {}
        temp = {"term": k, "num_char_terms": len(k), "count":v}
        termList.append(temp)

    #Producing a final document as a dictionary including all the required document fields
    # --> add your Python code here
    num_chars = 0
    for i in words:
        num_chars = num_chars + len(i)

    newDate = str(docDate) + "T00:00:00.000Z"

    document = {
        "_id" : int(docId),
        "text" : docText,
        "title" : docTitle,
        "num_chars" : num_chars,
        "date" : datetime.datetime.strptime(newDate, "%Y-%m-%dT%H:%M:%S.000Z"),
        "category" : docCat,
        "terms" : termList
    }

    # Insert the document
    # --> add your Python code here
    col.insert_one(document)

def deleteDocument(col, docId):

    # Delete the document from the database
    # --> add your Python code here
    col.delete_one({"_id": int(docId)})

def updateDocument(col, docId, docText, docTitle, docDate, docCat):

    # Delete the document
    deleteDocument(col, docId)

    # Create the document with the same id
    # --> add your Python code here
    createDocument(col, docId, docText, docTitle, docDate, docCat)

def getIndex(col):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here
    words = col.distinct("terms.term")
    pipeline = [
        {"$unwind" : "$terms"},
        {"$project" : {"terms.term":1, "title":1, "terms.count":1, "_id":0}}
    ]

    results = list(col.aggregate(pipeline))

    index = {}
    for x in words:
        string = ""

        for item in results:
            if item.get("terms").get("term") == x:
                string = string + str(item.get("title")) + ":" + str(item.get("terms").get("count")) + ", "
        
        string = string[:-2]
        index.update({x : string})

    return index
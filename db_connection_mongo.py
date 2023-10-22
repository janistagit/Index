#-------------------------------------------------------------------------
# AUTHOR: Janista Gitbumrungsin
# FILENAME: db_connection_mongo
# SPECIFICATION: Connects to database and allows updating of database for documents in an inverted index
# FOR: CS 4250- Assignment #2
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
from pymongo import MongoClient

def connectDataBase():

    # Create a database connection object using pymongo
    # --> add your Python code here
    client = MongoClient(host="localhost", port=27017)
    return client

def createDocument(col, docId, docText, docTitle, docDate, docCat):

    # create a dictionary to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
    # --> add your Python code here

    # create a list of dictionaries to include term objects.
    # --> add your Python code here

    #Producing a final document as a dictionary including all the required document fields
    # --> add your Python code here

    # Insert the document
    # --> add your Python code here
    pass

def deleteDocument(col, docId):

    # Delete the document from the database
    # --> add your Python code here
    pass

def updateDocument(col, docId, docText, docTitle, docDate, docCat):

    # Delete the document
    # --> add your Python code here

    # Create the document with the same id
    # --> add your Python code here
    pass

def getIndex(col):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here
    pass
#-------------------------------------------------------------------------
# AUTHOR: Janista Gitbumrungsin
# FILENAME: db_connection
# SPECIFICATION: Connects to database and allows updating of database for documents and categories in an inverted index
# FOR: CS 4250- Assignment #2
# TIME SPENT: 7 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
import re
import psycopg2
from psycopg2.extras import RealDictCursor

def connectDataBase():

    # Create a database connection object using psycopg2
    # --> add your Python code here
    DB_NAME = "corpus"
    DB_USER = "postgres"
    DB_PASS = "123"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    try:
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT,
                                cursor_factory=RealDictCursor)
        return conn
    except:
        print("Database not connected successfully")

def createCategory(cur, catId, catName):

    # Insert a category in the database
    # --> add your Python code here
    sql = "Insert into categories (id, name) Values (%s, %s)"
    recset = [catId, catName]
    cur.execute(sql, recset)    

def createDocument(cur, docId, docText, docTitle, docDate, docCat):

    # 1 Get the category id based on the informed category name
    # --> add your Python code here
    sql = "select id from categories where categories.name = %(docCat)s"
    cur.execute(sql, {'docCat': docCat})
    recset = cur.fetchall()
    catId_categories = recset[0]['id']

    # 2 Insert the document in the database. For num_chars, discard the spaces and punctuation marks.
    # --> add your Python code here
    newText = re.sub(r'[^\w\s]', '', docText)
    newText = newText.lower()
    words = newText.split()
    num_chars = 0
    for i in words:
        num_chars = num_chars + len(i)

    sql = "Insert into documents (doc, text, title, num_chars, date, id_categories) Values (%s, %s, %s, %s, %s, %s)"
    recset = [docId, docText, docTitle, num_chars, docDate, catId_categories]
    cur.execute(sql, recset)

    # 3 Update the potential new terms.
    # 3.1 Find all terms that belong to the document. Use space " " as the delimiter character for terms and Remember to lowercase terms and remove punctuation marks.
    # 3.2 For each term identified, check if the term already exists in the database
    # 3.3 In case the term does not exist, insert it into the database
    # --> add your Python code here
    for x in words:
        num = len(x)

        sql = "select term from terms where terms.term = %(word)s"
        cur.execute(sql, {"word":x})
        recset = cur.fetchall()

        if recset == []:
            sql = "Insert into terms (term, num_chars) Values (%s, %s)"
            recset = [x, num]
            cur.execute(sql, recset)

    # 4 Update the index
    # 4.1 Find all terms that belong to the document
    # 4.2 Create a data structure the stores how many times (count) each term appears in the document
    # 4.3 Insert the term and its corresponding count into the database
    # --> add your Python code here
    dict = {}
    for x in words:
        if x not in dict.keys():
            dict.update({x : words.count(x)})

    for k, v in dict.items():
        sql = "Insert into index (doc_documents, term_terms, count) Values (%s, %s, %s)"
        recset = [docId, k, v]
        cur.execute(sql, recset)

def deleteDocument(cur, docId):

    # 1 Query the index based on the document to identify terms
    # 1.1 For each term identified, delete its occurrences in the index for that document
    # 1.2 Check if there are no more occurrences of the term in another document. If this happens, delete the term from the database.
    # --> add your Python code here
    sql = "select term_terms from index where index.doc_documents = %(docId)s"
    cur.execute(sql, {"docId":docId})
    recset = cur.fetchall()

    ans = []
    values = []
    for rec in recset:
        ans.append(dict(rec))
    for obj in ans:
        values.append(obj["term_terms"])

    sql = "Delete from index where doc_documents = %(docId)s"
    cur.execute(sql, {'docId': docId})

    for x in values:
        sql = "select doc_documents from index where index.term_terms = %(word)s"
        cur.execute(sql, {"word":x})
        recset = cur.fetchall()

        if recset == []:
            sql = "Delete from terms where term = %(word)s"
            cur.execute(sql, {'word':x})

    # 2 Delete the document from the database
    # --> add your Python code here
    sql = "Delete from documents where doc = %(docId)s"
    cur.execute(sql, {'docId': docId})

def updateDocument(cur, docId, docText, docTitle, docDate, docCat):

    # 1 Delete the document
    # --> add your Python code here
    deleteDocument(cur, docId)

    # 2 Create the document with the same id
    # --> add your Python code here
    createDocument(cur, docId, docText, docTitle, docDate, docCat)

def getIndex(cur):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here
    title = []
    titledict = {}
    sql = "select doc, title from documents"
    cur.execute(sql)
    recset = cur.fetchall()
    for rec in recset:
        title.append(dict(rec))
    for obj in title:
        titledict.update({obj["doc"] : obj["title"]})

    sql = "select term from terms order by term asc"
    cur.execute(sql)
    recset = cur.fetchall()

    ans = []
    values = []
    for rec in recset:
        ans.append(dict(rec))
    for obj in ans:
        values.append(obj["term"])

    dictionary = {}
    for word in values:
        doclist = []
        string = ""
        sql = "select doc_documents, count from index where term_terms = %(word)s"
        cur.execute(sql, {"word" : word})
        recset = cur.fetchall()

        for rec in recset:
            doclist.append(dict(rec))

        for obj in doclist:
            string = string + str(titledict[obj["doc_documents"]]) + ":" + str(obj["count"]) + ", "

        string = string[:-2]
        dictionary.update({word : string})

    return(dictionary)
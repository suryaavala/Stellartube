import MySQLdb as mdb
import time
import datetime

db_hostname = 'localhost'
db_username = 'root'
db_passwords = 'Czz15133613611'
db_dbName = 'DB_DApp'

#Function used to connect to DB
#Parameters: 
def sql_StartSQLConnection(hostname, username, password, dbName):    
    print("Connecting to database server...")
    try:
        conn = mdb.connect(hostname, username, password, dbName)
        print("Successfully connected to database %s!" %dbName)
        return conn
    except Exception as error:
        print("Exception:%s" %error)
        return

#Initialize Data base
def sql_InitialDB(hostname, username, password, dbName):
    print("Initialing Database...:")
    try:
        conn = mdb.connect(hostname, username, password)
        cursor = conn.cursor()
        #cursor.execute('DROP DATABASE IF EXISTS %s' %dbName)
        cursor.execute('CREATE DATABASE IF NOT EXISTS %s' %dbName)
        conn = mdb.connect(hostname, username, password, dbName)
        sql_CreateTable(conn)
        sql_Close(conn)
        print("Successfully Initialed")
    except Exception as error:
        print("Exception: %s" %error)
   
#Create tables for DApp
def sql_CreateTable(conn):

    cursor = conn.cursor()    
    try:
        cursor.execute('CREATE TABLE IF NOT EXISTS Table_Users (UserID int AUTO_INCREMENT, Email varchar(32) NOT NULL, Password varchar(32) NOT NULL, FirstName varchar(32) NOT NULL, LastName varchar(32), primary key(UserID, Email))')
        cursor.execute('Alter table Table_Users AUTO_INCREMENT=1')
        cursor.execute('CREATE TABLE IF NOT EXISTS Table_Purchases (VideoID int NOT NULL, UserID int NOT NULL, Date Date, primary key(UserID, VideoID))')
        cursor.execute('CREATE TABLE IF NOT EXISTS Table_Videos (VideoID int AUTO_INCREMENT, Owner int, DateAdded Date, Title varchar(120), Description varchar(50),Price float, FileName varchar(255), primary key(VideoID))')
        cursor.execute('Alter table Table_Video AUTO_INCREMENT=1')
        cursor.execute('CREATE TABLE IF NOT EXISTS Table_Lable (VideoID int, Lable varchar(50), primary key(Lable, VideoID))')
        print("Create tables successfully!")
    except Exception as error:
        print("Exception:%s" %error)

def sql_GetConnection():
    global db_dbName
    global db_hostname
    global db_passwords
    global db_username
    conn = sql_StartSQLConnection(db_hostname, db_username, db_passwords, db_dbName)
    return conn

#insert data into DB
def sql_Insert(sql):
    conn = sql_GetConnection()
    cursor = conn.cursor()
    try:
        count = cursor.execute(sql)
        sql_Close(conn)
        print("Insert successfully!")
        return count
    except Exception as error:
        print("Exception: %s" %error)

#Close connection and write in data
def sql_Close(conn):    
    cursor = conn.cursor()
    try:
        cursor.close()
        conn.commit()
        conn.close()
        print("Disconnected successfuly")
    except Exception as error:
        print("Exception:%s" %error)

def sql_Select(sql):
    conn = sql_GetConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        sql_Close(conn)
        return results
    except Exception as error:
        print("Exception: %s" %error)
    
#get video's lables by video name
def sql_GetLableByVideoName(videoname):    
    return sql_Select("SELECT Lable FROM Table_Lable WHERE VideoID = (SELECT VideoID FROM Table_Video WHERE VideoName = \'%s\')" %videoname)

#Using username get password
def sql_checkUserPassword(userID, password):
    pws = sql_Select("SELECT Password FROM Table_Users WHERE UserID = \'%s\'" %userID)
    pw = pws[0]    
    if password == pw[0]:
        return True
    else:
        return False

def sql_getUser(userID):
    return sql_Select("SELECT Email, FirstName, LastName FROM Table_Users WHERE UserID = \'%s\'" %userID)

def sql_getVideo(videoID):
    return sql_Select("SELECT Owner, DateAdded, Title, Description, Price, FileName FROM Table_Videos WHERE VideoID = \'%d\'" %videoID)

def sql_GetVideoIDByVideoName(videoname):
    return sql_Select("SELECT VideoID FROM Table_Video WHERE VideoName = \'%s\'" %videoname)

def sql_GetVideoNameByLable(lable):
    return sql_Select("SELECT VideoName FROM Table_Video WHERE VideoID = (SELECT VideoID FROM Table_Lable WHERE Lable = \'%s\')" %lable)

def sql_getUserPurchases(userID):
    return sql_Select("SELECT VideoID FROM Table_Purchases WHERE UserID = \'%d\'" %userID)

def sql_GetVideosNameByUserID(userID):
    return sql_Select("SELECT VideoName FROM Table_Video WHERE VideoID = (SELECT VideoID FROM Table_User_Video WHERE UserID = \'%d\')" %userID)

def sql_GetUserIDByUsername(username):
    return sql_Select("SELECT UserID FROM Table_UserInfo WHERE Username = \'%s\'" %username)

def sql_GetVideoNameByLike(name):
    args = '%'+name+'%'
    return sql_Select("SELECT VideoName FROM Table_Video WHERE VideoName LIKE '%s'" %args)

def sql_searchVideos(searchString, maxResults):
    args = '%'+searchString+'%'
    ls_video = []
    results = sql_Select("SELECT VideoID FROM Table_Videos WHERE Title LIKE '%s" %args)
    ls_video.append(results)
    results = sql_Select("SELECT VideoID FROM Table_Videos WHERE Description LIKE '%s" %args)
    ls_video.append(results)
    if len(ls_video)>maxResults:
        return ls_video[:maxResults]
    else:
        return ls_video
    
def checkVideoPurchase(videoID, userID):
    result = sql_Select("SELECT Date FROM Table_Purchase WHERE VideoID = \'%s\' UserID = \'%s\'" %(videoID, userID))
    if len(result) > 0:
        return True
    else:
        return False

def sql_addPurchase(videoID, userID):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    count = sql_Insert("INSERT INTO Table_Purchases values(\'%d\', \'%d\', \'%s\')" %(videoID, userID, date))
    if count == 1:
        return 0
    else:
        return 1

def sql_addUser(email, password, firstname, lastname):
    count = sql_Insert("INSERT INTO Table_Users values(null, \'%s\', \'%s\', \'%s\', \'%s\')" %(email, password, firstname, lastname))
    if count == 1:
        return 0
    else:
        return 1

def sql_addVideo(userID, title, decription, price, file):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    count = sql_Insert("INSERT INTO Table_Videos values(null, \'%d\', \'%s\', \'%s\', \'%s\', \'%f\', \'%s\')" %(userID, date, title, decription, price, file))
    if count == 1:
        return 0
    else:
        return 1

def sql_InsertVideosLable(videoname, lable):
    sql_Insert("INSERT INTO Table_Lable values( (SELECT VideoID FROM Table_Video WHERE VideoName = \'%s\'), \'%s\')" %(videoname, lable))
    
def sql_doesUserExist(email):
    conn = sql_GetConnection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Table_UserInfo WHERE Username = \'%s\'" %email)
        result = cursor.fetchall()
        return result
    except Exception as error:
        print("Exception: %s" %error)
        return 0


#Initialize Database
sql_InitialDB(db_hostname, db_username, db_passwords, db_dbName)

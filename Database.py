import MySQLdb as mdb


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

def sql_InitialDB(hostname, username, password, dbName):
    print("Initialing Database...:")
    try:
        conn = mdb.connect(hostname, username, password)
        cursor = conn.cursor()
        cursor.execute('DROP DATABASE IF EXISTS %s' %dbName)
        cursor.execute('CREATE DATABASE IF NOT EXISTS %s' %dbName)
        conn = mdb.connect(hostname, username, password, dbName)
        sql_CreateTable(conn)
        conn.close()
        print("Successfully Initialed")
    except Exception as error:
        print("Exception: %s" %error)
   
#Create tables for DApp
def sql_CreateTable(conn):
    cursor = conn.cursor()    
    try:
        cursor.execute('CREATE TABLE IF NOT EXISTS Table_UserInfo (UserID int AUTO_INCREMENT NOT NULL, Username varchar(50), Passwords varchar(50), Useraddress varchar(50), primary key(UserID, Username))')
        cursor.execute('Alter table Table_UserInfo AUTO_INCREMENT=1')
        cursor.execute('CREATE TABLE IF NOT EXISTS Table_User_Video (UserID int, VideoID int, primary key(UserID, VideoID))')
        cursor.execute('CREATE TABLE IF NOT EXISTS Table_Video (VideoID int AUTO_INCREMENT, VideoAddress varchar(50), VideoDescription varchar(50), VideoName varchar(50), primary key(VideoName, VideoID))')
        cursor.execute('Alter table Table_Video AUTO_INCREMENT=1')
        cursor.execute('CREATE TABLE IF NOT EXISTS Table_Lable (VideoID int, Lable varchar(50), primary key(Lable, VideoID))')
        print("Create tables successfully!")
    except Exception as error:
        print("Exception:%s" %error)

#insert data into DB
def sql_Insert(conn, sql):
    cursor = conn.cursor()
    try:
        count = cursor.execute(sql)
        print("Insert successfully!")
        return count
    except Exception as error:
        print("Exception: %s" %error)

#get data from DB by select
#return rows that are affected
#return results
def sql_Select(conn, sql):
    cursor = conn.cursor()
    try:
        count = cursor.execute(sql)
        results = cursor.fetchall()
        return count, results
    except Exception as error:
        print("Exception: %s" %error)

#using the video's name get videoID
def sql_getVideoID(conn, videoName):
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT VideoID FROM TABLE_Video WHERE VideoName = %s' %videoName)
        results = cursor.fetchall()
        return results
    except Exception as error:
        print("Exception: %s" %error)
    
#get video's lables by video name
def sql_getLableOfVideo(conn, videoName):
    cursor = conn.cursor()
    try:
        videoID = sql_getVideoID(conn, videoName)
        cursor.execute('SELECT Lable FROM Table_Lable WHERE VideoID = %s' %videoID)
        results = cursor.fetchall()
        return results
    except Exception as error:
        print("Exception: %s" %error)
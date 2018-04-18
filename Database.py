import MySQLdb as mdb

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
        cursor.execute('CREATE TABLE IF NOT EXISTS Table_UserInfo (UserID int AUTO_INCREMENT, Username varchar(50) NOT NULL, Passwords varchar(50) NOT NULL, UserUniaddress varchar(50) NOT NULL, Balance float, primary key(UserID, Username))')
        cursor.execute('Alter table Table_UserInfo AUTO_INCREMENT=1')
        cursor.execute('CREATE TABLE IF NOT EXISTS Table_User_Video (UserID int NOT NULL, VideoID int NOT NULL, VideoPrice float, primary key(UserID, VideoID))')
        cursor.execute('CREATE TABLE IF NOT EXISTS Table_Video (VideoID int AUTO_INCREMENT, VideoAddress varchar(50), VideoDescription varchar(50), VideoName varchar(50), primary key(VideoID, VideoName))')
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
def sql_GetPasswordByUsername(Username):
    return sql_Select("SELECT Password FROM Table_UserInfo WHERE Username = \'%s\'" %Username)

def sql_GetVideoAddressByVideoID(videoID):
    return sql_Select("SELECT VideoAddress FROM Table_Video WHERE VideoID = \'%d\'" %videoID)

def sql_GetVideoIDByVideoName(videoname):
    return sql_Select("SELECT VideoID FROM Table_Video WHERE VideoName = \'%s\'" %videoname)

def sql_GetVideoNameByLable(lable):
    return sql_Select("SELECT VideoName FROM Table_Video WHERE VideoID = (SELECT VideoID FROM Table_Lable WHERE Lable = \'%s\')" %lable)

def sql_GetVideoIDByUserID(userID):
    return sql_Select("SELECT VideoID FROM Table_User_Video WHERE UserID = \'%d\'" %userID)

def sql_GetVideosNameByUserID(userID):
    return sql_Select("SELECT VideoName FROM Table_Video WHERE VideoID = (SELECT VideoID FROM Table_User_Video WHERE UserID = \'%d\')" %userID)

def sql_GetUserIDByUsername(username):
    return sql_Select("SELECT UserID FROM Table_UserInfo WHERE Username = \'%s\'" %username)
    
def sql_GetVideoNameByLike(name):
    args = '%'+name+'%'
    return sql_Select("SELECT VideoName FROM Table_Video WHERE VideoName LIKE '%s'" %args)

def sql_InsertUserVideo(userID, videoID, price):
    sql_Insert("INSERT INTO Table_User_Video values(\'%d\', \'%d\')" %(userID, videoID))

def sql_InsertUserInfo(username, passwords, useruniaddress, balance):
    sql_Insert("INSERT INTO Table_UserInfo values(null, \'%s\', \'%s\', \'%s\', \'%f\')" %(username, passwords, useruniaddress, balance))

def sql_InsertVideoInfo(videoaddress, videodescription, videoname):
    sql_Insert("INSERT INTO Table_Video values(null, \'%s\', \'%s\', \'%s\')" %(videoaddress, videodescription, videoname))

def sql_InsertVideosLable(videoname, lable):
    videoIDs = sql_GetVideoIDByVideoName(videoname)
    sql_Insert("INSERT INTO Table_Lable values( (SELECT VideoID FROM Table_Video WHERE VideoName = \'%s\'), \'%s\')" %(videoname, lable))
    
def sql_CheckUserExist(usernmae):
    conn = sql_GetConnection()
    cursor = conn.cursor()
    try:
        count = cursor.execute("SELECT * FROM Table_UserInfo WHERE Username = \'%s\'" %usernmae)
        return count
    except Exception as error:
        print("Exception: %s" %error)
        return 0


#Initialize Database
sql_InitialDB(db_hostname, db_username, db_passwords, db_dbName)

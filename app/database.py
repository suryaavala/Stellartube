import MySQLdb as mdb

db_hostname = 'localhost'
db_username = 'admin'
db_passwords = 'password'
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
        cursor.execute('CREATE TABLE IF NOT EXISTS Table_User_Video (UserID int NOT NULL, VideoID int NOT NULL, primary key(UserID, VideoID))')
        cursor.execute('CREATE TABLE IF NOT EXISTS Table_Video (VideoID int AUTO_INCREMENT, VideoAddress varchar(50), VideoDescription varchar(50), VideoName varchar(50), primary key(VideoID, VideoName))')
        cursor.execute('Alter table Table_Video AUTO_INCREMENT=1')
        cursor.execute('CREATE TABLE IF NOT EXISTS Table_Lable (VideoID int, Lable varchar(50), primary key(Lable, VideoID))')
        print("Create tables successfully!")
    except Exception as error:
        print("Exception:%s" %error)

#insert data into DB
def sql_Insert(sql):
    global db_dbName
    global db_hostname
    global db_passwords
    global db_username
    conn = sql_StartSQLConnection(db_hostname, db_username, db_passwords, db_dbName)
    cursor = conn.cursor()
    try:
        count = cursor.execute(sql)
        sql_Close(conn)
        print("Insert successfully!")
        return count
    except Exception as error:
        print("Exception: %s" %error)

#get data from DB by select
#return rows that are affected
#return results
def sql_Select(sql):
    global db_dbName
    global db_hostname
    global db_passwords
    global db_username

    conn = sql_StartSQLConnection(db_hostname, db_username, db_passwords, db_dbName)
    cursor = conn.cursor()
    try:
        count = cursor.execute(sql)
        results = cursor.fetchall()
        sql_Close(conn)
        return count, results
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

#using the video's name get videoID
def sql_GetVideoID(videoName):
    global db_dbName
    global db_hostname
    global db_passwords
    global db_username
    conn = sql_StartSQLConnection(db_hostname, db_username, db_passwords, db_dbName)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT VideoID FROM TABLE_Video WHERE VideoName = "%s"' %videoName)
        results = cursor.fetchall()
        sql_Close(conn)
        return results[0][0]
    except Exception as error:
        print("Exception: %s" %error)
    
#get video's lables by video name
def sql_GetLableOfVideo(videoName):
    global db_dbName
    global db_hostname
    global db_passwords
    global db_username
    conn = sql_StartSQLConnection(db_hostname, db_username, db_passwords, db_dbName)
    cursor = conn.cursor()
    try:
        videoID = sql_GetVideoID(videoName)
        cursor.execute('SELECT Lable FROM Table_Lable WHERE VideoID = "%s"' %videoID)
        results = cursor.fetchall()
        sql_Close(conn)
        return results[0][0]
    except Exception as error:
        print("Exception: %s" %error)

#Using username get password
def sql_GetPasswordByUsername(Username):
    global db_dbName
    global db_hostname
    global db_passwords
    global db_username
    conn = sql_StartSQLConnection(db_hostname, db_username, db_passwords, db_dbName)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT Passwords FROM Table_UserInfo WHERE Username = "%s"' %Username)
        result = cursor.fetchall()
        sql_Close(conn)
        return result[0][0]
    except Exception as error:
        print("Exception: %s" %error)

def sql_GetVideosByUsername(username):
    global db_dbName
    global db_hostname
    global db_passwords
    global db_username
    conn = sql_StartSQLConnection(db_hostname, db_username, db_passwords, db_dbName)
    cursor = conn.cursor()
    try:    
        results = cursor.execute('SELECT VideoAddress FROM Table_Video WHERE VideoID = (SELECT VideoID FROM Table_User_Video WHERE UserID = (SELECT UserID FROM Table_UserInfo WHERE Username = "%s"))' %username)
        sql_Close(conn)
        return results
    except Exception as error:
        print("Exception: %s" %error)

def sql_GetUsernameByUserID(userid):
    global db_dbName
    global db_hostname
    global db_passwords
    global db_username
    conn = sql_StartSQLConnection(db_hostname, db_username, db_passwords, db_dbName)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT Username FROM Table_UserInfo WHERE UserID = "%s"' %userid)
        result = cursor.fetchall()
        sql_Close(conn)
        return result[0][0]
    except Exception as error:
        print("Exception: %s" %error)
        return 0

def sql_GetUserIDByUsername(username):
    global db_dbName
    global db_hostname
    global db_passwords
    global db_username
    conn = sql_StartSQLConnection(db_hostname, db_username, db_passwords, db_dbName)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT UserID FROM Table_UserInfo WHERE Username = "%s"' %username)
        result = cursor.fetchall();
        sql_Close(conn)
        return result[0][0]
    except Exception as error:
        print("Exception: %s" %error)
        return 0

def sql_InsertUserInfo(username, passwords, useruniaddress, balance):
    global db_dbName
    global db_hostname
    global db_passwords
    global db_username

    conn = sql_StartSQLConnection(db_hostname, db_username, db_passwords, db_dbName)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO Table_UserInfo values(null, "%s", "%s", "%s", %f)' %(username, passwords, useruniaddress, balance))
        sql_Close(conn)
        return 1
    except Exception as error:
        print("Exception: %s" %error)
        return 0
    
def sql_CheckUserExist(usernmae):
    global db_dbName
    global db_hostname
    global db_passwords
    global db_username

    conn = sql_StartSQLConnection(db_hostname, db_username, db_passwords, db_dbName)
    cursor = conn.cursor()
    try:
        count = cursor.execute('SELECT * FROM Table_UserInfo WHERE Username = "%s"' %usernmae)
        return count
    except Exception as error:
        print("Exception: %s" %error)
        return 0


#Initialize Database
if __name__=='__main__':
    sql_InitialDB(db_hostname, db_username, db_passwords, db_dbName)

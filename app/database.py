import MySQLdb as mdb
import time
import datetime

db_hostname = 'localhost'
db_username = 'admin'
db_passwords = 'password'
db_dbName = 'DB_DApp2'

# Function used to connect to DB
# Parameters:


def sql_StartSQLConnection(hostname, username, password, dbName):
    print("Connecting to database server...")
    try:
        conn = mdb.connect(hostname, username, password, dbName)
        print("Successfully connected to database %s!" % dbName)
        return conn
    except Exception as error:
        print("Exception:%s" % error)
        return

# Initialize Data base


def sql_InitialDB(hostname, username, password, dbName):
    print("Initialing Database...:")
    try:
        conn = mdb.connect(hostname, username, password)
        cursor = conn.cursor()
        cursor.execute('DROP DATABASE IF EXISTS %s' % dbName)
        cursor.execute('CREATE DATABASE IF NOT EXISTS %s' % dbName)
        conn = mdb.connect(hostname, username, password, dbName)
        sql_CreateTable(conn)
        sql_Close(conn)
#        print("Successfully Initialed")
    except Exception as error:
        print("Exception: %s" % error)

# Create tables for DApp


def sql_CreateTable(conn):

    cursor = conn.cursor()
    try:
        cursor.execute('CREATE TABLE IF NOT EXISTS Table_Users (UserID int AUTO_INCREMENT, Email varchar(32) NOT NULL, Password varchar(32) NOT NULL, FirstName varchar(32) NOT NULL, LastName varchar(32), PassPhrase TEXT, Balance float, primary key(UserID, Email))')
        cursor.execute('Alter table Table_Users AUTO_INCREMENT=1')
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS Table_Purchases (VideoID int NOT NULL, UserID int NOT NULL, Date Date, primary key(UserID, VideoID))')
        cursor.execute('CREATE TABLE IF NOT EXISTS Table_Videos (VideoID int AUTO_INCREMENT, Owner int, DateAdded Date, Title varchar(120), Description varchar(50),Price float, FileName varchar(255), Lables varchar(50), primary key(VideoID))')
        cursor.execute('Alter table Table_Videos AUTO_INCREMENT=1')
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS Table_Lable (VideoID int, Lable varchar(50), primary key(Lable, VideoID))')
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS Table_Comments (CommentID int primary key AUTO_INCREMENT, VideoID int, DatePosted Date, ParentID int, Content varchar(500))')
        cursor.execute('Alter table Table_Comments AUTO_INCREMENT=1')
#        print("Create tables successfully!")
    except Exception as error:
        print("Exception:%s" % error)


def sql_GetConnection():
    global db_dbName
    global db_hostname
    global db_passwords
    global db_username
    conn = sql_StartSQLConnection(
        db_hostname, db_username, db_passwords, db_dbName)
    return conn

# insert data into DB


def sql_Insert(sql):
    conn = sql_GetConnection()
    cursor = conn.cursor()
    try:
        count = cursor.execute(sql)
        sql_Close(conn)
#        print("Insert successfully!")
        return count
    except Exception as error:
        print("Exception: %s" % error)

# Close connection and write in data


def sql_Close(conn):
    cursor = conn.cursor()
    try:
        cursor.close()
        conn.commit()
        conn.close()
#        print("Disconnected successfuly")
    except Exception as error:
        print("Exception:%s" % error)


def sql_Select(sql):
    conn = sql_GetConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        sql_Close(conn)
        return results
    except Exception as error:
        print("Exception: %s" % error)


def sql_Update(sql):
    conn = sql_GetConnection()
    cursor = conn.cursor()
    try:
        count = cursor.execute(sql)
        sql_Close(conn)
        return count
    except Exception as error:
        print("Exception: %s" % error)

# get video's lables by video name


def sql_GetLableByVideoName(videoname):
    return sql_Select("SELECT Lable FROM Table_Lable WHERE VideoID = (SELECT VideoID FROM Table_Video WHERE VideoName = \'%s\')" % videoname)


def sql_doesUserExist(email):
    conn = sql_GetConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM Table_Users WHERE Email = \'%s\'" % email)
        result = cursor.fetchone()
        return result[0]
    except Exception as error:
        print("Exception: %s" % error)
        return 0

# Using username get password


def sql_checkUserPassword(userID, password):
    pws = sql_Select(
        "SELECT Password FROM Table_Users WHERE UserID = \'%s\'" % userID)
    pw = pws[0]
    if password == pw[0]:
        return True
    else:
        return False


def sql_getUser(userID):
    return sql_Select("SELECT Email, FirstName, LastName FROM Table_Users WHERE UserID = \'%s\'" % userID)[0]


def sql_getAllUserInfo(userID):
    return sql_Select("SELECT Email, FirstName, LastName, PassPhrase, Balance FROM Table_Users WHERE UserID = \'%s\'" % userID)[0]


def sql_getVideo(videoID):
    result = sql_Select(
        "SELECT Owner, DateAdded, Title, Description, Price, FileName FROM Table_Videos WHERE VideoID = \'%d\'" % videoID)
    if result:
        return list(result[0])
    else:
        return None


def sql_getUserVideos(userID):
    result = sql_Select(
        "SELECT VideoID FROM Table_Videos WHERE Owner = '%s'" % userID)
    return [i[0] for i in result] if result else []


def sql_GetVideoNameByLable(lable):
    return sql_Select("SELECT VideoName FROM Table_Video WHERE VideoID = (SELECT VideoID FROM Table_Lable WHERE Lable = \'%s\')" % lable)


def sql_getUserPurchases(userID):
    return sql_Select("SELECT VideoID FROM Table_Purchases WHERE UserID = \'%d\'" % userID)


def sql_GetVideosNameByUserID(userID):
    return sql_Select("SELECT VideoName FROM Table_Video WHERE VideoID = (SELECT VideoID FROM Table_User_Video WHERE UserID = \'%d\')" % userID)


def sql_GetVideoNameByLike(name):
    args = '%'+name+'%'
    return sql_Select("SELECT VideoName FROM Table_Video WHERE VideoName LIKE '%s'" % args)


def sql_searchVideos(searchString, maxResults):
    args = '%'+searchString+'%'
    ls_video = []
    results = sql_Select(
        "SELECT VideoID FROM Table_Videos WHERE Title LIKE '%s'" % args)
    ls_video += [v[0] for v in results]
    results = sql_Select(
        "SELECT VideoID FROM Table_Videos WHERE Description LIKE '%s'" % args)
    ls_video += [v[0] for v in results]
    ls_video = list(set(ls_video))
    if len(ls_video) > maxResults:
        return ls_video[:maxResults]
    else:
        return ls_video


def sql_getVideoComments(videoID):
    results = sql_Select(
        "SELECT Content FROM Table_Comments WHERE VideoID = \'%s\'" % videoID)
    return results


def sql_getComments(commentID):
    results = sql_Select(
        "SELECT DatePosted, ParentID, Content FROM Table_Comments WHERE CommentID = \'%s\'" % commentID)
    return results


def checkVideoPurchase(videoID, userID):
    result = sql_Select(
        "SELECT Date FROM Table_Purchase WHERE VideoID = \'%s\' UserID = \'%s\'" % (videoID, userID))
    if len(result) > 0:
        return True
    else:
        return False


def sql_addPurchase(videoID, userID):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    count = sql_Insert("INSERT INTO Table_Purchases values(\'%d\', \'%d\', \'%s\')" % (
        videoID, userID, date))
    if count == 1:
        return 0
    else:
        return 1


def sql_addComment(videoID, parentsID, content):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    count = sql_Insert("INSERT INTO Table_Comments values(null, \'%d\', \'%s\', \'%d\', \'%s\')" % (
        videoID, date, parentsID, content))
    if count == 1:
        return 0
    else:
        return 1


def sql_addUser(email, password, firstname, lastname, passphrase, balance):
    count = sql_Insert("INSERT INTO Table_Users values(null, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%f\')" % (
        email, password, firstname, lastname, passphrase, balance))
    if count == 1:
        return 0
    else:
        return 1


def sql_addVideo(userID, title, decription, price, file, lable):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    count = sql_Insert("INSERT INTO Table_Videos values(null, \'%d\', \'%s\', \'%s\', \'%s\', \'%f\', \'%s\', \'%s\')" % (
        userID, date, title, decription, price, file, lable))
    if count == 1:
        return 0
    else:
        return 1


def sql_editUserEmail(userID, newEmail):
    result = sql_Update(
        "UPDATE Table_Users SET Email = \'%s\' WHERE UserID = \'%d\'" % (newEmail, userID))
    if result == 1:
        return 0
    else:
        return 1


def sql_editUserPassword(userID, newPassword):
    result = sql_Update(
        "UPDATE Table_Users SET Password = \'%s\' WHERE UserID = \'%d\'" % (newPassword, userID))
    if result == 1:
        return 0
    else:
        return 1


def sql_editUserBalance(userID, newBalance):
    result = sql_Update(
        "UPDATE Table_Users SET Balance = \'%f\' WHERE UserID = \'%d\'" % (float(newBalance), int(userID)))
    if result == 1:
        return 0
    else:
        return 1


def sql_editVideoInfo(videoID, newTitle, newDescription, newLables):
    sql = "UPDATE Table_Videos SET "
    try:
        if newTitle != '':
            sql_Update(sql + "Title = \'%s\' WHERE VideoID = \'%d\'" %
                       (newTitle, videoID))
        if newDescription != '':
            sql_Update(sql + "Description = \'%s\' WHERE VideoID = \'%d\'" %
                       (newDescription, videoID))
        if newLables != '':
            sql_Update(sql + "Lable = \'%s\' WHERE VideoID = \'%d\'" %
                       (newLables, videoID))
        return 0
    except Exception as error:
        print("Exception: %s" % error)
        return 1


def sql_InsertVideosLable(videoname, lable):
    sql_Insert("INSERT INTO Table_Lable values( (SELECT VideoID FROM Table_Video WHERE VideoName = \'%s\'), \'%s\')" % (
        videoname, lable))



# Initialize Database
if __name__ == "__main__":
    sql_InitialDB(db_hostname, db_username, db_passwords, db_dbName)

    # NOTE: Creating an admin app user for blockchain transaction validation
    from app.stellar_block import Stellar_block

    def initialise_admin_user():
        fname = 'app'
        lname = 'admin'
        email = 'suryatherisingstar@gmail.com'
        password = '%3oYbcQe4kq1&WN4'
        # NOTE: Blockchain user creation
        user_on_blockchain = Stellar_block()
        user_on_blockchain.create_account()
        passphrase = user_on_blockchain.get_passphrase()
        balance = float(user_on_blockchain._get_balance())
        try:
            sql_addUser(email, password, fname, lname, passphrase, balance)
            print('App admin created')
        except Exception:
            print('Unable to create app admin')

    initialise_admin_user()

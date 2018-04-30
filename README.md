# README

## Setup

Libraries used:

* Flask
* Flask-WTF
* Jinja2
* WTForms
* stellar-base

## INTEGRATING BLOCKCHAIN

###Pre-requisites
Before moving on to the blockchain integration, your app should be working without the blockchain.

You can check if it is working by the following commands:

```
cd <project>

git pull && git fetch

git checkout video_page

git pull

cd app

python3 database.py

cd ../

python3 run.py
```

Then goto the address shown in the terminal. It would look like this:

`http://<address>:<port>`

Check if you are able to create user, sign in and stuff

###Blockchain Installation

Change to appropriate branch

`git checkout blockchain && git pull`

Install dependencies

`pip3 install stellar-base`

<span style="color:red"><bold>I have changed the table schema for the Table_UserInfo inroder to fit the passphrase in BIP39 format, so you must drop and rebuild the database as follow:</bold></span>.

```
//from terminal

mysql

mysql> show DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| DB_DApp            |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)

mysql> drop database DB_DApp;
Query OK, 4 rows affected (2 min 37.45 sec)

mysql> show DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.00 sec)

mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.01 sec)

mysql> \q


cd <project>

cd app

$ python3 database.py
Initialing Database...:
Create tables successfully!
Disconnected successfuly
Successfully Initialed
```

###Usage

```
//from project directory run the following

python3 run.py
```

Create a new user on the GUI

Then goto the terminal and do the following:

```
mysql> use DB_DApp;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

mysql> DESCRIBE Table_UserInfo;
+----------------+-------------+------+-----+---------+----------------+
| Field          | Type        | Null | Key | Default | Extra          |
+----------------+-------------+------+-----+---------+----------------+
| UserID         | int(11)     | NO   | PRI | NULL    | auto_increment |
| Username       | varchar(50) | NO   | PRI | NULL    |                |
| Passwords      | varchar(50) | NO   |     | NULL    |                |
| UserUniaddress | text        | NO   |     | NULL    |                |
| Balance        | float       | YES  |     | NULL    |                |
+----------------+-------------+------+-----+---------+----------------+
5 rows in set (0.00 sec)


mysql> select * from Table_UserInfo;
+--------+----------+-----------+-------------------------------------------------------------------------------+---------+
| UserID | Username | Passwords | UserUniaddress                                                                | Balance |
+--------+----------+-----------+-------------------------------------------------------------------------------+---------+
|      2 | surya    | surya     | denial deny mouse win refuse affair swift mammal thank fossil gravity bicycle |       0 |
+--------+----------+-----------+-------------------------------------------------------------------------------+---------+
1 row in set (0.00 sec)
```

If you see a long string of text under `UserUniaddress` like (`denial deny mouse win refuse affair swift mammal thank fossil gravity bicycle`), then:

1.  The integration for user signup is working
2.  your account has been registered with the blockchain test network
3.  And your passphrase is stored in the database
4.  We can anytime retreive the details for the account like transactions, balances etc from the testnet (I will be writing further utility functions in the coming days)

###Utilities
Most of the actual blockchain code is in the module called `stellar_block.py` inside `app` dir.

I have written a few basic utility functions, you can play with them and from `python3` interpreter.

I will be writing code, modifying the app/database for the smart contract transactions on the blockchain.

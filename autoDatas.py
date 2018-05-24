import app
from app import database as db
from app.stellar_block import Stellar_block
import random

def populateUsers(num):
	list_firstname = ['Kobe', 'Peter', 'Tony', 'Aaron', 'Bill', 'Daniel', 'Edison', 'Gary', 'Hank', 'Jack']
	list_lastname = ['Stark', 'Park', 'Braint', 'Zhang', 'Li', 'Lin', 'Jobs', 'Brook', 'Green', 'Brown']

	for i in range(num):
		firstname = random.choice(list_firstname)
		lastname = random.choice(list_lastname)
		email = firstname + '.' + lastname + '@unsw.com'
		password = "admin"
		user = Stellar_block()
		user.create_account()
		passphrase = user.get_passphrase()
		balance = float(user._get_balance())
		db.sql_addUser(email, password, firstname, lastname, passphrase, balance)

def updateVideoFileName(num):
	for i in range(num):
		db.sql_addVideoRandom()

if __name__ == "__main__":
	populateUsers(10)
	updateVideoFileName(40)

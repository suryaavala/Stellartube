var express = require('express');
var bodyParser = require('body-parser');
var lightwallet = require('eth-lightwallet');
var keythereum = require('keythereum');
var mongoose = require('mongoose');

var app = express();
app.use(bodyParser.json());

mongoose.connect('mongodb://localhost/smartWallet'); // I tried it on Mongodb. Need to connect to our Mysql db. I tried installing it on my system. Getting some error while running Yunhe's database.py script
var db = mongoose.connection;
db.on('error', function() {
	console.log('connection error');
});
db.once('open', function() {
  console.log('connected to database');
});
var UserSchema = mongoose.Schema({
  username: {
  	type: String,
  	unique: true
  },
  password: String,
  seedPhrase: String,
  publicKey: String,
  keystore: String,
  privateKey: String,
});
var User = mongoose.model('User', UserSchema); // this is user schema

app.post('/wallet', function(req, res) { // it will listen for a post method, it will listen for the call your another application is doing
	var username = (req.body.username);
	var password = (req.body.password);
	User.findOne({ username: username }, function(err, user) { // Checking if the user info information is already present
		if (err) { res.send(err); } else if (!user) { // if user info is not registered i.e. user have no ether account linked to him, then register the new user
			var secretSeed = lightwallet.keystore.generateRandomSeed(); // this is used to generate 12 words passphrase seed
			lightwallet.keystore.createVault({
				password: password,
				seedPhrase: secretSeed,
				hdPathString: "m/44'/60'/0'/0"
			}, function(err, ks) { // here ks is the keystore, means a json wallet which is secured by password
				if (err) { res.send(err); } else {
					ks.keyFromPassword(password, function(err, pwDerivedKey) {
						if (err) { res.send(err); } else {
							ks.generateNewAddress(pwDerivedKey, 1); // this is used to generate the ethereum address on the basis of seed phrase
							var serialzedKeystore = ks.serialize(); // this is users json wallet
							var publicKey = (ks.getAddresses()[0]);
							var privateKey = (ks.exportPrivateKey(ks.getAddresses()[0], pwDerivedKey)); // this is ethereum private key
							var user = new User({
								username: username,
								password: password,
								seedPhrase: secretSeed,
								publicKey: publicKey,
								keystore: serialzedKeystore,
								privateKey: privateKey
							});
							user.save(function(err, user) {
								if (err) { res.send(err); } else {
									res.send(user);
								}
							}); //save this generated wallet information to database, so we don't have to generate this everytime
						}
					});
				}
			});
		} else if (password != user.password) {
			res.send("Wrong Password or User does not exist"); // if password does not match we get this error
		} else {
			res.send(user); // if user informaation is already generated and password is matched, it will respond with the information saved in the database
		}
	});
});

app.listen(3000, function(){
	console.log('Example app listening on port 3000!')
});
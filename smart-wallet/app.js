var express = require('express');
var bodyParser = require('body-parser');
var lightwallet = require('eth-lightwallet');
var keythereum = require('keythereum');
var mysql = require('mysql');

var app = express();
app.use(bodyParser.json());



var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'admin',
  password : 'password',
  database : 'db_dapp'
});
connection.connect();


app.post('/wallet', function(req, res) { // it will listen for a post method with JSON body having "username" and "password"
	var username = (req.body.username);
	var password = (req.body.password);

	connection.query('SELECT * FROM Table_UserInfo WHERE Username = "'+username+'"', function (error, results, fields) { //to check if the user exists in the database
	  if (error) { console.log(error); } else if (results.length) {
	  	// found user
	  	var userinfo = results[0];
	  	// check password match or not
	  	if (password == results[0].Passwords) {
	  		// password matched
	  		// search for wallet in wallet info
		  	connection.query('SELECT * FROM Table_WalletInfo WHERE UserID = "'+results[0].UserID+'" ', function (error, results, fields) {
			  if (error) { console.log(error); } else if (results.length) {
			  	// found wallet information
			  	// send user information
			  	console.log(results[0]);
			  	res.send(results[0]);
			  } else {
			  	// wallet information not found so register him
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
								var serialzedKeystore = ks.serialize(); // this is users json wallet that contains encrypted information about private key and other details
								var publicKey = (ks.getAddresses()[0]);
								var privateKey = (ks.exportPrivateKey(ks.getAddresses()[0], pwDerivedKey)); // this is ethereum private key
								var user = {
									UserID: userinfo.UserID,
									SeedPhrase: secretSeed,
									PublicKey: publicKey,
									KeyStore: serialzedKeystore,
									PrivateKey: privateKey
								};
								connection.query('INSERT INTO Table_WalletInfo SET ?', user, function (error, results, fields) {
								  if (error) throw error;
								  
								  res.send(user);
								})
								
							}
						});
					}
				});

			  }
			});
	  	} else {
	  		// invalid password
	  		// not authorized
	  		res.send("Password is Invalid");
	  	}
	  } else {
	  	// user not present
	  	// invalid user
	  	res.send("User not found");
	  }
	});

	
});

app.listen(3000, function(){
	console.log('Blockheads app listening on port 3000!')
});
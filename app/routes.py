from flask import Flask, render_template, redirect, request, url_for
from app import app

@app.route('/', methods=['get', 'post'])
def index():
    return '''
<html>
  <head>
    <title>Sign In</title>
  </head>
  <body>
    <h1>Sign In</h1>
    <p>username:</p>
    <p>password:</p>
  </body>
</html>
'''

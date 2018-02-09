#!/bin/python

from flask import Flask, request

app = Flask(__name__)

@app.route("/sshaccess/", methods=['post'])
def add_ssh():
    """
    Give ssh permission to user
    to access root
    """
    return "Hello world"

@app.route("/sshaccess/", methods=['delete'])
def delete_ssh():
    """
    Delete ssh permission to user
    to access root
    """
    return "Delete world"

if __name__ == '__main__':
    app.run(debug=True)
#!/bin/python

from flask import Flask, request, make_response, \
                  jsonify
from paramiko import SSHClient, AutoAddPolicy
from json import load

app = Flask(__name__)

@app.route("/sshaccess/", methods=['post'])
def add_ssh():
    """
    Give ssh permission to user
    to access root
    """
    # Check for arguments
    if not request.json or \
       not 'username' in request.json or \
       not 'password' in request.json:
         return make_response(jsonify({'Error':'Missing arguements'}), 400)
    
    with open('allowed_users.json') as json_file:
        data = load(json_file)
        if request.json['username'] not in data['allowed_users']:
            return make_response(jsonify({'Authentication Error': "User is not allowed to access the server"}), 400)
    
    #Establish SSH connection
    try:
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(hostname="localhost", username=request.json['username'],
                    password=request.json['password'])
    except Exception:
        client.close()
        return make_response(jsonify({'Authentication Error': "Please enter valid credentials"}), 400)
    
    #Setup password less communication
    stdin_, stdout_, stderr_ = client.exec_command("echo -e 'n\\n'| ssh-keygen -t rsa -b 4096 -f "
                                                   "/Users/%s/.ssh/id_rsa -P \"\"" %request.json['username'])
    stdout_.channel.recv_exit_status()
    stdin_, stdout_, stderr_ = client.exec_command("cat /Users/%s/.ssh/id_rsa.pub" %request.json['username'])
    stdout_.channel.recv_exit_status()
    user_pub = stdout_.read()

    with open("/Users/Kiran/.ssh/authorized_keys", "r") as read_file:
        file_read = read_file.readlines()
        if user_pub in file_read:
            return make_response(jsonify({'Authentication Error':'User is authenticated already'}), 400)

    with open("/Users/Kiran/.ssh/authorized_keys", "w") as write_file:
        file_read.append(user_pub)
        write_file.writelines(file_read)
    return jsonify({'Response':"User is authenticated"}), 200


@app.route("/sshaccess/", methods=['delete'])
def delete_ssh():
    """
    Delete ssh permission to user
    to access root
    """
    # Check for arguments
    if not request.json or \
       not 'username' in request.json or \
       not 'password' in request.json:
         return make_response(jsonify({'Error':'Missing arguements'}), 400)
    
    #Establish SSH connection
    try:
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(hostname="localhost", username=request.json['username'],
                    password=request.json['password'])
    except Exception:
        client.close()
        return make_response(jsonify({'Authentication Error': "Please enter valid credentials"}), 400)
 
    stdin_, stdout_, stderr_ = client.exec_command("cat /Users/%s/.ssh/id_rsa.pub" %request.json['username'])
    if (stdout_.channel.recv_exit_status() != 0):
        return make_response(jsonify({'Public key error': "Error in reading public key"}), 400)
    user_pub = stdout_.read()

    with open("/Users/Kiran/.ssh/authorized_keys", "r") as read_file:
        file_read = read_file.readlines()
        if user_pub not in file_read:
            return make_response(jsonify({'Authentication Error':'User is not authenticated already'}), 400)

    with open("/Users/Kiran/.ssh/authorized_keys", "w") as write_file:
        file_read.remove(user_pub)
        write_file.writelines(file_read)
    return jsonify({'Response':"Authenticated is removed successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
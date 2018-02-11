# SSH Key Management (Mac OSX)

## Prerequisites
- pip install -r requirements.txt
- allowed_users.json will contain list of users who are allowed to access admin

## Add/Remove users
- sudo ./create_user.sh \<username> \<password>
- sudo ./delete_user.sh \<username>

## Start the server from admin
- python app.py

## Add/remove ssh access to the admin from the user
- POST: (Add ssh access to admin)
    * curl -i -H "Content-Type: application/json" -X POST -d '{"username":"\<username>","password":"\<password>"}' http://localhost:5000/sshaccess/
    * Expected response:
        * ```HTTP/1.0 200 OK
          Content-Type: application/json
          Content-Length: 42
          Server: Werkzeug/0.14.1 Python/2.7.10
          Date: Sat, 10 Feb 2018 20:42:37 GMT
          {
            "Response": "User is authenticated"
          }
     * User can do passwordless ssh connection with admin
  
- DELETE: (Remove ssh access from admin)
    * curl -i -H "Content-Type: application/json" -X DELETE -d '{"username":"\<username>","password":"\<password>"}' http://localhost:5000/sshaccess/
    * Expected response:
        * ```HTTP/1.0 200 OK
             Content-Type: application/json
             Content-Length: 58
             Server: Werkzeug/0.14.1 Python/2.7.10
             Date: Sat, 10 Feb 2018 20:44:34 GMT
             {
                "Response": "Authenticated is removed successfully"
             }
    * User cannot do passwordless ssh connection with admin
  
  ## If admin wants to remove access of the user
  - sudo ./admin_remove_auth.sh \<admin> \<user>
  

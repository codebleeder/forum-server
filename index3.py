#!/usr/bin/env python

print """Content-type: text/html\r\n\r\n
<html>
    <head>
        <title>The Forum </title>
    </head>
    <body>
        <h2>The Forum </h2><br/>
        <form method="post" action="login2.py">
            username:<input type="text" name="username"><br/>
            password:<input type="text" name="password"><br/>
            <input type="submit" value="Submit">
        </form><br/><br/>

        <h3> sign up </h3><br/>
        <form method="post" action="signup.py">
            new username:<input type="text" name="new_username"><br/>
            new password:<input type="text" name="new_password"><br/>
            confirm new password:<input type="text" name="confirm_new_password"><br/>
            <input type="submit" value="Submit">
        </form>
    </body>
</html>
"""

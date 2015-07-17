#!/usr/bin/env python

print """Content-type: text/html\r\n\r\n
<html>
    <head>
        <title>The Forum </title>
    </head>
    <body>
        <h2>The Forum </h2><br/>
"""
for i in range(1, 4):
    print '<h3>(%s) survey corps </h3>' %(i)
print """
        <form method="post" action="login.py">
            username:<input type="text" name="username"><br/>
            password:<input type="text" name="password"><br/>
            <input type="submit" value="Submit">
        </form>
    </body>
</html>
"""

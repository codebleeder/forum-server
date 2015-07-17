#!/usr/bin/env python

print """Content-type: text/html
<h2> The Forum </h2>

<form method="post" action="login.py">
username:<input type="text" name="username"><br/>

password:<input type="text" name="password"><br/>

<input type="submit" value="Submit">
</form>"""

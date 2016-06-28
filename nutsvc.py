import json
import imaplib
import email
#import uuid
import cgi 
import sys
from email.mime.text import MIMEText
from subprocess import Popen, PIPE
from email.message import EmailMessage
from mysql.connector import (connection)

sys.path.append('/srv/http/nut')
import config


def application(environ, start_response):
	status = '200 OK'
	response_headers = [('Content-type', "application/json")] # "text/plain")]
#	if environ['REQUEST_METHOD'] != 'POST':
#			start_response(status,response_headers )
#			return [bytes(json.dumps('NOT POST'),'utf-8')]
	post_env = environ.copy()
	post_env['QUERY_STRING'] = ''
	post = cgi.FieldStorage(
			fp=environ['wsgi.input'],
			environ=post_env,
			keep_blank_values=True
		)
	try:
		qali = post['qali'].value
	except:
		start_response(status,response_headers )
		return [bytes("INVALID QUERY",'utf-8')]

	cnx = connection.MySQLConnection(user=config.username, 
				password=config.password,
                                 host=config.server,
                                 database='USDA')
	cursor = cnx.cursor()

	query = ("SELECT NDB_No,Long_Desc FROM `VIEW_P_V2` "
        	 "WHERE Long_Desc LIKE '%%%s%%'"%qali)
	cursor.execute(query)
	result = []
	for (idAli,descAli) in cursor:
		result.append( (idAli,descAli) )
	start_response(status,response_headers )
	#return [bytes(json.dumps('NOT POST'),'utf-8')]
	return [bytes(json.dumps(result),'utf-8')]

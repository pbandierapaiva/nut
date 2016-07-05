import json
import imaplib
import email
#import uuid
import cgi 
import sys
#from email.mime.text import MIMEText
#from subprocess import Popen, PIPE
from email.message import EmailMessage
from mysql.connector import (connection)

#from bottle import route, run, template

sys.path.append('/srv/http/nut')
import config

def dbConnection():
	cnx = connection.MySQLConnection(user=config.username, 
				password=config.password,
                                 host=config.server,
                                 database=config.database)
	return cnx   #.cursor()


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
	operation = None
	try:
		opera = post['op'].value  # QUERY / FETCH
	except:
		start_response(status,response_headers )
		return [bytes("No operation specified",'utf-8')]



	try:
		qali = post['q'].value
	except:
		start_response(status,response_headers )
		return [bytes("INVALID QUERY",'utf-8')]

	cnx = dbConnection()
	cursor = cnx.cursor()
	
	if opera=='QUERY':
		query = ("SELECT NDB_No,Long_Desc FROM `VIEW_P_V2` "
			 "WHERE Long_Desc LIKE '%%%s%%'"%qali)
		cursor.execute(query)
		result = []
		for (idAli,descAli) in cursor:
			result.append( (idAli,descAli) )
		start_response(status,response_headers )
		#return [bytes(json.dumps('NOT POST'),'utf-8')]
		return [bytes(json.dumps(result),'utf-8')]

	if opera=='FETCH':
		query = ("SELECT NutrDesc,Nutr_Val,Units FROM `VIEW_P_V3_X0` "
			 "WHERE NDB_No = '%s'"%qali)
		cursor.execute(query)
		result = []
		for (desc,val,unit) in cursor:
			result.append( (desc,val,unit))
		start_response(status,response_headers )
		return [bytes(json.dumps(result),'utf-8')]
	if opera=='MEDIDAS':
		query = ("SELECT Msre_Desc,Seq,Gm_Wgt FROM `P_V3_X1` "
			 "WHERE NDB_No = '%s' AND Amount=1"%qali)
		cursor.execute(query)
		result = []
		for (medida,seq,peso) in cursor:
			result.append( (medida,seq,peso))
		start_response(status,response_headers )
		return [bytes(json.dumps(result),'utf-8')]




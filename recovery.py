#!/usr/bin/python3

#import MySQLdb as mysql
import mysql.connector as mysql
import re
import logging
import logging.config

logfile='/home/eepdev/ServiceNow/Edge-Encryption-Proxy-Dev-01_443/logs/masking_recovery.log'
logging.basicConfig(filename=logfile,format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)


'''
Recovery from org_value to edge_token_map table
'''


dburl = 'rds-itms-dev-eep.cbg6qfufehbi.ap-northeast-2.rds.amazonaws.com'
dbuser = 'eepdev'
dbuserpw = 'ServiceNow'
database = 'eepdev'

con = mysql.connect(host=dburl, user=dbuser, passwd=dbuserpw, db=database)

cur = con.cursor()

# org_value : 
# - field1 : value
# - field2 : token

cur.execute("SELECT field2 FROM org_value")
tokens =[]

for val in cur.fetchall():
#    sql = "SELECT value FROM edge_token_map WHERE value = '" + j + "'"
    sql = "UPDATE edge_token_map SET value = (SELECT field1 FROM org_value WHERE field2 = '"
    sql = sql + val[0] + "') WHERE token = '" + val[0] + "'"
    text = 'Recover: ' + val[0]

    cur.execute(sql)

    logging.debug(text+"\t:"+val[0])
#    print(sql)
#print(cur.fetchall())

con.commit()
con.close()

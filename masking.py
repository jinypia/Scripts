#!/usr/bin/python3

#import MySQLdb as mysql
import mysql.connector as mysql
import re
import logging
import logging.config

logfile='/home/eepdev/ServiceNow/Edge-Encryption-Proxy-Dev-01_443/logs/masking.log'
logging.basicConfig(filename=logfile,format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)


'''
Mobile Phone : 010-1234-1234    regexp : [0][1]\d-\d{3,4}-\d{4}
Res No.      : 123456-1234567   regexp : \d{6}-\d{7}
License No.  : 12-12-123456-12  regexp : \d{2}-\d{2}-\d{6}-\d{2}
Others       : ETC (Card)
'''

# Pattern check
def patterns(val):
    regs = {}

    # Add patterns
    regs['[0][1]\d-\d{3,4}-\d{4}'] = 'PhoneNo.'
    regs['\d{6}-\d{7}'] = 'ResidenceNo.'
    regs['\d{2}-\d{2}-\d{6}-\d{2}'] = 'DriverLicenseNo.'

    for reg in regs.keys():
        p = re.compile(reg)
        if p.match(val):
            return regs[reg]
    return 'CardNo.'

# DBMS Information 
dburl = 'rds-itms-dev-eep.cbg6qfufehbi.ap-northeast-2.rds.amazonaws.com'
dbuser = 'eepdev'
dbuserpw = 'ServiceNow'
database = 'eepdev'

con = mysql.connect(host=dburl, user=dbuser, passwd=dbuserpw, db=database)
cur = con.cursor()

# Select value in edge_token_map table, which is not masked
cur.execute("SELECT value FROM edge_token_map")
notMasks =[]

for val in cur.fetchall():
    if val[0][-1] != '●':
        notMasks.append(val[0])

# Each value remains original one except the last 4 characters
for val in notMasks:
#    sql = "SELECT value FROM edge_token_map WHERE value = '" + j + "'"
#    sql = "UPDATE edge_token_map SET value = CONCAT(SUBSTRING(value, 1, 4), LPAD('*', CHAR_LENGTH(value)-4, '*')) WHERE value = '" + val + "'"
    no = patterns(val) 
    text = val[0:-4]
    for i in range(len(val)-4, len(val)):
        if val[i] == '-':
            text += '-'
        else:    
            text += '●'

    sql = "UPDATE edge_token_map SET value = '" + text +"' WHERE value = '" + val + "'"
    cur.execute(sql)
#    print(sql)

    logging.debug(text+" "+ no+ "\t:"+val)
#print(cur.fetchall())

con.commit()
con.close()

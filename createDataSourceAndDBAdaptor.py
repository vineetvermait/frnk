import time as t2
import sys
import os
from mocks import *

propFile = open(sys.argv[1])
all_data = []
for i in propFile:
    all_data += [[0] + [x for x in i.split(';')]]

credentialsPropFile = open(sys.argv[2])
credentials_map = {}
for i in credentialsPropFile:
    prop = i.split('=')
    credentials_map[prop[0]] = prop[1]

print(credentials_map)
# don't change the below ones


#
# method definitions
#



def main(args):
    # admin server url
    url = credentials_map['admin.url'].replace('\n', '')  # 't3://localhost:7101'
    username = credentials_map['admin.userid'].replace('\n', '')  # 'weblogic'
    password = credentials_map['admin.password'].replace('\n', '')  # 'welcome1'
    eis_name = 'eis/db/' + str(args[1])  # 20180507'
    ds_name = args[1]  # '20180507'
    jndi_name = 'jbdc/' + str(args[1])  # 20180507'
    server_name = args[2]  # 'DefaultServer'
    db_url = args[3]  # 'jdbc:oracle:thin:@localhost:1521:xe'
    db_user = args[4]  # 'system'
    db_password = args[5]  # 'oracle'
    db_driver = args[6]  # 'oracle.jdbc.xa.client.OracleXADataSource'
    domain = args[7]  # 'soa12c_domain'

    uniqueString = str(int(t2.time()))

    #
    # Create a JDBC Data Source.
    #

    try:
        print('=-> about to connect to weblogic')
        connect(username, password, url)
        print('=-> about to create a data source ' + ds_name)
        edit()
        startEdit()

        save()
        print('=-> activating changes')
        activate()
        print('=-> done')

        #
        # update the deployment plan
        #
        print('=-> about to update the deployment plan for the DbAdapter')
        startEdit()


    except:
        print('=-> something went wrong, bailing out')
        stopEdit('y')

    print('=-> disconnecting from admin server now')
    disconnect()


#
# this is the main entry point
#

for d in all_data:
    main(d)

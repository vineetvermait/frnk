import sys
import os
from mocks import *
from wlstLib import *

appName = 'FtpAdapter'

moduleOverrideName = appName + '.rar'
moduleDescriptorName = 'META-INF/weblogic-ra.xml'

soaHome = sys.argv[1]
appPath = soaHome + '/soa/soa/connectors/' + moduleOverrideName
planPath = soaHome + '/soa/soa/FTPAdapterPlan.xml'

print('Connecting to local weblogic domain... ')
username = sys.argv[2]
password = sys.argv[3]
url = sys.argv[4]

connect(username, password, url)

#
# Method to insert variable to deployment plan
#


#
# Update property for FTP adapter
#


#
# Method to create new FTP connection factory
#


#
# Create FTP connection factories
#
try:
    edit()
    startEdit()

    propFile = open(sys.argv[5])
    all_data = []
    for i in propFile:
        all_data += [[0] + [x for x in i.split(',')]]
    print(all_data)
    for data in all_data:
        create_ftp_connection_factory('eis/Ftp/' + data[1], data[2], data[3], data[4], data[5], data[6], data[7])

    print('Updating and restarting application...')

    cd('/AppDeployments/FtpAdapter/Targets');
    updateApplication(appName, planPath);
    startApplication(appName)

    print('Done with changes. Calling activate...')

    activate()
except:
    print('Unexpected error: ', sys.exc_info()[0])
    dumpStack()
    raise

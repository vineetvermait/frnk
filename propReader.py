from wlstLib import *

propFile = open('/workspace/frnk/build.properties')
properties = {}

for prop in propFile:
    if not prop.startswith('#') and prop.strip() != "":
        prop = prop.split("=")
        properties[prop[0].strip()] = prop[1].strip().replace("\n", "")

connect(properties['credentials.admin.userId'],
        properties['credentials.admin.password'],
        properties['credentials.admin.url'])
edit()
startEdit()

print("-----------------Creating JMS Servers----------------------------")

jmsServers = properties['SOA.JMSSERVER.name'].split(",")
for server in jmsServers:
    serverList = [{"name": serverName, "type": serverType} for serverName, serverType in
                  zip(properties['SOA.JMSSERVER.' + server + '.target.name'].split(","),
                      properties['SOA.JMSSERVER.' + server + '.target.type'].split(","))]

    create_jms_server(server, serverList)

print("-----------------Creating JMS Modules----------------------------")
jmsModules = properties['SOA.JMSMODULE.name'].split(",")
for module in jmsModules:
    serverList = [{"name": serverName, "type": serverType} for serverName, serverType in
                  zip(properties['SOA.JMSMODULE.' + module + '.target.name'].split(","),
                      properties['SOA.JMSMODULE.' + module + '.target.type'].split(","))]

    create_jms_module(module, serverList)
print("-----------------Creating JMS SubModules----------------------------")

jmsSubModules = properties['SOA.JMSSUBDEPLOYMENT.name'].split(",")
for subModule in jmsSubModules:
    module = properties['SOA.JMSSUBDEPLOYMENT.' + subModule + '.parent.module']
    serverList = [{"name": serverName, "type": serverType} for serverName, serverType in
                  zip(properties['SOA.JMSSUBDEPLOYMENT.' + subModule + '.target.names'].split(","),
                      properties['SOA.JMSSUBDEPLOYMENT.' + subModule + '.target.types'].split(","))]
    create_jms_sub_deployment(subModule, module, serverList)

print("-----------------Creating EventQueues----------------------------")

eventQueues = properties['SOA.EVENTQUEUE.names'].split(",")
for eventQueue in eventQueues:
    module = properties['SOA.' + eventQueue + '.module']
    subModule = properties['SOA.' + eventQueue + '.submodule']
    create_event_queues(eventQueue, module, subModule)

print("-----------------Creating EventQueue Connection Factories----------------------------")

connectionFactories = properties['SOA.EVENTCONNECTIONFACTORY.names'].split(",")
for connectionFactory in connectionFactories:
    module = properties['SOA.' + connectionFactory + '.jmsmodule']
    create_event_connection_factory(connectionFactory, module)

print("-----------------Creating DataSources----------------------------")

data_sources = properties['SOA.DATASOURCE.names'].split(",")
for data_source in data_sources:
    url = properties['SOA.' + data_source + '.db.url']
    user_id = properties['SOA.' + data_source + '.db.user']
    password = properties['SOA.' + data_source + '.db.password']
    driver = properties['SOA.' + data_source + '.db.driver']
    serverList = [{"name": serverName, "type": serverType} for serverName, serverType in
                  zip(properties['SOA.' + data_source + '.targets.server.names'].split(","),
                      properties['SOA.' + data_source + '.targets.server.types'].split(","))]
    # ds_name, db_url, db_driver, db_user, db_password, targets
    create_ds(data_source, url, user_id, password, driver, serverList)

redeploy_db_adapter(data_sources)

print("-----------------Creating FTP Adapters----------------------------")

ftp_adapters = properties['SOA.FTPADAPTER.names'].split(",")
soa_home = properties['SOA.HOME']

for adapter in ftp_adapters:
    ftp_type = properties['SOA.FTPADAPTER.' + adapter + '.type']
    host = properties['SOA.FTPADAPTER.' + adapter + '.host']
    port = properties['SOA.FTPADAPTER.' + adapter + '.port']
    secure_port = properties['SOA.FTPADAPTER.' + adapter + '.secureport']
    user = properties['SOA.FTPADAPTER.' + adapter + '.user']
    password = properties['SOA.FTPADAPTER.' + adapter + '.password']
    create_ftp_connection_factory(soa_home, adapter, ftp_type, host, port, secure_port, user, password)

cd('/AppDeployments/FtpAdapter/Targets')
updateApplication('FtpAdapter', soa_home + '/soa/soa/FTPAdapterPlan.xml')
startApplication('FtpAdapter')

print("---------------------------------------------")

save()
activate()

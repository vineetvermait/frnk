from mocks import *
import time as t2


def update_property_for_ftp_adapter(app_name, deployment_plan, jndi_name, property_name, property_value):
    short_jndi_name = jndi_name.split('/')[2]
    module_descriptor_name = 'META-INF/weblogic-ra.xml'
    res_string = '/weblogic-connector/outbound-resource-adapter/connection-definition-group/' \
                 '[connection-factory-interface="javax.resource.cci.ConnectionFactory"]' \
                 '/connection-instance/[jndi-name="' \
                 + jndi_name + \
                 '"]/connection-properties/' \
                 'properties/property/[name="' + property_name + '"]/value'
    make_deployment_plan_variable(deployment_plan,
                                  'ConfigProperty_' + property_name + '_Value_' + short_jndi_name,
                                  property_value,
                                  res_string,
                                  app_name + '.rar', module_descriptor_name)


def create_ftp_connection_factory(soa_home, jndi_name, ftp_type, host, port, secure_port, username, password):
    app_name = 'FtpAdapter'
    jndi_name = 'eis/Ftp/' + jndi_name
    app_path = soa_home + '/soa/soa/connectors/' + app_name + '.rar'
    plan_path = soa_home + '/soa/soa/FTPAdapterPlan.xml'
    module_descriptor_name = 'META-INF/weblogic-ra.xml'
    new_plan = loadApplication(app_path, plan_path)
    res_string = '/weblogic-connector/outbound-resource-adapter/connection-definition-group/' \
                 '[connection-factory-interface="javax.resource.cci.ConnectionFactory"]' \
                 '/connection-instance/[jndi-name="' + jndi_name + '"]/jndi-name'

    make_deployment_plan_variable(new_plan, 'ConnectionInstance_' + jndi_name + '_JNDIName', jndi_name,
                                  res_string,
                                  app_name + '.rar',
                                  module_descriptor_name)

    if ftp_type == 'sftp':
        update_property_for_ftp_adapter(app_name, new_plan, jndi_name, 'UseFtps', 'false')
        update_property_for_ftp_adapter(app_name, new_plan, jndi_name, 'UseSftp', 'true')
    elif ftp_type == 'ftps':
        update_property_for_ftp_adapter(app_name, new_plan, jndi_name, 'UseFtps', 'true')
        update_property_for_ftp_adapter(app_name, new_plan, jndi_name, 'UseSftp', 'false')
    else:
        update_property_for_ftp_adapter(app_name, new_plan, jndi_name, 'UseFtps', 'false')
        update_property_for_ftp_adapter(app_name, new_plan, jndi_name, 'UseSftp', 'false')

    update_property_for_ftp_adapter(app_name, new_plan, jndi_name, 'Host', host)
    update_property_for_ftp_adapter(app_name, new_plan, jndi_name, 'Username', username)
    update_property_for_ftp_adapter(app_name, new_plan, jndi_name, 'Password', password)
    update_property_for_ftp_adapter(app_name, new_plan, jndi_name, 'Port', port)
    update_property_for_ftp_adapter(app_name, new_plan, jndi_name, 'SecurePort', secure_port)

    new_plan.save()
    save()


def make_deployment_plan_variable(wlst_plan,
                                  name,
                                  value,
                                  xpath,
                                  module_override_name,
                                  module_descriptor_name,
                                  origin='planbased'):
    variable_assignment = wlst_plan.createVariableAssignment(name, module_override_name, module_descriptor_name)
    variable_assignment.setXpath(xpath)
    variable_assignment.setOrigin(origin)
    wlst_plan.createVariable(name, value)


def redeploy_db_adapter(ds_names):
    unique_string = str(int(t2.time()))
    app_name = 'DbAdapter'
    module_override_name = app_name + '.rar'
    module_descriptor_name = 'META-INF/weblogic-ra.xml'
    plan_path = get('/AppDeployments/DbAdapter/PlanPath')
    app_path = get('/AppDeployments/DbAdapter/SourcePath')

    plan = loadApplication(app_path, plan_path)
    for ds_name in ds_names:
        eis_name = "eis/db/" + ds_name
        res_str = '/weblogic-connector/outbound-resource-adapter/connection-definition-group/' \
                  '[connection-factory-interface="javax.resource.cci.ConnectionFactory"]' \
                  '/connection-instance/[jndi-name="' + ds_name + '"]'
        make_deployment_plan_variable(plan, 'ConnectionInstance_eis/DB/' + eis_name + '_JNDIName_' + unique_string,
                                      eis_name,
                                      res_str + '/jndi-name',
                                      module_override_name, module_descriptor_name)
        make_deployment_plan_variable(plan, 'ConfigProperty_xADataSourceName_Value_' + unique_string, eis_name,
                                      res_str +
                                      '/connection-properties/properties/property/[name="xADataSourceName"]/value',
                                      module_override_name, module_descriptor_name)
    plan.save()
    save()
    activate(block='true')
    cd('/AppDeployments/DbAdapter/Targets')
    redeploy(app_name, plan_path, targets=cmo.getTargets())
    print('=-> done')


def create_ds(ds_name, db_url, db_driver, db_user, db_password, targets):
    target_list = [ObjectName('com.bea:Name=' + server['name'] + ',Type=' + server['type']) for server in targets]
    cmo.createJDBCSystemResource(ds_name)
    base_path = '/JDBCSystemResources/' + ds_name + '/JDBCResource/' + ds_name
    cd(base_path)
    cmo.setName(ds_name)
    cd(base_path + '/JDBCDataSourceParams/' + ds_name)
    set('JNDINames', jarray.array([String('jbdc/' + str(ds_name))], String))
    cd(base_path + '/JDBCDriverParams/' + ds_name)
    cmo.setUrl(db_url)
    cmo.setDriverName(db_driver)
    cmo.setPassword(db_password)
    cd(base_path + '/JDBCConnectionPoolParams/' + ds_name)
    cmo.setTestTableName('DUAL')
    cd(base_path + '/JDBCDriverParams/' + ds_name + '/Properties/' + ds_name)
    cmo.createProperty('user')
    cd(base_path + '/JDBCDriverParams/' + ds_name + '/Properties/' + ds_name + '/Properties/user')
    cmo.setValue(db_user)
    cd(base_path + '/JDBCDataSourceParams/' + ds_name)
    cmo.setGlobalTransactionsProtocol('TwoPhaseCommit')
    cd('/JDBCSystemResources/' + ds_name)
    set('Targets', jarray.array(target_list, ObjectName))


def create_jms_server(primary_name, targets):
    target_list = [ObjectName('com.bea:Name=' + server['name'] + ',Type=' + server['type']) for server in targets]
    cd('/')
    cmo.createFileStore(primary_name + 'FileStore')
    cd('/FileStores/' + primary_name + 'FileStore')
    cmo.setDirectory('/FileStores/' + primary_name + 'FileStore')
    set('Targets', jarray.array(target_list, ObjectName))

    cd('/')
    cmo.createJMSServer(primary_name)
    cd('/JMSServers/' + primary_name)
    cmo.setPersistentStore(getMBean('/FileStores/' + primary_name + 'FileStore'))
    set('Targets', jarray.array(target_list, ObjectName))
    return


def create_jms_module(primary_name, targets):
    target_list = [ObjectName('com.bea:Name=' + server['name'] + ',Type=' + server['type']) for server in
                   targets]
    cd('/')
    cmo.createJMSSystemResource(primary_name)
    cd('/JMSSystemResources/' + primary_name)
    set('Targets', jarray.array(target_list, ObjectName))
    return primary_name


def create_jms_sub_deployment(primary_name, jms_module_name, subdeployment_targets):
    target_list = [ObjectName('com.bea:Name=' + server['name'] + ',Type=' + server['type']) for server in
                   subdeployment_targets]
    cd('/JMSSystemResources/' + jms_module_name)
    cmo.createSubDeployment(primary_name)

    cd('/JMSSystemResources/' + jms_module_name + '/SubDeployments/' + primary_name)

    set('Targets', jarray.array(target_list, ObjectName))
    return primary_name


def create_event_queues(primary_name, jms_module_name, jms_subdeployment):
    cd('/JMSSystemResources/' + jms_module_name + '/JMSResource/' + jms_module_name)

    cmo.createUniformDistributedQueue(primary_name)

    cd('/JMSSystemResources/' + jms_module_name + '/JMSResource/'
       + jms_module_name + '/UniformDistributedQueues/' + primary_name)

    cmo.setJNDIName('jms/' + primary_name)

    cd('/JMSSystemResources/' + jms_module_name + '/JMSResource/'
       + jms_module_name + '/UniformDistributedQueues/' + primary_name)

    cmo.setSubDeploymentName(jms_subdeployment)


def create_event_connection_factory(primary_name, jms_module_name):
    cd('/JMSSystemResources/' + jms_module_name + '/JMSResource/' + jms_module_name)

    cmo.createConnectionFactory(primary_name)

    cd('/JMSSystemResources/' + jms_module_name + '/JMSResource/'
       + jms_module_name + '/ConnectionFactories/' + primary_name)

    cmo.setJNDIName('jms/' + primary_name)

    cd('/JMSSystemResources/' + jms_module_name + '/JMSResource/'
       + jms_module_name + '/ConnectionFactories/' + primary_name + '/SecurityParams/' + primary_name)

    cmo.setAttachJMSXUserId(false)
    cmo.setSecurityPolicy('ThreadBased')

    cd('/JMSSystemResources/' + jms_module_name + '/JMSResource/' +
       jms_module_name + '/ConnectionFactories/' + primary_name + '/ClientParams/' + primary_name)

    cmo.setClientIdPolicy('Restricted')
    cmo.setSubscriptionSharingPolicy('Exclusive')
    cmo.setMessagesMaximum(10)

    cd('/JMSSystemResources/' + jms_module_name + '/JMSResource/'
       + jms_module_name + '/ConnectionFactories/' + primary_name + '/TransactionParams/' + primary_name)

    cmo.setXAConnectionFactoryEnabled(true)

    cd('/JMSSystemResources/' + jms_module_name + '/JMSResource/'
       + jms_module_name + '/ConnectionFactories/' + primary_name)

    cmo.setDefaultTargetingEnabled(true)

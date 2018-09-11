def cd(path):
    print("cd", path)


def startApplication(path):
    print("startApplication", path)


def updateApplication(a, b):
    print("updateApplication", a, b)


def getMBean(path):
    print("getMBean", path)
    return path


def connect(a, b, c):
    print("connect", a, b, c)


def edit():
    print("edit")


def dumpStack():
    print("dumpStack")


def startEdit():
    print("startEdit")


def save():
    print("save")


class VariableAssignment:
    def setXpath(self, path):
        print("setXpath", path)

    def setOrigin(self, origin):
        print("setOrigin", origin)


class Plan:
    def save(self):
        print("plan.save")

    def createVariableAssignment(self, name, module_override_name, module_descriptor_name):
        print("createVariableAssignment", name, module_override_name, module_descriptor_name)
        return VariableAssignment()

    def createVariable(self, name, value):
        print("createVariable", name, value)
        return VariableAssignment()


def loadApplication(a, b):
    print("loadApplication", a, b)
    return Plan()


def redeploy(a, b, targets=None):
    print("redeploy", a, b, targets)


def stopEdit(a):
    print('stopEdit', a)


def set(a, b):
    print("set", a, b)


def get(a):
    print("get", a)


def activate(block=""):
    print("activate", block)


def disconnect():
    print("disconnect")


true = True
false = False


class CMO:
    def setName(self, name):
        print("setName", name)

    def getTargets(self):
        print("getTargets")

    def setUrl(self, name):
        print("setUrl", name)

    def setDriverName(self, name):
        print("setDriverName", name)

    def setPassword(self, name):
        print("setPassword", name)

    def setTestTableName(self, name):
        print("setTestTableName", name)

    def createProperty(self, name):
        print("createProperty", name)

    def setValue(self, name):
        print("setValue", name)

    def setGlobalTransactionsProtocol(self, name):
        print("setGlobalTransactionsProtocol", name)

    def createJDBCSystemResource(self, name):
        print("createJDBCSystemResource", name)

    def createFileStore(self, name):
        print("createFileStore", name)

    def createJMSSystemResource(self, name):
        print("createFileStore", name)

    def createUniformDistributedQueue(self, name):
        print("createUniformDistributedQueue", name)

    def setJNDIName(self, name):
        print("setJNDIName", name)

    def setSubDeploymentName(self, name):
        print("setSubDeploymentName", name)

    def setSubscriptionSharingPolicy(self, name):
        print("setSubscriptionSharingPolicy", name)

    def setDirectory(self, name):
        print("setDirectory", name)

    def createJMSServer(self, name):
        print("createJMSServer", name)

    def setPersistentStore(self, name):
        print("setPersistentStore", name)

    def createSubDeployment(self, name):
        print('createSubDeployment', name)

    def createConnectionFactory(self, name):
        print('createConnectionFactory', name)

    def setAttachJMSXUserId(self, name):
        print('setAttachJMSXUserId', name)

    def setSecurityPolicy(self, name):
        print('setSecurityPolicy', name)

    def setClientIdPolicy(self, name):
        print('setClientIdPolicy', name)

    def setMessagesMaximum(self, name):
        print('setMessagesMaximum', name)

    def setXAConnectionFactoryEnabled(self, name):
        print('setXAConnectionFactoryEnabled', name)

    def setDefaultTargetingEnabled(self, name):
        print('setDefaultTargetingEnabled', name)


# setMessagesMaximum


class JArray:
    def array(self, name, d):
        return "jarray.array(" + str(name) + "," + str(d) + ")"


def ObjectName(dummy):
    return dummy


def String(dummy):
    return dummy


cmo = CMO()
jarray = JArray()

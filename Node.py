class Node:
    def __init__(self, labels=[], node_data={}):
        self.labels = labels
        self.node_data = node_data

    def build_attr_map(self):
        _obj = self.node_data
        obj_str = '{'
        for prop in _obj:
            obj_str += prop + ':"' + str(_obj[prop]) + '", '
        obj_str = obj_str[:-2]
        obj_str += '}'
        return obj_str

    def build_node_query(self, var):
        return '(' + var + ':' + ':'.join(self.labels) + self.build_attr_map() + ')'

    def add_label(self, label):
        self.labels += [label]

    def remove_label(self, label):
        if label in self.labels:
            self.labels.remove(label)

    def set_property(self, prop, value):
        self.node_data[prop] = value

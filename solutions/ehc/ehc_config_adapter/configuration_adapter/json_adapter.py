import yaml
import json

class JsonAdapter(object):

    def __init__(self, config_file):
        """docstring for __init__"""
        stream = open(config_file, "r")
        self.docs = json.load(stream)

    def persistent(self):
        for k, v in self.docs.items():
            self.read(k, v)

    def read(self,k,v):
        """docstring for from_json"""
        if str(type(v)) == "<type 'dict'>":
            for k1, v1 in v.items():
                self.read(k1, v1)
        else:
            print k, "->", v
            print '\n'
            return



#adapter = YamlAdapter("../config/E2EWF-1-LC1S.config.yaml")
adapter = JsonAdapter("../test/output.json")
adapter.persistent()
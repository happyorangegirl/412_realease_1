import json
import shlex


class YamlAdapter(object):
    def __init__(self, config, target_file):
        self.key_value_config = {}
        self.target_file = target_file
        if str(type(config)) == "<type 'dict'>":
            self.docs = config
        else:
            stream = open(config, "r")
            self.docs = json.load(stream)

    def persistent(self):
        for k, v in self.docs.items():
            self._read(k, v)
        self._update(self.key_value_config, self.target_file)

    def _read(self, k, v):
        """docstring for from_json"""
        if str(type(v)) == "<type 'dict'>":
            for k1, v1 in v.items():
                self._read(k1, v1)
        else:
            self.key_value_config[k] = v
            print k, "->", v
            return

    def _update(self, config_dict, file):
        print 'Total {} keys will be updated!'.format(len(config_dict))
        _list_content = []
        fh = open(file, 'rb')
        for i in fh.readlines():
            _list_content.append(i)
        fh.close()
        _content = ''
        mandatory_area = False

        for line in _list_content:
            if line.startswith('mandatory'):
                mandatory_area = True
                _content = _content + line
                continue
            if mandatory_area:
                if not line.startswith(' '):
                    mandatory_area = False
                items = shlex.split(line)
                if len(items) == 3 and items[0][:-1] in config_dict.keys():
                    value = str(config_dict[items[0][:-1]])
                    print 'update key {} with value {}'.format(items[0][:-1], value)
                    print 'try to replace {} with {}'.format(items[2],value)
                    quote_str = '\'{}\''.format(items[2])
                    if quote_str not in line and ' ' not in value:
                        line = line.replace(' {}'.format(items[2]), ' {}'.format(value))
                    elif quote_str in line:
                        line = line.replace(quote_str, "\'{}\'".format(value))
                    else:
                        line = line.replace(items[2], value)
                    print 'update line to {}.'.format(line)
            _content = _content + line
            _content = _content.encode("utf-8")
        with open(file, 'wb') as the_file:
            the_file.writelines(_content)
class PatternGenerator(object):
    __error__ = "hahahhaha"
    @classmethod
    def get(cls, key, type):
        if type == 'number':
            return '^-?[0-9]+$'
        else:
            return "."
#        elif 'fqdn' in key:
#            return '(?!-)[A-Z\d-]{1,63}(?<!-)$'
#        else:
#            return '[.]+'

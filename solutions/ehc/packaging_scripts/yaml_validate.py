"""
 Copyright 2017 EMC GSE SW Automation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""


import yaml, sys, os


class YamlValidator(object):
    def __init__(self):
        self.directory = ''
        self._errorlist = []

    def absoluteFilePaths(self, directory):
        for dirpath, _, filenames in os.walk(directory):
            for f in filenames:
                yield os.path.abspath(os.path.join(dirpath, f))

    def validate_yaml_in_dir(self, directory):
        print "Checking yaml files under folder {}".format(directory)
        for f in self.absoluteFilePaths(directory):
            print f
            if f.endswith('yaml'):
                self.is_yaml(f)
            elif os.path.isdir(f):
                self.validate_yaml_in_dir(f)

    def is_yaml(self, file_path):
        with open(file_path, 'r') as stream:
            try:
                yaml.load(stream)
            except yaml.YAMLError, exc:
                self._errorlist.append(str(exc))
            except:
                self._errorlist.append("Error occurred in {}".format(file_path))


if __name__ == "__main__":
    # sys.argv = ['', 'c:/Users/yinl1/ehc_dozer/solutions/ehc/ehc_e2e/conf']
    if len(sys.argv)<2 or not os.path.exists(sys.argv[1]):
        print "Provided directory {} is not valid".format(sys.argv[1])
    else:
        validator = YamlValidator()
        validator.validate_yaml_in_dir(sys.argv[1])
        if validator._errorlist:
            for error_message in validator._errorlist:
                print "\033[0;31;m" + error_message + "\033[0m"
            raise AssertionError(
                'Error occurred in yaml validation process, build fail.')

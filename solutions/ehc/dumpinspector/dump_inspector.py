#  Copyright 2016 EMC HCP SW Automation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import pickle
import sys
import shlex
from termcolor import colored
try:
    # import readline to support moving cursor when typing in console
    import readline
except ImportError:
    # import may have problem
    pass

from ehc_e2e.utils.context.model import YAMLData


class DumpInspector(object):
    colors = {1: 'yellow',
              2: 'green',
              3: 'cyan',
              4: 'red',
              5: 'blue',
              6: 'magenta'}

    def __init__(self, pickle_file):
        self.dump_file = pickle_file
        file2 = open(pickle_file, 'rb')
        self._dict = pickle.load(file2)

    def reload(self):
        file2 = open(self.dump_file, 'rb')
        self._dict = pickle.load(file2)
        print colored('Dump file is reloaded successfully!', 'green')

    def commit(self):
        with open(self.dump_file, 'wb') as dfile:
            pickle.dump(self._dict, dfile)
            print colored('Dump file is updated successfully!', 'green')

    def set_back(self, path_string, new_value):
        parts = path_string.split('.')
        if path_string.startswith('workflow.') and len(parts) > 1:
            self._set_attribute(self._dict, parts[1:], new_value)
            print colored('Dump key is updated successfully!', 'green')
            print colored('You can enter \'commit\' to save all changes persistent to dump file!', 'green')
        else:
            print colored('[ERROR] Key path is not started with \'workflow\' or not found!!', 'red')

    def pop_from_list_or_dict(self, path_string):
        parts = path_string.split('.')
        if path_string.startswith('workflow.') and len(parts) > 1:
            pass
        else:
            print colored('[ERROR] Key path is not started with \'workflow\' or not found!!', 'red')

        self._pop_list_or_dict(self._dict, parts[1:])

    def _pop_list_or_dict(self, target_obj, parts):
        final_attribute_index = len(parts) - 1
        current_attribute = target_obj
        i = 0
        for part in parts:
            is_list = False
            if part is None:
                print colored('[ERROR] None part found, please check the commands your input, maybe exits "..", '
                              'should be .B.C', 'red')
                return
            if part.endswith(']') and '[' in part:
                index = self._get_index_from_str(part)
                target_part = part[:part.index('[')]
                is_list = True
            else:
                target_part = part

            if not hasattr(current_attribute, target_part):
                print colored('No attribute <{}> found, no need to pop.'.format(part), 'green')
                return

            current_list = getattr(current_attribute, target_part)

            if i == final_attribute_index:
                if is_list:
                    if len(current_list) < index + 1:
                        print colored('Length of list: {} is {}, less then index: {}, no need to pop.'.format(part, len(
                            current_list), index), 'green')
                        return
                    else:
                        current_list.pop(index)
                        print colored('Dump key is updated successfully!', 'green')
                        print colored('You can enter \'commit\' to save all changes persistent to dump file!', 'green')
                        return
                else:
                    # pop key from dict
                    if hasattr(current_attribute, '__dict__'):
                        current_attribute.__dict__.pop(target_part)
                        print colored('Key <{}> is removed successfully!'.format(target_part), 'green')
                        print colored('You can enter \'commit\' to save all changes persistent to dump file!', 'green')
                        return
                    else:
                        print colored("[ERROR] The parent of <{}> don't have any key-value pair , so cannot remove it.".
                            format(target_part), 'red')
                        return

            if is_list:
                if not current_list:
                    print colored('Empty list: {} found, no need to pop.'.format(part), 'green')
                    return
                elif len(current_list) < index + 1:
                    print colored('Length of list: {} is {}, less then index: {}, no need to pop.'.format(part, len(current_list), index), 'green')
                    return

            current_attribute = current_list[index] if is_list else current_list

            if not current_attribute:
                print colored('None value for : {}, no need to pop.'.format(target_part), 'green')
                return

            i += 1

    def _set_attribute(self, target_obj, parts, new_value):

        final_attribute_index = len(parts) - 1
        current_attribute = target_obj
        i = 0
        for part in parts:
            is_list = False
            if part.endswith(']') and '[' in part:
                index = self._get_index_from_str(part)
                target_part = part[:part.index('[')]
                is_list = True
            else:
                target_part = part
            if not hasattr(current_attribute, target_part):
                if is_list:
                    init_list = [YAMLData() for j in xrange(index+1)]
                    setattr(current_attribute, target_part, init_list)
                else:
                    setattr(current_attribute, target_part, YAMLData())
            else:
                if is_list:
                    if not isinstance(getattr(current_attribute, target_part), list):
                        setattr(current_attribute, target_part, [])
                    current_list = getattr(current_attribute, target_part)
                    if len(current_list) < index+1:
                        starter = len(current_list)
                        current_list.extend([YAMLData() for k in xrange(starter, index+1)])
                    setattr(current_attribute, target_part, current_list)
            if current_attribute is None:
                print 'Error %s not found in %s' % (part, current_attribute)
                break
            # Set from A.B.C = 1 -> A.B.C.D[0] = 2 or A.B.C.D = 3.
            # C is str but need to add one attribute D, so need set C to type of YAMLData.
            if i != final_attribute_index:
                new_attr = getattr(current_attribute, target_part, None)[index] if is_list else getattr(
                    current_attribute, target_part, None)
                if not hasattr(new_attr, '__dict__'):
                    if is_list:
                        getattr(current_attribute, target_part)[index] = YAMLData()
                    else:
                        setattr(current_attribute, target_part, YAMLData())
            else:
                if is_list:
                    getattr(current_attribute, target_part)[index] = new_value
                    # self._set_attr_in_list(current_attribute, part, new_value)
                else:
                    if new_value == '[]':
                        setattr(current_attribute, part, [])
                    else:
                        setattr(current_attribute, part, new_value)

            new_attr = getattr(current_attribute, target_part, None)[index] if is_list else getattr(current_attribute,
                                                                         target_part, None)
            current_attribute = new_attr
            i += 1

    def _set_attr_in_list(self, target_obj, attr, new_value):
        if attr.endswith(']') and '[' in attr:
            attr_in_list = attr[:attr.index('[')]
            index = self._get_index_from_str(attr)
            if index != -1:
                original_list = getattr(target_obj, attr_in_list, None)
                if original_list is None or not isinstance(original_list, list):
                    original_list = []
                if len(original_list) < index + 1:
                    starter = len(original_list)
                    original_list.extend(['' for j in xrange(starter, index-1)])
                    original_list.append(new_value)
                else:
                    original_list[index] = new_value
                setattr(target_obj, attr_in_list, original_list)
            else:
                print colored('[ERROR] Error happened in writing back the changes to dump file', 'red')
        elif new_value == '[]':
            setattr(target_obj, attr, [])

    def _get_index_from_str(self, str_value):
        starter = str_value.index('[') + 1
        end = str_value.index(']')
        index = str_value[starter:end]
        if index.isdigit() is True:
            return int(index)
        else:
            return -1
        return index

    def view(self, parent, ctx_dict, level, wd_filters):
        if level == 1:
            ctx_dict = self._dict
        if level > 6:
            return
        for attr in dir(ctx_dict):
            if not attr.startswith('__'):
                value = getattr(ctx_dict, attr)
                if str(type(value)) == "<type 'builtin_function_or_method'>":
                    return
                if str(type(value)) == "<class 'ehc_e2e.utils.context.model.YAMLData'>":
                    current_parent = "{}.{}".format(parent, colored(attr, self.colors[level]))
                    level += 1
                    self.view(current_parent, value, level, wd_filters)
                    level -= 1
                elif str(type(value)) == "<type 'list'>":
                    current_parent = "{}.{}".format(parent, colored(attr, self.colors[level]))
                    for index, item in enumerate(value):
                        current_parent_in_list = "%s[%s]" % (current_parent, colored(index, self.colors[level]))
                        if str(type(item)) == "<type 'str'>" or str(type(item)) == "<type 'unicode'>":
                            if wd_filters is None:
                                print "%s = %s" % (current_parent_in_list, str(item))
                            else:
                                for wd_filter in wd_filters:
                                    if str(wd_filter).lower() in current_parent_in_list.lower() or str(wd_filter).lower() in str(attr).lower():
                                        print "%s = %s" % (current_parent_in_list, str(item))
                        else:
                            level += 1
                            self.view(current_parent_in_list, item, level, wd_filters)
                            level -= 1
                    if len(value) == 0:
                        if wd_filters is None:
                            print "%s = %s" % (current_parent, '[]')
                        else:
                            for wd_filter in wd_filters:
                                if str(wd_filter).lower() in current_parent.lower():
                                    print "%s = %s" % (current_parent, '[]')

                else:
                    if wd_filters is None:
                        print "%s.%s = %s" % (parent, colored(attr, self.colors[level]), value)
                    else:
                        for wd_filter in wd_filters:
                            if str(wd_filter).lower() in parent.lower() or str(wd_filter).lower() in str(attr).lower():
                                print "%s.%s = %s" % (parent, colored(attr, self.colors[level]), value)


if __name__ == '__main__':
    # sys.argv[1:] = r'C:/Users/yinl1/AppData/Local/Temp/2/dump-20170714-052449.yaml'.split()
    if not sys.argv[1:]:  # nothing input
        print 'NOT valid input'
        exit(-1)
    pi = DumpInspector(sys.argv[1])
    print ' '
    print ' '
    print '#' * 80
    print '#{}#'.format(' ' * 78)
    print '#{}#'.format(' ' * 78)
    print '#{}{}{}#'.format(' ' * 22, colored('Welcome to Dump file debugger v1.1', 'yellow'), ' ' * 22)
    print '#{}#'.format(' ' * 78)
    print '#{}#'.format(' ' * 78)
    print '#{}#'.format(' ' * 78)
    print '#' * 80
    print ' '
    while True:
        print ' '
        print "Please input the commands. [view/set/remove/commit/reset/exit/help]"
        print ' '
        user_input = raw_input('>')
        # user_input = "set \'workflow.current_context.added_cloud_storage[0].cluster_name = \'CRK-LON-CA-C1\'\'"
        # user_input = "remove \'workflow.current_context.vro.address\'"
        # user_input = "view  \'added_cloud_storage\'"
        # user_input = "commit"

        # remove space before and after "=".
        user_input = '='.join([part.strip() for part in user_input.split('=')])
        commands = shlex.split(user_input)
        if commands[0] == 'view':
            wd_filters = None if len(commands) == 1 else commands[1:]
            pi.view('workflow', None, 1, wd_filters)
        elif commands[0] == 'exit':
            print 'Thank you for using!'
            break
        elif commands[0] == 'set':
            if len(commands) < 2:
                print colored('[ERROR] Please provide the key and value to set, example: set key1.key2=value', 'red')
            else:
                key_value_formula = commands[1].split('=')
                key_value_formula = [ele.strip() for ele in key_value_formula]
                if len(key_value_formula) != 2:
                    print colored('[ERROR] Invalid formula, example: set key1.key2=value', 'red')
                else:
                    pi.set_back(key_value_formula[0], key_value_formula[1])
        elif commands[0] == 'remove':
            if len(commands) != 2:
                print colored('[ERROR] Invalid formula, example: remove key1.key[2] or remove key1.key3', 'red')
            else:
                pi.pop_from_list_or_dict(commands[1])
        elif commands[0] == 'commit':
            pi.commit()
        elif commands[0] == 'reset':
            pi.reload()
        elif commands[0] == 'help':
            print ''
            print 'Example: >{} --> display all keys and values in dump file'.format(colored('view','yellow'))
            print 'Example: >{} --> display all keys and values whose keys include \'specific_key\' in dump file'.format(colored('view specific_key','yellow'))
            print 'Example: >{} --> set value D to key A.B.C, using quotes if there is space in the key'.format(colored('set workflow.A.B.C=D','yellow'))
            print 'Example: >{} --> remove special key and value.'.format(colored('remove workflow.A.B[0].C[2] | remove workflow.A.B.C', 'yellow'))
            print 'Example: >{} --> Commit all changes to dump file'.format(colored('commit', 'yellow'))
            print 'Example: >{} --> Reset all changes in the memory'.format(colored('reset', 'yellow'))
            print 'Example: >{} --> exit from the command line'.format(colored('exit', 'yellow'))
        else:
            print 'Option Not Implemented!'
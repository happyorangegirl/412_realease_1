#  Copyright 2016 EMC HCE SW Automation
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

import sys, os
import argparse
import errno
import yaml
import glob
from colorama import Fore, init as colorinit
from functools import partial
from collections import OrderedDict
from distutils.util import strtobool
from robot.api import TestSuite
from ehc_e2e.setting import cleanup_before_workflow_execution as need_clean_up

# WORKFLOW_DIR = r'C:\ehc411_release_scenario\solutions\ehc\ehc_e2e\robot_tests\workflows'
# SCENARIO_DIR = r'C:\ehc411_release_scenario\solutions\ehc\ehc_e2e\robot_tests\scenarios'
# RESOURCE_FILE = r'C:\ehc411_release_scenario\solutions\ehc\ehc_e2e\robot_tests\scenarios\resources\ehc.robot'
# YAMLFile = r'C:\ehc411_release_scenario\solutions\ehc\ehc_e2e\conf\generic.yaml'
# CLEANUP_FILE_PATH = r'C:\Python27\Lib\site-packages\RestCleanup\cleanup.py'
# LISTENER_FILE_PATH = r'C:\ehc411_release_scenario\solutions\ehc\autocli\EHCAutoCLIListener.py'
# WF_DUMP_FILE_PATH = 'C:\ehc411_release_scenario\solutions\ehc\ehc_e2e\dump'
# SN_DUMP_FILE_PATH = 'C:\ehc411_release_scenario\solutions\ehc\ehc_e2e\dump'

WORKFLOW_DIR = r'/root/automation/ehc/workflows'
SCENARIO_DIR = r'/root/automation/ehc/scenarios'
RESOURCE_FILE = r'/root/automation/ehc/resources/ehc.robot'
YAMLFile = r'/root/automation/ehc/config/generic.yaml'
CLEANUP_FILE_PATH = r'/usr/lib/python2.7/site-packages/RestCleanup/cleanup.py'
LISTENER_FILE_PATH = r'/usr/lib/python2.7/site-packages/EHCAutoCLIListener.py'
WF_DUMP_FILE_PATH = '/root/automation/ehc/workflows/dump'
SN_DUMP_FILE_PATH = '/root/automation/ehc/scenarios/dump'

PRE_STEPS = ['Opens Browser To Resume', 'Login Browser To Resume']


def check_path_exist_create(path_str):
    if not os.path.exists(path_str):
        try:
            os.makedirs(path_str)
        except OSError as ex:  # Guard in case race condition
            if ex.errno != errno.EEXIST:
                return False
    return True


class Color(object):

    colorinit() #for windows cmd, but will block pycharm

    @staticmethod
    def colorfulstr(input,color=Fore.RESET):
        return color+str(input)+Fore.RESET

RED = partial(Color.colorfulstr, color=Fore.RED)
BLUE = partial(Color.colorfulstr, color=Fore.BLUE)
GREEN = partial(Color.colorfulstr, color=Fore.GREEN)
YELLOW = partial(Color.colorfulstr, color=Fore.YELLOW)
CYAN = partial(Color.colorfulstr, color=Fore.CYAN)
MAGENTA = partial(Color.colorfulstr, color=Fore.MAGENTA)
RESET = partial(Color.colorfulstr, color=Fore.RESET)


class WorkFlow(object):
    def __init__(self, name, doc, tags, steps, robotname, robotsource, libraries, workflow_obj):
        self.name = name
        self.doc = doc
        self.tags = tags
        self.keywords = self.__parse_robot_steps(steps)
        self.robotname = robotname
        self.robotsource = robotsource
        self.libraries = libraries
        self.current = workflow_obj

    def __parse_robot_steps(self, steps):
        keywords=[]
        for s in steps:
            if hasattr(s,'name'):
                if s.args:

                    keywords.append('{step} {args}'.format(step=s.name,args=str(','.join(s.args))))
                else:
                    keywords.append('{step}'.format(step=s.name))
        return keywords


class EHCTest(object):
    def __init__(self, scenario_dir=SCENARIO_DIR, workflow_dir=WORKFLOW_DIR):
        self.scenario_dir = scenario_dir
        self.workflow_dir = workflow_dir
        self.scenario_data, self.workflow_data, self.resource_dict = self.__load_test_data()
        self.__scenariodict = None
        self.__workflowdict = None

    def __load_test_data(self):
        from os.path import exists
        if not exists(self.scenario_dir):
            raise ValueError('No scenario directory')
        if not exists(self.workflow_dir):
            raise ValueError('No workflow directory')
        from robot.parsing.model import TestData, ResourceFile
        scenarios = TestData(source=self.scenario_dir)
        workflows = TestData(source=self.workflow_dir)
        resources = ResourceFile(source=RESOURCE_FILE).populate()
        resource_dict = {}
        for user_keyword in resources.keywords:
            keyword_name = user_keyword.name
            keyword_steps = []
            for step in user_keyword.steps:
                keyword_steps.append(step)
            resource_dict[keyword_name] = keyword_steps
        return scenarios, workflows, resource_dict

    def __init_workflow_dict(self):
        _dict = OrderedDict()
        for robotcase in self.workflow_data.children:
            for wf in robotcase.testcase_table.tests:
                _dict[wf.name] = WorkFlow(wf.name, wf.doc.value, wf.tags, wf.steps, robotcase.name, robotcase.source, [lib.name for lib in robotcase.imports.data], wf)
        return _dict

    def __init_scenario_dict(self):
        _dict = OrderedDict()
        for robotcase in self.scenario_data.children:
            for wf in robotcase.testcase_table.tests:
                _dict[wf.name] = WorkFlow(wf.name, wf.doc.value, wf.tags, wf.steps, robotcase.name, robotcase.source,
                                          [lib.name for lib in robotcase.imports.data], wf)
        return _dict

    @property
    def workflowdict(self):
        if not self.__workflowdict:
            self.__workflowdict= self.__init_workflow_dict()
        return self.__workflowdict

    @property
    def workflowlist(self):
         return [str(k) for k in self.workflowdict.keys()]

    @property
    def user_keywords(self):
        return self.resource_dict

    @workflowlist.setter
    def workflowlist(self,value):
        return self.workflowdict.keys().extend(value)

    def get_workflow_name(self,value=''):
        if value.isdigit():
            return self.workflowlist[int(value)-1]
        else:
            return value

    @property
    def scenariodict(self):
        if not self.__scenariodict:
            self.__scenariodict = self.__init_scenario_dict()
        return self.__scenariodict

    @property
    def scenariolist(self):
        return [str(k) for k in self.scenariodict.keys()]

    @scenariolist.setter
    def scenariolist(self, value):
        return self.scenariodict.keys().extend(value)

    def get_scenario_name(self, value=''):
        if value.isdigit():
            return self.scenariolist[int(value) - 1]
        else:
            return value


class ConfigYaml(object):
    def __init__(self, yamlpath=YAMLFile):
        self.yamlpath = yamlpath
        self.data=self.load_config()

    def load_config(self):
        with open(self.yamlpath,'r') as f:
            return self.__ordered_load(f, yaml.SafeLoader)

    def save_config(self,savedata=None):
        savedata = savedata or self.data
        with open(self.yamlpath,'w') as f:
           self.__ordered_dump(savedata,f,Dumper=yaml.SafeDumper)

    def __ordered_load(self,stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
        class OrderedLoader(Loader):
            pass
        def construct_mapping(loader, node):
            loader.flatten_mapping(node)
            return object_pairs_hook(loader.construct_pairs(node))
        OrderedLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            construct_mapping)
        return yaml.load(stream, OrderedLoader)

    def __ordered_dump(self,data, stream=None, Dumper=yaml.Dumper, **kwds):
        class OrderedDumper(Dumper):
            pass
        def _dict_representer(dumper, data):
            return dumper.represent_mapping(
                yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                data.items())
        OrderedDumper.add_representer(OrderedDict, _dict_representer)
        return yaml.dump(data, stream, OrderedDumper, **kwds)

    def data_to_str(self,printdata=None,keylist=None):
        printdata = printdata or self.data
        retstr=''
        for k,v in printdata.iteritems():
            if (not keylist) or (keylist and k in keylist):
                if isinstance(v,OrderedDict):
                    retstr +='%s :\n' % (k)
                    for kk,vv in v.iteritems():
                        retstr +='  %s : %s\n' % (kk,vv)
                else:
                   retstr +='%s : %s\n' % (k,v)

        return retstr


class Helper(object):
    """Helper most used for parse input."""

    @staticmethod
    def parse_input(inputval,inputtype):
        inputval=inputval.strip()
        if len(inputval) == 0:
            return False
        if inputtype == 'list':
            return [s.strip() for s in inputval.split(',')]
        else:
            return inputval

    @staticmethod
    def query_yes_no(question):
        print question + RED(' [yes(y)/no(n)]') +' or '+ RED('[true(t)/false(f)]\n')
        while True:
            try:
                return strtobool(raw_input().lower())
            except ValueError:
                print RED('Please respond with yes(y)/no(n) or true(t)/false(f)...\n')

    @staticmethod
    def get_similiar_value(inputval,listval):
        """find similiar value"""
        from difflib import get_close_matches
        close_commands = get_close_matches(inputval, listval)
        if close_commands:
            return close_commands
        else:
            return False


class Output(object):
    def __init__(self, filepath):
        self.terminal = sys.stdout
        self.filepath = filepath
        self.__file = None

    def __enter__(self):
        self.__file = open(self.filepath, "w")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__file:
            self.__file.close()
            self.__file = None

    def close(self):
        self.__exit__(None, None, None)

    def write(self, message):
        if not self.__file:
            self.__enter__()
        # if '::' in message:
        #     if '...' in message:
        #         message='[00] '+message[:62]+'...'  #78-len('| pass |') ,70-len('[0]  ')
        #     else:
        #         message='[0]  '+message[:65]     #get index by name
        self.__file.write(message)
        self.terminal.write(message)

    def flush(self):
        self.__file.flush()
        self.terminal.flush()


class ArgParse(object):
    '''
    class for argparse
    '''
    def __init__(self):
        self._parserbase = argparse.ArgumentParser(add_help=False)
        self.parsecmd = argparse.ArgumentParser(prog='EHCAutoCLI',
                                                description='%(prog)s, EHC Solutions Automation',
                                                epilog="EHC Solution end to end verification",
                                                parents=[self._parserbase],
                                                add_help=False)
        self.ehctest = EHCTest()
        self.config = ConfigYaml()
        self.args = None
        self.__init_arguments()

    def __init_arguments(self):
        self._group = self.parsecmd.add_argument_group('General Options')
        self._group.add_argument('-v', '--version', action='version', version='%(prog)s 0.0.1')
        self._group.add_argument('-h', '--help', action='help',help='show {command} help')

        self._subparsers = self.parsecmd.add_subparsers(title='Command Options',dest='cmdopt')#,description='')
        # Command options for scenarios
        self._parsescenario = self._subparsers.add_parser('scenario', help='List/Run EHC scenarios')
        self._parsescenario.add_argument('-l', '--list',
                                         action='store_const',
                                         const=self.ehctest.scenariolist,
                                         help='List all scenario(s)')
        self._parsescenario.add_argument('-a', '--all',
                                         action='store_const',
                                         const=self.ehctest.scenariolist,
                                         help='Run all scenario(s)')
        self._parsescenario.add_argument('-s', '--show',
                                         nargs='+',
                                         metavar='',
                                         # choices=self.choices,
                                         help='Show detail of scenario(s). Input name or index...')
        self._parsescenario.add_argument('-r', '--run',
                                         nargs='+',
                                         metavar='',
                                         # choices=self.choices,
                                         help='Run specific scenario(s). Input name or index...')
        self._parsescenario.add_argument('-c', '--resume',
                                         nargs='+',
                                         metavar='',
                                         # choices=self.choices,
                                         help='Continue specific scenario. Input scenario id...')
        self._parsescenario.add_argument('-i', '--start',
                                         nargs='+',
                                         metavar='',
                                         # choices=self.choices,
                                         help='Start step to continue specific scenario. Input step index...')

        self._parsescenario.add_argument('-f', '--file',
                                         nargs='+',
                                         metavar='',
                                         # choices=self.choices,
                                         help='Absolute path of dump file...')

        self._parsescenario.add_argument('-t', '--teardown',
                                         nargs='+',
                                         metavar='',
                                         # choices=self.choices,
                                         help='Tag to enable tear down')

        # Command options for workflows
        self._parseworkflow = self._subparsers.add_parser('workflow',help='List/Run EHC workflows')
        self._parseworkflow.add_argument('-l', '--list',
                                         action='store_const',
                                         const= self.ehctest.workflowlist,
                                         help='List all workflow(s)')
        self._parseworkflow.add_argument('-a', '--all',
                                         action='store_const',
                                         const= self.ehctest.workflowlist,
                                         help='Run all workflow(s)')
        self._parseworkflow.add_argument('-s', '--show',
                                         nargs='+',
                                         metavar='',
                                         #choices=self.choices,
                                         help='Show detail of workflow(s). Input name or index...')
        self._parseworkflow.add_argument('-r', '--run',
                                         nargs='+',
                                         metavar='',
                                         #choices=self.choices,
                                         help='Run specific workflow(s). Input name or index...')
        self._parseworkflow.add_argument('-c', '--resume',
                                         nargs='+',
                                         metavar='',
                                         # choices=self.choices,
                                         help='Continue specific workflow. Input workflow id...')
        self._parseworkflow.add_argument('-i', '--start',
                                         nargs='+',
                                         metavar='',
                                         # choices=self.choices,
                                         help='Start step to continue specific workflow. Input step index...')

        self._parseworkflow.add_argument('-f', '--file',
                                         nargs='+',
                                         metavar='',
                                         # choices=self.choices,
                                         help='Absolute path of dump file...')

        self._parseworkflow.add_argument('-t', '--teardown',
                                         nargs='+',
                                         metavar='',
                                         # choices=self.choices,
                                         help='Tag to enable tear down')

        self._parseconfig = self._subparsers.add_parser('config',help='View/Set configuration settings')
        self._parseconfig.add_argument('-l', '--list',
                                       action='store_const',
                                       const= self.config.data.keys(),
                                       help='List all configuration settings')
        self._parseconfig.add_argument('-a', '--all',
                                       action='store_const',
                                       const= self.config.data.keys(),
                                       help='Edit all configuration settings')
        self._parseconfig.add_argument('-s', '--show',
                                       nargs='+',
                                       metavar='',
                                       # choices=self.config.data.keys(),
                                       help='Show specific configuration settings.')
        self._parseconfig.add_argument('-e', '--edit',
                                       nargs='+',
                                       metavar='',
                                       # choices=self.config.data.keys(),
                                       help='Edit specific configuration settings.')

    def validate_input_arguments(self, inputlist, verifylist, argument, isindex=False):
        __choice_format = YELLOW('\nUnknown "{0}". Please select choices from:\n')
        for inputval in inputlist:
            __choice_err = __choice_format.format(inputval)
            if inputval.isdigit() and isindex:
                if int(inputval) <= 0 or int(inputval) > len(verifylist):
                    choicestr = ''.join(['{0:<3}-- {1}\n'.format(idx+1,verify) for idx,verify in enumerate(verifylist)])
                    raise argparse.ArgumentError(argument,__choice_err+GREEN(choicestr))
            else:
                if inputval not in verifylist:
                    guesslist = Helper.get_similiar_value(inputval, verifylist)
                    if guesslist:
                        choicestr = ''.join(['{0}\n'.format(guess) for guess in guesslist])
                        raise argparse.ArgumentError(argument,__choice_err+GREEN(choicestr))
                    else:
                        choicestr = ''.join(['{0}\n'.format(verify) for verify in verifylist])
                        raise argparse.ArgumentError(argument,__choice_err+GREEN(choicestr))

    def parse_args(self):
        if not sys.argv[1:]:  #nothing input
            self.parsecmd.print_help()
            exit(-1)

        (args_base, args_cmd) = self._parserbase.parse_known_args()

        if args_cmd:
            self.args = self.parsecmd.parse_args(args=args_cmd, namespace=args_base)
            if self.args.cmdopt == 'scenario':
                if not (self.args.list or self.args.all or self.args.show or self.args.run or self.args.resume):
                    self._parsescenario.print_help()
                    exit(-1)
                try:
                    if self.args.show:
                        self.validate_input_arguments(self.args.show, self.ehctest.scenariolist,
                                                      self._parsescenario._option_string_actions['--show'], True)
                    if self.args.run:
                        self.validate_input_arguments(self.args.run, self.ehctest.scenariolist,
                                                      self._parsescenario._option_string_actions['--run'], True)
                    if self.args.resume:
                        if not self.args.start:
                            self.args.start = [0]
                        if not self.args.file:
                            print YELLOW(
                                '[WARN] No dump file specified, try to use the latest one in folder {}...'.format(
                                    SN_DUMP_FILE_PATH))
                            dump_list = [f for f in glob.iglob(SN_DUMP_FILE_PATH + '/*.yaml')]
                            if dump_list:
                                newest = max(dump_list, key=os.path.getctime)
                                if newest is not None:
                                    print YELLOW('Found dump file "{}"!'.format(newest))
                                    self.args.file = [newest]
                                else:
                                    # This should always not reach.
                                    print RED(
                                        '[ERROR] No dump file is provided, program will exit.')
                                    return
                            else:
                                print RED(
                                    'No dump file created yet, resume stops, program will exit!')
                                return

                        self.validate_input_arguments(self.args.resume, self.ehctest.scenariolist,
                                                      self._parsescenario._option_string_actions['--resume'], True)
                    self.__parse_workflow()
                except argparse.ArgumentError:
                    err = sys.exc_info()[1]
                    self.parsecmd.error(str(err))

            if self.args.cmdopt == 'workflow':
                if not (self.args.list or self.args.all or self.args.show or self.args.run or self.args.resume):
                    self._parseworkflow.print_help()
                    exit(-1)
                try:
                    if self.args.show:
                        self.validate_input_arguments(self.args.show,self.ehctest.workflowlist,self._parseworkflow._option_string_actions['--show'],True)
                    if self.args.run:
                        self.validate_input_arguments(self.args.run,self.ehctest.workflowlist,self._parseworkflow._option_string_actions['--run'],True)
                    if self.args.resume:
                        if not self.args.start:
                            self.args.start = [0]
                        if not self.args.file:
                            print YELLOW(
                                '[WARN] No dump file specified, try to use the latest one in folder {}...'.format(WF_DUMP_FILE_PATH))
                            dump_list = [f for f in glob.iglob(WF_DUMP_FILE_PATH + '/*.yaml')]
                            if dump_list:
                                newest = max(dump_list, key=os.path.getctime)
                                if newest is not None:
                                    print YELLOW('Found dump file "{}"!'.format(newest))
                                    self.args.file = [newest]
                                else:
                                    # This should always not reach.
                                    print RED(
                                        '[ERROR] No dump file is provided, program will exit.')
                                    return
                            else:
                                print RED(
                                    'No dump file created yet, resume stops, program will exit!')
                                return

                        self.validate_input_arguments(self.args.resume, self.ehctest.workflowlist, self._parseworkflow._option_string_actions['--resume'], True)
                    self.__parse_workflow()
                except argparse.ArgumentError:
                    err = sys.exc_info()[1]
                    self.parsecmd.error(str(err))

            if self.args.cmdopt == 'config':
                if not (self.args.list or self.args.all or self.args.show or self.args.edit):
                    self._parseconfig.print_help()
                    exit(-1)
                try:
                    if self.args.show:
                        self.validate_input_arguments(self.args.show,self.config.data.keys(),self._parseconfig._option_string_actions['--show'])
                    if self.args.edit:
                        self.validate_input_arguments(self.args.edit,self.config.data.keys(),self._parseconfig._option_string_actions['--edit'])
                    self.__parse_config()
                except argparse.ArgumentError:
                    err = sys.exc_info()[1]
                    self.parsecmd.error(str(err))

    def __parse_workflow(self):
        test_dict = self.ehctest.workflowdict if self.args.cmdopt == 'workflow' else self.ehctest.scenariodict
        if self.args.list:
            format_wf = '{0:<3}{1:<20}{2}'
            test_column = 'Workflow' if self.args.cmdopt == 'workflow' else 'Scenario'
            print format_wf.format('Id', 'Group', test_column)
            print(format_wf.format('='*len('Id'),'='*len('Group'),'='*len(test_column)))
            format_wf = MAGENTA('{0:<3}')+BLUE('{1:<20}')+GREEN('{2}')
            for idx, workflow in enumerate(test_dict.values()):
                    print format_wf.format(idx+1,workflow.robotname,workflow.name)

        if self.args.show:
            print('')
            for showflow in self.args.show:
                name = self.ehctest.get_workflow_name(showflow) if self.args.cmdopt == 'workflow' else self.ehctest.get_scenario_name(showflow)

                if test_dict.has_key(name):
                    workflow = test_dict[name]
                    from argparse import HelpFormatter,Action
                    h = HelpFormatter('')
                    h.start_section(MAGENTA('%s'% workflow.robotname))
                    h.add_text(GREEN('%s'% workflow.name))
                    h.add_text(YELLOW('%s'% workflow.doc))
                    h.start_section('AUC Steps')
                    counter = 0
                    for k in workflow.keywords:
                        counter += 1
                        if k.startswith('Comment'):
                            comment = k[8:]
                            h.add_argument(Action('','', help='{}.{}'.format(str(counter), BLUE(comment))))
                        elif self.ehctest.resource_dict.has_key(k):
                            h.add_argument(Action('', '', help='{}.{}'.format(str(counter), CYAN(k))))
                            sub_keys = self.ehctest.resource_dict[k]
                            for sub_key in sub_keys:
                                counter += 1
                                h.add_argument(Action('', '', help='{}.{}'.format(str(counter), MAGENTA('{} {}'.format(sub_key.name, ' '.join(sub_key.args))))))
                        else:
                            h.add_argument(Action('','', help='{}.{}'.format(str(counter), CYAN(k))))
                    h.end_section()
                    h.end_section()
                    print(h.format_help())

        inputcases = self.args.run or self.args.all or self.args.resume

        from time import localtime, strftime
        timestamp = strftime('%Y%m%d-%H%M%S', localtime())
        test_dir = self.ehctest.workflow_dir if self.args.cmdopt == 'workflow' else self.ehctest.scenario_dir
        robothistory = os.path.join(test_dir, self.config.data['history_dir'])
        if not os.path.exists(robothistory):
            os.mkdir(robothistory)

        robotout = os.path.join(robothistory, 'output%s' % timestamp)
        if not os.path.exists(robotout):
            os.mkdir(robotout)
        summarypath = os.path.join(robotout, 'summary%s.txt' % timestamp)

        if inputcases and not self.args.resume:
            # Check whether clean up is needed before workflow execution
            if need_clean_up:
                from subprocess import call
                call(["python {}".format(CLEANUP_FILE_PATH)], shell=True)
            self.__check_dump_folders(WF_DUMP_FILE_PATH)
            self.__check_dump_folders(SN_DUMP_FILE_PATH)
            testcases = [self.ehctest.get_workflow_name(t) for t in inputcases] if self.args.cmdopt == 'workflow' else [self.ehctest.get_scenario_name(t) for t in inputcases]
            DUMP_FILE_PATH = WF_DUMP_FILE_PATH if self.args.cmdopt == 'workflow' else SN_DUMP_FILE_PATH
            import robot.run
            with Output(summarypath) as output:
                if self.args.teardown:
                    variables = 'SkipTeardown:False' if 'true' in self.args.teardown else 'SkipTeardown:True'
                else:
                    variables = 'SkipTeardown:False'
                robot.run(test_dir, outputdir=robotout, loglevel='DEBUG', timestampoutputs=True, test=testcases, variable=variables,
                          listener=LISTENER_FILE_PATH, consolecolors='on', stdout=output, consolewidth=78)

            print('Summary: %s' % os.path.abspath(summarypath))
            print('Dir:     %s' % os.path.abspath(robotout))
            dump_list = [f for f in glob.iglob(DUMP_FILE_PATH + '/*.yaml')]
            if dump_list:
                newest = max(dump_list, key=os.path.getctime)
                print('Dump:    %s' % os.path.join(robotout, newest))
            else:
                print('Dump:    No dump file created yet.')

        elif self.args.resume:
            test_names = [self.ehctest.get_workflow_name(t) for t in inputcases] if self.args.cmdopt == 'workflow' else [self.ehctest.get_scenario_name(t) for t in inputcases]
            suite = self.__build_test_on_fly(self.args.cmdopt, test_names, self.args.file, self.args.start[0])
            with Output(summarypath) as output:
                xml_report = 'resume.xml'
                if self.args.teardown:
                    variables = 'SkipTeardown:False' if 'true' in self.args.teardown else 'SkipTeardown:True'
                else:
                    variables = 'SkipTeardown:False'
                result = suite.run(outputdir=robotout, loglevel='DEBUG', timestampoutputs=True, listener=LISTENER_FILE_PATH,
                               consolecolors='on', stdout=output, consolewidth=78, output=xml_report, variable=variables)
                from robot.api import ResultWriter
                # Report and xUnit files can be generated based on the result object.
                ResultWriter(result).write_results(report=os.path.join(robotout, 'report.html'))
                # Generating log files requires processing the earlier generated output XML.
                ResultWriter(os.path.join(robotout, 'resume-%s.xml' % timestamp)).write_results(outputdir=robotout)
            print('Log:  %s' % os.path.join(robotout, 'log.html'))
            print('Report:  %s' % os.path.join(robotout, 'report.html'))
            print('Summary: %s' % os.path.abspath(summarypath))
            print('Dir:     %s' % os.path.abspath(robotout))
            DUMP_FILE_PATH = WF_DUMP_FILE_PATH if self.args.cmdopt == 'workflow' else SN_DUMP_FILE_PATH
            dump_list = [f for f in glob.iglob(DUMP_FILE_PATH + '/*.yaml')]
            if dump_list:
                newest = max(dump_list, key=os.path.getctime)
                print('Dump:    %s' % os.path.join(robotout, newest))
            else:
                print('Dump:    No dump file created yet.')

    def __check_dump_folders(self, folder):
        print GREEN('Check if dump file folder:{} exists, will create if not exist.'.format(
            folder))
        if check_path_exist_create(folder):
            print GREEN('Dump file folder:{} exits.'.format(folder))
        else:
            print YELLOW(
                'Dump file folder:{} does not exist, creating dump file will fail.'.format(
                    folder))

    def __build_test_on_fly(self, test_type, test_names, dump_files, start_step_index = 0):
        if len(test_names)!= 1:
            print "[ERROR] Resuming multiple scenarios/workflows execution is not supported yet!"
            return
        if isinstance(start_step_index, str) and start_step_index.isdigit():
            start_step_index = int(start_step_index)
        elif isinstance(start_step_index, int):
            pass
        else:
            print "[WARN] Start point is not digit, will take 0 by default!"
            start_step_index = 1
        # Checking the test type
        setup_keyword = 'Apply Settings From Dump'
        if test_type == 'workflow':
            robot_test = self.ehctest.workflowdict[test_names[0]]
            suite = TestSuite('Resuming workflow mode')

            for library in robot_test.libraries:
                suite.imports.resource(library) if library.endswith('.robot') or library.endswith(
                    '.txt') else suite.imports.library(library)
            test_obj = robot_test.current
            test = suite.tests.create(test_obj.name, tags=test_obj.tags)
            test.keywords.create(setup_keyword, args=dump_files, type='setup')

            for step in test_obj.steps[2:start_step_index - 1]:
                test.keywords.create(name='Comment', args=[step.name]+step.args)
            for pre_step in PRE_STEPS:
                test.keywords.create(name=pre_step)
            for step in test_obj.steps[start_step_index - 1:]:
                test.keywords.create(name=step.name, args=step.args)
            test.keywords.create(test_obj.teardown.name, args=test_obj.teardown.args, type='teardown')
        else:
            robot_test = self.ehctest.scenariodict[test_names[0]]
            suite = TestSuite('Resuming scenario mode')
            for library in robot_test.libraries:
                suite.imports.resource(library) if library.endswith('.robot') or library.endswith(
                    '.txt') else suite.imports.library(library)
            test_obj = robot_test.current
            test = suite.tests.create(test_obj.name, tags=test_obj.tags)
            test.keywords.create(setup_keyword, args=dump_files, type='setup')
            parent_index, child_index = self.__get_relative_indexes(test_obj.steps, start_step_index)
            failed_step = test_obj.steps[parent_index]
            # Comment all keywords before the failed point
            for step in test_obj.steps[0:parent_index]:
                test.keywords.create(name='Comment', args=[step.name]+step.args)
                for sub_step in self.ehctest.resource_dict[step.name]:
                    test.keywords.create(name='Comment', args=[sub_step.name]+sub_step.args)
            # Expand the failed point keyword
            test.keywords.create(name='Comment', args=[failed_step.name])
            for sub_step in self.ehctest.resource_dict[failed_step.name][0:child_index]:
                test.keywords.create(name='Comment', args=[sub_step.name]+sub_step.args)
            for pre_step in PRE_STEPS:
                test.keywords.create(name=pre_step)
            for sub_step in self.ehctest.resource_dict[failed_step.name][child_index:]:
                test.keywords.create(name=sub_step.name, args=sub_step.args)
            # Continue the following keywords
            for step in test_obj.steps[parent_index+1:]:
                test.keywords.create(name=step.name, args=step.args)
            test.keywords.create(test_obj.teardown.name, args=test_obj.teardown.args, type='teardown')
        return suite

    def __get_relative_indexes(self, steps, absolute_index):
        father_index = -1
        child_index = -1
        accumulated_steps = 1
        for index, step in enumerate(steps):
            accumulated_steps = accumulated_steps + len(self.ehctest.resource_dict[step.name]) + 1
            if accumulated_steps >= absolute_index:
                father_index = index
                child_index = len(self.ehctest.resource_dict[step.name]) + absolute_index - accumulated_steps
                break
        if father_index != -1 and child_index != -1:
            return father_index, child_index
        else:
            raise ValueError('Cannot find the right resume point you gave by index, please double check.')


    def __parse_config(self):

        def set_config_by_input(keylist=None):
            defaultformat= '\nkey: ##{0}##. \nvalue: {1} type: {2}. \n'
            forformat='\nkey: ##{0}## For **{3}**. \nvalue: {1} type: {2}.\n'
            listinfo="Use ',' to split for list.\n"
            inputinfo=YELLOW('Press <Enter> to keep default value\n{0}>')

            for k, v in self.config.data.iteritems():
                if (not keylist) or (keylist and k in keylist):
                    if isinstance(v,OrderedDict):
                        for kk,vv in v.iteritems():
                            typename = type(vv).__name__
                            prompt=forformat.format(CYAN(kk),GREEN(vv),MAGENTA(typename),CYAN(k))
                            prompt = prompt+listinfo if isinstance(vv,list) else prompt
                            prompt+=inputinfo.format(CYAN(kk))
                            inputval = Helper.parse_input(raw_input(prompt),typename)
                            if inputval:
                                self.config.data[k][kk]=inputval
                    else:
                            typename = type(v).__name__
                            prompt = defaultformat.format(CYAN(k),GREEN(v),MAGENTA(typename))
                            prompt = prompt+listinfo if isinstance(v,list) else prompt
                            prompt+=inputinfo.format(CYAN(k))
                            inputval = Helper.parse_input(raw_input(prompt),typename)
                            if inputval:
                                self.config.data[k]=inputval

            is_save = Helper.query_yes_no('Do want to save the configuration?')
            if is_save:
                self.config.save_config()
                print('Save the configuration into %s' % os.path.abspath(self.config.yamlpath))
            else:
                self.config.load_config()

        inputkeys = self.args.show or self.args.list
        if inputkeys:
            print(self.config.data_to_str(keylist=inputkeys))

        inputkeys = self.args.edit or self.args.all
        if inputkeys:
            set_config_by_input(inputkeys)


if __name__ == '__main__':
    # sys.argv[1:]='workflow -c 1 -i 2 -f /root/automation/test.yaml'.split()
    # sys.argv[1:] = 'scenario -s 3'.split()
    # sys.argv[1:] = r'scenario -c 3 -i 4 -f C:/Users/yinl1/AppData/Local/Temp/2/dump-20170707-061627.yaml'.split()
    # sys.argv[1:] = r'scenario -s 2'.split()
    ArgParse().parse_args()
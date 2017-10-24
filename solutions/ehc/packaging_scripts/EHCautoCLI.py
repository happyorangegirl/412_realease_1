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

import sys,os
import argparse
import yaml
from colorama import Fore, init as colorinit
from functools import partial
from collections import OrderedDict
from distutils.util import strtobool
from robot.api import TestSuite
import glob

ROBOTDir = r'/root/automation/ehc/workflows'
YAMLFile = r'/root/automation/ehc/config/generic.yaml'


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
    def __init__(self, name,doc,tags,steps,robotname, robotsource, libraries, workflow_obj):
        self.name = name
        self.doc = doc
        self.tags = tags
        self.keywords = self.__parse_robot_steps(steps)
        self.robotname = robotname
        self.robotsource = robotsource
        self.libraries = libraries
        self.current = workflow_obj

    def __parse_robot_steps(self,steps):
        keywords=[]
        for s in steps:
            if hasattr(s,'name'):
                if s.args:

                    keywords.append('{step} {args}'.format(step=s.name,args=str(','.join(s.args))))
                else:
                    keywords.append('{step}'.format(step=s.name))
        return keywords

class EHCTest(object):
    def __init__(self,robotdir=ROBOTDir):
        self.robotdir = robotdir

        self.testdatadirectory = self.__load_test_data()
        self.__workflowdict = None

    def __load_test_data(self):
        from os.path import exists
        if not exists(self.robotdir):
            raise ValueError('No workflow directory')
        from robot.parsing.model import TestData
        testdatadirectory = TestData(source=self.robotdir)
        return testdatadirectory


    def __init_workflow_dict(self):
        _dict = OrderedDict()
        for robotcase in self.testdatadirectory.children:
            for wf in robotcase.testcase_table.tests:
                _dict[wf.name] = WorkFlow(wf.name, wf.doc.value, wf.tags, wf.steps, robotcase.name, robotcase.source, [lib.name for lib in robotcase.imports.data], wf)
        return _dict

    @property
    def workflowdict(self):
        if not self.__workflowdict:
            self.__workflowdict= self.__init_workflow_dict()
        return self.__workflowdict

    @property
    def workflowlist(self):
         return [str(k) for k in self.workflowdict.keys()]

    @workflowlist.setter
    def workflowlist(self,value):
        return self.workflowdict.keys().extend(value)

    def get_workflow_name(self,value=''):
        if value.isdigit():
            return self.workflowlist[int(value)-1]
        else:
            return value


class ConfigYaml(object):
    def __init__(self,yamlpath=YAMLFile):
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
                                                description='%(prog)s, EHC Solution Automation',
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

    def validate_input_arguments(self,inputlist,verifylist,argument,isindex=False) :
        __choice_format = YELLOW('\nUnknown "{0}". Please select choices from:\n')
        for inputval in inputlist:
            __choice_err = __choice_format.format(inputval)
            if inputval.isdigit() and isindex:
                if int(inputval) <= 0 or int(inputval) > len(verifylist):
                    choicestr = ''.join(['{0:<3}-- {1}\n'.format(idx+1,verify) for idx,verify in enumerate(verifylist)])
                    raise argparse.ArgumentError(argument,__choice_err+GREEN(choicestr))
            else:
                if inputval not in verifylist:
                    guesslist = Helper.get_similiar_value(inputval,verifylist)
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
            self.args= self.parsecmd.parse_args(args=args_cmd,namespace=args_base)

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
                                "[WARN] No dump file specified, try to use the latest one in folder /root/automation/ehc/config/temp...")
                            dump_folder = '/root/automation/ehc/config/temp/'
                            newest = None
                            if os.listdir(dump_folder):
                                newest = max(glob.iglob('{}*.yaml'.format(dump_folder)), key=os.path.getctime)
                            if newest is not None:
                                print YELLOW("Found dump file \"{}\"!".format(newest))
                                self.args.file = [newest]
                            else:
                                print RED('[ERROR] No dump file is provided, program will exit.')
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
        if self.args.list:
            format_wf = '{0:<3}{1:<20}{2}'
            print format_wf.format('Id','Group','Workflow')
            print(format_wf.format('='*len('Id'),'='*len('Group'),'='*len('Workflow')))
            format_wf = MAGENTA('{0:<3}')+BLUE('{1:<20}')+GREEN('{2}')
            for idx, workflow in enumerate(self.ehctest.workflowdict.values()):
                    print format_wf.format(idx+1,workflow.robotname,workflow.name)

        if self.args.show:
            print('')
            for showflow in self.args.show:
                name = self.ehctest.get_workflow_name(showflow)
                if self.ehctest.workflowdict.has_key(name):
                    workflow = self.ehctest.workflowdict[name]
                    from argparse import HelpFormatter,Action
                    h = HelpFormatter('')
                    h.start_section(MAGENTA('%s'% workflow.robotname))
                    h.add_text(GREEN('%s'% workflow.name))
                    h.add_text(YELLOW('%s'% workflow.doc))
                    h.start_section('AUC Steps')
                    for idx, k in enumerate(workflow.keywords):
                        if k.startswith('Comment'):
                            comment = k[8:]
                            h.add_argument(Action('','', help='{}.{}'.format(str(idx+1), BLUE(comment))))
                        else:
                            h.add_argument(Action('','', help='{}.{}'.format(str(idx+1), CYAN(k))))

                    h.end_section()
                    h.end_section()
                    print(h.format_help())

        inputcases = self.args.run or self.args.all or self.args.resume

        from time import localtime, strftime
        timestamp = strftime('%Y%m%d-%H%M%S', localtime())

        robothistory = os.path.join(self.ehctest.robotdir, self.config.data['history_dir'])
        if not os.path.exists(robothistory):
            os.mkdir(robothistory)

        robotout = os.path.join(robothistory, 'output%s' % timestamp)
        if not os.path.exists(robotout):
            os.mkdir(robotout)
        summarypath = os.path.join(robotout, 'summary%s.txt' % timestamp)

        if inputcases and not self.args.resume:
            testcases = [self.ehctest.get_workflow_name(t) for t in inputcases]
            import robot.run
            with Output(summarypath) as output:
                robot.run(self.ehctest.robotdir,outputdir=robotout,loglevel='DEBUG',timestampoutputs=True,test=testcases,
                          consolecolors='on',stdout=output,consolewidth=78, exitonfailure=True)
            print('Summary: %s' % os.path.abspath(summarypath))
            print('Dir:     %s' % os.path.abspath(robotout))
            newest = max(glob.iglob('/root/automation/ehc/config/temp/*.yaml'), key=os.path.getctime)
            print('Dump:    %s' % os.path.join(robotout, newest))

        elif self.args.resume:
            workflow_names = [self.ehctest.get_workflow_name(t) for t in inputcases]
            suite = self.__build_test_on_fly(workflow_names, self.args.file, self.args.start[0])
            with Output(summarypath) as output:
                xml_report = 'resume.xml'
                result = suite.run(outputdir=robotout, loglevel='DEBUG', timestampoutputs=True,
                               consolecolors='on', stdout=output, consolewidth=78, output=xml_report)
                from robot.api import ResultWriter
                # Report and xUnit files can be generated based on the result object.
                ResultWriter(result).write_results(report=os.path.join(robotout, 'report.html'))
                # Generating log files requires processing the earlier generated output XML.
                ResultWriter(os.path.join(robotout, 'resume-%s.xml' % timestamp)).write_results(outputdir=robotout)
            print('Log:  %s' % os.path.join(robotout, 'log.html'))
            print('Report:  %s' % os.path.join(robotout, 'report.html'))
            print('Summary: %s' % os.path.abspath(summarypath))
            print('Dir:     %s' % os.path.abspath(robotout))
            newest = max(glob.iglob('/root/automation/ehc/config/temp/*.yaml'), key=os.path.getctime)
            print('Dump:    %s' % os.path.join(robotout, newest))

    def __build_test_on_fly(self, workflow_names, dump_files, start_step_index = 0):
        if len(workflow_names)!= 1:
            print "[ERROR] Resuming multiple workflows execution is not supported yet!"
            return
        if isinstance(start_step_index, str) and start_step_index.isdigit():
            start_step_index = int(start_step_index)
        elif isinstance(start_step_index, int):
            pass
        else:
            print "[WARN] Start point is not digit, will take 0 by default!"
            start_step_index = 1
        workflow = self.ehctest.workflowdict[workflow_names[0]]
        suite = TestSuite('Resuming workflow mode')
        for library in workflow.libraries:
            suite.imports.library(library)
        workflow_obj = workflow.current
        test = suite.tests.create(workflow_obj.name, tags=workflow_obj.tags)
        test.keywords.create("Apply Settings From Dump", args=dump_files, type='setup')
        if start_step_index >= 3:
            test.keywords.create(name="Cloud Administrator Opens Browser")
            test.keywords.create(name="Cloud Administrator Login")
        for step in workflow_obj.steps[start_step_index-1:]:
            test.keywords.create(name=step.name, args=step.args)
        test.keywords.create(workflow_obj.teardown.name, args=workflow_obj.teardown.args, type='teardown')
        return suite

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

if __name__=='__main__':
    # sys.argv[1:]='workflow -c 1 -i 2 -f /root/automation/test.yaml'.split()
    # sys.argv[1:] = 'workflow -r 1'.split()
    # sys.argv[1:] = 'workflow -s 1'.split()
    ArgParse().parse_args()
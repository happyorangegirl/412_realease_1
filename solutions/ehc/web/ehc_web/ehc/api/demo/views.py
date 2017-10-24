# coding=utf-8

import datetime
import json
import ast
import yaml
import logging
from collections import OrderedDict

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.conf import settings

from api_autocli import all_workflows,sc_workflows,sc_sub_workflows
from ehc_config_adapter.configuration_adapter.yaml_adapter import YamlAdapter
from ehc_config_adapter.runner.ui_schema_gen import UISchemaGen


class IndexView(View):
    """BDL YAML configuration"""
    
    def __init__(self):
        super(IndexView, self).__init__()
        self.now = datetime.datetime.now()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_sc_sub_workflow(self,id):
        for sc_sub_workflow in sc_sub_workflows():
            if sc_sub_workflow['id'] == id:
                return sc_sub_workflow

    # @login_required
    def get(self, request, tpl):
        schema = None
        error = None
        scenario_workflows = []
        select_workflow = request.GET.get('select_workflow')
        sync = request.GET.get('sync')
        if request.GET.get('scenario_workflows'):
            scenario_workflows = json.loads(request.GET.get('scenario_workflows'))
        workflow_id = 0
        if select_workflow is not None:
            select_workflow = json.loads(select_workflow)
            workflow_id = select_workflow['id']
            group_type = select_workflow['group']

        print 'Workflow selected is {}'.format(workflow_id)
        if str(group_type).lower() == 'scenario workflows':
            scenario_workflow_ids = select_workflow['workflows inside']
            if scenario_workflow_ids:
                print 'Workflows id inside scenario {}'.format(scenario_workflow_ids)
                workflow_id = scenario_workflow_ids[0]
                select_workflow = self.get_sc_sub_workflow(scenario_workflow_ids[0])
                for scenario_workflow_id in scenario_workflow_ids:
                   scenario_workflows.append(self.get_sc_sub_workflow(scenario_workflow_id))


        # TODO: schema_filename = request.GET['schema_filename']
        schema_gen = UISchemaGen()
        schema_filename = schema_gen.generate(settings.EHC_CONFIG[str(workflow_id)],sync=='true')
        print 'loading schema file {}..'.format(schema_filename)
        try:
            with open(schema_filename, 'r') as f:
                stream = f.read()
                print stream
                schema = json.loads(stream)
        except Exception as e:
            error = e
        var = OrderedDict([
            ('schema', schema),
            ('error', error),
            ('select_workflow', select_workflow),
            ('schema_filename', schema_filename),
            ('scenario_workflows', scenario_workflows)
        ])
        return HttpResponse(json.dumps(var,sort_keys=True, indent=4), content_type='application/json')

    def post(self, request, tpl):
        """API: 
        :return JsonResult {}
        """
        print "#########################"
        body = ast.literal_eval(request.body)
        #print 'get {}'.format(body)
        data = body.get('editor_data')
        print "#########################"
        from os import path
        file_path = settings.AIM_CONFIG_LC1S_DP_SCHEMA
        if not path.exists(file_path):
            print "schema file doesn't exist"
            pass
        print "#########################"
        print "Writing to file {}".format(file_path)
        outF = open(file_path, "w")
        outF.write(data)
        outF.close()
        adapter = YamlAdapter(file_path, settings.AIM_CONFIG_LC1S_DP)
        adapter.persistent()
        try:
            if mode == 'RAW':
                good_syntax = self._good_yaml_syntax(text)
                if good_syntax[0]:
                    with open(settings.BDL_CONFIG_FILE, 'w') as f:
                        f.write(text)
                    return JsonResponse({'detail': 'Successfully: write raw text', 'error': False, 'title': 'Saved'})
                else:
                    return JsonResponse({'detail': str(good_syntax[1]), 'error': True, 'title': 'Unsaved'})
            elif mode == 'JSON':
                _text = self._json_to_yaml(text, settings.BDL_CONFIG_FILE)

                return JsonResponse({'detail': 'Successfully: write JSON text', 'error': False, 'title': 'Saved', 'text': _text})
            else:
                return JsonResponse({'detail': 'Available mode: RAW|JSON', 'error': True, 'title': 'Bad mode'})
        except Exception, e:
            return JsonResponse({'detail': str(e), 'error': True, 'title': 'Exception!'},
                                status=500)

    def _good_yaml_syntax(self, raw_yaml_text):
        try:
            yml = yaml.load(raw_yaml_text, yaml.SafeLoader)
            print yml
            return True, None
        except yaml.YAMLError as e:
            return False, e

    def _json_to_yaml(self, my_dict, yaml_file_name):

        yaml_text = yaml.dump(my_dict, default_flow_style=False)

        with open(yaml_file_name, 'wb') as f:
            f.write(yaml_text)
        return yaml_text


class WorkflowView(View):
    """BDL YAML configuration"""
    
    def __init__(self):
        super(WorkflowView, self).__init__()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(WorkflowView, self).dispatch(request, *args, **kwargs)

    # @login_required
    def get(self, request):
        # TODO: make up true data
        workflows = all_workflows()
        all_scenario_workflows = sc_workflows()
        var = OrderedDict([
            ('workflows', workflows),
            ('all_scenario_workflows', all_scenario_workflows)
        ])

        return HttpResponse(json.dumps(var, indent=4), content_type='application/json')

    # @login_required
    def post(self, request):
        body = json.loads(request.body)
        #print 'get {}'.format(body)
        print 'current the type is {}'.format(type(body))
        schema_filename = body.get('schema_filename')
        editor_data = body.get('editor_data')
        import os.path
        file_path = schema_filename
        if not os.path.exists(file_path):
            print "schema file doesn't exist"
            pass
        print "#########################"
        print "Writing to file {}".format(file_path)
        outF = open(file_path, "w")
        jsondata=json.dumps(editor_data, sort_keys=True, indent=4,separators=(',', ':'))
        outF.write(jsondata)
        outF.close()
        workflow_id = settings.EHC_CONFIG_SCHEMA[schema_filename]
        config_file = settings.EHC_CONFIG[str(workflow_id)]
        print 'Get configuration file by schema - {}'.format(config_file)
        adapter = YamlAdapter(file_path, config_file)
        adapter.persistent()
        logging.debug(editor_data)
        ret = {'detail': 'Successfully: upload JSON text', 'error': False, 'title': 'Saved', 'text': schema_filename}
        return HttpResponse(json.dumps(ret, indent=4), content_type='application/json')
# coding=utf-8
import logging
import json
import yaml
import subprocess
import autoclear
import time
import os
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
from ehc_e2e_common.generic_yaml_file_parser import GenericYamlFileParser


class IndexView(View):
    """get dash board data"""

    def __init__(self):
        super(IndexView, self).__init__()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        global_context = GenericYamlFileParser.parse_context()

        vra_host = global_context.vra_host
        vra_address = vra_host.replace('https://', '').replace('/vcac/org/', '')        
        vra_tenant = global_context.vra_tenant
        business_group = global_context.vra_business_group
        vra_username = global_context.config_admin_username

        vro_address = global_context.vro_host
        vro_username = global_context.vro_username

        dashboard_data = dict(vra_username=vra_username,
                              business_group=business_group,
                              vra_tenant=vra_tenant,
                              vro_address=vro_address,
                              vro_username=vro_username,
                              vra_address=vra_address)
        return HttpResponse(json.dumps(dashboard_data, indent=4), content_type='application/json')


class AutoclearView(View):
    def __init__(self):
        super(AutoclearView, self).__init__()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AutoclearView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        autoclear_out = open("/root/automation/ehc/logs/autoclear_out.txt", 'w')
        vra_tenant = request.GET.get('vra_tenant')
        sub_autoclear = subprocess.Popen("python /usr/lib/python2.7/site-packages/autoclear/cleanup.py '{0}' "
                                         "".format(vra_tenant), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                         shell=True)
        autoclear_out.write("Start auto clear process for tanent {0}".format(vra_tenant) + "\n" + "\n")
        while True:
            line = sub_autoclear.stdout.readline()
            if not line:
                break
            autoclear_out.write(line + "\n")
            autoclear_out.flush()

        autoclear_out.close()
        return HttpResponse(json.dumps("success", indent=4), content_type='application/json')


class ClearlogView(View):
    def __init__(self):
        super(ClearlogView, self).__init__()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ClearlogView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        log_content = None
        if not os.path.isfile("/root/automation/ehc/logs/autoclear_out.txt"):
            log_content = "Autoclear may hasn't been run from web UI yet."
        else:
            try:
                autoclear_out = open("/root/automation/ehc/logs/autoclear_out.txt", 'r')
                log_content = autoclear_out.read()
                autoclear_out.close()
            except Exception as e:
                log_content = "Error occured when try to read autoclear log."
        return HttpResponse(log_content, content_type='text/plain')

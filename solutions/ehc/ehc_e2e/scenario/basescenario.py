#  Copyright 2016 EMC GSE SW Automation
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

import os
import sys
import functools
from robot.api import logger
from robot.errors import ExecutionFailed
from ehc_e2e.workflow.setting import workflow_continue_on_failure, resume_also_include_workflow_yaml_file
from ehc_e2e.workflow.rp4vmworkflow import RP4VMWorkflow
from ehc_e2e.workflow.srmworkflow import SRMDRWorkflow
from ehc_e2e.utils.context.datacontext import DataContext
from ehc_e2e.utils.context.model import merge_yaml_data, YAMLData
from ehc_e2e.auc.executable.clean_up import CleanUp
from ehc_e2e.auc.executable.dump_context import DumpContext
import ehc_e2e.constants.yaml_config_constants as yaml_config_constants


def catch_assert_exception(f):
    """
    Just used for handling assert error and raise ExecutionFailed to let workflow continue running.
    """

    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except AssertionError as ex:
            raise ExecutionFailed(ex.message, continue_on_failure=workflow_continue_on_failure)

    return func


class BaseScenario(RP4VMWorkflow, SRMDRWorkflow):
    def __init__(self):
        super(BaseScenario, self).__init__()
        self.sn_context = DataContext()
        self._SCENARIO_KEYS = []
        self._CURRENT_CONTEXT = 'current_context'
        self._IS_RUNNING_WORKFLOW = 'is_running_workflow'
        self._SCENARIO_KEYS = 'scenario_keys'
        self.sn_context.update_context(None, self._CURRENT_CONTEXT)
        setattr(self.sn_context, self._SCENARIO_KEYS, [])
        # This key is used to indicate whether one workflow is running.
        # If no workflow is running won't merge yaml with dump context in method "apply_settings_from_dump" when resume.
        setattr(self.sn_context, self._IS_RUNNING_WORKFLOW, False)

    # update the latest workflow context:  self.wf_context into self.sn_context
    def update_scenario_context(self):
        yaml_path = getattr(self.wf_context, self.__class__.YAML_KEY_TO_WORKFLOW_CONFIG_FILE)
        # C:/ehc_e2e/conf/E2EWF-1-LC1S.config.yaml  -> E2EWF-1-LC1S
        yaml_key = os.path.split(yaml_path)[-1].split('.')[0]
        setattr(self.sn_context, yaml_key, self.wf_context)
        current_scenario_keys = getattr(self.sn_context, self._SCENARIO_KEYS, [])
        if yaml_key not in current_scenario_keys:
            current_scenario_keys.append(yaml_key)
        logger.debug('Save current context into key: {} in scenario context.'.format(yaml_key))
        setattr(self.sn_context, self._IS_RUNNING_WORKFLOW, False)
        logger.debug('Have set flag of IS_RUNNING_WORKFLOW to False after finish running.')
        logger.info('[AUC] - "Update Scenario Context" - PASSED', False, True)

    def reset_scenario_context(self):
        self.wf_context = YAMLData(**{})

    def apply_settings_for_scenario(self):
        pass

    @catch_assert_exception
    def apply_settings_from_dump(self, dump_file):
        import pickle
        assert os.path.isfile(dump_file), '"{}" is not provided.'.format(dump_file)
        try:
            with open(dump_file, 'rb') as dump_f:
                self.sn_context = pickle.load(dump_f)
                dump_context = getattr(self.sn_context, self._CURRENT_CONTEXT)
                if resume_also_include_workflow_yaml_file and getattr(self.sn_context, self._IS_RUNNING_WORKFLOW, False):
                    logger.debug('Use workflow yaml file to update mandatory keys in dump context.')
                    workflow_yaml_context = DataContext(None, 'DUMP_CONTEXT')
                    wf_yaml_file = getattr(
                        dump_context, self.__class__.YAML_KEY_TO_WORKFLOW_CONFIG_FILE, None)
                    gl_yaml_file = getattr(
                        dump_context, self.__class__.YAML_KEY_TO_GLOBAL_CONFIG_FILE, None)
                    assert wf_yaml_file, 'failed to get workflow yaml file path from dump file.'
                    assert gl_yaml_file, 'failed to get global yaml file path from dump file.'
                    workflow_yaml_context.update_context(wf_yaml_file, 'DUMP_CONTEXT')
                    workflow_yaml_context.update_context(gl_yaml_file, 'DUMP_CONTEXT')
                    assert getattr(
                        dump_context, self.__class__.YAML_KEY_TO_MANDATORY_SECTION, None) is not None, \
                        'dump content does not contain {} section'.format(
                            self.__class__.YAML_KEY_TO_MANDATORY_SECTION)
                    assert getattr(
                        workflow_yaml_context.DUMP_CONTEXT,
                        self.__class__.YAML_KEY_TO_MANDATORY_SECTION, None) is not None, \
                        'workflow yaml content does not contain {} section'.format(
                            self.__class__.YAML_KEY_TO_MANDATORY_SECTION)
                    from uiacore.modeling.webui.browser import Browser
                    update_exclusive_keys = ['added', 'existed', 'backup_service_levels']
                    self.data_context_attributes_compare_update(
                        dump_context, workflow_yaml_context.DUMP_CONTEXT, [Browser], update_exclusive_keys,
                        ['blueprint_machine_pairs'])
                    logger.debug(
                        'Updated dump context object mandatory keys using workflow config:{}'.format(
                            wf_yaml_file))
                self.wf_context = dump_context
                if hasattr(self.wf_context, 'shared'):
                    setattr(self.wf_context.shared.current_browser, 'is_login', False)
                    setattr(self.wf_context.shared.current_browser, 'current_user', None)
                    setattr(self.wf_context.shared.current_browser, 'launched', False)
                    logger.debug('Reset flag of is_login and launched.')
        except IOError:
            logger.error('Opening dump file:{} encountered error:{}'.format(dump_file, sys.exc_info()))
            raise

    def clean_up_environment_for_scenario(self):
        try:
            # update current workflow context into sn_context when encounter error
            CleanUp(
                name='CleanUp',
                ctx_in=self.sn_context,
                ctx_out=self.sn_context
            ).run()
        except:
            logger.warn('Failed to clean up chrome browser, please check the running processes manually!', True)

        try:
            DumpContext(
                name='DumpContext',
                ctx_in=self.sn_context,
                ctx_out=self.sn_context
            ).run()
        except:
            import sys
            import traceback
            logger.warn('error:{}'.format(sys.exc_info()))
            logger.warn('trace:{}'.format(traceback.print_stack()))
            logger.warn(
                'Failed to generate the dump file due to some corrupt data in run time! resume scenario may not work!',
                True)

    def prepare_workflow_data(self, global_file, yaml_file):
        assert os.path.isfile(global_file), '"{}" is not provided.'.format(global_file)
        assert yaml_file, 'Config file for sub workflow is not provided.'
        assert os.path.isfile(yaml_file), 'This is not a validate file: "{}".'.format(yaml_file)
        last_workflow_context = self.wf_context
        ctx = DataContext(None, self._GC_TAG)
        ctx.update_context(None, self._WORKFLOW_TAG)
        ctx.update_context(yaml_file, self._WORKFLOW_TAG)
        ctx.update_context(global_file, self._WORKFLOW_TAG)
        ctx.update_context(global_file, self._GC_TAG)
        self.wf_context = getattr(ctx, self._WORKFLOW_TAG)

        setattr(self.wf_context, self.__class__.YAML_KEY_TO_WORKFLOW_CONFIG_FILE, yaml_file)
        setattr(self.wf_context, self.__class__.YAML_KEY_TO_GLOBAL_CONFIG_FILE, global_file)

        # keep current browser status.
        if hasattr(last_workflow_context, 'shared') and hasattr(last_workflow_context.shared, 'current_browser') and \
                hasattr(self.wf_context, 'shared'):
            setattr(self.wf_context.shared, 'current_browser', getattr(last_workflow_context.shared, 'current_browser'))
            logger.debug(msg='Set current browser status in to current workflow context.')

        setattr(self.sn_context, self._IS_RUNNING_WORKFLOW, True)
        logger.debug('Have set flag of IS_RUNNING_WORKFLOW to True.')
        setattr(self.sn_context, self._CURRENT_CONTEXT, self.wf_context)
        logger.debug('Have rightly set workflow context and current context.')
        logger.info('[AUC] - "Prepare Workflow Data" - PASSED', False, True)

    def merge_context(self):
        last_workflow_context = self.wf_context
        self.wf_context = YAMLData(**{})
        for key in getattr(self.sn_context, self._SCENARIO_KEYS):
            value = getattr(self.sn_context, key, YAMLData(**{}))
            if value.__dict__:
                self.wf_context = merge_yaml_data(self.wf_context, value)
        # keep current browser status.
        if hasattr(last_workflow_context, 'shared') and hasattr(last_workflow_context.shared, 'current_browser') and \
                hasattr(self.wf_context, 'shared'):
            setattr(self.wf_context.shared, 'current_browser',
                    getattr(last_workflow_context.shared, 'current_browser'))
            logger.debug(msg='Set current browser status in to current workflow context.')
        setattr(self.sn_context, self._CURRENT_CONTEXT, self.wf_context)

        logger.info('[AUC] - "Merge Context" - PASSED', False, True)

    @catch_assert_exception
    def write_added_asr_from_current_workflow_to_scenario(self):
        self._parse_key_from_wf_context_to_scenario_contex(yaml_config_constants.ADDED_ASR_KEY_NAME)

    def _parse_key_from_wf_context_to_scenario_contex(self, key):
        key_value = getattr(self.wf_context, key, None)
        assert key_value is not None, "No {} is found when trying to parse it to scenario context.".format(key)
        setattr(self.sn_context, key, key_value)
        logger.info("Wrote value:{0} to key: {1} in context.".format(key_value, key))

    @catch_assert_exception
    def write_added_asr_from_scenario_to_current_workflow(self):
        try:
            self._parse_key_from_sn_context_to_wf_context(yaml_config_constants.ADDED_ASR_KEY_NAME)
            logger.info(
                '[AUC] - "{}" - {}'.format(
                    ' '.join([word.capitalize() for word in
                              self.write_added_asr_from_scenario_to_current_workflow.__name__.split('_')]), 'PASSED'),
                False, True)
        except Exception as e:
            logger.info('[AUC] - "{}" - {}'.format(
                ' '.join([word.capitalize()
                          for word in self.write_added_asr_from_scenario_to_current_workflow.__name__.split('_')]),
                'FAILED'), html=False, also_console=True)
            raise AssertionError(
                "Error {} occurs when trying to writing added ASR from scenarios to current workflow."
                    .format(e))
        
    def _parse_key_from_sn_context_to_wf_context(self, key):
        key_value = getattr(self.sn_context, key, None)
        assert key_value is not None, "No {} is found when trying to parse it to workflow context.".format(key)
        setattr(self.wf_context, key, key_value)
        logger.info("Wrote value:{0} to key: {1} in context.".format(key_value, key))

    def write_added_hwi_from_current_workflow_to_scenario(self):
        try:
            self._parse_key_from_wf_context_to_scenario_contex(yaml_config_constants.ADDED_HWI_KEY_NAME)
            logger.info(
                '[AUC] - "{}" - {}'.format(
                    ' '.join([word.capitalize() for word in
                              self.write_added_hwi_from_current_workflow_to_scenario.__name__.split('_')]), 'PASSED'),
                False, True)
        except Exception as e:
            logger.info('[AUC] - "{}" - {}'.format(
                ' '.join([word.capitalize()
                          for word in self.write_added_hwi_from_current_workflow_to_scenario.__name__.split('_')]),
                'FAILED'), html=False, also_console=True)
            raise AssertionError(
                "Error {} occurs when trying to writing added hwi from current workflow to scenario."
                    .format(e))

    def write_added_hwi_from_scenario_to_current_workflow(self):
        try:
            self._parse_key_from_sn_context_to_wf_context(yaml_config_constants.ADDED_HWI_KEY_NAME)
            logger.info(
                '[AUC] - "{}" - {}'.format(
                    ' '.join([word.capitalize() for word in
                              self.write_added_hwi_from_scenario_to_current_workflow.__name__.split('_')]), 'PASSED'),
                False, True)
        except Exception as e:
            logger.info('[AUC] - "{}" - {}'.format(
                ' '.join([word.capitalize()
                          for word in self.write_added_hwi_from_scenario_to_current_workflow.__name__.split('_')]),
                'FAILED'), html=False, also_console=True)
            raise AssertionError(
                "Error {} occurs when trying to write added hwi from scenario to current workflow."
                    .format(e))

    @catch_assert_exception
    def reverse_added_hwi_in_current_workflow(self):
        try:
            key_value = self._reverse_values_for_key_in_current_workflow(yaml_config_constants.ADDED_HWI_KEY_NAME)
            setattr(self.wf_context, yaml_config_constants.ADDED_HWI_KEY_NAME, key_value)
            logger.info(
                '[AUC] - "{}" - {}'.format(
                    ' '.join([word.capitalize() for word in
                              self.reverse_added_hwi_in_current_workflow.__name__.split('_')]), 'PASSED'),
                False, True)
        except Exception as e:
            logger.info('[AUC] - "{}" - {}'.format(
                ' '.join([word.capitalize()
                          for word in self.reverse_added_hwi_in_current_workflow.__name__.split('_')]),
                'FAILED'), html=False, also_console=True)
            raise AssertionError(
                "Error {} occurs when trying to reverse added hwi in current workflow."
                    .format(e))

    def _reverse_values_for_key_in_current_workflow(self, key):
        key_value = getattr(self.wf_context, key, None)
        assert key_value is not None, \
            "No {} is found in current workflow's context.".format(key)
        if isinstance(key_value, list):
            key_value.reverse()
            logger.info("Values for key: {0} is reversed to: {1}in current workflow."
                        .format(key, key_value))
            return key_value

    def _filter_mapping_relation_for_workflow_by_workflow_type(self, key):
        key_value = getattr(self.wf_context, 'workflow_relation_list', None)
        assert key_value is not None, \
            "'workflow_relation_list' in current workflow's context should not be None."
        assert isinstance(key_value, list), '{} should be list type.'.format(key_value)
        filtered_mapping_value = []
        for mapping_obj in key_value:
            assert mapping_obj.get_workflow_type(), \
                'Please provide workflow type in yaml file for relation mapping: {}.'.format(mapping_obj)
            if mapping_obj.get_workflow_type().lower() == key.lower():
                filtered_mapping_value.append(mapping_obj)
        setattr(self.wf_context, 'filtered_workflow_relation_mappings', filtered_mapping_value)
        logger.info(
            'Filtered mapping relation for next steps by key: {}.'.format(key))

    def filter_rp4vm_mapping_relation_for_workflow(self):
        self._filter_mapping_relation_for_workflow_by_workflow_type('RP4VM')

    def filter_local_mapping_relation_for_workflow(self):
        self._filter_mapping_relation_for_workflow_by_workflow_type('Local')

    def write_workflow_relation_mappings_from_current_workflow_to_scenario(self):
        self._parse_key_from_wf_context_to_scenario_contex(yaml_config_constants.MAPPING_LIST_KEY_NAME)

    def write_workflow_relation_mappings_from_scenario_to_current_workflow(self):
        self._parse_key_from_sn_context_to_wf_context(yaml_config_constants.MAPPING_LIST_KEY_NAME)

    @catch_assert_exception
    def generate_parameters_for_provision_cloud_storage(self):
        try:
            added_hwi_list = getattr(self.wf_context, yaml_config_constants.ADDED_HWI_KEY_NAME)
            provision_cloud_storage_list = self.wf_context.provision_multiple_cloud_storage
            for counter, item in enumerate(provision_cloud_storage_list):
                item.hwi_name = added_hwi_list[counter]
                logger.info('hwi name: {0} is set to provision cloud storage: {1}'
                            .format(added_hwi_list[counter], item))
            logger.info(
                '[AUC] - "{}" - {}'.format(
                    ' '.join([word.capitalize() for word in
                              self.generate_parameters_for_provision_cloud_storage.__name__.split('_')]), 'PASSED'),
                False, True)
        except Exception as e:
            logger.info('[AUC] - "{}" - {}'.format(
                ' '.join([word.capitalize()
                          for word in self.generate_parameters_for_provision_cloud_storage.__name__.split('_')]),
                'FAILED'), html=False, also_console=True)
            raise AssertionError(
                "Error {} occurs when trying to generate hwi name for provision multiple cloud storage."
                .format(e))

    def update_backup_service_level_to_mapping_relation(self):
        workflow_relation_list = getattr(self.wf_context, 'workflow_relation_list', None)
        assert workflow_relation_list, '"workflow_relation_list" in workflow context should not be None.'
        assert isinstance(workflow_relation_list, list), \
            '{} in context shoule be list type.'.format(workflow_relation_list)
        added_bsl = getattr(self.wf_context.shared.backup_service_levels, 'for_deletion', [])
        assert added_bsl, 'for_deletion in context should not be None.'
        for mapping_obj in workflow_relation_list:
            mapping_obj.update_backup_svc_levels(added_bsl)

    def update_blueprints_to_mapping_relation(self):
        workflow_relation_list = getattr(self.wf_context, 'workflow_relation_list', None)
        assert workflow_relation_list, '"workflow_relation_list" in workflow context should not be None.'
        assert isinstance(workflow_relation_list, list), \
            '{} in context shoule be list type.'.format(workflow_relation_list)
        blueprint_list = getattr(self.wf_context, 'blueprints', [])
        assert blueprint_list, 'Please provide blueprint in yaml file.'
        assert len(blueprint_list) == len(workflow_relation_list), \
            'The count of provided blueprints should equal to the count of relation mappings.'
        for i, mapping_obj in enumerate(workflow_relation_list):
            mapping_obj.set_blueprint(blueprint_list[i].blueprint_name)

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

import sys
from robot.api import logger
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.rest import GetARRFromvRO
from ehc_e2e.auc.uimap.shared import CatalogPage
from ehc_e2e.auc.uimap.shared import LoadingWindow
from ehc_e2e.auc.uimap.shared import RequestsPage
from ehc_e2e.auc.uimap.specific import ARRPage
from .arr_entity import ARR_Entity
import ehc_e2e.constants.ehc_constants as ehc_constants

class AddARR(BaseUseCase):
    """
    Add an Avamar Replication Relationship
    """

    # save the request result
    request_result = None
    step_failed_msg = 'Running on step: "Add Avamar Replication Relationship"-FAILED, {}'.format
    #  get arr added from arrs list which get from vRO
    arr = None
    # the entity which save the information of adding arr
    arr_entity = None

    def test_add_arr(self):
        arr_page = ARRPage()
        catalog_page = CatalogPage()
        load_window = LoadingWindow()
        logger.info(msg='Start to switch to catalog frame')
        navigate_to_catalog = catalog_page.navigate_to_catalog(self.current_browser)
        self.assertTrue(navigate_to_catalog,
                        msg=self.step_failed_msg('switch to catalog frame failed.'))
        catalog_page.wait_for_loading_complete(3)
        self.assertTrue(catalog_page.lnk_data_protection_services.exists(),
                        msg=self.step_failed_msg('cannot find Data Protection Services card in the left page.'))
        catalog_page.lnk_data_protection_services.click()
        catalog_page.wait_for_loading_complete(3)

        logger.info(msg='Start to click Avamar Replication Relationship (ARR) Maintenance request button.')
        self.assertTrue(catalog_page.btn_arr_maintenance_request.exists(),
                        msg=self.step_failed_msg(
                            'cannot find Avamar Replication Relationship (ARR) Maintenance card in the right page.'))
        catalog_page.btn_arr_maintenance_request.click()
        load_window.wait_loading(self.current_browser, 30)
        try:
            logger.info(msg='Start to fill items in the Request information tab')
            self.assertTrue(arr_page.txt_description.exists(),
                            msg=self.step_failed_msg('there is no input box: description'))
            arr_page.txt_description.set(self.description)
            arr_page.wait_for_loading_complete(2)
            self.assertTrue(arr_page.btn_next.exists(),
                            msg=self.step_failed_msg('there is no Next Button.'))
            arr_page.btn_next.click()
            load_window.wait_loading(self.current_browser, 30)

            logger.info(msg='Start to fill items in the Action Choose tab')
            self.assertTrue(arr_page.lnk_operation_type_menu.exists(),
                            msg=self.step_failed_msg('Action DropDownList open button does not exist.'))
            arr_page.lnk_operation_type_menu.click()
            self.assertTrue(
                arr_page.click_drop_down_list(
                    arr_page.lnk_select_dropdownlist,
                    'div',
                    self.operation_type),
                msg=self.step_failed_msg('cannot find option: "{}" in DropDownList Action'.format(self.operation_type)))
            load_window.wait_loading(self.current_browser, 30)
            self.assertTrue(arr_page.btn_next.exists(),
                            msg=self.step_failed_msg('there is no Next Button.'))
            arr_page.btn_next.click()
            load_window.wait_loading(self.current_browser, 30)

            logger.info(msg='Start to fill items in Add ARR tab')
            self.arr_entity = arr_page.add_arr(self.current_browser, self.onboard_cluster_type, self.arr_entity)
            self.assertIsNotNone(self.arr_entity,
                                 self.step_failed_msg('failed to fill items in Add ARR tab.'))

            logger.info(msg='Start to go into Submit Request tab')
            self.assertTrue(arr_page.btn_submit.exists(),
                            msg=self.step_failed_msg('there is no Submit Button.'))
            load_window.wait_loading(self.current_browser, 30)
            arr_page.btn_submit.click()
        except AssertionError:
            arr_page.save_request()
            raise
        except:
            arr_page.save_request()
            self.fail(msg=self.step_failed_msg('more error info: {}'.format(sys.exc_info())))

        logger.info(msg='Start to go into the request has been submitted successully page')
        self.assertTrue(arr_page.lbl_confirmation_success.exists(),
                        msg=self.step_failed_msg('there is no label: The request has been submitted successfully'))
        # wait to load frame
        arr_page.wait_for_loading_complete(2)
        arr_page.btn_ok.click()

        # switch to request
        logger.info(msg='Start to switch to request frame')
        arr_page.wait_for_loading_complete(2)
        self.assertTrue(RequestsPage().navigate_to_request(self.current_browser),
                        msg=self.step_failed_msg('switch to request frame failed.'))

        # check the request
        logger.info(msg='Start to check request result')
        req_result = RequestsPage().get_request_result(self.description)
        self.assertIsNotNone(req_result,
                             msg=self.step_failed_msg('failed to get the request result.'))
        self.request_result = req_result

        # get vro arrs list and filter arrs
        arr_list = GetARRFromvRO().get_arr_from_vro(self.ctx_in.vro)
        self.assertIsNotNone(arr_list, msg=self.step_failed_msg('failed to get arrs list from vRO.'))
        self.arr = arr_page.__class__.get_add_arr_from_all(arr_list, self.arr_entity)


    def fetch_matched_existed_arr(self):
        """
        If the ASR - Avamar grid combination already exists in other ARRs, cancel this add operation.
        :return: True or False
        """
        try:
            arr_list = GetARRFromvRO().get_arr_from_vro(self.ctx_in.vro)
            arr_entity_grid_set = set([self.arr_entity.site1_grid,
                                       self.arr_entity.site2_grid,
                                       self.arr_entity.site3_grid])

            for arr_item in arr_list:
                arr_site_grid_set = set([str(arr_item.site1_grid),
                                         str(arr_item.site2_grid),
                                         str(arr_item.site3_grid)])
                # Found a "duplicated" ARR
                if arr_item.parent_asr == self.arr_entity.parent_asr and \
                                arr_item.arr_type == self.arr_entity.arr_type and \
                                arr_entity_grid_set == arr_site_grid_set:
                    logger.info("Found existed ARR: {0} with same ASR: {1}, avamar grids: {2}, Put it in added_arr directly."
                           .format(arr_item.name, arr_item.parent_asr, arr_site_grid_set))
                    self.arr = arr_item
                    return True
            else:
                self.arr = None
                return False
        except Exception as e:
            logger.error("Exception: {} occurs when trying to get all ARRs from vRO.".format(e))
            raise AssertionError("Exception: {} occurs when trying to get all ARRs from vRO.".format(e))

    def runTest(self):
        self.added_arr_list = []
        for index, arr_item in enumerate(self.add_arr):
            self.parent_asr = ''
            self.asr_name = ''
            self.arr_name = ''
            # make sure asr value from add_arr.avamar_site_relationship_name or added_avamar_site_relationship
            if getattr(arr_item, 'avamar_site_relationship_name'):
                self.asr_name = arr_item.avamar_site_relationship_name
                self.parent_asr = arr_item.split('-')[0]
            elif self.added_asr_list[index]:
                asr_obj = self.added_asr_list[index]
                assert getattr(asr_obj, 'asr_name'), self.step_failed_msg(
                    'please check whether wrote back asr_name in YAML item added_avamar_site_relationship '
                    'after adding asr successfully.')
                assert getattr(asr_obj, 'backup_env_type'), self.step_failed_msg(
                    'please check whether wrote back backup_env_type in YAML item added_avamar_site_relationship '
                    'after adding asr successfully.')
                assert getattr(asr_obj, 'sites'), self.step_failed_msg(
                    'please check if sites are wrote back in added_avamar_site_relationship.'
                    'after adding asr successfully.')
                self.parent_asr = asr_obj.asr_name
                # template is ASR00001-[2C2VC-NewYork-Seattle]
                self.asr_name = self.parent_asr + '-[' + asr_obj.backup_env_type + '-' + '-'.join(
                    asr_obj.sites) + ']'
            else:
                self.fail(msg=self.step_failed_msg(
                    'please check whether test case added one asr successfully: '
                    'Cloud Administrator Adds Avamar Site Relationship.'))

            self.generate_avamar_grids(arr_item)
            self.arr_entity = ARR_Entity(self.get_arr_type.get(self.onboard_cluster_type), self.parent_asr,
                                         self.asr_name,
                                         self.site1_avamar_grid, self.site2_avamar_grid, self.site3_avamar_grid)

            if arr_item.allow_duplicated_arr:
                self.add_new_arr()
            else:
                # arr already exists, don't run add arr request.
                if self.fetch_matched_existed_arr():
                    arr_full_name = self.generate_arr_full_name()
                else:
                    arr_full_name = self.add_new_arr()
            self.added_arr_list.append(arr_full_name)

    def generate_avamar_grids(self, arr_item):
        self.site1_avamar_grid = ''
        self.site2_avamar_grid = ''
        self.site3_avamar_grid = ''

        _site1_avamar_in_add_arr = getattr(arr_item, 'site1_avamar_grid', None)
        _site2_avamar_in_add_arr = getattr(arr_item, 'site2_avamar_grid', None)
        _site3_avamar_in_add_arr = getattr(arr_item, 'site3_avamar_grid', None)
        if self.onboard_cluster_type in ['DR2S', 'CA2S', 'MP2S', 'LC2S', 'VS2S']:
            flag = _site1_avamar_in_add_arr and _site2_avamar_in_add_arr \
                   or \
                   len(self.added_avamar_grid) >= 2
            assert flag, self.step_failed_msg(
                'please check whether test case added two Avamar Grids successfully: '
                'Cloud Administrator Adds Avamar Grid.')
            if _site1_avamar_in_add_arr and _site2_avamar_in_add_arr:
                self.site1_avamar_grid = _site1_avamar_in_add_arr
                self.site2_avamar_grid = _site2_avamar_in_add_arr
            else:
                self.site1_avamar_grid = self.added_avamar_grid[0]
                self.site2_avamar_grid = self.added_avamar_grid[1]

        if self.onboard_cluster_type in ['LC1S', 'CA1S', 'VS1S']:
            flag = _site1_avamar_in_add_arr \
                   or \
                   len(self.added_avamar_grid) >= 1
            assert flag, self.step_failed_msg(
                'please check whether test case added one Avamar Grid successfully: '
                'Cloud Administrator Adds Avamar Grid.')
            if _site1_avamar_in_add_arr:
                self.site1_avamar_grid = _site1_avamar_in_add_arr
            else:
                self.site1_avamar_grid = self.added_avamar_grid[0]

        if self.onboard_cluster_type == 'MP3S':
            flag = _site1_avamar_in_add_arr and _site2_avamar_in_add_arr and _site3_avamar_in_add_arr \
                   or \
                   len(self.added_avamar_grid) >= 3
            assert flag, self.step_failed_msg(
                'please check whether test case added three Avamar Grids successfully: '
                'Cloud Administrator Adds Avamar Grid.')

            if _site1_avamar_in_add_arr and _site2_avamar_in_add_arr and _site3_avamar_in_add_arr:
                self.site1_avamar_grid = _site1_avamar_in_add_arr
                self.site2_avamar_grid = _site2_avamar_in_add_arr
                self.site3_avamar_grid = _site3_avamar_in_add_arr
            else:
                self.site1_avamar_grid = self.added_avamar_grid[0]
                self.site2_avamar_grid = self.added_avamar_grid[1]
                self.site2_avamar_grid = self.added_avamar_grid[2]

    def add_new_arr(self):
        self.test_add_arr()
        arr_full_name = self.generate_arr_full_name()
        if self.request_result is not None:
            more_details = "{" + self.arr_name + ", " + self.request_result.status + ", " + \
                           self.request_result.status_details + "}"
            self.assertTrue(self.request_result.status == 'Successful',
                            msg='Add an Avamar Replication Relationship failed: {0}, '
                                'for more details: {1}'.format(self.arr_name, more_details))
            logger.info('Add an Avamar Replication Relationship successful: {0}, for more details: {1}'.format(
                self.arr_name, more_details), False, True)
        return arr_full_name

    def generate_arr_full_name(self):
        """
        
        :return: arr_name(STRING)
        """
        back_type = self.get_arr_type.get(self.onboard_cluster_type)
        arr_name = '{0} ({1}{2}{3}{4})'.format(self.arr.name, back_type,
                                               ('-' + self.arr.site1_grid) if self.arr.site1_grid != '' else '',
                                               ('-' + self.arr.site2_grid) if self.arr.site2_grid != '' else '',
                                               ('-' + self.arr.site3_grid) if self.arr.site3_grid != '' else '')
        logger.info('ARR full name is: {}'.format(arr_name))
        return arr_name

    def _validate_context(self):
        _all_cluster_type = ehc_constants.CLUSTER_TYPES
        self.get_arr_type = {
            'LC1S': '1C1VC',
            'DR2S': '2C2VC',
            'CA1S': '1C1VC',
            'CA2S': '2C1VC',
            'MP2S': '2C2VC',
            'MP3S': '3C2VC',
            'LC2S': 'MC2VC',
            'VS1S': '1C1VC',
            'VS2S': 'MC2VC',
        }

        if self.ctx_in:
            # set operation action
            self.operation_type = 'Add ARR'
            self.description = 'test_add_arr'
            # validate browser and vro info
            self.current_browser = getattr(self.ctx_in.shared, 'current_browser', None)
            assert self.current_browser, self.step_failed_msg('please login to vRA, The flag "is_login" is False.')
            self.vro_address = getattr(self.ctx_in.vro, 'address', None)
            self.vro_username = getattr(self.ctx_in.vro, 'username', None)
            self.vro_password = getattr(self.ctx_in.vro, 'password', None)
            assert self.vro_address, self.step_failed_msg('vRO address is not provided!')
            assert self.vro_username, self.step_failed_msg('vRO username is not provided!')
            assert self.vro_password, self.step_failed_msg('vRO password is not provided!')

            # validate onboard cluster type
            self.onboard_cluster_type = getattr(self.ctx_in, 'onboard_cluster_type', None)
            assert self.onboard_cluster_type, self.step_failed_msg('please provide onboard cluster type.')
            assert self.onboard_cluster_type in _all_cluster_type, \
                self.step_failed_msg("onboard cluster type should be in {0}.".format(_all_cluster_type))

            # get added_avamar_grid if not exists , set default value: []
            self.added_avamar_grid = getattr(self.ctx_in, 'added_avamar_grid', [])

            # get added_avamar_site_relationship
            self.added_asr_list = self.ctx_in.added_avamar_site_relationship
            assert len(self.added_asr_list) > 0, self.step_failed_msg('No added asr info is provided.')

            # get value in add_an_avamar_replication_relationship
            self.add_arr = getattr(self.ctx_in, 'add_an_avamar_replication_relationship', None)
            assert len(self.add_arr) > 0, self.step_failed_msg('No add arr info is provided.')

    def _finalize_context(self):
        setattr(self.ctx_out, 'added_avamar_replication_relationship', self.added_arr_list)

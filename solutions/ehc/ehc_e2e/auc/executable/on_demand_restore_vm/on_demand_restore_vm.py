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
import time
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared import ItemPage, BasePage, LoadingWindow
from ehc_e2e.auc.uimap.specific import OperateVMPage, OndemandRestoreVMPage
from robot.api import logger
from ehc_e2e.auc.reusable import context_util
from ehc_e2e.auc.reusable.browser_relauncher import close_relaunch_browser_operation


class NoBackupPointFoundException(BaseException):
    # Dropdown item content
    # message = 'No backups found for this machine, may be backup schedule did not start yet for this machine'
    message = 'No LOCAL backups found for this machine, may be backup schedule did not start for this machine yet'
    fragment = 'did not start'

    def __init__(self):
        super(NoBackupPointFoundException, self).__init__()
        self.message = NoBackupPointFoundException.message


class OnDemandRestoreVM(BaseUseCase):
    """
    TAF-446: AUC-15 Day2 Operation - On Demand Restore
    """
    MAX_TIMES_TO_CLOSE_RELAUNCH = 5

    def test_on_demand_restore(self):
        self.target_page = OndemandRestoreVMPage()
        self.operatevm_page = OperateVMPage(self._vm_name)
        try:
            self._start_new_service_request()
            try:
                if self._fill_out_request_info() is False:
                    return False
                self._submit_request()
            except AssertionError, e:
                if e.message == NoBackupPointFoundException.message and self.wait_in_workflow:
                    if BasePage().btn_cancel.exists():
                        BasePage().btn_cancel.click()
                        time.sleep(2)
                        logger.debug("Clicked close button to sa the request.")
                    raise NoBackupPointFoundException()
                else:
                    BasePage().save_request()
                    raise e
        except:
            if not self.wait_in_workflow:
                ex = sys.exc_info()
                logger.error('{0} encounters error: {1}'.format(self.test_on_demand_restore.__name__, ex))
            raise

    def _start_new_service_request(self):
        self.assertTrue(ItemPage.get_vm_status(self.current_browser, self._vm_name) == 'Off',
                        msg='VM should turn off first')

        items_page = ItemPage(self.current_browser)
        self.assertTrue(items_page.enter_frame(), msg='Failed to switch to items page')
        time.sleep(3)
        items_page.enter_vm_frame(self._vm_name)

        self.assertTrue(self.operatevm_page.btn_on_demand_restore.exists(), msg='OnDemandRestore button does not exist')
        self.operatevm_page.btn_on_demand_restore.click()
        time.sleep(3)
        LoadingWindow().wait_loading2(self.current_browser, 120)

    def _fill_out_request_info(self):
        if self.__file_out_description_and_reason()is False:
            return False
        self.__chose_backup_point()

    def _submit_request(self):
        self.assertTrue(self.operatevm_page.btn_submit.exists(), msg='Submit button does not exist')
        logger.debug('Submitting enable on demand backup button')
        self.operatevm_page.btn_submit.click()

        if self.operatevm_page.btn_ok.exists():
            self.operatevm_page.btn_ok.click()
            logger.info('Click request successful OK button.')

    def __file_out_description_and_reason(self):
        if self.operatevm_page.txt_description.exists():
            logger.info('Found description input box', False, True)
        else:
            logger.warn('Description input box does not exist')
            return False
        self.assertTrue(self.operatevm_page.txt_reasons.exists(), msg='Reasons input box does not exist')
        self.operatevm_page.txt_description.set(self._description)
        self.operatevm_page.txt_reasons.set(self._reason)
        self.operatevm_page.btn_next.click()

    def __chose_backup_point(self):
        self.assertTrue(self.target_page.cbo_backup_points.exists(), 'Element backup-points combobox not exists')
        backup_points = self.target_page.cbo_backup_points.items()
        empty_points = [point for point in backup_points if NoBackupPointFoundException.fragment in point]
        self.assertTrue(len(empty_points) == 0, NoBackupPointFoundException.message)
        self.assertTrue(len(backup_points) >= 1, 'Backup points item count should not less than 1')
        first_point = backup_points[0]
        self.target_page.cbo_backup_points.select(by_visible_text=first_point)
        logger.info('Selected backup point: {}'.format(first_point), also_console=True)

    def runTest(self):
        retry_times = 1
        max_times = OnDemandRestoreVM.MAX_TIMES_TO_CLOSE_RELAUNCH
        while retry_times <= max_times \
                and self.test_on_demand_restore() is False:
            logger.info('The {} time to close and relaunch browser'.format(retry_times), False, True)
            close_relaunch_browser_operation()
            self.current_browser = \
                context_util.get_last_baseworkflow_instance().wf_context.shared.current_browser
            retry_times += 1

        self.assertTrue(retry_times <= max_times,
                        'On demand restore vm failed after {} times close and relaunch browser'.format(
                            max_times))

    def _validate_input_args(self, current_browser=None, is_login=False, description=None, vm_name=None,
                             wait_in_workflow=True):
        assert current_browser is not None, 'current_browser is None, maybe there is no active browser.'
        assert is_login is True, "Not logged in."
        assert vm_name is not None, 'Name of VM should not be None.'

        self.current_browser = current_browser
        self._description = description
        self._vm_name = vm_name
        self._reason = description
        self.wait_in_workflow = wait_in_workflow

    def _finalize_context(self):
        pass

    def run(self, result=None):
        """
        Overwrite the behaviors of BaseUseCase
        Only
        """
        import traceback
        import warnings
        from unittest.case import SkipTest, _ExpectedFailure, _UnexpectedSuccess
        from robot.errors import ExecutionFailed

        orig_result = result
        if result is None:
            result = self.defaultTestResult()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()

        self._resultForDoCleanups = result
        result.startTest(self)

        testMethod = getattr(self, self._testMethodName)
        if (getattr(self.__class__, "__unittest_skip__", False) or
                getattr(testMethod, "__unittest_skip__", False)):
            # If the class or method was skipped.
            try:
                skip_why = (getattr(self.__class__, '__unittest_skip_why__', '') or
                            getattr(testMethod, '__unittest_skip_why__', ''))
                self._addSkip(result, skip_why)
            finally:
                result.stopTest(self)
            return
        try:
            success = False

            try:
                _output_key = 'output'

                if _output_key in self._kwargs:
                    self._output = self._kwargs.pop(_output_key)

                    if not isinstance(self._output, (list, dict, set, bytearray)):
                        raise ValueError('The output parameter must be mutable.')

                self._validate_input_args(**self._kwargs)
            except SkipTest as e:
                self._addSkip(result, str(e))
            except KeyboardInterrupt:
                raise
            except:
                raise
            else:
                self.setUp()

                try:
                    testMethod()
                except KeyboardInterrupt:
                    raise
                except _ExpectedFailure as e:
                    addExpectedFailure = getattr(result, 'addExpectedFailure', None)
                    if addExpectedFailure is not None:
                        addExpectedFailure(self, e.exc_info)
                    else:
                        warnings.warn("TestResult has no addExpectedFailure method, reporting as passes",
                                      RuntimeWarning)
                        result.addSuccess(self)
                except _UnexpectedSuccess:
                    addUnexpectedSuccess = getattr(result, 'addUnexpectedSuccess', None)
                    if addUnexpectedSuccess is not None:
                        addUnexpectedSuccess(self)
                    else:
                        warnings.warn("TestResult has no addUnexpectedSuccess method, reporting as failures",
                                      RuntimeWarning)
                        result.addFailure(self, sys.exc_info())
                except SkipTest as e:
                    self._addSkip(result, str(e))
                except:
                    raise
                else:
                    success = True
                finally:
                    # Set the tearDown() method as the last resort for error recovery
                    # NB: Exception raised from testMethod() will be overwritten by the one raised from tearDown()
                    try:
                        self.tearDown()
                    except KeyboardInterrupt:
                        raise
                    except:
                        raise

            cleanUpSuccess = self.doCleanups()
            success = success and cleanUpSuccess
            if success:
                result.addSuccess(self)
        except Exception as ex:
            result.addFailure(self, sys.exc_info())

            if isinstance(ex, self.failureException):
                tb = traceback.format_tb(sys.exc_info()[-1])
                msg = 'Within "<b>{}</b>" AUC,<p> <b>Code Stack:</b>\n{}'.format(
                    self._name, ''.join(tb[1:]))

                logger.debug(msg, html=True)

            if not self._ignore_failure():
                logger.error(ex.message)
                raise ExecutionFailed(ex.message, continue_on_failure=True)
        finally:
            if hasattr(self, '_output'):
                self._finalize_output_params()

            if result.failures or result.errors:
                status = 'FAILED'
            else:
                status = 'PASSED'

            if not self.wait_in_workflow:
                logger.info('[AUC] - "{}" - {}'.format(
                    ' '.join([word.capitalize()
                              for word in self._name.split('_')]),
                    status), html=False, also_console=True)

            result.stopTest(self)
            if orig_result is None:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()

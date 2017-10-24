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
import traceback
import unittest
import warnings
from unittest.case import SkipTest, _ExpectedFailure, _UnexpectedSuccess
from robot.api import logger
from robot.errors import ExecutionFailed
from selenium.common.exceptions import WebDriverException


class BaseUseCase(unittest.TestCase):
    def __init__(self, name=None, method_name='runTest',
                 ctx_in=None, ctx_out=None, **kwargs):
        super(BaseUseCase, self).__init__(method_name)
        self._kwargs = kwargs

        self._name = name or self.__class__.__name__
        self.ctx_in = ctx_in
        self.ctx_out = ctx_out

    def setUp(self):
        if self.ctx_in:
            self._validate_context()

    def tearDown(self):
        # Finalize the involved test context
        self._finalize_context()

    def run(self, result=None):
        """
        Overwrite the behaviors of catching exceptions
        - failureExceptions will be treated as robot ExecutionFailed and
            won't block the followed test case
        - other Exceptions will be bubbled up to higher level (e.g., robot framework)
        """

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
                skip_why = (getattr(self.__class__, '__unittest_skip_why__', '')
                            or getattr(testMethod, '__unittest_skip_why__', ''))
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

                    if type(self._output) not in [list, dict, set, bytearray]:
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
                    if not success:
                        try:
                            from ehc_e2e.utils.snapshot import SnapShot
                            SnapShot.takes_screen_shot()
                        except:
                            logger.warn('Encounter error when taking screen shot in baseusecase, '
                                        'detail info: {}'.format(sys.exc_info()))
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

            if isinstance(ex, WebDriverException):
                ex.message = ex.msg

            ex.message = ex.message if ex.message else str(ex)
            logger.error('Encounters exception, type:{}, exception message:{}'.format(
                type(ex), ex.message))
            from ehc_e2e.setting import workflow_continue_on_failure
            raise ExecutionFailed(ex.message, continue_on_failure=workflow_continue_on_failure)
        finally:
            if hasattr(self, '_output'):
                self._finalize_output_params()

            if result.failures or result.errors:
                status = 'FAILED'
            else:
                status = 'PASSED'

            logger.info('[AUC] - "{}" - {}'.format(
                ' '.join([word.capitalize()
                          for word in self._name.split('_')]),
                status), html=False, also_console=True)

            result.stopTest(self)
            if orig_result is None:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()

    def _validate_context(self):
        pass

    def _finalize_context(self):
        if self.ctx_out:
            setattr(self.ctx_out, 'context', None)

    def _ignore_failure(self, debug_only=True):
        if debug_only:
            import inspect
            for frame in inspect.stack()[::-1]:
                if frame[1].endswith('pydevd.py'):
                    return True
            else:
                return bool(sys.flags.debug)

        return False

    def _validate_input_args(self, **kwargs):
        pass

    def _finalize_output_params(self):
        pass

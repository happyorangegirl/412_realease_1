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

from time import localtime, strftime
from robot.api import logger
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.utils.context.model import YAMLData


class DumpContext(BaseUseCase):
    """
    Dump current context object into temp file
    """
    def test_dump_context(self):
        assert self.ctx_in is not None, '[WARN] Context object is None, skip the dump step.'
        timestamp = strftime('%Y%m%d-%H%M%S', localtime())
        test_type = 'workflows'
        # reset the object value
        if hasattr(self.ctx_in, 'current_context'):
            logger.debug('Test Type: {scenarios}')
            test_type = 'scenarios'
            for data in [value for value in self.ctx_in.__dict__.itervalues() if hasattr(value, 'shared')]:
                if hasattr(data.shared, 'current_browser'):
                    setattr(data.shared.current_browser, 'instance', 1)
            logger.debug('Have set current browser instance to 1 in sn_context, '
                         'make sure dump file can be load successful in autodebug or resume.')
        else:
            if hasattr(self.ctx_in, 'shared') and hasattr(self.ctx_in.shared, 'current_browser'):
                setattr(self.ctx_in.shared.current_browser, 'instance', 1)
        dump_file = '/root/automation/ehc/{}/dump/dump-{}.yaml'.format(test_type, timestamp)
        from sys import platform
        if 'win' in platform:
            logger.info('Current platform is windows, will take windows temporary directory.')
            import os
            temp_dir = os.getenv('TEMP')
            dump_file = os.path.join(temp_dir, 'dump-{}.yaml'.format(timestamp))
        import pickle
        with open(dump_file, 'wb') as dfile:
            pickle.dump(self.ctx_in, dfile)
            logger.info('Dump file generated at: {}'.format(dump_file))

    def runTest(self):
        self.test_dump_context()

    def props(self, x):
        if isinstance(x, YAMLData):
            return dict((key, self.props(getattr(x, key))) for key in dir(x) if key not in dir(x.__class__))
        else:
            return dict((key, getattr(x, key)) for key in dir(x) if key not in dir(x.__class__))

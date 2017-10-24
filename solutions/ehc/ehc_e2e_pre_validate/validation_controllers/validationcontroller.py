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

import logging

from ehc_e2e_pre_validate.validators import ValidatorBase


class ValidationController(object):
    def __init__(self, validator_sequence_name):
        self._validator_queue = []
        self._results = {}
        self._validator_sequence_name = validator_sequence_name

    @property
    def Results(self):
        return self._results

    def add_validators(self, validators):
        if validators:
            if isinstance(validators, ValidatorBase):
                logging.info(
                    'Adding validator:{validator_name} into {sequence_name} validation queue.'.format(
                        validator_name=validators.name, sequence_name=self._validator_sequence_name))
                self._validator_queue.append(validators)
            else:
                for validator in validators:
                    if isinstance(validator, ValidatorBase):
                        logging.info(
                            'Adding validator:{validator_name} into {sequence_name} validation '
                            'queue.'.format(
                                validator_name=validator.name,
                                sequence_name=self._validator_sequence_name))
                        self._validator_queue.append(validator)
                    else:
                        logging.warn(
                            '"{}" is not a valid validator, will skip it.'.format(validator.__name__))

    def process_validators(self):
        logging.info('Start processing validators in validator queue:{}'.format(
            self._validator_sequence_name))
        for validator in self._validator_queue:
            validator.validate()
            if validator.validation_result:
                logging.info('Completed validation for validator:{validator_name}, PASSED.'.format(
                    validator_name=validator.name))
            else:
                logging.error('Completed validation for validator:{validator_name}, FAILED.'.format(
                    validator_name=validator.name))
            if self._results.get(validator.name, None):
                logging.warn('There is already a validator:{} in result collection.'.format(
                    validator.name))

            self._results.update({validator: validator.validation_result})

    def validator_queue_generator(self):
        for validator in self._validator_queue:
            yield validator

    def print_results(self):
        print '+--------------------------------------------------------------------+'
        print '| {} Validator Name {} |  Result  |'.format(
            self._validator_sequence_name, ''.join(
                [' ' for i in xrange(1, 70- 30 - len(self._validator_sequence_name))]))
        print '+--------------------------------------------------------------------+'

        for validator, result in self._results.iteritems():
            print '| ' + validator.name.ljust(56, ' ') + '|  ' + str(result.validation_result).ljust(8, ' ') + '|'

        print '+--------------------------------------------------------------------+'

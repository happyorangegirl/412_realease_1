#  Copyright 2016 EMC HCE EHC SW Automation
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
from robot.api import logger
import time
import datetime


class Schedule(object):
    _SCHEDULE_TYPES = ['Daily', 'Weekly', 'Monthly']
    _RETENTION_TYPES = ['Forever', 'For', 'Until']
    _RETENTION_UNITS = ['Days', 'Weeks', 'Months', 'Years']
    _WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    _WEEK_NUMBER = ['First', 'Second', 'Third', 'Fourth', 'Last']

    @staticmethod
    def validate_weekday(weekday):
        if weekday is None:
            return False
        is_valid = weekday in Schedule._WEEKDAYS
        if not is_valid:
            logger.error("{} is Not a valid weekday in schedule configuration! Please pick a value from {}"
                         .format(weekday, Schedule._WEEKDAYS))
        return is_valid

    @staticmethod
    def validate_time_with_suffix(time_str):
        try:
            if time_str is None:
                return False
            time.strptime(time_str, '%H:%M %p')
            return True
        except ValueError:
            logger.error('{} is Not a valid time(AM/PM must be provided) in configuration file!'.format(time_str))
            return False

    @staticmethod
    def validate_time(time_str):
        try:
            if time_str is None:
                return False
            time.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            logger.error('{} is Not a valid time provided in configuration file!'.format(time_str))
            return False

    @staticmethod
    def validate_week_number(str_week_num):
        if str_week_num is None:
            return False
        is_valid = str_week_num in Schedule._WEEK_NUMBER
        if not is_valid:
            logger.error('{} is Not a valid week number in configuration file! please pick a value from {}'
                         .format(str_week_num, Schedule._WEEK_NUMBER))
        return is_valid

    @staticmethod
    def validate_number(str_num):
        if str_num is None:
            return False
        is_valid =str_num.isdigit()
        if not is_valid:
            logger.error('{} is Not a valid number provided in configuration file!'.format(str_num))
        return is_valid

    @staticmethod
    def validate_date(str_date):
        if str_date is None:
            return False
        try:
            datetime.datetime.strptime(str_date, '%m/%d/%y')
            return True
        except ValueError:
            logger.error('{} is Not a valid date format %m/%d/%Y provided in configuration file!'.format(str_date))
            return False

    @staticmethod
    def failure_exit():
        assert False, 'Invalid configurations in backup service level schedule/retention!'

    @staticmethod
    def pass_validation(policy):
        logger.info("Validated configuration for \'{}\' configuration.".format(policy), True, True)
        return True

    @staticmethod
    def get_date_one_month_later():
        d1 = datetime.datetime.now()
        use_date = d1 + datetime.timedelta(days=+60)
        one_month_later = use_date.strftime('%m/%d/%y')
        return one_month_later


class BSLRetention(Schedule):
    def __init__(self, retention_policy, long_term_retention_year, retention_number, retention_unit, retention_date, retention_time):
        self._retention_policy = retention_policy
        self._long_term_retention_year = long_term_retention_year
        self._retention_number = retention_number
        self._retention_unit = retention_unit
        self._retention_date = self.get_date_one_month_later()
        self._retention_time = retention_time

    @property
    def retention_policy(self):
        return self._retention_policy

    @property
    def long_term_retention_year(self):
        return self._long_term_retention_year

    @property
    def retention_number(self):
        return self._retention_number

    @property
    def retention_unit(self):
        return self._retention_unit

    @property
    def retention_date(self):
        return self._retention_date

    @property
    def retention_time(self):
        return self._retention_time

    @staticmethod
    def validate_retention_unit(retention_unit):
        if retention_unit is None:
            return False
        return retention_unit in Schedule._RETENTION_UNITS

    def validate_retention(self):
        if self._retention_policy is not None and self._retention_policy in self._RETENTION_TYPES:
            log_message = '{} retention policy'.format(self._retention_policy)
            if self._retention_policy == 'Forever':
                if self.validate_number(self._long_term_retention_year):
                    return self.pass_validation(log_message)
                else:
                    self.failure_exit()
            elif self._retention_policy == 'For':
                if self.validate_number(self._long_term_retention_year) and self.validate_number(self._retention_number)\
                        and self.validate_retention_unit(self._retention_unit):
                    return self.pass_validation(log_message)
                else:
                    self.failure_exit()
            else:
                if self.validate_number(self._long_term_retention_year) and self.validate_date(self._retention_date) \
                        and self.validate_time_with_suffix(self._retention_time):
                    return self.pass_validation(log_message)
                else:
                    self.failure_exit()
        else:
            logger.error("Retention type {} is not supported! Please double check your configurations.".format(
                self._retention_policy))
            self.failure_exit()


class BSLSchedule(Schedule):

    def __init__(self, schedule_type, schedule_week_number, schedule_weekday, schedule_start_time):
        self._schedule_type = schedule_type
        self._schedule_week_number = schedule_week_number
        self._schedule_weekday = schedule_weekday
        self._schedule_start_time = schedule_start_time

    @property
    def schedule_type(self):
        return self._schedule_type

    @property
    def schedule_week_number(self):
        return self._schedule_week_number

    @property
    def schedule_weekday(self):
        return self._schedule_weekday

    @property
    def schedule_start_time(self):
        return self._schedule_start_time

    def validate_schedule(self):
        if self._schedule_type is not None and self._schedule_type.capitalize() in self._SCHEDULE_TYPES:
            log_message = '{} schedule policy'.format(self._schedule_type)
            if self._schedule_type == 'Monthly':
                if self.validate_week_number(self._schedule_week_number) \
                        and self.validate_weekday(self._schedule_weekday):
                    return self.pass_validation(log_message)
                else:
                    self.failure_exit()
            elif self._schedule_type == 'Weekly':
                if self.validate_weekday(self._schedule_weekday):
                    return self.pass_validation(log_message)
                else:
                    self.failure_exit()
            else:
                if self.validate_time(self._schedule_start_time):
                    return self.pass_validation(log_message)
                else:
                    self.failure_exit()
        else:
            logger.error("Schedule type {} is not supported! Please double check your configurations.".format(
                self._schedule_type))
            self.failure_exit()



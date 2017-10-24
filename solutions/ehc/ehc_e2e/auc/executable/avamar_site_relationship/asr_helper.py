"""
 Copyright 2016 EMC GSE SW Automation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

from robot.api import logger


def filter_latest_added_asr(list_asr, asr_type, *sites):
    if len(sites) > 3:
        logger.error(
            'Avamar site relationship currently only supports three sites.')
        return None

    final_result = None
    if len(list_asr) >= 1:
        logger.debug('Retrieved {} ASR(s) from vRO.'.format(len(list_asr)))
        asr_type_matches = [asr for asr in list_asr if (
            asr.asr_type == asr_type and asr.site1.lower() == (
                sites[0].lower() if len(sites) > 0 else '') and asr.site2.lower() == (
                    sites[1].lower() if len(sites) > 1 else '') and asr.site3.lower() == (
                        sites[2].lower() if len(sites) > 2 else ''))]
        if len(asr_type_matches) >= 1:
            logger.info(
                'Found {0} ASR(s) with specified condition: [asr_type:{1}, sites: {2}] found in vRO.'
                ''.format(len(asr_type_matches), asr_type, ', '.join(sites)),
                False, True)

            final_result = sorted(
                asr_type_matches, key=lambda asr_item: int(asr_item.id))[-1].name
            logger.debug('Filtered out the latest ASR {} as the result.'
                         ''.format(final_result))
        else:
            logger.error(
                'ASR with specified condition: [asr_type:{0}, sites: {1}]'
                ' not found in vRO.'
                ''.format(asr_type, ', '.join(sites)))
    else:
        logger.warn('No ASR retrieved from vRO!')

    return final_result

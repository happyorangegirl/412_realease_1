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

from uiacore.modeling.webui.controls import WebFrame as Frame


class WebFrame(Frame):
    @property
    def current(self):
        """
        Get the iframe with specific attribute
        :return: WebElement
        """

        _attribute = 'onload'
        _value = self._constraints.pop(_attribute, None)

        if _value:
            self._current = None

            _iframes = [_iframe for _iframe in self._find_elements()
                        if _iframe.get_attribute(_attribute) and (
                            _value in _iframe.get_attribute(_attribute))]

            for _iframe in _iframes:
                for key, value in self._constraints.iteritems():
                    if _iframe.get_attribute(key) != value:
                        break
                else:
                    self._current = _iframe
                    break

            if self._current and self._current.get_attribute('id'):
                self._constraints.setdefault(
                    'id', self._current.get_attribute('id'))
            else:
                self._constraints[_attribute] = _value

            return self._current

        return super(WebFrame, self).current

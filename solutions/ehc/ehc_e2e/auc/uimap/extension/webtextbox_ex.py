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

# pylint: disable=too-many-ancestors

import time
from uiacore.foundation.imp.web.selenium.controls.webedit import  WebEdit

class WebTextBoxEx(WebEdit):
    """
    Extension class for uiacore version of WebTextBox, to provide more stable set method for ehc vRA request textboxes.
    We bypassed TechFactory().active.get_element_type call which was for bridging the actual implementation and model
     interface, to directly hack an extension version of WebTextBox class, just to override set method.
    """

    def set(self, value=None):
        """
        overrides selenium tech implementation in uiacore, to add focus and sleep
        before each action to the textbox element.
        This is because some ehc vRA textbox is having JS scripts registered, but those JS scripts
         is not running elegant enough which is likely to impact focus for webelement between ui actions.
        """
        if not self.exists():
            raise RuntimeError('WebEdit control is not displayed')

        self.activate()
        time.sleep(1)
        self.object.clear()

        self.activate()
        time.sleep(1)
        self.object.send_keys(value)


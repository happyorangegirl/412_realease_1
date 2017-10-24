from uiacore.modeling.webui.controls import WebTextBox, WebButton
from ehc_e2e.auc.uimap.shared.basepage import BasePage


class FabricGroupPage(BasePage):
    def __init__(self):
        super(FabricGroupPage, self).__init__()

        self.btn_new_fg = WebButton(xpath='//span[text()="New"]')
        self.txt_fg_name = WebTextBox(xpath='//input[contains(@id, "txtName")]')
        self.txt_admin = WebTextBox(xpath='//input[contains(@id, "txtMembers_UserPicker_I")]')
        self.btn_user_search = WebButton(xpath='//a[@class="UserPickerSearch"]')
        self.btn_ok = WebButton(xpath='//span[text()="OK"]')

from uiacore.modeling.webui.controls import WebTextBox, WebButton
from .basepage import BasePage


class LogoutPage(BasePage):
    def __init__(self):
        self.btn_logout = WebButton(id='SHELL_LOGOUT')
        self.btn_back_to_login_page = WebButton(xpath='//button[text()="Go back to login page"]')
        self.btn_back_to_login_page_xpath = '//button[text()="Go back to login page"]'
        self.txt_username = WebTextBox(id='username')
        self.txt_username_xpath = '//*[@id="username"]'

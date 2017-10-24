from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared.loadingwindow import LoadingWindow
from ehc_e2e.auc.uimap.shared import InfrastructurePage
from ehc_e2e.auc.uimap.specific import FabricGroupPage
from selenium.common.exceptions import NoSuchElementException
from robot.api import logger


class FabricGroup(BaseUseCase):
    def __init__(self, name=None, method_name='runTest', **kwargs):
        super(FabricGroup, self).__init__(name, method_name, **kwargs)
        self.current_browser = kwargs.get('current_browser')
        self.fg_name = kwargs.get('fg_name')
        self.admin_list = kwargs.get('admin_list', [])

    def create_fabric_group(self):
        logger.info('Start to create Fabric Group', False, True)
        driver = self.current_browser.instance._browser.current

        loading_window = LoadingWindow()
        infra_page = InfrastructurePage()
        fg_page = FabricGroupPage()

        self.assertTrue(infra_page.navigate_to_dest_page(
            self.current_browser, infra_page.btn_endpoints, infra_page.btn_dest_fabric_groups),
            'Failed to navigate to Fabric Group page.')

        fg_frame_url = 'https://vra-vip.vlab.local/vcac/VMPSAdmin/ViewEntAdmins.aspx'
        self.assertTrue(infra_page.navigate_to_iframe(
            self.current_browser, attribute_name='src', url_in_attribute=fg_frame_url),
            'Failed to switch to Fabric Group iframe.')

        logger.info('Navigated to Fabric Group page.')

        self.assertTrue(fg_page.btn_new_fg.exists(), 'Cannot find New button to create fg.')
        fg_page.btn_new_fg.click()
        fg_page.wait_for_loading_complete(3)

        self.assertTrue(fg_page.txt_fg_name.exists(), 'Cannot find Name textbox.')
        fg_page.txt_fg_name.set(self.fg_name)
        fg_page.wait_for_loading_complete(1)

        self.assertTrue(fg_page.txt_admin.exists(), 'Cannot find Fabric administrator textbox.')
        self.assertTrue(fg_page.btn_user_search.exists(), 'Cannot find search user button.')

        for user in self.admin_list:
            fg_page.txt_admin.set(user)
            fg_page.btn_user_search.click()
            loading_window.wait_loading_add_fg_page(self.current_browser)
            fg_page.wait_for_loading_complete(3)

            try:
                lbl_admin_user = driver.find_element_by_xpath('//td[text()="{0}"]'.format(user))
                lbl_admin_user.click()
                fg_page.wait_for_loading_complete(1)

            except NoSuchElementException:
                logger.error('Cannot find user {0}'.format(user))
                raise

        fg_page.wait_for_loading_complete(1)

        cr_checkbox_list = driver.find_elements_by_xpath('//input[@type="checkbox" and @autocomplete]')
        for cb in cr_checkbox_list:
            cb.click()

        fg_page.wait_for_loading_complete(1)
        self.assertTrue(fg_page.btn_ok.exists(), 'Cannot find OK button to submit.')
        fg_page.btn_ok.click()
        fg_page.wait_for_loading_complete(3)
        logger.info('Fabric Group submitted. Validating...', False, True)

        driver.implicitly_wait(10)
        error_labels = driver.find_elements_by_xpath('//li[@class="error"]')
        if len(error_labels) > 0:
            self.fail('Failed to create Fabric Group. Error message from vRA: {0}'.format(error_labels[0].text))
        else:
            logger.info('Fabric Group created.')

    def runTest(self):
        self.create_fabric_group()

from autosetup import Autosetup

autosetup = Autosetup()
autosetup.load_config('autosetup_config.yaml')


def before_prepare_tenant():
    autosetup.init_vra_util()


def test_prepare_tenant():
    autosetup.create_a_tenant()
    autosetup.create_an_ad()
    autosetup.assign_roles()


def before_config_tenant():
    autosetup.init_vro_util()
    autosetup.add_a_vra_host()
    autosetup.add_an_iaas_host()


def test_config_tenant():
    autosetup.create_machine_prefixes()
    autosetup.create_business_groups()
    autosetup.create_credentials()
    autosetup.create_endpoints()
    autosetup.update_vro_config()
    autosetup.create_a_fabric_group()


def after_config_tenant():
    autosetup.remove_a_vra_host()
    autosetup.remove_an_iaas_host()


def before_config_vipr():
    autosetup.init_vipr_util()


def test_config_vipr():
    autosetup.create_a_vipr_project()


def after_config_vipr():
    autosetup.close_vipr_session()


def __main__():

    before_prepare_tenant()
    test_prepare_tenant()

    before_config_tenant()
    test_config_tenant()
    after_config_tenant()

    before_config_vipr()
    test_config_vipr()
    after_config_vipr()


main = __main__

if __name__ == '__main__':
    __main__()

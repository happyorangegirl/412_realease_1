from ehc_e2e.workflow import BaseWorkflow


def __main__():
    import os
    _cd = os.path.dirname(os.path.realpath(__file__))
    _parent_dir = os.path.abspath(os.path.join(_cd, os.pardir))
    _global = os.path.join(_parent_dir, 'conf/generic.yaml')
    _wf = [
        os.path.join(_parent_dir, 'conf/test-extend-vcenter-relationship.config.yaml'),
    ]

    wf = BaseWorkflow()
    wf.apply_settings_from_files(_global, *_wf)
    wf.cloud_administrator_opens_browser()
    wf.cloud_administrator_login()

    wf.cloud_administrator_extends_vcenter_relationship()

    wf.cloud_administrator_logout()
    wf.cloud_administrator_closes_browser()
    wf.reset_settings()

main = __main__

if __name__ == '__main__':
    __main__()

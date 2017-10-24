import os
from ehc_e2e.scenario.basescenario import BaseScenario

if __name__ == '__main__':
    _cd = os.path.dirname(os.path.realpath(__file__))

    _parent_dir = os.path.abspath(os.path.join(_cd, os.pardir, os.pardir))
    _global = os.path.join(_parent_dir, 'conf\generic.yaml')

    _wf = [
        os.path.join(_parent_dir, 'test/test_data/test_scenario_conf/E2ESN-1-LC1S.config.yaml'),
        os.path.join(_parent_dir, 'test/test_data/test_scenario_conf/E2ESN-1-DR2S.config.yaml'),
        os.path.join(_parent_dir, 'test/test_data/test_scenario_conf/E2ESN-1-RP4VM.config.yaml')
    ]

    b = BaseScenario()
    b.apply_settings_for_scenario()
    # # operate LC1S
    b.prepare_workflow_data(_global, os.path.join(_parent_dir, 'test/test_data/test_scenario_conf/E2ESN-1-LC1S.config.yaml'))
    b.cloud_administrator_opens_browser()
    b.cloud_administrator_login()
    b.cloud_administrator_adds_site()
    b.update_scenario_context()
    b.prepare_workflow_data(_global, os.path.join(_parent_dir, 'test/test_data/test_scenario_conf/E2ESN-1-DR2S.config.yaml'))
    b.cloud_administrator_adds_site()
    b.update_scenario_context()
    b.merge_context()


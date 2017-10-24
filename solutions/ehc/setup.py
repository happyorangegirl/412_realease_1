desc = """
Automation test suites (containing AUCs and workflows) for Enterprise Hybrid Cloud (EHC)
"""
try:
    from setuptools import (setup, find_packages)
    kwargs = {
        'install_requires': [
            'robotframework >= 3.0',
        ],
        'packages': find_packages(
            exclude=(
                'ehc_e2e.tests',
                'ehc_e2e.tests.uimap',
            )
        ),
        'include_package_data': True,
        'test_suite': 'ehc_e2e.tests',
    }
except ImportError:
    print '[ERROR] package build failure.'

setup(
    name='ehc_e2e',
    version='1.0.0',
    description='EHC E2E Automation for Challenger',
    long_description=desc,
    url='http://www.emc.com',
    license='Apache License V2',
    author='HCE AIM Automation Team',
    author_email='HCESWAutomationQE@emc.com',
    platform='linux',
    **kwargs
)
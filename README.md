# Zebrunner pytest agent test repository
## Prerequisites
1. python 3.8+
2. pip
3. virtualenv
4. pytest
5. selenium standalone server to run web tests locally
## Installation guide
clone this repo
> git@github.com:shukal94/zebrunner_py_test.git
navigate to the repo root
> cd zebrunner_py_test/

**OPTIONAL** create and activate the virtual environment for this project
> python3 -m virtualenv dev && source dev/bin/activate

install all the dependencies, they are at `requirements.txt` file
> pip install -r requirements.txt
####NOTE: zebrunnerpy plugin in this file is 0.6, please - ensure you're using the latest version (https://pypi.org/project/zebrunnerpy/)
register the installed plugin in your project at `conftest.py`
```

from zebrunnerpy import connector_obj, PyTestZafiraListener

from src.common.logging_config import apply_initial_logging_configuration


pytest_plugins = ['zebrunnerpy.plugin']
is_zafira_plugged_in = True
connector_obj.pytest_listener = PyTestZafiraListener(connector_obj.state)
apply_initial_logging_configuration()


def pytest_configure(config):
    """
    Attaches wrapped hooks as plugin
    """
    config.pluginmanager.register(connector_obj.pytest_listener)

```
update your config `zafira_properties.ini` with the corresponding options
```
service_url = base URL of your Zebrunner tenant
zafira_enabled = True or False
access_token = refresh token you got from zebrunner user settings
job_name = any String (mocked yet, will add this capability soon)
artifact_expires_in_default_time = any Integer (mocked yet, will add this capability soon)
artifact_log_name = any String (mocked yet, will add this capability soon)
aws_screen_shot_bucket = any String (mocked yet, will add this capability soon)
s3_save_screenshots = any String (mocked yet, will add this capability soon)
zafira_project = any String (mocked yet, will add this capability soon)
```
define the test maintainers at `pytest.ini`
```
[pytest]
#custom pytest markers including test owners
markers=sshukalovich dmishin test1
```
####NOTE: sshukalovich dmishin test1 are real users for the test tenant
example
```
@pytest.mark.sshukalovich
    def test_passed(self):
        self.LOGGER.info('PASS')
        assert 1 == 1, 'is not as expected'
```
ensure you have pytest as the default testrunner on your IDE and working directory is the root of the project

start selenium server, the props and capabilities you can find at `gui_properties.ini`

That's it!
##USAGE
just run your tests
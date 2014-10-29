from distutils.core import setup

setup(
    name='home_automation',
    version='1.0',
    package_dir={
        'home_automation':'home-automation',
        'home_automation.base':'home-automation/base'
    },
    packages=['home_automation', 'home_automation.base'],
    requires=['xbee', 'xively']
)


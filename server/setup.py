from distutils.core import setup

setup(
    name='home_automation',
    version='1.0',
    package_dir={
        'home_automation':'home-automation',
        'home_automation.base_modules':'home-automation/base_modules'
    },
    packages=['home_automation', 'home_automation.base_modules'],
    requires=['xbee', 'xively']
)


from distutils.core import setup

setup(
    name='home_automation',
    version='1.0',
    description='Python modules to manage the home automation',
    author='Takashi Ando',
    author_email='dodo5522@gmail.com',
    url='http://qiita.com/dodo5522/items/63d1efee3f70b3d5f2f6',
    package_dir={
        'home_automation':'home-automation',
        'home_automation.base':'home-automation/base'
    },
    packages=['home_automation', 'home_automation.base'],
    requires=['xbee', 'xively']
)


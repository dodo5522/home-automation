#!/usr/bin/env python3
"""
 Server side code work on raspberry pi for my home automation.
 Editor     : Takashi Ando
 Version    : 1.0
"""
import os
import configparser
import logging

class Configuration(object):
    '''
    Read the configuration file.
    This class should be inherited by user class.
    The user class name will be section name automatically.
    '''
    def __init__(self, path_to_config='/etc/home-automation/setting.conf', log_level=logging.INFO):
        self._logger = logging.getLogger(name=type(self).__name__)
        self._logger.setLevel(log_level)

        self._config_data = configparser.ConfigParser()
        self._config_data.read(path_to_config)

    def read_config(self, option, value_type=str):
        '''
        read_config: option string -> value

        Return the value read from configuration file.
        If no section or option, this method returns None.
        '''
        section = type(self).__name__.lower()
        option = option.lower()

        if option is None:
            self._logger.debug('option is none.')
            return None
        if not self._config_data.has_section(section):
            self._logger.debug('{0} is none.'.format(section))
            return None
        if not self._config_data.has_option(section, option):
            self._logger.debug('{0} does not have {1}.'.format(section, option))
            return None

        value = self._config_data[section][option]
        return value_type(value)


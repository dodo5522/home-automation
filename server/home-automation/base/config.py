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
    def __init__(self, path_to_config, log_level=logging.INFO):
        self._logger = logging.getLogger(name=type(self).__name__)
        self._logger.setLevel(log_level)

        self._config_data = configparser.ConfigParser()
        self._config_data.read(path_to_config)

        if log_level == logging.DEBUG:
            for section in self._config_data.sections():
                if section != type(self).__name__.lower():
                    continue

                for option in self._config_data.options(section):
                    value = self._config_data[section][option]
                    self._logger.debug('{0}:{1}={2}'.format(section, option, value))

    def read_config(self, key, value_type=str, int_base=10):
        ''' Read the configuration with the specified key.
            This function returns the value with the specified data type.

        Args:
            key (str) : keyword to store the configuration on the file.
            value_type (type) : data type should be returned.
            int_base (int) : base to be returned if value_type is int.

        Returns:
            Data of string or int.
            If no section or key, this function returns None.
        '''
        section = type(self).__name__.lower()
        key = key.lower()

        if key is None:
            self._logger.debug('key "{0}" is none.'.format(key))
            return None
        if not self._config_data.has_section(section):
            self._logger.debug('section "{0}" is none.'.format(section))
            return None
        if not self._config_data.has_option(section, key):
            self._logger.debug('option "{0}" does not have key "{1}".'.format(section, key))
            return None

        value = self._config_data[section][key]

        if value_type == int:
            return value_type(value, int_base)
        else:
            return value_type(value)


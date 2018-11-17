import logging
import os
import xml.etree.ElementTree as Etree


class Config(object):
    def __init__(self):
        self.name = None
        self.version = None
        self.init_script = None
        self.start_script = None
        self.stop_script = None
        self.log_location = None
        self.result_location = None
        self.report_location = None

    @classmethod
    def load(cls, config_fname):
        def get_value(element):
            if element is None:
                return ""
            return element.text

        if not os.path.exists(config_fname):
            logging.error("config file not exists!")
            return None

        cfg = cls()
        et = Etree.parse(config_fname)
        root = et.getroot()
        """:type root: xml.etree.ElementTree.Element"""

        cfg.name = get_value(root.find('tool_name'))
        cfg.version = get_value(root.find('version'))
        cfg.log_location = get_value(root.find('./log/location'))
        cfg.result_location = get_value(root.find('./result/location'))
        cfg.report_location = get_value(root.find('./report/location'))

        return cfg

    def dump(self):
        logging.info("name: " + self.name)
        logging.info("log_location: " + self.log_location)
        logging.info("result_location: " + self.result_location)
        logging.info("report_location: " + self.report_location)


__config = None  # type: Config


def load():
    _config = Config.load('config.xml')


def get_name():
    return __config.name


def get_version():
    return __config.version


def get_log_location():
    return __config.log_location


def get_result_location():
    return __config.result_location


def get_report_location():
    return __config.report_location

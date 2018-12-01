import traceback

from py_common.py_modules.mako.template import Template
import logging


def make(report_info):
    HTML_TEMPLATE = 'report.mako'
    logging.info('make report')
    try:
        template = Template(filename=HTML_TEMPLATE, output_encoding='utf-8')
        html = template.render(**report_info)
        with open('report.html', 'w+') as f:
            f.write(html)
        logging.info('make report success')
    except Exception as e:
        logging.error('make report failed')
        traceback.print_exc()

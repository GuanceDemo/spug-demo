#!/usr/bin/env python
# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
"""Django's command-line utility for administrative tasks."""
import os
import sys
from ddtrace import tracer
import logging
import os
from configparser import ConfigParser

cf = ConfigParser()
cf.read("spug.conf")
# ddtrace环境变量
os.environ["DD_SERVICE"] = cf["ddtrace"]["dd_service"]   # 设置服务名
os.environ["DD_ENV"] =  cf["ddtrace"]["dd_env"]           # 设置环境名
os.environ["DD_VERSION"] = cf["ddtrace"]["dd_env"]          # 设置版本号
os.environ["DD_LOGS_INJECTION"] = cf["ddtrace"]["dd_logs_injection"]  # 开启log注入
os.environ["DD_REMOTE_CONFIGURATION_ENABLED"] = cf["ddtrace"]["dd_remote_configuration_enabled"]  # 开启log注入
os.environ["DD_AGENT_HOST"] = cf["ddtrace"]["dd_agent_host"]   #datakit host
os.environ["DD_AGENT_PORT"] = cf["ddtrace"]["dd_agent_port"]  #datakit port

# mysql环境变量
os.environ["MYSQL_DATABASE"] = cf["mysql"]["db_name"] 
os.environ["MYSQL_USER"] = cf["mysql"]["db_user"] 
os.environ["MYSQL_PASSWORD"] = cf["mysql"]["db_password"] 
os.environ["MYSQL_HOST"] = cf["mysql"]["db_host"] 
os.environ["MYSQL_PORT"] = cf["mysql"]["db_port"]

FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
          '- %(message)s')

logging.basicConfig(level=logging.INFO,format=FORMAT)

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spug.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
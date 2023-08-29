#!/bin/bash
# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
# start worker service

echo "export DD_SERVICE=python-spug" >> ~/.bashrc
echo "export DD_TAGS=project:mobie_sdk_demo,env:test,version:1.0" >> ~/.bashrc
#echo "export DD_AGENT_HOST=https://pe-dk.guance.space" >> ~/.bashrc
echo "export DD_AGENT_HOST=47.106.191.26" >> ~/.bashrc
echo "export DD_AGENT_PORT=9529" >> ~/.bashrc
echo "export DD_LOGS_INJECTION='true'" >> ~/.bashrc
echo "export DD_VERSION=1.1" >> ~/.bashrc
echo "export DD_REMOTE_CONFIGURATION_ENABLED='true'" >> ~/.bashrc

source ~/.bashrc


cd /data/spug/spug_api/
python3 manage.py updatedb
python3 manage.py user add -u admin -p admin -s -n admin

exec ddtrace-run python3 manage.py runserver 0.0.0.0:8000

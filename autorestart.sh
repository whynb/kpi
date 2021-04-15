#!/bin/bash
source ~/.bash_profile
/usr/bin/nohup /usr/local/bin/python3 ~/kpi/manage.py runserver 0.0.0.0:8001 >> /tmp/kpi.txt > /dev/null 2>&1 &

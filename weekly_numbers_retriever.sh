#!/bin/bash -e
cd /var/www/api.sms.et/
source api_env/bin/activate 
#exec 3>&1 4>&2
#trap 'exec 2>&4 1>&3' 0 1 2 3

today='date +%Y-%m-%d_%H:%M:%S'
echo $today
python ./numbers_retriever.py

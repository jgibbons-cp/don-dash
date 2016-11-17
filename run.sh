#!/bin/sh
source /home/core/.cloudpassage.yml

#/opt/cloudpassage/bin/cphalo --agent-key=$HALO_AGENT_KEY --tag=$SERVER_GROUP --server-label="don-dash" 2>&1 >/dev/null &

sleep 10
export AGENT_ID=`cat /opt/cloudpassage/data/id`

python -m flask run --host=0.0.0.0


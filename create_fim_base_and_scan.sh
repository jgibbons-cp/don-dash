#!/bin/sh
/opt/cloudpassage/bin/cphalo --agent-key=$HALO_AGENT_KEY --tag=$SERVER_GROUP --server-label="don-dash" 2>&1 >/dev/null &

echo "We'll sleep for 10s to give the agent a chance to authenticate"
sleep 10
export AGENT_ID=`cat /opt/cloudpassage/data/id`

python /app/create_fim_base_and_self_assess.py
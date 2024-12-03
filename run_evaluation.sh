#!/bin/bash

export WORK_DIR=/home/ehcho/code/AdaptiveADS
export CARLA_ROOT=${WORK_DIR}/carla
export CARLA_SERVER=${CARLA_ROOT}/CarlaUE4.sh
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla/dist/carla-0.9.10-py3.7-linux-x86_64.egg
export PYTHONPATH=$PYTHONPATH:${WORK_DIR}/scenario_runner
export PYTHONPATH=$PYTHONPATH:${WORK_DIR}/leaderboard
export PYTHONPATH=$PYTHONPATH:${WORK_DIR}/transfuser

export CHALLENGE_TRACK_CODENAME=SENSORS
export RESUME=1
export TEAM_CONFIG=${WORK_DIR}/model_ckpt

export AGENT="$1"
export CHECKPOINT_ENDPOINT=${WORK_DIR}/results/${AGENT}_longest6.json
export TEAM_AGENT=${WORK_DIR}/transfuser/${AGENT}_agent.py

export PORT="$2"

export ROUTE_NAME="$3"
export SCENARIO_NAME="$4"
export ROUTES=${WORK_DIR}/leaderboard/data/routes/${ROUTE_NAME}.xml
export SCENARIOS=${WORK_DIR}/leaderboard/data/scenarios/${SCENARIO_NAME}.json

python3 leaderboard/leaderboard/leaderboard_evaluator.py \
--port=${PORT} \
--routes=${ROUTES} \
--scenarios=${SCENARIOS}  \
--agent=${TEAM_AGENT} \
--agent-config=${TEAM_CONFIG} \
--track=${CHALLENGE_TRACK_CODENAME} \
--resume=${RESUME} \
--checkpoint=${CHECKPOINT_ENDPOINT}

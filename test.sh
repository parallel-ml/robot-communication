#!/bin/bash

python app.py --broker "mqtt://localhost" --label "ROBOT 1" --topics-publish robot_1 --topics-subscribe robot_2 robot_3 robot_4 robot_5 &
python app.py --broker "mqtt://localhost" --label "ROBOT 2" --topics-publish robot_2 --topics-subscribe robot_1 robot_3 robot_4 robot_5 &
python app.py --broker "mqtt://localhost" --label "ROBOT 3" --topics-publish robot_3 --topics-subscribe robot_1 robot_2 robot_4 robot_5 &
python app.py --broker "mqtt://localhost" --label "ROBOT 4" --topics-publish robot_4 --topics-subscribe robot_1 robot_2 robot_3 robot_5 &
python app.py --broker "mqtt://localhost" --label "ROBOT 5" --topics-publish robot_5 --topics-subscribe robot_1 robot_2 robot_3 robot_4 &

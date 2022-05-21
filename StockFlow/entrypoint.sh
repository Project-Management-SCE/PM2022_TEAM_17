#!/bin/bash

# THIS WILL CHECK IF IT GOT PORT VARIABLE FROM HEROKU
# IF NOT IT WILL SET DEFAULT PORT FOR YOU APPLICATION (you can choose anyport you like)

if [ -z "$PORT" ]
then
    #echo "\$PORT is empty"
    #DEFAULT PORT
    PORT=8000
fi



echo "Running on port $PORT"
# RUNSERVER ON PORT IT GETS FROM HEROKU OR THE DEFAULT PORT.
python manage.py runserver 0.0.0.0:$PORT
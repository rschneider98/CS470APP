#!/bin/sh
printf "Script to start the server"
printf "Database User: "
read db_user
printf "\n"

stty -echo
printf "Password: "
read db_pwd
stty echo
printf "\n"

stty -echo
printf "Flask Password (does not matter, but should have reasonable entropy): "
read FLASK_KEY
stty echo
printf "\n"

# start gunicorn
nohup python3 -m gunicorn -c gunicorn.config.py app.py:app &> server_log.out &

# wait five seconds and print the beginning of the logs to the user
printf "Started Server"
sleep 5
cat server_log.out

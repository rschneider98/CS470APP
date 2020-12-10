#!/bin/bash
echo "Script to start the server"
read -p "Database User: " db_user
export db_user

read -sp "Password: " db_pwd
export db_pwd
echo ""

read -sp "Flask Password (does not matter, but should have reasonable entropy): " FLASK_KEY
export FLASK_KEY
echo ""

# start gunicorn
nohup gunicorn -c gunicorn.config.py app:app&

# wait five seconds and print the beginning of the logs to the user
echo "Started Server"
sleep 5
cat nohup.out

ps -aux | grep gunicorn | awk 'BEGIN {ORS=" "; print "kill -9"} {print $2}' | sh
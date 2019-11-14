#!/bin/bash
######The following is not needed changed#################

#service memcached restart
PRODIR=$(pwd)
PRONAME=$(basename $PRODIR)


PIDFILE="$PRODIR/running/uwsgi.pid"
LOGFILE="$PRODIR/log/uwsgi.log"
SOCKFILE="$PRODIR/running/uwsgi.sock"

MODULE="$PRONAME.wsgi:application"

if [ -f $PIDFILE ]; then
    kill -INT `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

uwsgi --processes 8 --max-requests 10000 --master --chdir $PRODIR --daemonize $LOGFILE --module $MODULE\
      --socket $SOCKFILE --pidfile $PIDFILE --http-timeout 60000 --log-maxsize 50000000


# uwsgi --processes 8 --max-requests 10000 --master --chdir /alidata/DetectCenter/ --daemonize /alidata/DetectCenter/log/uwsgi.log --module DetectCenter.wsgi:application --socket /alidata/DetectCenter/running/uwsgi.sock --pidfile /alidata/DetectCenter/running/uwsgi.pid --http-timeout 60000 --log-maxsize 50000000
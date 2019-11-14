#!/bin/bash
######The following is not needed changed#################

#service memcached restart
PRODIR=$(pwd)
PRONAME=$(basename $PRODIR)


PIDFILE="$PRODIR/running/supervisord.pid"
LOGFILE="$PRODIR/log/supervisord.log"
SOCKFILE="$PRODIR/running/supervisord.sock"

CONFIG="$PRODIR/supervisord_celery.conf"

if [ -f $PIDFILE ]; then
    kill -INT `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

supervisord -c $CONFIG

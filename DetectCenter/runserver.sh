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
	ps --ppid `cat -- $PIDFILE`| awk '{if($1~/[0-9]+/) print $1}'| xargs kill -9
	kill -INT `cat -- $PIDFILE`
	
    rm -f $PIDFILE
fi
CPU_NUM=$(cat /proc/cpuinfo | grep processor | wc -l)
# CPU_NUM=3
#

echo `date +"%Y-%m-%d %H:%M:%S"` > $PRODIR/log/START_TIME.log

uwsgi --processes $CPU_NUM --max-requests 10000 --master --chdir $PRODIR --daemonize $LOGFILE --module $MODULE\
      --enable-threads --threads 5\
      --reload-on-as 1280 --reload-on-rss 960 --harakiri 1800 --socket-timeout 1800\
      --socket $SOCKFILE --pidfile $PIDFILE --http-timeout 600000 --log-maxsize 50000000 --buffer-size 100000000 --touch-reload $PIDFILE

# uwsgi --enable-threads --threads 5 --processes $CPU_NUM --max-requests 10000 --master --chdir $PRODIR --daemonize $LOGFILE --module $MODULE\
#       --http 0.0.0.0:9001 --pidfile $PIDFILE --http-timeout 60000 --log-maxsize 50000000 --buffer-size 100000000
#python bootup.py

# uwsgi --enable-threads --threads 5 --processes $CPU_NUM --max-requests 10000 --master --chdir $PRODIR --daemonize $LOGFILE --module $MODULE\
#       --reload-on-as 128 --reload-on-rss 96\
#       --socket $SOCKFILE --pidfile $PIDFILE --http-timeout 60000 --log-maxsize 50000000 --buffer-size 100000000 --touch-reload $PIDFILE

echo -e crashed, restart at `date +"%w %Y/%m/%d, %H:%M:%S"`  >> $PRODIR/log/RESTART.log

#--chmod-socket 666 --logfile-chmod 644 --py-autoreload 1 --uid www --gid www
#--logfile-chmod 666 --py-autoreload 1

## --gevent-monkey-patch

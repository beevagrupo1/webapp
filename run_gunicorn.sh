#!/bin/bash
NAME=”Druzi” # Name of the application
DJANGODIR=/home/ec2-user/proyectos/webapp # Django project directory
SOCKFILE=/home/ec2-user/proyectos/webapp/gunicorn.sock # we will communicte using this unix socket

USER=ec2-user # the user to run as
GROUP=ec2-user # the group to run as
NUM_WORKERS=4 # how many worker processes should Gunicorn spawn

MAX_REQUESTS=1 # reload the application server for each request
DJANGO_SETTINGS_MODULE=projectdruzi.settings # which settings file should Django use
DJANGO_WSGI_MODULE=projectdruzi.wsgi # WSGI module name

echo “Starting $NAME as `whoami`”

# Activate the virtual environment
cd $DJANGODIR
source venv/bin/activate

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn’t exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn

# Programs meant to be run under supervisor should not daemonize themselves (do not use –daemon)
exec venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application –n $NAME –w $NUM_WORKERS –-max-requests $MAX_REQUESTS --user=$USER --group=$GROUP --bind=unix:${SOCKFILE} --reload

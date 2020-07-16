#!/bin/sh

/etc/init.d/nginx start
uwsgi --ini /opt/techbrew/tb2_uwsgi.ini

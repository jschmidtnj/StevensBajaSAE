#!/bin/sh
#RUNS EVERY TIME THE APP STARTS

sudo mysql -u "root" < sql-startup.sql

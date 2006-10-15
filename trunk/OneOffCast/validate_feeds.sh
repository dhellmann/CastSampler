#!/bin/sh
#
# $Id$
#

BASE_URL=http://localhost:7000/cast/feed
ATOM_URL=$BASE_URL/atom/dhellmann/
RSS_URL=$BASE_URL/rss/dhellmann/

VALIDATOR_HOME=~/Devel/OneOffCast/feedvalidator

for URL in $ATOM_URL $RSS_URL
do
  echo $URL
  python $VALIDATOR_HOME/src/demo.py $URL
done

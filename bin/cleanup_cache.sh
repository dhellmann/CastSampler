#!/bin/sh
#
# $Id$
#
# Remove old files from the cache.
#

# How long do we let files stay in the cache?
CACHE_CLEANUP_DAYS=7

# Where is the cache?
CACHE_DIR=`(cd ../CastSampler; python -c "import prod_settings; print prod_settings.ONEOFFCAST_CACHE_DIR")`
if [ "$CACHE_DIR" = "" ]
then
	echo "Could not determine the cache directory!"
	exit 1
fi

# Cleanup
find $CACHE_DIR -type f -ctime $CACHE_CLEANUP_DAYS -exec rm -f {} \;

#!/bin/sh
#
# $Id$
#
# Do a database dump for the backup
#
pg_dump \
	--format=p \
	--insert \
	-U castsampler \
	-h localhost \
	--file=/home/castsampler/Backup/castsampler_backup.sql \
	castsampler

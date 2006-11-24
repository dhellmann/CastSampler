#!/bin/sh
#
# $Id$
#
# Create the CSS file from the input.
#
# #664D22; dark brown
# #9F7E32; light brown
# #00528E; dark blue
# #0D83D1; light blue
# #eeeeee; light grey
# #d0dab0; light beige
#

IN=static/css/site_in.css
OUT=static/css/site.css

cat $IN \
	| sed 's/DARK1/#664D22/g' \
	| sed 's/LIGHT1/#9F7E32/g' \
	| sed 's/DARK2/#664D22/g' \
	| sed 's/LIGHT2/#9F7E32/g' \
	| sed 's/LIGHT3/#D0DAB0/g' \
	> $OUT


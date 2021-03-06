#!/usr/bin/env python
#
# $Id$
#
# Copyright 2006 Doug Hellmann.
#
#
#                         All Rights Reserved
#
# Permission to use, copy, modify, and distribute this software and
# its documentation for any purpose and without fee is hereby
# granted, provided that the above copyright notice appear in all
# copies and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of Doug
# Hellmann not be used in advertising or publicity pertaining to
# distribution of the software without specific, written prior
# permission.
#
# DOUG HELLMANN DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN
# NO EVENT SHALL DOUG HELLMANN BE LIABLE FOR ANY SPECIAL, INDIRECT OR
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

"""Cache management for downloaded podcast feeds.

"""

#
# Import system modules
#
from django.conf import settings
import logging
import md5
import os
try:
    import cPickle as pickle
except:
    import pickle
import sys
import time

#
# Import Local modules
#
from oneoffcast import feedparser


#
# Module
#

# Our logger
logger = logging.getLogger('oneoffcast.download_cache')

# How long do we want contents of the cache to live?
CACHE_TTL_SECS = getattr(settings, 'ONEOFFCAST_CACHE_TTL_SECS', 60*5)

# Where is the cache?
CACHE_DIR = getattr(settings, 'ONEOFFCAST_CACHE_DIR', '/tmp/oneoffcast/cache')


def retrieve_feed(feed_url):
    """Retrieve the parsed feed, either from the cache or the web.

    The cache contents are pickles containing the parsed results of
    the feed.  The cache is updated if the modification time on the
    cache file is older than ONEOFFCAST_CACHE_TTL_SECS and the feed
    contents have actually been updated.
    """
    #
    # Compute an md5 hash of the feed to use as the filename
    #
    m = md5.new()
    m.update(feed_url)
    feed_hash = m.hexdigest()
    cache_file = os.path.join(CACHE_DIR, feed_hash)

    logger.debug('URL: %s', feed_url)
    logger.debug('  TTL: %s', CACHE_TTL_SECS)
    logger.debug('  FILE: %s', cache_file)

    #
    # Initialize some fetch arguments
    #
    modified = None
    etag = None
    need_to_fetch = False
    
    #
    # Look for the data in the cache
    #
    now = time.time()
    logger.debug('  now: %s', now)
    try:
        #
        # Start by trying to load data from the cache.
        # If we cannot, we get an IOError, which
        # we handle by fetching the data.
        #
        f = open(cache_file, 'rb')
        try:
            logger.debug('  Found cache file')
            try:
                cached_result = pickle.load(f)
                logger.debug('  Read cache file')
            except Exception, err:
                logger.debug('  Could not read cache file %s', err)
                cached_result = None
        finally:
            f.close()

        #
        # Remember the modified and etag values from
        # the feed so we can send them to the feedparser
        # below if we end up repulling the feed.
        #
        try:
            modified = cached_result.modified
        except AttributeError:
            pass
        try:
            etag = cached_result.etag
        except AttributeError:
            pass
        logger.debug('  cache modified: %s', str(modified))
        logger.debug('  cache etag: %s', etag)
            
        #
        # Next we look at the modification time on
        # the cache file to see if it is out of date.
        #
        statinfo = os.stat(cache_file)
        cache_mtime = statinfo.st_mtime
        cache_age = now - cache_mtime

        logger.debug('  cache_mtime: %s', str(cache_mtime))
        logger.debug('  cache_age: %s', cache_age)
            
        if cache_age > CACHE_TTL_SECS:
            need_to_fetch = True
            
        # Now look at the contents of the file.  If there was an
        # error, we should always try to fetch again.
        try:
            if cached_result.bozo_exception:
                logger.debug('  cache includes error: %s', str(cached_result.bozo_exception))
                need_to_fetch = True
        except AttributeError:
            pass

    except (OSError, IOError):
        logger.debug('  No cache file')
        need_to_fetch = True
        cached_result = None

    #
    # Now, do we need to update the cache?
    #
    if need_to_fetch:
        logger.debug('  fetching')
        try:
            parsed_result = feedparser.parse(feed_url,
                                             agent='CastSampler.com',
                                             modified=modified,
                                             etag=etag,
                                             )
        except Exception, err:
            logger.debug('  ERROR: feedparser.parse raised %s', err)
            raise
        else:
            logger.debug('  done fetching')

        #
        # Figure out if we got new data
        #
        try:
            status = parsed_result.status
        except AttributeError:
            status = None
        if status == 304:
            #
            # No new data, but we need to update the mtime
            # on the cache file so we do not repull on
            # every access now.  We rewrite the *CACHED*
            # results to the cache file.
            #
            logger.debug('  updating cache mtime')
            f = open(cache_file, 'wb')
            try:
                pickle.dump(cached_result, f)
            finally:
                f.close()
            
        else:
            #
            # We found new contents, so write them
            # to the cache file.
            #
            logger.debug('  updating cache contents')
            cache_ok = True
            try:
                f = open(cache_file, 'wb')
            except IOError:
                # Cannot create the cache.
                logger.debug('Could not write cache to %s' % cache_file)
                cache_ok = False
            else:
                try:
                    try:
                        pickle.dump(parsed_result, f)
                    except Exception, err:
                        logger.debug('Error writing cache: %s' % str(err))
                        cache_ok = False
                finally:
                    f.close()

            if not cache_ok:
                os.unlink(cache_file)

            #
            # Now that we have written those results to the cache,
            # we can call them the cached_result.  That makes
            # returning from this function easier.
            #
            cached_result = parsed_result

    return cached_result
    

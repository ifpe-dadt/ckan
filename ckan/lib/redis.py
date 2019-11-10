# encoding: utf-8

u'''
Redis utilities.

.. versionadded:: 2.7
'''
import logging

from redis import ConnectionPool, Redis

from ckan.common import config


log = logging.getLogger(__name__)

REDIS_URL_SETTING_NAME = u'ckan.redis.url'

REDIS_URL_DEFAULT_VALUE = u'redis://localhost:6379/0'

# Redis connection pool. Do not use this directly, use ``connect_to_redis``
# instead.
_connection_pool = None


def connect_to_redis():
    u'''
    (Lazily) connect to Redis.

    The connection is set up but not actually established. The latter
    happens automatically once the connection is used.

    :returns: A lazy Redis connection.
    :rtype: ``redis.Redis``

    .. seealso:: :py:func:`is_redis_available`
    '''
    global _connection_pool
    if _connection_pool is None:
        url = config.get(REDIS_URL_SETTING_NAME, REDIS_URL_DEFAULT_VALUE)
        log.debug(u'Using Redis at {}'.format(url))
        _connection_pool = ConnectionPool.from_url(url)
    return Redis(connection_pool=_connection_pool)


def is_redis_available():
    u'''
    Check whether Redis is available.

    :returns: The availability of Redis.
    :rtype: bool

    .. seealso:: :py:func:`connect_to_redis`
    '''
    redis_conn = connect_to_redis()
    try:
        return redis_conn.ping()
    except Exception:
        log.exception(u'Redis is not available')
        return False

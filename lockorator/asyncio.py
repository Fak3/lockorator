import asyncio
from functools import wraps
from weakref import WeakValueDictionary

from sniffio import current_async_library

try:
    import trio
except ImportError:
    pass

    
locks = WeakValueDictionary()


class lock_or_exit:
    """
    Decorator. Before decorated function starts, try to acquire lock with 
    specified identifier. If lock is acquired successfully, proceed executing
    the function. Otherwise, return immediately.
    The `key` argument can contain templated string, wich will be rendered
    with args and kwargs, passed to the function.

    Example:

    >>> @lock_or_exit('lock_work_{}')
    >>> async def workwork(x):
    >>>     pass
    >>>
    >>> await workwork(3)  # Will try to acquire lock 'lock_work_3'

    """
    def __init__(self, id=None):
        """ Initalize decorator. """
        self.id = id
        
    def __call__(self, f):
        """ Decorate the function. """
        
        @wraps(f)
        async def wrapped(*args, **kw):
            if self.id:
                id = self.id.format(*args, **kw)
            else:
                id = f.__name__
            
            if current_async_library() == 'trio':
                lock = locks.setdefault(id, trio.Lock())
            else:
                lock = locks.setdefault(id, asyncio.Lock())
        
            if lock.locked():
                return
            
            async with lock:
                return await f(*args, **kw)
            
        return wrapped

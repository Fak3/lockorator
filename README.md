This package provides decorators that will try to acquire lock before calling decorated
function.

## Installation

```bash
pip install lockorator
```

## Usage

This package provides two flavours of lock decorators: redis and asyncio.
Both flavours have the same api.

Package `lockorator.asyncio` provides asyncio lock decorators, also compatible with `trio`.

Package `lockorator.redis` provides redis lock decorators.

To use redis locks, set `LOCKORATOR_REDIS_URL` in your environment:

```
export LOCKORATOR_REDIS_URL="redis://localhost:6379"
```

### API

#### lock_or_exit

Decorator. Before decorated function starts, try to acquire lock
with specified identifier. If lock is acquired successfully, proceed executing
the function. Otherwise, return immediately.
The `id` argument can contain templated string, wich will be rendered
with args and kwargs, passed to the function.

Example:

```python
from lockorator.asyncio import lock_or_exit

@lock_or_exit('lock_work_{}')
def workwork(x):
    pass

workwork(3)  # Will try to acquire lock 'lock_work_3'
```

#### lock_wait

Decorator. Before decorated function starts, try to acquire lock
with specified identifier, waiting for `waittime` seconds if needed. If lock is
acquired successfully, proceed executing the function. Otherwise, raise
`lockorator.TimeoutError`.
The `id` argument can contain templated string, wich will be rendered
with args and kwargs, passed to the function.

Example:

```python
from lockorator.redis import lock_wait

@lock_wait('lock_work_{}', waittime=4)
def workwork(x):
    pass

workwork(3)  # Will try to acquire lock 'lock_work_3' for 4 seconds
```

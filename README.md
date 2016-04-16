# redis_proxy
Proxy that implements Redis clustering

Pure python3, no external deps.

# Usage
1. Add your Redis servers to `SERVERS` in `settings.py`.
2. run `python redis_proxy.async_server.py`.
3. Point your Redis client to the specified `PROXY_HOST` and `PROXY_PORT` specified in `settings.py`.


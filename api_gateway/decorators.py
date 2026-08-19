import functools
import os

import redis.asyncio as redis
from fastapi import HTTPException
from jose import JWTError, jwt

# Secret Key
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# init Redis for Rate Limiting
REDIS_URL = os.getenv("REDIS_URL")
redis_client = redis.from_url(REDIS_URL, decode_response=True)


# verify_token
def verify_token(func):
    @functools.wraps(func)
    async def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token is invalid or expired")

        token = auth_header.split(" ")[1]

        try:
            # decode JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            # payload -> state
            request.state.user = payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Token is invalid or expired")

        return await func(request, *args, **kwargs)

    return wrapper


# require_role(role)
def require_role(role: str):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(request, *args, **kwargs):
            user = getattr(request.state, "user", None)

            if not user:
                raise HTTPException(status_code=401, detail="Authentication required")

            user_role = user.get("role", "")

            if user_role.upper() != role.upper() and user_role.upper() != "ADMIN":
                raise HTTPException(
                    status_code=403, detail="Forbidden: Insufficient role"
                )

            return await func(request, *args, **kwargs)

        return wrapper

    return decorator


# rate_limit(limit, window)
def rate_limit(limit: int, window: int):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(request, *args, **kwargs):
            ip = request.client.host
            key = f"rate_limit:{ip}"

            # Redis +
            current_count = await redis_client.incr(key)

            # If first request
            if current_count == 1:
                await redis_client.expire(key, window)

            if current_count > limit:
                raise HTTPException(status_code=429, detail="Rate limit exceeded")

            return await func(*args, **kwargs)

        return decorator

    return decorator

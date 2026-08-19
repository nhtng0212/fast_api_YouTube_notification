import logging
import time
from uuid import uuid4

from fastapi import HTTPException

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class RequestTracer:
    def __init__(self, request):
        self.start_time = 0
        self.trace_id = str(uuid4())
        self.request = request
        self.error_response = None

    async def __aenter__(self):
        self.start_time = time.perf_counter()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        execution_time = time.perf_counter() - self.start_time

        if exc_type is not None:
            logger.error(
                f"Trace: [{self.trace_id}] | t: {execution_time:.4f}s | Error: {exc_val}"
            )

            raise HTTPException(
                status_code=500,
                detail={"error": "Internal Server Error", "trace_id": self.trace_id},
            )

        logger.info(
            f"Trace: [{self.trace_id}] | t: {(time.perf_counter() - self.  start_time)}s"
        )

        return False

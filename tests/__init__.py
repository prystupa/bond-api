"""bond-async unit tests."""

from datetime import datetime
import asyncio
import time


def mock_time_changed(loop: asyncio.AbstractEventLoop, datetime_: datetime) -> None:
    """Call events in the future."""
    for task in list(loop._scheduled):
        if not isinstance(task, asyncio.TimerHandle):
            continue
        if task.cancelled():
            continue

        mock_seconds_into_future = datetime_.timestamp() - time.time()
        future_seconds = task.when() - loop.time()

        if mock_seconds_into_future >= future_seconds:
            task._run()
            task.cancel()

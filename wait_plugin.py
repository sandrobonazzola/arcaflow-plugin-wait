#!/usr/bin/env python3

import signal
import sys
import time
import typing
from dataclasses import dataclass, field
from threading import Event

from arcaflow_plugin_sdk import plugin, validation


@dataclass
class InputParams:
    seconds: typing.Annotated[float, validation.min(0.0)] = field(
       metadata={
           "id": "seconds",
           "name": "seconds",
           "description": "number of seconds to wait as a floating point "
                          "number for subsecond precision."
       }
    )


@dataclass
class SuccessOutput:
    """
    This is the output data structure for the success case.
    """
    message: str
    actual_wait_seconds: float


@dataclass
class ErrorOutput:
    """
    This is the output data structure in the error  case.
    """
    error: str
    actual_wait_seconds: float


exit = Event()
finished_early = False


@plugin.step(
    id="wait",
    name="Wait",
    description="Waits for the given amount of time",
    outputs={"success": SuccessOutput, "error": ErrorOutput},
)
def wait(
    params: InputParams
) -> typing.Tuple[str, typing.Union[SuccessOutput, ErrorOutput]]:
    """
    :param params:

    :return: the string identifying which output it is,
             as well the output structure
    """
    start_time = time.time()
    exit.wait(params.seconds)
    if finished_early:
        actual_time = time.time() - start_time
        return "cancelled_early", ErrorOutput(
            "Aborted {:0.2f} seconds after being scheduled to wait for {}"
            " seconds.".format(actual_time, params.seconds),
            actual_time
        )
    else:
        actual_time = time.time() - start_time
        return "success", SuccessOutput(
            "Waited {:0.2f} seconds after being scheduled to wait for {}"
            " seconds.".format(actual_time, params.seconds),
            actual_time
        )


def exit_early(*args):
    global finished_early
    finished_early = True
    exit.set()
    time.sleep(0.5)


if __name__ == "__main__":
    for sig in ('TERM', 'HUP', 'INT'):
        signal.signal(getattr(signal, 'SIG'+sig), exit_early)

    sys.exit(plugin.run(plugin.build_schema(
        wait,
    )))

#!/usr/bin/env python3

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


class WaitStep:

    @plugin.step(
        id="wait",
        name="Wait",
        description="Waits for the given amount of time",
        outputs={
            "success": SuccessOutput,
            "error": ErrorOutput,
        },
    )
    def wait(
        self,
        params: InputParams,
    ) -> typing.Tuple[str, typing.Union[SuccessOutput, ErrorOutput]]:
        """
        :param params:

        :return: the string identifying which output it is,
                as well the output structure
        """
        start_time = time.time()
        self.exit.wait(params.seconds)
        actual_time = time.time() - start_time
        return "success", SuccessOutput(
            "Waited {:0.2f} seconds after being scheduled to wait for {}"
            " seconds.".format(actual_time, params.seconds),
            actual_time
        )


if __name__ == "__main__":
    sys.exit(plugin.run(plugin.build_schema(
        WaitStep.wait,
    )))

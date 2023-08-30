#!/usr/bin/env python3

import sys
import time
import typing
from dataclasses import dataclass, field
from threading import Event

from arcaflow_plugin_sdk import plugin, validation, predefined_schemas


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
    exit = Event()
    finished_early = False

    @plugin.signal_handler(
        id=predefined_schemas.cancel_signal_schema.id,
        name=predefined_schemas.cancel_signal_schema.display.name,
        description=predefined_schemas.cancel_signal_schema.display.
        description,
        icon=predefined_schemas.cancel_signal_schema.display.icon,
    )
    def cancel_step(self, input: predefined_schemas.cancelInput):
        # First, let it know that this is the reason it's exiting.
        self.finished_early = True
        # Now signal to exit.
        self.exit.set()

    @plugin.step_with_signals(
        id="wait",
        name="Wait",
        description="Waits for the given amount of time",
        outputs={"success": SuccessOutput, "error": ErrorOutput},
        signal_handler_method_names=["cancel_step"],
        signal_emitters=[],
        step_object_constructor=lambda: WaitStep(),
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
        if self.finished_early:
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


if __name__ == "__main__":
    sys.exit(plugin.run(plugin.build_schema(
        WaitStep.wait,
    )))

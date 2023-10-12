#!/usr/bin/env python3
import unittest

from arcaflow_plugin_sdk import plugin

import time
import arcaflow_plugin_wait

WAIT_TIME = 0.1
SKIPPED_WAIT_TIME = 1.0
PREMATURE_TIME = 0.05


class WaitTest(unittest.TestCase):
    @staticmethod
    def test_serialization():
        plugin.test_object_serialization(
            arcaflow_plugin_wait.InputParams(
                WAIT_TIME
            )
        )

        plugin.test_object_serialization(
            arcaflow_plugin_wait.SuccessOutput(
                "Waited {:0.2f} seconds after being scheduled to wait for"
                " {} seconds.".format(WAIT_TIME, WAIT_TIME),
                actual_wait_seconds=WAIT_TIME
            )
        )

        plugin.test_object_serialization(
            arcaflow_plugin_wait.ErrorOutput(
                error="Aborted {:0.2f} seconds after being scheduled to wait"
                " for {} seconds.".format(PREMATURE_TIME, WAIT_TIME),
                actual_wait_seconds=PREMATURE_TIME
            )
        )

    def test_functional(self):
        # Test simple wait
        input_params = arcaflow_plugin_wait.InputParams(
            seconds=WAIT_TIME
        )
        wait_step = arcaflow_plugin_wait.WaitStep()
        output_id, output_data = wait_step.wait(input_params)

        self.assertEqual("success", output_id)
        self.assertEqual(
            output_data.message,
            "Waited {:0.2f} seconds after being scheduled to wait for {}"
            " seconds.".format(output_data.actual_wait_seconds, WAIT_TIME)
        )


if __name__ == '__main__':
    unittest.main()

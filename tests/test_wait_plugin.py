#!/usr/bin/env python3
import unittest

from arcaflow_plugin_sdk import plugin

import wait_plugin

WAIT_TIME = 0.1
PREMATURE_TIME = 0.05


class WaitTest(unittest.TestCase):
    @staticmethod
    def test_serialization():
        plugin.test_object_serialization(
            wait_plugin.InputParams(
                WAIT_TIME
            )
        )

        plugin.test_object_serialization(
            wait_plugin.SuccessOutput(
                "Waited {:0.2f} seconds after being scheduled to wait for {} seconds."
                    .format(WAIT_TIME, WAIT_TIME),
                actual_wait_seconds=WAIT_TIME
            )
        )

        plugin.test_object_serialization(
            wait_plugin.ErrorOutput(
                error="Aborted {:0.2f} seconds after being scheduled to wait for {} seconds."
                    .format(PREMATURE_TIME, WAIT_TIME),
                actual_wait_seconds=PREMATURE_TIME
            )
        )

    def test_functional(self):
        input_params = wait_plugin.InputParams(
            seconds=WAIT_TIME
        )

        output_id, output_data = wait_plugin.wait(input_params)

        self.assertEqual("success", output_id)
        self.assertEqual(
            output_data.message,
            "Waited {:0.2f} seconds after being scheduled to wait for {} seconds."
                .format(output_data.actual_wait_seconds, WAIT_TIME)
        )


if __name__ == '__main__':
    unittest.main()

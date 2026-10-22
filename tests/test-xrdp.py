#!/usr/bin/env python3

import argparse
import socket
import sys
import time
import unittest

START_TIMEOUT = 120  # seconds to wait for the container to be usable
XRDP_PORT = 3389


def wait_for_container(container, timeout=START_TIMEOUT):
    print("Waiting for the container to be usable...")
    deadline = time.time() + timeout
    while True:
        container.reload()
        state = container.attrs.get("State", {})
        status = state.get("Status")
        if status in ("exited", "dead"):
            logs = container.logs().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"The container stopped before it was usable (status={status}).\n{logs}"
            )
        if status == "running":
            try:
                if container.exec_run(["true"]).exit_code == 0:
                    # The server needs a moment to start.
                    if container.exec_run(["sh", "-c", "pgrep -x xrdp"]).exit_code == 0:
                        print("The container is usable.")
                        return
            except Exception:
                pass
        if time.time() > deadline:
            logs = container.logs().decode("utf-8", errors="replace")
            raise RuntimeError(f"The container was not usable within {timeout}s.\n{logs}")
        time.sleep(2)


def run_tests(image_name):
    import docker
    import requests

    class TestXrdp(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            cls.client = docker.from_env()
            cls.container = cls.client.containers.run(
                image_name,
                detach=True,
                ports={f"{XRDP_PORT}": f"{XRDP_PORT}"},
            )
            wait_for_container(cls.container)

        @classmethod
        def tearDownClass(cls):
            cls.container.stop()
            cls.container.remove()

        def test_xrdp_is_running(self):
            print("Running the xrdp test...")
            result = self.container.exec_run(["sh", "-c", "pgrep -x xrdp"])
            self.assertEqual(result.exit_code, 0, "The xrdp server does not run")
            print("Xrdp test passed.")

        def test_the_port_is_open(self):
            print("Running the port test...")
            # The server needs a moment to open the port.
            deadline = time.time() + 60
            last_error = None
            while True:
                try:
                    with socket.create_connection(("127.0.0.1", XRDP_PORT), timeout=5):
                        print("Port test passed.")
                        return
                except OSError as error:
                    last_error = error
                if time.time() > deadline:
                    self.fail(f"The xrdp port is not open: {last_error}")
                time.sleep(2)

    print(f"Starting the container from the image '{image_name}'...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestXrdp)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the tests for the xrdp image.")
    parser.add_argument(
        "--image",
        type=str,
        default="satishweb/docker-xrdp:ci",
        help="The image that is tested",
    )
    args = parser.parse_args()

    run_tests(args.image)

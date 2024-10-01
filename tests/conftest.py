# Copyright 2024 DataRobot, Inc. and its affiliates.
# All rights reserved.
# DataRobot, Inc.
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
# Released under the terms of DataRobot Tool and Utility Agreement.

# mypy: ignore-errors

import os
import subprocess
import time
import datarobot as dr
import uuid
import pandas as pd
import pytest
import logging
from dotenv import dotenv_values
from datarobot_predict.deployment import predict

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def stack_name():
    short_uuid = str(uuid.uuid4())[:5]
    return f"test-stack-{short_uuid}"


@pytest.fixture(scope="session")
def session_env_vars():
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    env_vars = dotenv_values(env_file)
    os.environ.update(env_vars)
    return None


def run_command(command):
    print(f"Running command: {' '.join(command)}")
    proc = subprocess.run(command, check=False, text=True, capture_output=True)
    cmd = " ".join(command)
    if proc.returncode:
        msg = f"'{cmd}' exited {proc.returncode}"
        logger.warning(msg)
        msg = f"'{cmd}' STDOUT:\n{proc.stdout}"
        logger.warning(msg)
        msg = f"'{cmd}' STDERR:\n{proc.stderr}"
        logger.warning(msg)
    return proc


@pytest.fixture(scope="function")
def pulumi_up(stack_name, session_env_vars):
    logger.info(f"Running {stack_name} with {session_env_vars}")
    run_command(["pulumi", "stack", "init", stack_name, "--non-interactive"])
    yield

    run_command(["pulumi", "down", "-y", "--non-interactive"])
    run_command(["pulumi", "stack", "rm", stack_name, "-y", "--non-interactive"])


def run_pulumi(path, stack_name):
    proc = run_command(
        ["pulumi", "up", "-s", stack_name, "-y", "--non-interactive", "--cwd", path]
    )
    print(proc)
    try:
        if proc.returncode:
            raise RuntimeError(f"`pulumi up` failed for {stack_name}")
        yield
    except Exception as e:
        raise e


@pytest.fixture
def dr_client(session_env_vars):
    return dr.Client()


def predict_with_retry(
    deployment, data_frame, max_wait_seconds=300, retry_interval_seconds=5
):
    start_time = time.time()
    while True:
        try:
            prediction = predict(deployment, data_frame=data_frame)
            return prediction
        except dr.errors.ServerError as e:
            if "Inference server is starting" in str(e):
                elapsed_time = time.time() - start_time
                if elapsed_time > max_wait_seconds:
                    raise TimeoutError(
                        f"Server did not start within {max_wait_seconds} seconds"
                    )
                logger.info(
                    f"Server is starting. Retrying in {retry_interval_seconds} seconds..."
                )
                time.sleep(retry_interval_seconds)
            else:
                # If it's a different ServerError, re-raise it
                raise


@pytest.fixture
def make_prediction(dr_client):
    def predict_function(input_json, deployment_id):
        deployment = dr.Deployment.get(deployment_id)
        predict_df = pd.DataFrame(input_json)
        while True:
            try:
                prediction = predict_with_retry(
                    deployment, data_frame=predict_df
                ).dataframe
                break
            except dr.errors.ServerError as e:
                if "Inference server is starting" in str(e):
                    continue

        return prediction.to_dict(orient="records")[0]

    return predict_function


@pytest.fixture
def custom_py():
    return """\
def load_model(input_dir):
    return ''

def score(data, model, **kwargs):
    import pandas as pd
    preds = pd.DataFrame([42 for _ in range(data.shape[0])], columns=["Predictions"])
    return preds
"""


@pytest.fixture
def folder_path(tmp_path, custom_py):
    dir = tmp_path / "custom_model"
    dir.mkdir()
    p = dir / "custom.py"
    p.write_text(custom_py)
    return str(dir.resolve())


@pytest.fixture
def another_folder_path(tmp_path, custom_py):
    dir = tmp_path / "another_custom_model"
    dir.mkdir()
    p = dir / "custom.py"
    p.write_text(custom_py)
    return str(dir.resolve())

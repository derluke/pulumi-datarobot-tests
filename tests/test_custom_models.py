#
# Copyright 2024 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
# https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf

import json
import pathlib
from subprocess import CompletedProcess
import tempfile
from typing import Optional
import zipfile
import datarobot as dr

from .conftest import run_command


def run_pulumi_up(
    stack_name: str, cwd: str, extra: Optional[list[str]] = None
) -> CompletedProcess[str]:
    return run_command(
        [
            "pulumi",
            "up",
            "-s",
            stack_name,
            "-y",
            "--cwd",
            cwd,
            "--non-interactive",
        ]
        + (extra or [])
    )


def run_set_config(stack_name, run, cwd) -> CompletedProcess[str]:
    return run_command(
        [
            "pulumi",
            "-s",
            stack_name,
            "--cwd",
            cwd,
            "config",
            "set",
            "run",
            f"{run}",
        ]
    )


def run_get_output(stack_name, cwd) -> CompletedProcess[str]:
    return run_command(
        [
            "pulumi",
            "-s",
            stack_name,
            "--cwd",
            cwd,
            "stack",
            "output",
            "--show-secrets",
            "-j",
        ]
    )


def test_custom_model_with_deployment(pulumi_up, stack_name):
    cwd = "tests/custom_model"
    run = 1
    cm_versions = {}
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)

    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name)
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    custom_model_id = json.loads(output.stdout)["custom_model_id"]
    custom_model_version_id = json.loads(output.stdout)["custom_model_version_id"]
    cm_versions[run] = {
        "custom_model_id": custom_model_id,
        "custom_model_version_id": custom_model_version_id,
    }

    run = 2
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)
    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name, extra=["--expect-no-changes"])
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    custom_model_id = json.loads(output.stdout)["custom_model_id"]
    custom_model_version_id = json.loads(output.stdout)["custom_model_version_id"]
    cm_versions[run] = {
        "custom_model_id": custom_model_id,
        "custom_model_version_id": custom_model_version_id,
    }

    assert cm_versions[1]["custom_model_id"] == cm_versions[2]["custom_model_id"]
    assert (
        cm_versions[1]["custom_model_version_id"]
        == cm_versions[2]["custom_model_version_id"]
    )
    run = 3
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)
    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name)
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    custom_model_id = json.loads(output.stdout)["custom_model_id"]
    custom_model_version_id = json.loads(output.stdout)["custom_model_version_id"]
    cm_versions[run] = {
        "custom_model_id": custom_model_id,
        "custom_model_version_id": custom_model_version_id,
    }
    assert cm_versions[2]["custom_model_id"] == cm_versions[3]["custom_model_id"]
    assert (
        cm_versions[2]["custom_model_version_id"]
        != cm_versions[3]["custom_model_version_id"]
    )
    cm = dr.CustomInferenceModel.get(custom_model_id)
    run = 4
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)
    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name)
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    custom_model_id = json.loads(output.stdout)["custom_model_id"]
    custom_model_version_id = json.loads(output.stdout)["custom_model_version_id"]
    cm_versions[run] = {
        "custom_model_id": custom_model_id,
        "custom_model_version_id": custom_model_version_id,
    }
    assert cm_versions[3]["custom_model_id"] == cm_versions[4]["custom_model_id"]
    assert (
        cm_versions[3]["custom_model_version_id"]
        != cm_versions[4]["custom_model_version_id"]
    )

    cm = dr.CustomInferenceModel.get(custom_model_id)
    assert len(cm.latest_version.runtime_parameters) > 0
    assert cm.latest_version.runtime_parameters[0].field_name == "pytest_credential"

    run = 5
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)
    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name)
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    custom_model_id = json.loads(output.stdout)["custom_model_id"]
    custom_model_version_id = json.loads(output.stdout)["custom_model_version_id"]
    cm_versions[run] = {
        "custom_model_id": custom_model_id,
        "custom_model_version_id": custom_model_version_id,
    }
    assert cm_versions[4]["custom_model_id"] == cm_versions[5]["custom_model_id"]
    assert (
        cm_versions[4]["custom_model_version_id"]
        == cm_versions[5]["custom_model_version_id"]
    )
    run = 6
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)
    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name)
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    custom_model_id = json.loads(output.stdout)["custom_model_id"]
    custom_model_version_id = json.loads(output.stdout)["custom_model_version_id"]
    cm_versions[run] = {
        "custom_model_id": custom_model_id,
        "custom_model_version_id": custom_model_version_id,
    }
    assert cm_versions[5]["custom_model_id"] == cm_versions[6]["custom_model_id"]
    assert (
        cm_versions[5]["custom_model_version_id"]
        != cm_versions[6]["custom_model_version_id"]
    )
    run = 7
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)
    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name)
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    custom_model_id = json.loads(output.stdout)["custom_model_id"]
    custom_model_version_id = json.loads(output.stdout)["custom_model_version_id"]
    cm_versions[run] = {
        "custom_model_id": custom_model_id,
        "custom_model_version_id": custom_model_version_id,
    }
    assert cm_versions[6]["custom_model_id"] == cm_versions[7]["custom_model_id"]
    assert (
        cm_versions[6]["custom_model_version_id"]
        != cm_versions[7]["custom_model_version_id"]
    )
    run = 8
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)
    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name)
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    custom_model_id = json.loads(output.stdout)["custom_model_id"]
    custom_model_version_id = json.loads(output.stdout)["custom_model_version_id"]
    cm_versions[run] = {
        "custom_model_id": custom_model_id,
        "custom_model_version_id": custom_model_version_id,
    }
    assert cm_versions[7]["custom_model_id"] == cm_versions[8]["custom_model_id"]
    assert (
        cm_versions[7]["custom_model_version_id"]
        == cm_versions[8]["custom_model_version_id"]
    )
    with tempfile.TemporaryDirectory() as d:
        zip_file_path = pathlib.Path(d) / "model.zip"
        dr.CustomModelVersion.get(
            custom_model_id=custom_model_id,
            custom_model_version_id=custom_model_version_id,
        ).download(zip_file_path)

        # iterate over the zip file contents to find file1
        zip_ref = zipfile.ZipFile(zip_file_path, "r")
        assert "files/file1" in zip_ref.namelist()
        assert "requirements.txt" in zip_ref.namelist()
        assert zip_ref.read("files/file1") == b"foo"
        assert zip_ref.read("requirements.txt") == b"scikit-learn==1.4.2"


def test_custom_model_no_deployment(pulumi_up, stack_name):
    cwd = "tests/custom_model_no_deployment"
    run = 1
    cm_versions = {}
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)

    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name)
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    custom_model_id = json.loads(output.stdout)["custom_model_id"]
    custom_model_version_id = json.loads(output.stdout)["custom_model_version_id"]
    cm_versions[run] = {
        "custom_model_id": custom_model_id,
        "custom_model_version_id": custom_model_version_id,
    }

    run = 2
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)
    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name, extra=["--expect-no-changes"])
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    custom_model_id = json.loads(output.stdout)["custom_model_id"]
    custom_model_version_id = json.loads(output.stdout)["custom_model_version_id"]
    cm_versions[run] = {
        "custom_model_id": custom_model_id,
        "custom_model_version_id": custom_model_version_id,
    }

    assert cm_versions[1]["custom_model_id"] == cm_versions[2]["custom_model_id"]
    assert (
        cm_versions[1]["custom_model_version_id"]
        == cm_versions[2]["custom_model_version_id"]
    )
    run = 3
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)
    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name)
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    custom_model_id = json.loads(output.stdout)["custom_model_id"]
    custom_model_version_id = json.loads(output.stdout)["custom_model_version_id"]
    cm_versions[run] = {
        "custom_model_id": custom_model_id,
        "custom_model_version_id": custom_model_version_id,
    }
    assert cm_versions[2]["custom_model_id"] == cm_versions[3]["custom_model_id"]
    assert (
        cm_versions[2]["custom_model_version_id"]
        != cm_versions[3]["custom_model_version_id"]
    )
    cm = dr.CustomInferenceModel.get(custom_model_id)
    run = 4
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)
    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name)
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    custom_model_id = json.loads(output.stdout)["custom_model_id"]
    custom_model_version_id = json.loads(output.stdout)["custom_model_version_id"]
    cm_versions[run] = {
        "custom_model_id": custom_model_id,
        "custom_model_version_id": custom_model_version_id,
    }
    assert cm_versions[3]["custom_model_id"] == cm_versions[4]["custom_model_id"]
    assert (
        cm_versions[3]["custom_model_version_id"]
        != cm_versions[4]["custom_model_version_id"]
    )

    cm = dr.CustomInferenceModel.get(custom_model_id)
    assert len(cm.latest_version.runtime_parameters) > 0
    assert cm.latest_version.runtime_parameters[0].field_name == "pytest_credential"

    run = 5
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)
    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name)
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    custom_model_id = json.loads(output.stdout)["custom_model_id"]
    custom_model_version_id = json.loads(output.stdout)["custom_model_version_id"]
    cm_versions[run] = {
        "custom_model_id": custom_model_id,
        "custom_model_version_id": custom_model_version_id,
    }
    assert cm_versions[4]["custom_model_id"] == cm_versions[5]["custom_model_id"]
    assert (
        cm_versions[4]["custom_model_version_id"]
        == cm_versions[5]["custom_model_version_id"]
    )
    run = 6
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)
    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name)
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    custom_model_id = json.loads(output.stdout)["custom_model_id"]
    custom_model_version_id = json.loads(output.stdout)["custom_model_version_id"]
    cm_versions[run] = {
        "custom_model_id": custom_model_id,
        "custom_model_version_id": custom_model_version_id,
    }
    assert cm_versions[5]["custom_model_id"] == cm_versions[6]["custom_model_id"]
    assert (
        cm_versions[5]["custom_model_version_id"]
        != cm_versions[6]["custom_model_version_id"]
    )
    run = 7
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)
    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name)
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    custom_model_id = json.loads(output.stdout)["custom_model_id"]
    custom_model_version_id = json.loads(output.stdout)["custom_model_version_id"]
    cm_versions[run] = {
        "custom_model_id": custom_model_id,
        "custom_model_version_id": custom_model_version_id,
    }
    assert cm_versions[6]["custom_model_id"] == cm_versions[7]["custom_model_id"]
    assert (
        cm_versions[6]["custom_model_version_id"]
        != cm_versions[7]["custom_model_version_id"]
    )
    run = 8
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)
    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name)
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    custom_model_id = json.loads(output.stdout)["custom_model_id"]
    custom_model_version_id = json.loads(output.stdout)["custom_model_version_id"]
    cm_versions[run] = {
        "custom_model_id": custom_model_id,
        "custom_model_version_id": custom_model_version_id,
    }
    assert cm_versions[7]["custom_model_id"] == cm_versions[8]["custom_model_id"]
    assert (
        cm_versions[7]["custom_model_version_id"]
        == cm_versions[8]["custom_model_version_id"]
    )
    with tempfile.TemporaryDirectory() as d:
        zip_file_path = pathlib.Path(d) / "model.zip"
        dr.CustomModelVersion.get(
            custom_model_id=custom_model_id,
            custom_model_version_id=custom_model_version_id,
        ).download(zip_file_path)

        # iterate over the zip file contents to find file1
        zip_ref = zipfile.ZipFile(zip_file_path, "r")
        assert "files/file1" in zip_ref.namelist()
        assert "requirements.txt" in zip_ref.namelist()
        assert zip_ref.read("files/file1") == b"foo"
        assert zip_ref.read("requirements.txt") == b"scikit-learn==1.4.2"

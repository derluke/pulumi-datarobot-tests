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


def test_app_source(pulumi_up, stack_name):
    cwd = "tests/custom_apps"
    run = 1
    cm_versions = {}
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)

    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name)
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    app_id = json.loads(output.stdout)["app_id"]
    app_source_id = json.loads(output.stdout)["app_source_id"]
    app_source_version_id = json.loads(output.stdout)["app_source_version_id"]

    cm_versions[run] = {
        "app_id": app_id,
        "app_source_id": app_source_id,
        "app_source_version_id": app_source_version_id,
    }

    run = 2
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)

    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name)
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    app_id = json.loads(output.stdout)["app_id"]
    app_source_id = json.loads(output.stdout)["app_source_id"]
    app_source_version_id = json.loads(output.stdout)["app_source_version_id"]

    cm_versions[run] = {
        "app_id": app_id,
        "app_source_id": app_source_id,
        "app_source_version_id": app_source_version_id,
    }
    assert cm_versions[1]["app_id"] == cm_versions[2]["app_id"]
    assert cm_versions[1]["app_source_id"] == cm_versions[2]["app_source_id"]
    assert (
        cm_versions[1]["app_source_version_id"]
        == cm_versions[2]["app_source_version_id"]
    )
    run = 3
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)

    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name)
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    app_id = json.loads(output.stdout)["app_id"]
    app_source_id = json.loads(output.stdout)["app_source_id"]
    app_source_version_id = json.loads(output.stdout)["app_source_version_id"]

    cm_versions[run] = {
        "app_id": app_id,
        "app_source_id": app_source_id,
        "app_source_version_id": app_source_version_id,
    }
    assert cm_versions[2]["app_id"] == cm_versions[3]["app_id"]
    assert cm_versions[2]["app_source_id"] == cm_versions[3]["app_source_id"]
    assert (
        cm_versions[2]["app_source_version_id"]
        == cm_versions[3]["app_source_version_id"]
    )
    run = 4
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)

    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name)
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    app_id = json.loads(output.stdout)["app_id"]
    app_source_id = json.loads(output.stdout)["app_source_id"]
    app_source_version_id = json.loads(output.stdout)["app_source_version_id"]

    cm_versions[run] = {
        "app_id": app_id,
        "app_source_id": app_source_id,
        "app_source_version_id": app_source_version_id,
    }
    assert cm_versions[3]["app_id"] == cm_versions[4]["app_id"]
    assert cm_versions[3]["app_source_id"] == cm_versions[4]["app_source_id"]
    assert (
        cm_versions[3]["app_source_version_id"]
        == cm_versions[4]["app_source_version_id"]
    )
    run = 5
    print(f"Run {run}")
    run_set_config(run=run, stack_name=stack_name, cwd=cwd)

    proc = run_pulumi_up(cwd=cwd, stack_name=stack_name)
    assert proc.returncode == 0
    output = run_get_output(stack_name=stack_name, cwd=cwd)
    app_id = json.loads(output.stdout)["app_id"]
    app_source_id = json.loads(output.stdout)["app_source_id"]
    app_source_version_id = json.loads(output.stdout)["app_source_version_id"]

    cm_versions[run] = {
        "app_id": app_id,
        "app_source_id": app_source_id,
        "app_source_version_id": app_source_version_id,
    }
    assert cm_versions[5]["app_id"] == cm_versions[4]["app_id"]
    assert cm_versions[5]["app_source_id"] == cm_versions[4]["app_source_id"]
    assert (
        cm_versions[5]["app_source_version_id"]
        != cm_versions[4]["app_source_version_id"]
    )

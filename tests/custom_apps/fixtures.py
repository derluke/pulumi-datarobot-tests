import os
import pathlib


def base_environment_id() -> str:
    return "6542cd582a9d3d51bf4ac71e"


def start_script() -> str:
    return """\
#!/usr/bin/env bash
#
#  Copyright 2024 DataRobot, Inc. and its affiliates.
#
#  All rights reserved.
#  This is proprietary source code of DataRobot, Inc. and its affiliates.
#  Released under the terms of DataRobot Tool and Utility Agreement.
#
echo "Starting App"

streamlit run app.py
"""


tmp_path = pathlib.Path("./output")
tmp_path.mkdir(exist_ok=True)


def requirements():
    return """\
streamlit==1.29.0
"""


def app_py():
    return """\
import streamlit as st

st.write('Hello World!')
"""


def app_context_path() -> str:
    ts = 1701797283
    p = tmp_path / "requirements.txt"
    p.write_text(requirements())
    os.utime(p, (ts, ts))
    p = tmp_path / "app.py"
    p.write_text(app_py())
    os.utime(p, (ts, ts))
    p = tmp_path / "start-app.sh"
    p.write_text(start_script())
    os.utime(p, (ts, ts))
    return str(tmp_path.resolve())


def app_context_path_mod() -> str:
    ts = 1701797283
    p = tmp_path / "requirements.txt"
    p.write_text("streamlit==1.28.0")
    os.utime(p, (ts, ts))
    p = tmp_path / "app.py"
    p.write_text(app_py())
    os.utime(p, (ts, ts))
    p = tmp_path / "start-app.sh"
    p.write_text(start_script())
    os.utime(p, (ts, ts))
    return str(tmp_path.resolve())

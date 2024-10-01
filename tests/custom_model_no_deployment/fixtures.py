from pathlib import Path
import pathlib
import pulumi_datarobot as datarobot
import yaml


tmp_path = Path("./output")
tmp_path.mkdir(exist_ok=True)


def custom_py():
    return """\
def load_model(input_dir):
    return ''

def score(data, model, **kwargs):
    import pandas as pd
    preds = pd.DataFrame([42 for _ in range(data.shape[0])], columns=["Predictions"])
    return preds
"""


def sklearn_drop_in_env():
    """Sklearn drop-in environment id."""
    return "5e8c889607389fe0f466c72d"


def folder_path():
    dir = tmp_path / "custom_model"
    dir.mkdir(exist_ok=True)
    p = dir / "custom.py"
    p.write_text(custom_py())
    return str(dir.resolve())


def another_folder_path():
    dir = tmp_path / "another_custom_model"
    dir.mkdir(exist_ok=True)
    p = dir / "custom.py"
    p.write_text(custom_py())
    return str(dir.resolve())


def dummy_credential():
    name = "pytest_credential"
    credential = datarobot.ApiTokenCredential(
        resource_name="test-credential", name=name, api_token="foobar"
    )
    return name, credential


def runtime_parameter_values():
    creds = dummy_credential()
    return [
        datarobot.CustomModelRuntimeParameterValueArgs(
            key=creds[0],
            type="credential",
            value=creds[1].id,
        )
    ]


def model_metadata():
    return {
        "name": "pytest custom model",
        "type": "inference",
        "targetType": "regression",
        "runtimeParameterDefinitions": [
            {
                "fieldName": "pytest_credential",
                "type": "credential",
            }
        ],
    }


def folder_path_with_metadata():
    p = pathlib.Path(folder_path())
    p = p / "model-metadata.yaml"
    with open(p, "w") as f:
        yaml.safe_dump(model_metadata(), f)
    return folder_path()


def another_folder_path_with_metadata():
    p = pathlib.Path(another_folder_path())
    p = p / "model-metadata.yaml"
    with open(p, "w") as f:
        yaml.dump(model_metadata(), f)
    return another_folder_path()


def folder_path_with_metadata_and_reqs():
    requirements = "scikit-learn==1.4.0"
    p = pathlib.Path(folder_path_with_metadata())
    (p / "requirements.txt").write_text(requirements)
    return folder_path_with_metadata()


def files_with_metadata_and_reqs():
    p = pathlib.Path(folder_path_with_metadata())
    file_paths = []
    for file in p.glob("**/*"):
        if file.is_file():
            relative_path = file.relative_to(p)
            file_paths.append((str(file), str(relative_path)))
    return file_paths


def updated_folder_path_with_metadata_and_reqs():
    requirements = "scikit-learn==1.4.2"
    p = pathlib.Path(another_folder_path_with_metadata())
    (p / "requirements.txt").write_text(requirements)
    p = p / "files"
    p.mkdir(exist_ok=True)
    (p / "file1").write_text("foo")
    return another_folder_path_with_metadata()

import pulumi_datarobot as datarobot
import pulumi

from fixtures import (  # type: ignore[import-not-found]
    sklearn_drop_in_env,
    folder_path_with_metadata_and_reqs,
    updated_folder_path_with_metadata_and_reqs,
    runtime_parameter_values,
    files_with_metadata_and_reqs,
)

run = int(pulumi.Config().require("run"))

if run == 1:
    custom_model = datarobot.CustomModel(
        resource_name="test-custom-model",
        name="pytest custom model",
        description="pytest custom model",
        base_environment_id=sklearn_drop_in_env(),
        folder_path=str(folder_path_with_metadata_and_reqs()),
        target_type="Regression",
        target_name="dummy",
    )

elif run == 2:
    # same exact model again
    custom_model = datarobot.CustomModel(
        resource_name="test-custom-model",
        name="pytest custom model",
        description="pytest custom model",
        base_environment_id=sklearn_drop_in_env(),
        folder_path=folder_path_with_metadata_and_reqs(),
        target_type="Regression",
        target_name="dummy",
    )
elif run == 3:
    # update resource settings
    custom_model = datarobot.CustomModel(
        resource_name="test-custom-model",
        name="pytest custom model",
        description="pytest custom model",
        base_environment_id=sklearn_drop_in_env(),
        folder_path=folder_path_with_metadata_and_reqs(),
        resource_settings=datarobot.CustomModelResourceSettingsArgs(
            memory_mb=4096,
        ),
        target_type="Regression",
        target_name="dummy",
    )

elif run == 4:
    # add runtime parameters
    custom_model = datarobot.CustomModel(
        resource_name="test-custom-model",
        name="pytest custom model",
        description="pytest custom model",
        base_environment_id=sklearn_drop_in_env(),
        folder_path=folder_path_with_metadata_and_reqs(),
        runtime_parameter_values=runtime_parameter_values(),
        resource_settings=datarobot.CustomModelResourceSettingsArgs(
            memory_mb=4096,
        ),
        target_type="Regression",
        target_name="dummy",
    )
elif run == 5:
    # same again
    custom_model = datarobot.CustomModel(
        resource_name="test-custom-model",
        name="pytest custom model",
        description="pytest custom model",
        base_environment_id=sklearn_drop_in_env(),
        folder_path=folder_path_with_metadata_and_reqs(),
        runtime_parameter_values=runtime_parameter_values(),
        resource_settings=datarobot.CustomModelResourceSettingsArgs(
            memory_mb=4096,
        ),
        target_type="Regression",
        target_name="dummy",
    )
elif run == 6:
    # update files
    custom_model = datarobot.CustomModel(
        resource_name="test-custom-model",
        name="pytest custom model",
        description="pytest custom model",
        base_environment_id=sklearn_drop_in_env(),
        files=files_with_metadata_and_reqs(),
        runtime_parameter_values=runtime_parameter_values(),
        resource_settings=datarobot.CustomModelResourceSettingsArgs(
            memory_mb=4096,
        ),
        target_type="Regression",
        target_name="dummy",
    )
elif run == 7:
    # update folder
    custom_model = datarobot.CustomModel(
        resource_name="test-custom-model",
        name="pytest custom model",
        description="pytest custom model",
        base_environment_id=sklearn_drop_in_env(),
        folder_path=updated_folder_path_with_metadata_and_reqs(),
        runtime_parameter_values=runtime_parameter_values(),
        resource_settings=datarobot.CustomModelResourceSettingsArgs(
            memory_mb=4096,
        ),
        target_type="Regression",
        target_name="dummy",
    )

elif run == 8:
    # same again
    custom_model = datarobot.CustomModel(
        resource_name="test-custom-model",
        name="pytest custom model",
        description="pytest custom model",
        base_environment_id=sklearn_drop_in_env(),
        folder_path=updated_folder_path_with_metadata_and_reqs(),
        runtime_parameter_values=runtime_parameter_values(),
        resource_settings=datarobot.CustomModelResourceSettingsArgs(
            memory_mb=4096,
        ),
        target_type="Regression",
        target_name="dummy",
    )

registered_model = datarobot.RegisteredModel(
    resource_name="test-registered-model",
    custom_model_version_id=custom_model.version_id,
    name="pytest registered model",
)
prediction_environment = datarobot.PredictionEnvironment(
    resource_name="test-prediction-environment",
    name="pytest prediction environment",
    platform="datarobotServerless",
)
deployment = datarobot.Deployment(
    resource_name="test-deployment",
    registered_model_version_id=registered_model.version_id,
    label="pytest deployment",
    prediction_environment_id=prediction_environment.id,
)
pulumi.export("custom_model_id", custom_model.id)
pulumi.export("custom_model_version_id", custom_model.version_id)

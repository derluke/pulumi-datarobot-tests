import pulumi_datarobot as datarobot
from fixtures import app_context_path, app_context_path_mod  # type: ignore[import-not-found]
import pulumi


run = int(pulumi.Config().require("run"))

if run == 1:
    app_source = datarobot.ApplicationSource(
        resource_name="test-app-source",
        name="pytest app source",
        folder_path=app_context_path(),
    )
    custom_app = datarobot.CustomApplication(
        resource_name="test-custom-app",
        name="pytest app",
        source_version_id=app_source.version_id,
    )
elif run == 2:
    # same
    app_source = datarobot.ApplicationSource(
        resource_name="test-app-source",
        name="pytest app source",
        folder_path=app_context_path(),
    )
    custom_app = datarobot.CustomApplication(
        resource_name="test-custom-app",
        name="pytest app",
        source_version_id=app_source.version_id,
    )
elif run == 3:
    # share. app_id stays the same
    app_source = datarobot.ApplicationSource(
        resource_name="test-app-source",
        name="pytest app source",
        folder_path=app_context_path(),
    )
    custom_app = datarobot.CustomApplication(
        resource_name="test-custom-app",
        name="pytest app",
        source_version_id=app_source.version_id,
        external_access_enabled=True,
    )
elif run == 4:
    # rename. app_id stays the same
    app_source = datarobot.ApplicationSource(
        resource_name="test-app-source",
        name="pytest app source",
        folder_path=app_context_path(),
    )
    custom_app = datarobot.CustomApplication(
        resource_name="test-custom-app",
        name="pytest app 2",
        source_version_id=app_source.version_id,
    )
elif run == 5:
    # change source. app_id stays the same - source changes
    app_source = datarobot.ApplicationSource(
        resource_name="test-app-source",
        name="pytest app source",
        folder_path=app_context_path_mod(),
    )

    custom_app = datarobot.CustomApplication(
        resource_name="test-custom-app",
        name="pytest app 2",
        source_version_id=app_source.version_id,
    )

pulumi.export("app_id", custom_app.id)
pulumi.export("app_source_id", app_source.id)
pulumi.export("app_source_version_id", app_source.version_id)

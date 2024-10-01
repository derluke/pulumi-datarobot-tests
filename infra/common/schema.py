# Copyright 2024 DataRobot, Inc. and its affiliates.
# All rights reserved.
# DataRobot, Inc.
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
# Released under the terms of DataRobot Tool and Utility Agreement.

from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, Field
import pulumi_datarobot as datarobot
import pulumi

from .globals import (
    GlobalGuardrailTemplateName,
    GlobalLLM,
    GlobalPredictionEnvironmentPlatforms,
)
from datarobot.enums import VectorDatabaseChunkingMethod, VectorDatabaseEmbeddingModel


class Stage(str, Enum):
    PROMPT = "prompt"
    RESPONSE = "response"


class ModerationAction(str, Enum):
    BLOCK = "block"
    REPORT = "report"
    REPORT_AND_BLOCK = "reportAndBlock"


class GuardConditionComparator(Enum):
    """The comparator used in a guard condition."""

    GREATER_THAN = "greaterThan"
    LESS_THAN = "lessThan"
    EQUALS = "equals"
    NOT_EQUALS = "notEquals"
    IS = "is"
    IS_NOT = "isNot"
    MATCHES = "matches"
    DOES_NOT_MATCH = "doesNotMatch"
    CONTAINS = "contains"
    DOES_NOT_CONTAIN = "doesNotContain"


class Condition(BaseModel):
    comparand: float | str | bool | list[str]
    comparator: GuardConditionComparator


class Intervention(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    action: ModerationAction
    condition: Condition
    message: str
    # send_notification: bool


class GuardrailTemplate(BaseModel):
    template_name: str
    registered_model_name: Optional[str] = None
    name: str
    stages: list[Stage]
    intervention: Intervention


class CustomModelArgs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    resource_name: str
    name: str
    description: str | None = None
    base_environment_id: str
    base_environment_name: str
    base_environment_version_id: str | None = None
    target_name: str | None = None
    target_type: str | None = None
    runtime_parameter_values: (
        list[datarobot.CustomModelRuntimeParameterValueArgs] | None
    ) = None
    files: list[tuple[str, str]] | None = None
    class_labels: list[str] | None = None
    negative_class_label: str | None = None
    positive_class_label: str | None = None
    folder_path: str | None = None


class RegisteredModelArgs(BaseModel):
    resource_name: str
    name: str


class DeploymentArgs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    resource_name: str
    label: str
    association_id_settings: datarobot.DeploymentAssociationIdSettingsArgs | None = None
    bias_and_fairness_settings: (
        datarobot.DeploymentBiasAndFairnessSettingsArgs | None
    ) = None
    challenger_models_settings: (
        datarobot.DeploymentChallengerModelsSettingsArgs | None
    ) = None
    challenger_replay_settings: (
        datarobot.DeploymentChallengerReplaySettingsArgs | None
    ) = None
    drift_tracking_settings: datarobot.DeploymentDriftTrackingSettingsArgs | None = None
    health_settings: datarobot.DeploymentHealthSettingsArgs | None = None
    importance: str | None = None
    prediction_intervals_settings: (
        datarobot.DeploymentPredictionIntervalsSettingsArgs | None
    ) = None
    prediction_warning_settings: (
        datarobot.DeploymentPredictionWarningSettingsArgs | None
    ) = None
    predictions_by_forecast_date_settings: (
        datarobot.DeploymentPredictionsByForecastDateSettingsArgs | None
    ) = None
    predictions_data_collection_settings: (
        datarobot.DeploymentPredictionsDataCollectionSettingsArgs | None
    ) = None
    predictions_settings: datarobot.DeploymentPredictionsSettingsArgs | None = None
    segment_analysis_settings: (
        datarobot.DeploymentSegmentAnalysisSettingsArgs | None
    ) = None


class CustomModelGuardConfigurationArgs(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    stages: list[Stage]
    template_name: GlobalGuardrailTemplateName
    intervention: Intervention
    input_column_name: str | None = None
    output_column_name: str | None = None


class PlaygroundArgs(BaseModel):
    resource_name: str
    name: str


class LLMSettings(BaseModel):
    max_completion_length: int = Field(le=512)
    system_prompt: str


class VectorDatabaseSettings(BaseModel):
    max_documents_retrieved_per_prompt: Optional[int] = None
    max_tokens: Optional[int] = None


class LLMBlueprintArgs(BaseModel):
    resource_name: str
    name: str
    llm_settings: LLMSettings
    llm_id: GlobalLLM
    vector_database_settings: VectorDatabaseSettings


class ChunkingParameters(BaseModel):
    embedding_model: VectorDatabaseEmbeddingModel | None = None
    chunking_method: VectorDatabaseChunkingMethod | None = None
    chunk_size: int | None = Field(ge=128, le=512)
    chunk_overlap_percentage: int | None = None
    separators: list[str] | None = None


class VectorDatabaseArgs(BaseModel):
    resource_name: str
    name: str
    chunking_parameters: ChunkingParameters


class DatasetArgs(BaseModel):
    resource_name: str
    name: str
    file_path: str


class UseCaseArgs(BaseModel):
    resource_name: str
    name: str
    description: str | None
    opts: Optional[pulumi.ResourceOptions] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)


class PredictionEnvironmentArgs(BaseModel):
    resource_name: str
    name: str
    platform: GlobalPredictionEnvironmentPlatforms


class CredentialArgs(BaseModel):
    resource_name: str
    name: str


class QaApplicationArgs(BaseModel):
    resource_name: str
    name: str


class ApplicationSourceArgs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    resource_name: str
    files: Optional[Any] = None
    folder_path: Optional[str] = None
    name: Optional[str] = None
    resource_settings: Optional[datarobot.ApplicationSourceResourceSettingsArgs] = None

# Copyright 2024 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: LicenseRef-.amazon.com.-AmznSL-1.0
# Licensed under the Amazon Software License  http://aws.amazon.com/asl/
#
# A licença ASL concede direitos perpétuos, mundiais, não exclusivos e livres de royalties
# para reproduzir, criar obras derivadas e distribuir em código-fonte ou binário.

from enum import Enum
import os
from typing import Optional, TYPE_CHECKING

import boto3
from botocore.config import Config

from aws_lambda_powertools.logging import Logger

if TYPE_CHECKING:
    # mypy_boto3_* is a test-dependency only and not available at runtime
    # It is also only ever used as type-hints, so we can import it during TYPE_CHECKING only
    from mypy_boto3_bedrock_runtime.client import BedrockRuntimeClient
else:
    Table = object

logger = Logger()


class ConverseModelIds(Enum):
    """
    Enum containing Claude model IDs que defines available AI models 
    para threat modeling analysis usando Anthropic's latest versions.
    """
    CLAUDE_V4_SONNET_MODEL_ID = "anthropic.claude-sonnet-4-20250514-v1:0"
    CLAUDE_V4_5_SONNET_MODEL_ID = "anthropic.claude-sonnet-4-5-20250929-v1:0"
    CLAUDE_V4_HAIKU_MODEL_ID = "anthropic.claude-haiku-4-5-20251001-v1:0"


class EMBEDDING_MODEL_IDS(Enum):
    """
    Embedding model identifiers que defines available embedding models 
    para image and text processing em threat modeling.
    """
    TITAN_EMBED_IMAGE_V1_MODEL_ID = "amazon.titan-embed-image-v1"


def get_s3_client(region: Optional[str] = None):
    """
    Creates S3 client que handles file storage operations 
    para diagram uploads e report generation.
    """
    if region is None:
        target_region = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION"))
    else:
        target_region = region

    session = boto3.Session(region_name=target_region)
    return session.client("s3")


def get_bedrock_client(assumed_role: Optional[str] = None,
                       region: Optional[str] = None) -> "BedrockRuntimeClient":
    """
    Creates Bedrock client que handles AI model interactions with retry configuration 
    e cross-account role assumption para threat analysis.
    """
    if region is None:
        target_region = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION"))
    else:
        target_region = region

    session_kwargs = {"region_name": target_region}
    client_kwargs = {**session_kwargs}

    retry_config = Config(
        region_name=target_region,
        connect_timeout=120,
        read_timeout=120,
        retries={
            "max_attempts": 10,
            "mode": "adaptive",
        },
    )

    session = boto3.Session(**session_kwargs)

    if assumed_role:
        logger.debug(f"  Using role: {assumed_role}")
        sts = session.client("sts", config=Config(retries={"max_attempts": 3, "mode": "adaptive"}))
        response = sts.assume_role(
            RoleArn=str(assumed_role),
            RoleSessionName="x-acct-role-for-tm-prototype"
        )

        client_kwargs["aws_access_key_id"] = response["Credentials"]["AccessKeyId"]
        client_kwargs["aws_secret_access_key"] = response["Credentials"]["SecretAccessKey"]
        client_kwargs["aws_session_token"] = response["Credentials"]["SessionToken"]

    bedrock_client = session.client(
        service_name="bedrock-runtime",
        config=retry_config,
        **client_kwargs
    )

    return bedrock_client


class RefreshCredentials:
    """
    Decorator class que automatically refreshes AWS credentials when they expire 
    durante Bedrock API calls usando retry mechanism.
    """
    def __init__(descriptor, exception_descriptions=None, retries: int = 1):

        if exception_descriptions is None:
            exception_descriptions = ["ExpiredTokenException"]

        descriptor._exception_descriptions = exception_descriptions
        descriptor._retries = retries

    def __call__(descriptor, fn):
        descriptor._decorated_fn = fn

        return descriptor

    def __get__(descriptor, instance, owner=None):
        if instance is None:
            return descriptor

        def refresher(self, *args, **kwargs):
            for i in range(descriptor._retries + 1):
                try:
                    return descriptor._decorated_fn(self, *args, **kwargs)
                except Exception as ex:
                    if any(exc_desc in str(ex) for exc_desc in descriptor._exception_descriptions):
                        logger.warning(
                            f"Credentials expired when calling {descriptor._decorated_fn.__name__}. Refreshing credentials. Attempt: {i + 1}")
                        self._bedrock_client = get_bedrock_client(assumed_role=self._assumed_role, region=self._region)
                        continue
                    raise
            raise Exception(
                f"Function {descriptor._decorated_fn.__name__} failed to refresh assumed role credentials after {descriptor._retries} retries.")

        return refresher.__get__(instance, owner)


class BedrockClient:
    """
    Wrapper for Amazon Bedrock service client que handles credential refresh 
    e automatic retry quando AssumeRole credentials expire after 15 minutes.
    
    This wrapper will refresh the credentials if the calls raise an exception that matches `exception_description` and
    will retry up to `retries` times para ensure continuous AI model access.
    """

    def __init__(self, assumed_role: Optional[str] = None, region: Optional[str] = None):
        self._assumed_role = assumed_role
        self._region = region

        self._bedrock_client = get_bedrock_client(assumed_role=assumed_role, region=region)

    @RefreshCredentials(exception_descriptions=["ExpiredTokenException"], retries=1)
    def invoke_model(self, *args, **kwargs):
        return self._bedrock_client.invoke_model(*args, **kwargs)

    @RefreshCredentials(exception_descriptions=["ExpiredTokenException"], retries=1)
    def converse(self, *args, **kwargs):
        return self._bedrock_client.converse(*args, **kwargs)

    # Delegate all remaining methods to the underlying client
    def __getattr__(self, item):
        return getattr(self._bedrock_client, item)

# Copyright 2024 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: LicenseRef-.amazon.com.-AmznSL-1.0
# Licensed under the Amazon Software License  http://aws.amazon.com/asl/
#
# A licença ASL concede direitos perpétuos, mundiais, não exclusivos e livres de royalties
# para reproduzir, criar obras derivadas e distribuir em código-fonte ou binário.

import os
from typing import TYPE_CHECKING

from aws_lambda_powertools import Logger

from genai_core.clients import get_bedrock_client, ConverseModelIds
from genai_core.metrics import llm_metrics
from genai_core.model import DFD

if TYPE_CHECKING:
    from mypy_boto3_bedrock_runtime.type_defs import ConverseResponseTypeDef
else:
    ConverseResponseTypeDef = object

# We are accessing claude 4.5 cross account and using PDX region with CRIS for extra quota
BEDROCK_XACCT_ROLE = os.getenv("BEDROCK_XACCT_ROLE")
BEDROCK_CRIS_REGION = "us-west-2" if BEDROCK_XACCT_ROLE else None  # we use a client in PDX region for CRIS, otherwise we don't about region

logger = Logger()

DFD_SCHEMA = DFD.model_json_schema()

DFD_AS_TOOL = [{
    "toolSpec": {
        "name": DFD_SCHEMA["title"],
        "description": DFD_SCHEMA["description"],
        "inputSchema": {
            "json": DFD_SCHEMA
        }
    }
}]


@llm_metrics
def extract_dfd(image: bytes, diagram_description: str,
                model_id: ConverseModelIds = ConverseModelIds.CLAUDE_V4_5_SONNET_MODEL_ID) -> ConverseResponseTypeDef:
    """
    Extracts Data Flow Diagram components from architecture diagrams que analyzes image and description 
    para identify processes, data stores, actors e trust boundaries using AI models.
    
    :param image: Architecture diagram image bytes
    :param diagram_description: Detailed description of the diagram
    :param model_id: Claude model identifier para analysis
    :return: Bedrock API response with DFD components
    """

    bedrock_client = get_bedrock_client(assumed_role=BEDROCK_XACCT_ROLE, region=BEDROCK_CRIS_REGION)

    # TODO: incorporate few shot examples:

    system_prompt = (
        "You are a security specialist. Considering the architecture diagram image and its "
        "provided description, describe in detail a Data Flow Diagram that will be used for a Threat Model exercise. "
        "Focus on extracting the component types (Processes, Data Stores, Data Flows, Actors, Trust Boundaries and "
        "External Entities). Don't represent the data flow graphically."
    )

    image_and_description_message = {
        "role": "user",
        "content": [
            {"image": {"format": "png", "source": {"bytes": image}}},
            {"text": diagram_description},
        ]
    }

    response = bedrock_client.converse(
        modelId=model_id.value,
        system=[{"text": system_prompt}],
        # TODO: PEAPO6WPA3ZY-14 - extract inferenceConfig to somewhere that makes more sense...
        inferenceConfig={
            "maxTokens": 4000,
            "temperature": 0,
            "stopSequences": ["\n\nHuman:"]
        },
        messages=[
            image_and_description_message,
        ],
        toolConfig={
            "tools": DFD_AS_TOOL,
            "toolChoice": {
                "tool": {
                    "name": DFD_SCHEMA["title"],
                }
            }
        }
    )

    return response


def get_dfd_from_diagram_and_description(image: bytes, diagram_description: str,
                                         model_id: str) -> DFD:
    """
    Wrapper function que processes DFD extraction requests with string model ID 
    e returns validated DFD object para threat modeling workflow.
    """
    model_id = model_id or ConverseModelIds.CLAUDE_V4_5_SONNET_MODEL_ID
    response = extract_dfd(image, diagram_description, ConverseModelIds(model_id))

    return DFD.model_validate_bedrock_response(response)

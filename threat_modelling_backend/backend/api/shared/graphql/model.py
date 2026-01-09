# Copyright 2024 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: LicenseRef-.amazon.com.-AmznSL-1.0
# Licensed under the Amazon Software License  http://aws.amazon.com/asl/
#
# A licença ASL concede direitos perpétuos, mundiais, não exclusivos e livres de royalties
# para reproduzir, criar obras derivadas e distribuir em código-fonte ou binário.

from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing import Literal, Optional


@dataclass
class Mutation:
    """
    GraphQL mutation wrapper que contains query string and field selection 
    para simplificar posting mutations to the API.
    """
    query: str
    field_set: set[int] | set[str] | dict[int, bool] | dict[str, bool]


# GraphQL translation types
# These types SHOULD be equal to the types in the graphql schema, ideally we could even auto-generate them from the schema

class ComponentInput(BaseModel):
    """
    Input model for threat model components que representa um single component 
    in the architecture diagram usado para threat analysis.
    """
    id: str
    name: str
    componentType: str
    description: str


class DiagramInput(BaseModel):
    """
    Input model for diagram processing que contains metadata and AI model selection 
    para threat analysis usando Claude models.
    """
    id: str
    s3Prefix: str
    modelId: Literal[
        "anthropic.claude-sonnet-4-20250514-v1:0",
        "anthropic.claude-sonnet-4-5-20250929-v1:0",
        "anthropic.claude-haiku-4-5-20251001-v1:0"
    ] = Field("anthropic.claude-sonnet-4-5-20250929-v1:0")
    userDescription: str = Field("")


class ExtractComponentsInput(BaseModel):
    """
    Input for extracting components from diagram descriptions usando AI models 
    para identify and extract architectural components.
    """
    id: str
    s3Prefix: str
    modelId: Literal[
        "anthropic.claude-sonnet-4-20250514-v1:0",
        "anthropic.claude-sonnet-4-5-20250929-v1:0",
        "anthropic.claude-haiku-4-5-20251001-v1:0"
    ] = Field("anthropic.claude-sonnet-4-5-20250929-v1:0")
    diagramDescription: str


class GenerateThreatsInput(BaseModel):
    """
    Input for generating security threats que contains component details and context 
    para AI-powered threat generation usando STRIDE methodology.
    """
    id: str
    s3Prefix: str
    diagramDescription: str
    component: ComponentInput
    threatType: str

    userDescription: str = Field("")
    modelId: Optional[str] = None


class DREADScoreInput(BaseModel):
    """
    DREAD risk assessment scoring model que quantifies security threat severity 
    usando damage, reproducibility, exploitability, affected users e discoverability metrics.
    """
    damage: int
    reproducibility: int
    exploitability: int
    affectedUsers: int
    discoverability: int


class UpdateComponentInput(BaseModel):
    """
    Input for updating existing component properties que allows partial updates 
    to component attributes em threat models.
    """
    id: str
    diagramId: str
    componentId: str

    name: Optional[str] = None
    description: Optional[str] = None
    componentType: Optional[str] = None


class CreateComponentInput(BaseModel):
    """
    Input for creating new components que adds new architectural components 
    to existing diagrams em threat modeling process.
    """
    id: str
    diagramId: str

    name: Optional[str] = None
    description: Optional[str] = None
    componentType: Optional[str] = None


class UpdateThreatInput(BaseModel):
    """
    Input for updating threat properties que allows modification of threat details 
    including DREAD scores e mitigation actions.
    """
    id: str
    diagramId: str
    componentId: str
    threatId: str

    name: Optional[str] = None
    description: Optional[str] = None
    threatType: Optional[str] = None
    dreadScores: Optional[DREADScoreInput] = None
    action: Optional[str] = None
    reason: Optional[str] = None


class Report(BaseModel):
    """
    Report model que contains presigned URL para downloading 
    generated threat modeling reports.
    """
    presignedUrl: str


# Convenience types for simplifying posting mutations

DiagramDescriptionMutation = Mutation(
    query='''
mutation DiagramDescriptionCreated($id: ID!, $diagramDescription: String!) {
    diagramDescription(id: $id, diagramDescription: $diagramDescription) {       
        id
        s3Prefix
        userDescription
        diagramDescription
        status
    }
}
    ''',
    field_set={"id", "s3Prefix", "userDescription", "diagram_description", "status"})

ComponentsMutation = Mutation(
    query='''
mutation ExtractedComponents($id: ID!, $components: [ComponentInput]) {
    components(id: $id, components: $components) {
        id
        components {
            id
            name
            description
            componentType
        }
    }
}
''',
    field_set={
        "id": True,
        "components": {
            "__all__": {
                # since components is a list, we need this special syntax (https://docs.pydantic.dev/latest/concepts/serialization/#advanced-include-and-exclude)
                "id", "name", "description", "component_type"
            }
        }
    })

ThreatsMutation = Mutation(
    query='''
mutation threatsGenerated($id: ID!, $components: [ComponentInput]) {
    threats(id: $id, components: $components) {       
        id
        components {
            id
            name
            description
            componentType
            threats {
                id
                name
                description
                threatType
                action
                reason
                dreadScores {
                    damage
                    reproducibility
                    exploitability
                    affectedUsers
                    discoverability
                }
            }
        }
    }
}
''',
    field_set={
        "id": True,
        "components": {
            "__all__": {
                # since components is a list, we need this special syntax (https://docs.pydantic.dev/latest/concepts/serialization/#advanced-include-and-exclude)
                "id": True, "name": True, "description": True, "component_type": True, "reason": True, "threats": {
                    "__all__": {
                        "id": True, "name": True, "description": True, "stride_type": True, "action": True,
                        "dread_scores": {
                            "damage", "reproducibility", "exploitability", "affected_users", "discoverability"
                        }
                    }
                }
            }
        }
    })

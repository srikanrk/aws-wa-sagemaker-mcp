# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Data models for the SageMaker Well-Architected MCP Server."""

from mcp.types import TextContent
from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class CallToolResult(BaseModel):
    """Base class for tool call results with TextContent only."""

    content: List[TextContent] = Field(..., description='Response content')
    isError: bool = Field(False, description='Whether this is an error response')


class Finding(BaseModel):
    """A single Well-Architected finding."""

    pillar: str = Field(..., description='Well-Architected pillar name')
    severity: str = Field(..., description='Severity level: HIGH, MEDIUM, or LOW')
    resource: str = Field(..., description='Resource name or identifier')
    check: str = Field(..., description='Check identifier')
    detail: str = Field(..., description='Description of the finding')
    recommendation: str = Field(..., description='Recommended remediation')


class PillarSummary(BaseModel):
    """Summary of findings for a single pillar."""

    HIGH: int = Field(0, description='Number of HIGH severity findings')
    MEDIUM: int = Field(0, description='Number of MEDIUM severity findings')
    LOW: int = Field(0, description='Number of LOW severity findings')


class ValidateResourceResponse(CallToolResult):
    """Response model for single resource validation."""

    resource: str = Field(..., description='Name of the validated resource')
    resource_type: str = Field(..., description='Type of the resource')
    summary: Dict[str, PillarSummary] = Field(..., description='Findings summary by pillar')
    findings: List[Finding] = Field(..., description='List of findings')


class ValidateAllResponse(CallToolResult):
    """Response model for batch validation."""

    resources_validated: List[str] = Field(..., description='List of validated resource names')
    total_findings: int = Field(..., description='Total number of findings')
    summary: Dict[str, PillarSummary] = Field(
        ..., description='Aggregated findings summary by pillar'
    )
    findings: List[Finding] = Field(..., description='List of all findings')


class ResourceSummary(BaseModel):
    """Summary of a SageMaker resource."""

    name: str = Field(..., description='Resource name')
    status: Optional[str] = Field(None, description='Resource status')


class ListResourcesResponse(CallToolResult):
    """Response model for listing SageMaker resources."""

    endpoints: List[ResourceSummary] = Field(default_factory=list, description='List of endpoints')
    training_jobs: List[ResourceSummary] = Field(
        default_factory=list, description='List of training jobs'
    )
    notebook_instances: List[ResourceSummary] = Field(
        default_factory=list, description='List of notebook instances'
    )
    models: List[ResourceSummary] = Field(default_factory=list, description='List of models')


class PillarCheck(BaseModel):
    """Description of a single validation check."""

    id: str = Field(..., description='Check identifier')
    description: str = Field(..., description='What this check validates')


class PillarInfoResponse(CallToolResult):
    """Response model for pillar information."""

    name: str = Field(..., description='Pillar name')
    description: str = Field(..., description='Pillar description')
    checks: List[PillarCheck] = Field(..., description='List of checks for this pillar')

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

"""Well-Architected pillar validators."""

from awslabs.sagemaker_wa_mcp_server.validators.security import validate_security
from awslabs.sagemaker_wa_mcp_server.validators.reliability import validate_reliability
from awslabs.sagemaker_wa_mcp_server.validators.performance import validate_performance
from awslabs.sagemaker_wa_mcp_server.validators.cost import validate_cost
from awslabs.sagemaker_wa_mcp_server.validators.operational_excellence import (
    validate_operational_excellence,
)
from awslabs.sagemaker_wa_mcp_server.validators.sustainability import validate_sustainability


def run_all_validators(
    resource_type: str,
    resource_info: dict,
    tags: list[dict],
    region_name: str | None = None,
) -> list[dict]:
    """Run all pillar validators against a resource.

    Args:
        resource_type: Type of SageMaker resource
        resource_info: Resource description from AWS API
        tags: Resource tags
        region_name: AWS region name

    Returns:
        List of finding dictionaries
    """
    findings: list[dict] = []
    findings.extend(validate_security(resource_type, resource_info, tags, region_name))
    findings.extend(validate_reliability(resource_type, resource_info, region_name))
    findings.extend(validate_performance(resource_type, resource_info, region_name))
    findings.extend(validate_cost(resource_type, resource_info, tags, region_name))
    findings.extend(
        validate_operational_excellence(resource_type, resource_info, tags, region_name)
    )
    findings.extend(validate_sustainability(resource_type, resource_info, tags, region_name))
    return findings

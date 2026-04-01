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
# ruff: noqa: D101, D102, D103
"""Tests for the HTML report generator."""

import os
import tempfile
from awslabs.sagemaker_wa_mcp_server.report_generator import (
    generate_batch_html_report,
    generate_html_report,
)


SAMPLE_FINDINGS = [
    {
        'pillar': 'Security',
        'severity': 'HIGH',
        'resource': 'endpoint/ep-1',
        'check': 'vpc-isolation',
        'detail': 'Not in VPC',
        'recommendation': 'Deploy in VPC',
    },
    {
        'pillar': 'Reliability',
        'severity': 'MEDIUM',
        'resource': 'endpoint/ep-1',
        'check': 'single-instance',
        'detail': 'Only 1 instance',
        'recommendation': 'Use 2+',
    },
    {
        'pillar': 'Cost Optimization',
        'severity': 'LOW',
        'resource': 'training_job/tj-1',
        'check': 'no-spot',
        'detail': 'No spot',
        'recommendation': 'Enable spot',
    },
]


class TestGenerateHtmlReport:

    def test_creates_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, 'report.html')
            result = generate_html_report('ep-1', 'endpoint', SAMPLE_FINDINGS, {}, path)
            assert os.path.exists(result)
            assert result == path

    def test_contains_resource_name(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, 'report.html')
            generate_html_report('my-endpoint', 'endpoint', SAMPLE_FINDINGS, {}, path)
            with open(path) as f:
                content = f.read()
            # Resource name appears in the findings table
            assert 'endpoint/ep-1' in content

    def test_contains_account_and_region(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, 'report.html')
            generate_html_report(
                'ep-1', 'endpoint', SAMPLE_FINDINGS, {}, path,
                account_id='123456789012', region='us-east-1',
            )
            with open(path) as f:
                content = f.read()
            assert '123456789012' in content
            assert 'us-east-1' in content

    def test_contains_title(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, 'report.html')
            generate_html_report('ep-1', 'endpoint', SAMPLE_FINDINGS, {}, path)
            with open(path) as f:
                content = f.read()
            assert 'SageMaker Well-Architected Review' in content

    def test_default_path(self):
        result = generate_html_report('ep-1', 'endpoint', SAMPLE_FINDINGS, {})
        assert os.path.exists(result)
        assert result.endswith('wa-report.html')
        os.remove(result)


class TestGenerateBatchHtmlReport:

    def test_creates_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, 'batch.html')
            result = generate_batch_html_report(
                ['endpoint/ep-1', 'training_job/tj-1'],
                SAMPLE_FINDINGS, {}, path,
            )
            assert os.path.exists(result)

    def test_contains_resource_count(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, 'batch.html')
            generate_batch_html_report(
                ['endpoint/ep-1', 'training_job/tj-1'],
                SAMPLE_FINDINGS, {}, path,
            )
            with open(path) as f:
                content = f.read()
            assert '2 Resources Evaluated' in content

    def test_contains_all_pillars(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, 'batch.html')
            generate_batch_html_report(
                ['endpoint/ep-1'], SAMPLE_FINDINGS, {}, path,
            )
            with open(path) as f:
                content = f.read()
            assert 'Security' in content
            assert 'Reliability' in content
            assert 'Cost Optimization' in content

    def test_empty_findings(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, 'empty.html')
            result = generate_batch_html_report([], [], {}, path)
            assert os.path.exists(result)
            with open(path) as f:
                content = f.read()
            assert 'SageMaker Well-Architected Review' in content

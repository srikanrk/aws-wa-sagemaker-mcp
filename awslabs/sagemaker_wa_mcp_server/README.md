# SageMaker Well-Architected Validation Checks

This document details all validation checks performed by the SageMaker Well-Architected MCP Server, organized by pillar.

## Overview

| Pillar | Checks |
|--------|:------:|
| [Operational Excellence](#operational-excellence) | 10 |
| [Security](#security) | 21 |
| [Reliability](#reliability) | 10 |
| [Performance Efficiency](#performance-efficiency) | 8 |
| [Cost Optimization](#cost-optimization) | 9 |
| [Sustainability](#sustainability) | 7 |
| **Total** | **65** |

---

## Operational Excellence

Run and monitor systems to deliver business value and continually improve processes.

### Monitoring & Observability

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `no-cloudwatch-metrics` | Verifies that SageMaker endpoints are actively monitored with CloudWatch metrics for performance tracking | MEDIUM | Endpoint |
| `no-cloudwatch-logs` | Confirms CloudWatch log groups exist for SageMaker resources to capture operational logs | MEDIUM | All |
| `no-log-retention` | Validates that CloudWatch logs have appropriate retention periods configured to balance cost and compliance | LOW | All |

### Automation & Change Management

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `no-model-registry` | Ensures models are registered and versioned in Model Registry for governance and traceability | MEDIUM | Endpoint |
| `no-sagemaker-project` | Checks if SageMaker Projects are used to standardize MLOps workflows and templates | LOW | Endpoint |

### Alerting & Incident Response

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `no-error-alarms` | Verifies CloudWatch alarms are configured to alert on endpoint 4XX and 5XX invocation errors | HIGH | Endpoint |
| `no-latency-alarms` | Confirms alarms exist to monitor and alert on high model latency affecting user experience | MEDIUM | Endpoint |

### Tagging & Organization

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `missing-operational-tags` | Validates operational tags (Environment, Team, Application) are present for resource organization | LOW | All |

### Scaling

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `no-autoscaling` | Checks if auto-scaling is configured for endpoints to handle traffic variations | MEDIUM | Endpoint |

### Experiment Tracking

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `no-experiment-tracking` | Validates experiment tracking for training job reproducibility | LOW | Training Job |

---

## Security

Protect data, systems, and assets through risk assessments and mitigation strategies.

### Identity & Access Management

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `no-iam-role` | Validates that SageMaker resources use IAM roles (not user credentials) for secure access control | HIGH | All |
| `overly-permissive-role` | Lists SageMaker-related IAM roles for regular security review and least-privilege validation | HIGH | All |
| `no-iam-access-analyzer` | Confirms IAM Access Analyzer is enabled to identify unintended resource access | MEDIUM | All |

### Network Security

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `vpc-isolation` | Verifies SageMaker resources are deployed within a VPC for network isolation | HIGH | All |
| `direct-internet-access` | Ensures notebook instances have direct internet access disabled to prevent data exfiltration | HIGH | Notebook |
| `no-vpc-endpoint` | Confirms VPC endpoints exist for SageMaker API access to avoid internet gateway routing | MEDIUM | All (VPC-deployed) |
| `no-vpc-flow-logs` | Validates VPC Flow Logs are enabled for network traffic monitoring and security analysis | MEDIUM | All (VPC-deployed) |

### Data Protection & Encryption

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `encryption-at-rest` | Verifies all SageMaker resources use KMS encryption at rest for data protection | HIGH | All |
| `s3-no-encryption` | Confirms S3 buckets storing training data and models have encryption enabled | HIGH | Training Job, Model |
| `s3-no-versioning` | Validates S3 bucket versioning is enabled for data protection and recovery | MEDIUM | Training Job, Model |
| `no-kms-key-rotation` | Ensures KMS keys have automatic rotation enabled for enhanced security posture | MEDIUM | All (KMS-encrypted) |

### Access Control & Monitoring

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `root-access` | Confirms root access is disabled on production notebook instances to limit security exposure | MEDIUM | Notebook |
| `no-cloudtrail` | Verifies CloudTrail is logging all SageMaker API calls for audit and compliance | HIGH | All |
| `s3-no-access-logging` | Confirms S3 access logging is enabled for audit trails of data access patterns | LOW | Training Job, Model |
| `no-aws-config` | Validates AWS Config is actively recording SageMaker resource configurations for compliance | MEDIUM | All |
| `no-guardduty` | Confirms GuardDuty is enabled for intelligent threat detection across AWS resources | MEDIUM | All |
| `no-security-hub` | Verifies Security Hub is enabled for centralized security findings and compliance checks | MEDIUM | All |

### Compliance & Governance

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `no-data-classification-tags` | Validates resources have appropriate tags for data classification and governance tracking | LOW | All |
| `no-sagemaker-config-rules` | Confirms SageMaker-specific AWS Config rules are enabled for automated compliance monitoring | LOW | All |

### Data In Transit

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `inter-container-encryption` | Checks encryption for inter-container traffic in distributed training | MEDIUM | Training Job |
| `network-isolation` | Validates network isolation to prevent outbound network calls from containers | MEDIUM | Training Job, Model |

---

## Reliability

Ensure workloads perform their intended function correctly and consistently.

### High Availability

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `no-multi-az` | Verifies endpoints are deployed across multiple Availability Zones for high availability | HIGH | Endpoint |
| `single-instance-endpoint` | Confirms production endpoints have 2+ instances for redundancy and fault tolerance | HIGH | Endpoint |

### Auto Scaling & Capacity

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `no-autoscaling` | Validates auto-scaling is configured for endpoints to handle variable traffic loads | HIGH | Endpoint |
| `no-target-tracking-policy` | Confirms target-tracking scaling policies are configured for automatic capacity adjustment | MEDIUM | Endpoint |
| `low-endpoint-quota` | Reviews current SageMaker service quotas to prevent hitting limits during scale-up | MEDIUM | Endpoint |

### Backup & Recovery

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `s3-no-versioning-artifacts` | Ensures S3 versioning is enabled for model artifacts to support rollback and recovery | MEDIUM | Training Job, Model |
| `no-cross-region-replication` | Validates critical data has cross-region replication configured for disaster recovery | LOW | Training Job, Model |

### Training Resilience

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `training-timeout` | Validates training jobs have reasonable timeout limits to prevent runaway jobs | MEDIUM | Training Job |
| `no-checkpointing` | Checks if training checkpointing is configured for failure recovery | MEDIUM | Training Job |
| `no-retry-strategy` | Validates retry strategy for automatic recovery from transient failures | LOW | Training Job |

---

## Performance Efficiency

Use computing resources efficiently to meet requirements and maintain efficiency as demand changes.

### Instance Optimization

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `instance-type-review` | Reviews endpoint instance types to ensure they match workload requirements (CPU/GPU/memory) | LOW | Endpoint |
| `underutilized-endpoint` | Analyzes CloudWatch metrics to identify over-provisioned instances for right-sizing | MEDIUM | Endpoint |
| `overutilized-endpoint` | Analyzes CloudWatch metrics to identify under-provisioned instances for right-sizing | MEDIUM | Endpoint |
| `older-instance-generation` | Flags older generation instance types (m4/c4/p2) for upgrade consideration | MEDIUM | Endpoint, Training Job |
| `older-notebook-instance` | Flags older notebook instance types (t2/m4) for upgrade consideration | LOW | Notebook |

### Model Optimization

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `no-neo-compilation` | Checks if models are compiled with SageMaker Neo for optimized inference performance | LOW | Endpoint, Model |

### Data & Monitoring

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `no-data-capture` | Checks if data capture is enabled for model monitoring and drift detection | LOW | Endpoint |
| `data-distribution` | Validates data distribution strategy (ShardedByS3Key vs FullyReplicated) for multi-instance training | MEDIUM | Training Job |

---

## Cost Optimization

Avoid unnecessary costs and optimize spending.

### Instance Cost Management

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `no-spot-training` | Verifies training jobs use managed spot instances for 60-90% cost savings | MEDIUM | Training Job |
| `running-notebook` | Identifies running notebook instances that may be idle and candidates for termination | MEDIUM | Notebook |
| `no-lifecycle-config` | Confirms notebook instances have lifecycle configs attached for automatic start/stop | MEDIUM | Notebook |

### Resource Utilization

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `consider-multi-model` | Checks if multi-model endpoints are used to share resources and reduce costs | LOW | Endpoint |
| `consider-serverless` | Suggests serverless inference for single-instance endpoints with intermittent traffic | LOW | Endpoint |
| `large-training-volume` | Flags oversized training volumes (>500 GB) for review | LOW | Training Job |

### Cost Monitoring

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `missing-cost-tags` | Validates resources have cost allocation tags for accurate cost tracking and chargeback | LOW | All |

### Storage Cost Optimization

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `s3-no-lifecycle-policy` | Confirms S3 lifecycle policies exist to automatically archive or delete old data | LOW | Training Job |
| `s3-no-intelligent-tiering` | Verifies S3 Intelligent-Tiering is configured for automatic cost optimization | LOW | Training Job |

---

## Sustainability

Minimize environmental impacts of running cloud workloads.

### Energy Efficiency

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `consider-graviton-endpoint` | Checks if endpoints use AWS Graviton instances for up to 60% less energy consumption | LOW | Endpoint |
| `consider-graviton` | Suggests Graviton-based instances for training jobs where compatible | LOW | Training Job |
| `spot-for-sustainability` | Recommends spot training to use spare capacity and improve infrastructure utilization | LOW | Training Job |

### Resource Lifecycle Management

| Check ID | Description | Severity | Resource Types |
|----------|-------------|:--------:|----------------|
| `long-running-endpoint` | Lists active endpoints running >90 days for review and cleanup of unused resources | LOW | Endpoint |
| `stale-notebook` | Identifies notebook instances stopped >30 days that should be reviewed for potential deletion | LOW | Notebook |
| `oversized-notebook` | Flags potentially oversized notebook instances for right-sizing | LOW | Notebook |
| `no-lifecycle-tags` | Validates resources have lifecycle tags (CreatedDate, ExpiryDate) for automated cleanup | LOW | All |

---

## AWS Services Used

The validation checks query the following AWS services (all read-only operations):

| AWS Service | Purpose |
|-------------|---------|
| Amazon SageMaker | Resource descriptions, tags, endpoint configs, model details |
| Amazon CloudWatch | Metrics, alarms, log groups, log retention |
| Amazon S3 | Bucket encryption, versioning, lifecycle policies, access logging, replication, Intelligent-Tiering |
| AWS IAM | Role policies, IAM Access Analyzer |
| Amazon EC2 | VPC endpoints, VPC Flow Logs, subnet-to-VPC resolution |
| AWS CloudTrail | Trail status and logging verification |
| AWS Config | Configuration recorder status, Config rules |
| Amazon GuardDuty | Detector status |
| AWS Security Hub | Hub enablement status |
| AWS Service Quotas | SageMaker endpoint instance quotas |
| Application Auto Scaling | Scalable targets and scaling policies |

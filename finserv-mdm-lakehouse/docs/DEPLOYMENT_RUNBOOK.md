# Horizon Bank Holdings — Deployment Runbook

## Prerequisites
- AWS account with VPC, S3, EMR, Glue, Lambda, Step Functions
- Terraform >= 1.5
- Python 3.9+
- Node.js 18+ (for dashboard)
- Snowflake account (for external tables)

## Phase 1: Infrastructure (Day 1)
```bash
cd infra/terraform
terraform init
terraform plan -var="env=dev"
terraform apply -var="env=dev"
```

## Phase 2: Data Generation (Day 1)
```bash
pip install -r requirements.txt
python src/data_generation/generate_all.py --company "Horizon Bank Holdings"
python tests/test_data_quality.py
```

## Phase 3: Pipeline Deployment (Day 2-3)
1. Deploy Bronze ingestion (Glue jobs + Lambda CDC)
2. Deploy Silver transforms (EMR PySpark)
3. Deploy MDM matching engine
4. Deploy Gold star schema (dbt models)
5. Deploy Step Functions orchestration

## Phase 4: Dashboard (Day 3-4)
```bash
# Deploy React dashboard
cd src/dashboards
npm install
npm run build
aws s3 sync build/ s3://horizon-dashboard-prod/
```

## Phase 5: Monitoring (Day 4)
- CloudWatch dashboards for pipeline health
- SNS alerts → PagerDuty for SLO breaches
- Weekly DQ report generation

## Rollback Procedure
```bash
# Terraform rollback
terraform apply -target=module.emr -var="version=previous"
# Delta Lake time travel
RESTORE TABLE gold.dim_customer TO VERSION AS OF <version_number>
```

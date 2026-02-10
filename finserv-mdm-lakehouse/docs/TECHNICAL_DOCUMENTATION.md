# Horizon Bank Holdings — Technical Documentation

## Architecture Overview

The Horizon Bank Holdings MDM Lakehouse implements a four-layer medallion architecture on AWS, designed for a diversified financial services company with credit cards, personal/auto loans, savings/CD accounts, and digital banking products.

### Medallion Layers

| Layer | Purpose | Storage | DQ Gate |
|-------|---------|---------|---------|
| Bronze | Raw source system replicas | S3 + Delta Lake (append-only) | Schema validation |
| Silver | Cleaned, conformed, PII-classified | S3 + Delta Lake (SCD2) | Type/null/dedup checks |
| MDM | Golden records via fuzzy matching | S3 + Delta Lake | Match confidence ≥0.75 |
| Gold | Kimball star schema for analytics | S3 + Delta Lake / Snowflake | Referential integrity |

### Source Systems

| System | Type | Entities | Extraction |
|--------|------|----------|------------|
| Core Banking | Oracle DB (JDBC) | CIF, Accounts, Transactions | Incremental CDC every 4hrs |
| Salesforce | REST API (Bulk v2) | Accounts, Contacts, Opportunities | Incremental every 2hrs + real-time CDC |
| Fiserv | SFTP (CSV) | Party, Card Transactions, Payments | Full file daily at 02:00 UTC |

### MDM Matching Engine

**Algorithm**: Weighted Jaro-Winkler composite scoring across 5 dimensions.

| Dimension | Weight | Method | Threshold |
|-----------|--------|--------|-----------|
| Name | 30% | Jaro-Winkler string similarity | ≥0.85 |
| Email | 25% | Exact match after normalization | 1.0 (exact) or 0.0 |
| Phone | 20% | E.164 normalized comparison | ≥0.8 (7-digit prefix match) |
| Address | 15% | Token-based fuzzy on city+state | ≥0.7 |
| Cross-System | 10% | Bonus for records from different sources | 0.15 if cross-system |

**Decision Tiers**:
- AUTO_MERGE: composite ≥ 0.92 → Merge automatically
- REVIEW: composite 0.75-0.92 → Data steward queue
- NO_MATCH: composite < 0.75 → Separate records

### Survivorship Rules

| Field | Priority | Rule |
|-------|----------|------|
| Legal Name | Core Banking → Fiserv → Salesforce | Finance-verified |
| Email | Salesforce → Core Banking → Fiserv | CRM is owner, most recent |
| Phone | Salesforce → Core Banking → Fiserv | Most recently updated, E.164 |
| Billing Address | Core Banking → Fiserv → Salesforce | Finance-verified |
| FICO Score | Core Banking → Fiserv | Authoritative credit data |
| Annual Income | Core Banking → Salesforce | Underwriting verified |

### Privacy Architecture

- **Classification at Ingestion**: PII/SPII/Confidential/Public tags at Bronze
- **Consent-Aware Pipelines**: Consent checked before Silver transforms
- **Tokenization**: PII tokenized at Silver boundary, KMS-controlled
- **Right to Erasure**: GDPR Article 17 cascade from MDM through all facts

### Self-Recovering ETL Patterns

1. **Checkpoint Recovery**: Delta Lake transaction log resumes from exact row
2. **Idempotent Transforms**: MERGE INTO with built-in dedup
3. **Dead Letter Queue**: Malformed records → S3+SQS DLQ
4. **Exponential Backoff**: Retry 1s→2s→4s→8s→16s, max 5
5. **Circuit Breaker**: Auto-pause on source failure, health-check every 30s
6. **SLO Monitoring**: Freshness <4hrs, completeness >99.5%, DQ pass >97%

### Deployment Strategy

- **IaC**: Terraform for VPC, EMR, S3, Glue, Step Functions
- **Blue-Green**: Two environments, instant switch on failure
- **Canary**: 5% traffic → monitor DQ → roll to 100% or rollback
- **Rollback**: Tagged artifacts + Terraform state, <5 minute recovery

## Data Quality

34 automated tests across 8 categories, all passing:
- Completeness (8 tests)
- Uniqueness (3 tests)
- Referential Integrity (5 tests)
- Business Rules (6 tests)
- Financial Compliance (3 tests)
- MDM Quality (4 tests)
- Bronze Source (4 tests)
- Temporal Consistency (1 test)

---

*Built with Claude Opus 4.6 | Simultaneous | February 2026*

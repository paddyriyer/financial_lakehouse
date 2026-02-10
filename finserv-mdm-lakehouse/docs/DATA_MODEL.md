# Horizon Bank Holdings — Data Model Reference

## Star Schema (Gold Layer)

### Dimension Tables

#### dim_customer (2,000 rows)
Golden customer records — MDM-merged from 3 source systems.

| Column | Type | Description |
|--------|------|-------------|
| customer_id | VARCHAR(10) | Primary key (CUST-XXXXX) |
| first_name | VARCHAR(50) | First name |
| last_name | VARCHAR(50) | Last name |
| email | VARCHAR(100) | Email address |
| phone | VARCHAR(15) | Phone (E.164) |
| date_of_birth | DATE | DOB |
| ssn_hash | VARCHAR(16) | SHA-256 hash of SSN |
| segment | VARCHAR(20) | mass_market/mass_affluent/affluent/high_net_worth/ultra_hnw |
| risk_tier | VARCHAR(20) | super_prime/prime/near_prime/subprime/deep_subprime |
| fico_score | INT | FICO score (300-850) |
| annual_income | DECIMAL | Verified annual income |
| acquisition_channel | VARCHAR(30) | How customer was acquired |
| status | VARCHAR(15) | active/inactive/closed/suspended |
| digital_enrolled | BOOLEAN | Digital banking enrollment |
| mobile_app_user | BOOLEAN | Mobile app active |

#### dim_account (3,867 rows)
All financial accounts across credit cards, loans, and deposits.

| Column | Type | Description |
|--------|------|-------------|
| account_id | VARCHAR(10) | Primary key (ACCT-XXXXX) |
| customer_id | VARCHAR(10) | FK → dim_customer |
| product_id | VARCHAR(6) | FK → dim_product |
| balance | DECIMAL | Current balance |
| credit_limit | DECIMAL | Credit limit (0 for deposits) |
| apr | DECIMAL | Interest rate |
| status | VARCHAR(15) | open/closed/delinquent/frozen |

#### dim_product (19 rows)
Product catalog: 8 credit cards, 5 loan products, 6 deposit products.

#### dim_date (1,095 rows)
3-year calendar dimension (2023-2025).

### Fact Tables

#### fact_transactions (30,000 rows)
Card transactions with MCC codes, merchant info, rewards.

#### fact_loan_payments (20,486 rows)
Loan payment history with delinquency tracking.

#### fact_credit_risk (1,844 rows)
Credit risk snapshot: FICO, DPD, PD, LGD, expected loss.

#### digital_events (40,000 rows)
Mobile/web app events, sessions, conversions.

#### fraud_alerts (644 rows)
Fraud/AML alerts with ML model scores and investigation status.

#### partner_performance (120 rows)
Monthly partner metrics: transactions, spend, interchange, CSAT.

#### hourly_metrics (336 rows)
Real-time operational KPIs (2 weeks, hourly).

#### mdm_match_pairs (32 rows)
MDM fuzzy match results with component and composite scores.

### Bronze Layer

#### core_banking_customers (800 rows)
Core banking system extract (Oracle format: CIF_NUM, CUST_NAME uppercase).

#### salesforce_accounts (1,200 rows)
Salesforce CRM extract (SFDC format: AccountId, PersonEmail).

#### fiserv_parties (1,000 rows)
Fiserv processor extract (PARTY_ID, FULL_NAME variations).

---

**Total: 15 tables, 103,443 records**

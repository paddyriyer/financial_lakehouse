#!/usr/bin/env python3
"""
Data Quality Tests — Horizon Bank Holdings MDM Lakehouse
============================================================
Validates data integrity, referential integrity, business rules,
and financial compliance across all layers.
"""
import csv, os, sys, math
from datetime import datetime
from collections import defaultdict

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
PASSED = 0
FAILED = 0

def load(subdir, fname):
    path = os.path.join(BASE, subdir, fname)
    if not os.path.exists(path): return []
    with open(path) as f: return list(csv.DictReader(f))

def check(name, condition, detail=""):
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  ✅ {name}")
    else:
        FAILED += 1
        print(f"  ❌ {name} — {detail}")

def main():
    print("\n" + "="*60)
    print("  DATA QUALITY TESTS — PINNACLE FINANCIAL GROUP")
    print("="*60)
    
    # Load data
    customers = load("gold", "dim_customer.csv")
    accounts = load("gold", "dim_account.csv")
    products = load("gold", "dim_product.csv")
    txns = load("gold", "fact_transactions.csv")
    payments = load("gold", "fact_loan_payments.csv")
    events = load("clickstream", "digital_events.csv")
    fraud = load("fraud", "fraud_alerts.csv")
    risk = load("gold", "fact_credit_risk.csv")
    partners = load("partners", "partner_performance.csv")
    metrics = load("realtime", "hourly_metrics.csv")
    mdm = load("mdm", "mdm_match_pairs.csv")
    bronze_core = load("bronze", "core_banking_customers.csv")
    bronze_sfdc = load("bronze", "salesforce_accounts.csv")
    bronze_fiserv = load("bronze", "fiserv_parties.csv")
    dates = load("gold", "dim_date.csv")
    
    # ─── 1. Completeness Tests ───
    print("\n▶ COMPLETENESS TESTS")
    check("DIM_CUSTOMER row count ≥ 2000", len(customers) >= 2000, f"Got {len(customers)}")
    check("DIM_ACCOUNT row count ≥ 3000", len(accounts) >= 3000, f"Got {len(accounts)}")
    check("FACT_TRANSACTIONS row count ≥ 25000", len(txns) >= 25000, f"Got {len(txns)}")
    check("FACT_LOAN_PAYMENTS row count ≥ 10000", len(payments) >= 10000, f"Got {len(payments)}")
    check("DIGITAL_EVENTS row count ≥ 30000", len(events) >= 30000, f"Got {len(events)}")
    check("FRAUD_ALERTS row count ≥ 100", len(fraud) >= 100, f"Got {len(fraud)}")
    check("PARTNER_PERFORMANCE row count ≥ 100", len(partners) >= 100, f"Got {len(partners)}")
    check("DIM_DATE row count = 1095 (3 years)", len(dates) == 1095, f"Got {len(dates)}")
    
    # ─── 2. Uniqueness Tests ───
    print("\n▶ UNIQUENESS TESTS")
    cust_ids = [c["customer_id"] for c in customers]
    check("Customer IDs are unique", len(cust_ids) == len(set(cust_ids)), f"{len(cust_ids) - len(set(cust_ids))} duplicates")
    
    acct_ids = [a["account_id"] for a in accounts]
    check("Account IDs are unique", len(acct_ids) == len(set(acct_ids)))
    
    txn_ids = [t["transaction_id"] for t in txns]
    check("Transaction IDs are unique", len(txn_ids) == len(set(txn_ids)))
    
    # ─── 3. Referential Integrity Tests ───
    print("\n▶ REFERENTIAL INTEGRITY TESTS")
    cust_set = set(cust_ids)
    acct_custs = set(a["customer_id"] for a in accounts)
    check("All accounts reference valid customers", acct_custs.issubset(cust_set), f"{len(acct_custs - cust_set)} orphans")
    
    acct_set = set(acct_ids)
    txn_accts = set(t["account_id"] for t in txns)
    check("All transactions reference valid accounts", txn_accts.issubset(acct_set), f"{len(txn_accts - acct_set)} orphans")
    
    pmt_accts = set(p["account_id"] for p in payments)
    check("All loan payments reference valid accounts", pmt_accts.issubset(acct_set), f"{len(pmt_accts - acct_set)} orphans")
    
    fraud_txns = set(f["transaction_id"] for f in fraud)
    txn_set = set(txn_ids)
    check("All fraud alerts reference valid transactions", fraud_txns.issubset(txn_set), f"{len(fraud_txns - txn_set)} orphans")
    
    prod_ids = set(p["product_id"] for p in products)
    acct_prods = set(a["product_id"] for a in accounts)
    check("All accounts reference valid products", acct_prods.issubset(prod_ids), f"{len(acct_prods - prod_ids)} orphans")
    
    # ─── 4. Business Rule Tests ───
    print("\n▶ BUSINESS RULE TESTS")
    for c in customers:
        if c["fico_score"]:
            fico = int(c["fico_score"])
            if not (300 <= fico <= 850):
                check("FICO scores in valid range [300-850]", False, f"Got {fico}")
                break
    else:
        check("FICO scores in valid range [300-850]", True)
    
    valid_segments = {"mass_market","mass_affluent","affluent","high_net_worth","ultra_hnw"}
    seg_ok = all(c["segment"] in valid_segments for c in customers)
    check("Customer segments are valid enum values", seg_ok)
    
    valid_risk = {"super_prime","prime","near_prime","subprime","deep_subprime"}
    risk_ok = all(c["risk_tier"] in valid_risk for c in customers)
    check("Risk tiers are valid enum values", risk_ok)
    
    # Transactions should have positive amounts
    pos_amt = all(float(t["amount"]) > 0 for t in txns)
    check("All transaction amounts are positive", pos_amt)
    
    # Credit limits should be non-negative
    cl_ok = all(float(a["credit_limit"]) >= 0 for a in accounts)
    check("Credit limits are non-negative", cl_ok)
    
    # APR should be reasonable (0-35%)
    apr_ok = all(0 <= float(a["apr"]) <= 35 for a in accounts)
    check("APR values in reasonable range [0-35%]", apr_ok)
    
    # ─── 5. Financial Compliance Tests ───
    print("\n▶ FINANCIAL COMPLIANCE TESTS")
    # No raw SSN in any file (should be hashed)
    ssn_pattern_found = False
    for c in customers:
        for v in c.values():
            if isinstance(v, str) and len(v) == 9 and v.isdigit():
                ssn_pattern_found = True
                break
    check("No raw SSN values in customer data (hashed only)", not ssn_pattern_found)
    
    # KYC verified for all active customers
    active_kyc = all(c["kyc_verified"] == "True" for c in customers if c["status"] == "active")
    check("All active customers have KYC verification", active_kyc)
    
    # Fraud alerts have risk scores
    fraud_scores = all(0 <= float(f["risk_score"]) <= 1 for f in fraud)
    check("Fraud risk scores in valid range [0-1]", fraud_scores)
    
    # ─── 6. MDM Quality Tests ───
    print("\n▶ MDM QUALITY TESTS")
    check("MDM match pairs generated", len(mdm) > 0, f"Got {len(mdm)}")
    
    valid_tiers = {"auto_merge","review","no_match"}
    tier_ok = all(m["match_tier"] in valid_tiers for m in mdm)
    check("MDM match tiers are valid", tier_ok)
    
    # Composite scores should be between 0 and 1
    score_ok = all(0 <= float(m["composite_score"]) <= 1 for m in mdm)
    check("MDM composite scores in [0,1]", score_ok)
    
    # Auto-merge should have score >= 0.92
    auto_merges = [m for m in mdm if m["match_tier"] == "auto_merge"]
    am_ok = all(float(m["composite_score"]) >= 0.92 for m in auto_merges) if auto_merges else True
    check("Auto-merge pairs have score ≥ 0.92", am_ok)
    
    # ─── 7. Bronze Source Tests ───
    print("\n▶ BRONZE SOURCE LAYER TESTS")
    check("Core banking source has records", len(bronze_core) >= 500, f"Got {len(bronze_core)}")
    check("Salesforce source has records", len(bronze_sfdc) >= 500, f"Got {len(bronze_sfdc)}")
    check("Fiserv source has records", len(bronze_fiserv) >= 500, f"Got {len(bronze_fiserv)}")
    
    # Source systems should have overlapping customers (for MDM)
    total_bronze = len(bronze_core) + len(bronze_sfdc) + len(bronze_fiserv)
    check("Bronze sources have more records than gold (duplicates exist)", total_bronze > len(customers), f"Bronze: {total_bronze}, Gold: {len(customers)}")
    
    # ─── 8. Temporal Tests ───
    print("\n▶ TEMPORAL CONSISTENCY TESTS")
    # Account open dates should be after customer acquisition dates
    cust_dates = {c["customer_id"]: c["acquisition_date"] for c in customers}
    temporal_ok = True
    for a in accounts:
        acq = cust_dates.get(a["customer_id"], "2000-01-01")
        if a["open_date"] < acq:
            temporal_ok = False
            break
    check("Account open dates ≥ customer acquisition dates", temporal_ok)
    
    # ─── Summary ───
    print(f"\n{'='*60}")
    print(f"  RESULTS: {PASSED} passed, {FAILED} failed out of {PASSED+FAILED} tests")
    print(f"  Pass rate: {PASSED/(PASSED+FAILED)*100:.1f}%")
    print(f"{'='*60}\n")
    
    return 0 if FAILED == 0 else 1

if __name__ == "__main__":
    sys.exit(main())

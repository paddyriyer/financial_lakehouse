#!/usr/bin/env python3
"""
Financial Services MDM Lakehouse — Master Data Generator
=========================================================
Generates realistic sample data for a diversified financial services company.
Products: Credit Cards, Personal/Auto Loans, Savings/CD, Digital Banking.

Usage: python generate_all.py [--company "Your Company Name"]
"""
import csv, os, random, hashlib, argparse, math
from datetime import datetime, timedelta
from collections import defaultdict

# ─── Config ───
random.seed(42)
COMPANY = "Horizon Bank Holdings"  # Default, overridable
BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "..", "..", "data")

# ─── Helpers ───
def out(subdir, name):
    d = os.path.join(DATA, subdir)
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, name)

def write_csv(path, rows):
    if not rows: return
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print(f"  ✓ {os.path.basename(path):40s} → {len(rows):>6,} rows")

def uid(prefix, i): return f"{prefix}-{i:05d}"
def rdate(start, end):
    d = (end - start).days
    return start + timedelta(days=random.randint(0, max(d, 1)))
def rts(start, end):
    d = rdate(start, end)
    return d.replace(hour=random.randint(0,23), minute=random.randint(0,59), second=random.randint(0,59))

STATES = ["CA","TX","NY","FL","IL","PA","OH","GA","NC","MI","NJ","VA","WA","AZ","MA","TN","IN","MO","MD","WI","CO","MN","SC","AL","LA","KY","OR","OK","CT","UT","IA","NV","AR","MS","KS","NM","NE","ID","WV","HI","NH","ME","MT","RI","DE","SD","ND","AK","VT","WY"]
CITIES = {"CA":"San Francisco,Los Angeles,San Diego,Sacramento","TX":"Houston,Dallas,Austin,San Antonio","NY":"New York,Buffalo,Rochester,Albany","FL":"Miami,Tampa,Orlando,Jacksonville","IL":"Chicago,Springfield,Naperville","PA":"Philadelphia,Pittsburgh","OH":"Columbus,Cleveland","GA":"Atlanta,Savannah","NC":"Charlotte,Raleigh","MI":"Detroit,Grand Rapids","NJ":"Newark,Jersey City","VA":"Richmond,Virginia Beach","WA":"Seattle,Tacoma","AZ":"Phoenix,Tucson","MA":"Boston,Cambridge"}
FIRST_NAMES = ["James","Mary","Robert","Patricia","John","Jennifer","Michael","Linda","David","Elizabeth","William","Barbara","Richard","Susan","Joseph","Jessica","Thomas","Sarah","Christopher","Karen","Charles","Lisa","Daniel","Nancy","Matthew","Betty","Anthony","Margaret","Mark","Sandra","Donald","Ashley","Steven","Kimberly","Paul","Emily","Andrew","Donna","Joshua","Michelle","Kenneth","Carol","Kevin","Amanda","Brian","Dorothy","George","Melissa","Timothy","Deborah","Ronald","Stephanie","Edward","Rebecca","Jason","Sharon","Jeffrey","Laura","Ryan","Cynthia","Jacob","Kathleen","Gary","Amy","Nicholas","Angela","Eric","Shirley","Jonathan","Anna","Stephen","Brenda","Larry","Pamela","Justin","Emma","Scott","Nicole","Brandon","Helen","Benjamin","Samantha","Samuel","Katherine","Raymond","Christine","Gregory","Debra","Frank","Rachel","Alexander","Carolyn","Patrick","Janet","Jack","Catherine","Dennis","Maria","Jerry","Heather"]
LAST_NAMES = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin","Lee","Perez","Thompson","White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson","Walker","Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores","Green","Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell","Carter","Roberts","Gomez","Phillips","Evans","Turner","Diaz","Parker","Cruz","Edwards","Collins","Reyes","Stewart","Morris","Morales","Murphy","Cook","Rogers","Gutierrez","Ortiz","Morgan","Cooper","Peterson","Bailey","Reed","Kelly","Howard","Ramos","Kim","Cox","Ward","Richardson","Watson","Brooks","Chavez","Wood","James","Bennett","Gray","Mendoza","Ruiz","Hughes","Price","Alvarez","Castillo","Sanders","Patel","Myers","Long","Ross","Foster","Jimenez","Powell"]
EMAILS = ["gmail.com","yahoo.com","outlook.com","icloud.com","aol.com","hotmail.com","protonmail.com"]
CHANNELS = ["branch","web","mobile_app","phone","mail","partner_referral","social_media"]
SEGMENTS = ["mass_market","mass_affluent","affluent","high_net_worth","ultra_hnw"]
RISK_TIERS = ["super_prime","prime","near_prime","subprime","deep_subprime"]
FICO_RANGES = {"super_prime":(750,850),"prime":(700,749),"near_prime":(650,699),"subprime":(580,649),"deep_subprime":(300,579)}

# ─── Product Catalogs ───
CREDIT_CARDS = [
    {"product_id":"CC-001","name":"Horizon Venture Rewards","category":"travel","annual_fee":95,"apr_range":"17.99-25.99","rewards_rate":"3x travel, 2x dining, 1x other","signup_bonus":60000},
    {"product_id":"CC-002","name":"Horizon Unlimited Cashback","category":"cashback","annual_fee":0,"apr_range":"19.99-27.99","rewards_rate":"1.5% unlimited cashback","signup_bonus":200},
    {"product_id":"CC-003","name":"Horizon Savor Dining","category":"dining","annual_fee":0,"apr_range":"19.99-27.99","rewards_rate":"4% dining, 2% grocery, 1% other","signup_bonus":200},
    {"product_id":"CC-004","name":"Horizon Elite Travel","category":"premium_travel","annual_fee":395,"apr_range":"19.24-26.24","rewards_rate":"5x flights, 10x hotels, 2x other","signup_bonus":100000},
    {"product_id":"CC-005","name":"Horizon Spark Business","category":"business","annual_fee":0,"apr_range":"18.49-25.49","rewards_rate":"2% unlimited on business purchases","signup_bonus":500},
    {"product_id":"CC-006","name":"Horizon Secured Builder","category":"secured","annual_fee":0,"apr_range":"24.99-29.99","rewards_rate":"1% cashback on all purchases","signup_bonus":0},
    {"product_id":"CC-007","name":"Horizon Platinum Balance","category":"balance_transfer","annual_fee":0,"apr_range":"15.99-23.99","rewards_rate":"0% intro APR 15 months","signup_bonus":0},
    {"product_id":"CC-008","name":"Horizon Quicksilver Student","category":"student","annual_fee":0,"apr_range":"19.99-27.99","rewards_rate":"1.5% cashback, $50 annual credit","signup_bonus":100},
]
LOAN_PRODUCTS = [
    {"product_id":"PL-001","name":"Personal Loan Standard","category":"personal","term_months":"36,48,60","apr_range":"7.49-22.99","min_amount":1000,"max_amount":50000},
    {"product_id":"PL-002","name":"Personal Loan Jumbo","category":"personal_jumbo","term_months":"48,60,72,84","apr_range":"6.99-18.99","min_amount":25000,"max_amount":100000},
    {"product_id":"AL-001","name":"Auto Loan New Vehicle","category":"auto_new","term_months":"36,48,60,72","apr_range":"4.49-12.99","min_amount":10000,"max_amount":80000},
    {"product_id":"AL-002","name":"Auto Loan Used Vehicle","category":"auto_used","term_months":"36,48,60","apr_range":"5.49-15.99","min_amount":5000,"max_amount":50000},
    {"product_id":"AL-003","name":"Auto Refinance","category":"auto_refi","term_months":"36,48,60","apr_range":"4.99-14.49","min_amount":5000,"max_amount":75000},
]
SAVINGS_PRODUCTS = [
    {"product_id":"SA-001","name":"360 Performance Savings","category":"hisa","apy":"4.25","min_balance":0},
    {"product_id":"SA-002","name":"360 Checking","category":"checking","apy":"0.10","min_balance":0},
    {"product_id":"CD-001","name":"12-Month CD","category":"cd","apy":"4.50","min_balance":500},
    {"product_id":"CD-002","name":"18-Month CD","category":"cd","apy":"4.30","min_balance":500},
    {"product_id":"CD-003","name":"5-Year CD","category":"cd","apy":"4.00","min_balance":500},
    {"product_id":"MM-001","name":"Money Market Account","category":"money_market","apy":"4.00","min_balance":10000},
]
ALL_PRODUCTS = CREDIT_CARDS + LOAN_PRODUCTS + SAVINGS_PRODUCTS

# ─── Merchant Categories (for card transactions) ───
MCC_CATEGORIES = [
    {"mcc":"5411","category":"Grocery","avg_txn":67},
    {"mcc":"5812","category":"Restaurants","avg_txn":42},
    {"mcc":"5541","category":"Gas Stations","avg_txn":55},
    {"mcc":"5311","category":"Department Stores","avg_txn":89},
    {"mcc":"5912","category":"Pharmacy","avg_txn":34},
    {"mcc":"4511","category":"Airlines","avg_txn":380},
    {"mcc":"7011","category":"Hotels","avg_txn":210},
    {"mcc":"5732","category":"Electronics","avg_txn":156},
    {"mcc":"5691","category":"Clothing","avg_txn":72},
    {"mcc":"5814","category":"Fast Food","avg_txn":15},
    {"mcc":"7832","category":"Entertainment","avg_txn":28},
    {"mcc":"8011","category":"Medical","avg_txn":145},
    {"mcc":"5942","category":"Bookstores","avg_txn":32},
    {"mcc":"7523","category":"Parking","avg_txn":18},
    {"mcc":"4121","category":"Rideshare/Taxi","avg_txn":25},
    {"mcc":"5999","category":"Online Shopping","avg_txn":64},
]

# ─── Partners ───
PARTNERS = [
    {"partner_id":"PTR-001","name":"Costco Wholesale","type":"co_brand","category":"retail"},
    {"partner_id":"PTR-002","name":"Amazon","type":"marketplace","category":"ecommerce"},
    {"partner_id":"PTR-003","name":"Delta Airlines","type":"co_brand","category":"travel"},
    {"partner_id":"PTR-004","name":"Walmart","type":"rewards_network","category":"retail"},
    {"partner_id":"PTR-005","name":"Uber","type":"digital_partner","category":"rideshare"},
    {"partner_id":"PTR-006","name":"Whole Foods","type":"rewards_network","category":"grocery"},
    {"partner_id":"PTR-007","name":"Marriott","type":"co_brand","category":"hospitality"},
    {"partner_id":"PTR-008","name":"Apple","type":"digital_partner","category":"technology"},
    {"partner_id":"PTR-009","name":"Starbucks","type":"rewards_network","category":"dining"},
    {"partner_id":"PTR-010","name":"AutoNation","type":"dealer_network","category":"auto"},
]

# ═══════════════════════════════════════════════
# GENERATION
# ═══════════════════════════════════════════════

def gen_customers(n=2000):
    """Generate 2000 customers across source systems with intentional duplicates for MDM."""
    customers = []
    now = datetime.now()
    start = datetime(2018, 1, 1)
    
    for i in range(1, n+1):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        st = random.choice(STATES[:20])  # Focus on top 20 states
        city = random.choice(CITIES.get(st, "Springfield,Columbus,Madison").split(","))
        seg = random.choices(SEGMENTS, weights=[40,30,15,10,5])[0]
        risk = random.choices(RISK_TIERS, weights=[25,35,20,15,5])[0]
        fico_lo, fico_hi = FICO_RANGES[risk]
        fico = random.randint(fico_lo, fico_hi)
        dob = rdate(datetime(1955,1,1), datetime(2002,12,31))
        acq_date = rdate(start, now - timedelta(days=30))
        income = {"mass_market":random.randint(30000,75000),"mass_affluent":random.randint(75000,150000),"affluent":random.randint(150000,300000),"high_net_worth":random.randint(300000,750000),"ultra_hnw":random.randint(750000,5000000)}[seg]
        
        email = f"{first.lower()}.{last.lower()}{random.randint(1,99)}@{random.choice(EMAILS)}"
        phone = f"+1{random.randint(200,999)}{random.randint(1000000,9999999)}"
        
        customers.append({
            "customer_id": uid("CUST", i),
            "first_name": first,
            "last_name": last,
            "email": email,
            "phone": phone,
            "date_of_birth": dob.strftime("%Y-%m-%d"),
            "ssn_hash": hashlib.sha256(f"SSN-{i:09d}".encode()).hexdigest()[:16],
            "address_line1": f"{random.randint(100,9999)} {random.choice(['Main','Oak','Elm','Maple','Pine','Cedar','Walnut','Park','Lake','River'])} {random.choice(['St','Ave','Blvd','Dr','Ln','Way','Ct'])}",
            "city": city,
            "state": st,
            "zip_code": f"{random.randint(10000,99999)}",
            "country": "US",
            "segment": seg,
            "risk_tier": risk,
            "fico_score": fico,
            "annual_income": income,
            "employment_status": random.choices(["employed","self_employed","retired","student","unemployed"], weights=[65,15,10,5,5])[0],
            "acquisition_channel": random.choice(CHANNELS),
            "acquisition_date": acq_date.strftime("%Y-%m-%d"),
            "customer_since": acq_date.strftime("%Y-%m-%d"),
            "status": random.choices(["active","inactive","closed","suspended"], weights=[80,10,8,2])[0],
            "digital_enrolled": random.choices([True, False], weights=[75, 25])[0],
            "mobile_app_user": random.choices([True, False], weights=[60, 40])[0],
            "preferred_channel": random.choice(["mobile","web","branch","phone"]),
            "opt_in_marketing": random.choices([True, False], weights=[65, 35])[0],
            "kyc_verified": True,
            "kyc_date": (acq_date + timedelta(days=random.randint(0,14))).strftime("%Y-%m-%d"),
            "_source_system": random.choice(["core_banking","salesforce","fiserv"]),
            "_ingested_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        })
    return customers

def gen_bronze_sources(customers):
    """Create bronze-layer source system replicas with intentional mismatches for MDM."""
    core = []
    sfdc = []
    fiserv = []
    
    for c in customers[:800]:  # 800 in core banking
        core.append({
            "CIF_NUM": c["customer_id"].replace("CUST","CIF"),
            "CUST_NAME": f"{c['last_name']}, {c['first_name']}".upper(),
            "SSN_HASH": c["ssn_hash"],
            "DOB": c["date_of_birth"],
            "ADDR1": c["address_line1"].upper(),
            "CITY": c["city"].upper(),
            "STATE": c["state"],
            "ZIP": c["zip_code"],
            "PHONE": c["phone"].replace("+1",""),
            "EMAIL": c["email"],
            "ACCT_OPEN_DT": c["acquisition_date"],
            "STATUS_CD": {"active":"A","inactive":"I","closed":"C","suspended":"S"}[c["status"]],
            "FICO": c["fico_score"],
        })
    
    for c in customers[:1200]:  # 1200 in SFDC (overlap with core)
        # Introduce slight mismatches for MDM testing
        email = c["email"]
        if random.random() < 0.15:
            email = email.replace("@", f"{random.randint(1,9)}@")  # Slightly different email
        phone = c["phone"]
        if random.random() < 0.1:
            phone = phone[:-1] + str(random.randint(0,9))  # Last digit different
            
        sfdc.append({
            "AccountId": f"001{hashlib.md5(c['customer_id'].encode()).hexdigest()[:12]}",
            "FirstName": c["first_name"],
            "LastName": c["last_name"],
            "PersonEmail": email,
            "Phone": phone,
            "MailingStreet": c["address_line1"],
            "MailingCity": c["city"],
            "MailingState": c["state"],
            "MailingPostalCode": c["zip_code"],
            "Annual_Revenue__c": c["annual_income"],
            "Segment__c": c["segment"],
            "Lead_Source__c": c["acquisition_channel"],
            "CreatedDate": c["acquisition_date"],
        })
    
    for c in customers[500:1500]:  # 1000 in Fiserv (overlap zone)
        name = f"{c['first_name']} {c['last_name']}"
        if random.random() < 0.08:
            name = f"{c['first_name'][0]}. {c['last_name']}"  # Abbreviated
            
        fiserv.append({
            "PARTY_ID": f"FSV{random.randint(100000,999999)}",
            "FULL_NAME": name,
            "EMAIL_ADDR": c["email"].upper() if random.random() < 0.2 else c["email"],
            "PHONE_NUM": c["phone"],
            "STREET_ADDR": c["address_line1"],
            "CITY_NAME": c["city"],
            "STATE_CODE": c["state"],
            "POSTAL_CODE": c["zip_code"],
            "RISK_RATING": c["risk_tier"].upper(),
            "CREDIT_SCORE": c["fico_score"],
            "ONBOARD_DATE": c["acquisition_date"],
        })
    
    return core, sfdc, fiserv

def gen_accounts(customers):
    """Generate financial accounts — each customer gets 1-4 products."""
    accounts = []
    now = datetime.now()
    acct_num = 10000
    
    for c in customers:
        if c["status"] == "closed": continue
        n_products = random.choices([1,2,3,4], weights=[25,40,25,10])[0]
        held = set()
        
        for _ in range(n_products):
            # Product selection weighted by segment
            if c["segment"] in ["high_net_worth","ultra_hnw"]:
                pool = ALL_PRODUCTS
            elif c["segment"] == "affluent":
                pool = [p for p in ALL_PRODUCTS if p.get("category") != "secured"]
            else:
                pool = [p for p in ALL_PRODUCTS if p.get("category") not in ["premium_travel","personal_jumbo"]]
            
            prod = random.choice(pool)
            if prod["product_id"] in held: continue
            held.add(prod["product_id"])
            
            acct_num += 1
            open_dt = rdate(datetime.strptime(c["acquisition_date"],"%Y-%m-%d"), now - timedelta(days=10))
            
            # Balance logic by product type
            if prod["product_id"].startswith("CC"):
                credit_limit = random.choice([2000,5000,8000,10000,15000,20000,30000,50000])
                balance = round(random.uniform(0, credit_limit * 0.7), 2)
                apr = round(random.uniform(15, 28), 2)
            elif prod["product_id"].startswith(("PL","AL")):
                balance = round(random.uniform(float(prod.get("min_amount",1000)), float(prod.get("max_amount",50000))), 2)
                credit_limit = balance
                apr = round(random.uniform(4, 22), 2)
            else:  # Savings/CD/MM
                balance = round(random.uniform(500, {"mass_market":25000,"mass_affluent":100000,"affluent":500000,"high_net_worth":2000000,"ultra_hnw":10000000}[c["segment"]]), 2)
                credit_limit = 0
                apr = round(float(prod.get("apy", "4.0")), 2)
            
            accounts.append({
                "account_id": uid("ACCT", acct_num),
                "customer_id": c["customer_id"],
                "product_id": prod["product_id"],
                "product_name": prod["name"],
                "product_category": prod.get("category",""),
                "account_number": f"{''.join([str(random.randint(0,9)) for _ in range(16)])}",
                "open_date": open_dt.strftime("%Y-%m-%d"),
                "status": random.choices(["open","closed","delinquent","frozen"], weights=[85,8,5,2])[0],
                "balance": balance,
                "credit_limit": credit_limit,
                "apr": apr,
                "monthly_payment": round(balance * 0.025, 2) if prod["product_id"].startswith(("PL","AL")) else 0,
                "autopay_enrolled": random.choices([True,False], weights=[55,45])[0],
                "paperless": random.choices([True,False], weights=[70,30])[0],
                "last_activity_date": rdate(now - timedelta(days=90), now).strftime("%Y-%m-%d"),
            })
    return accounts

def gen_transactions(accounts, n=30000):
    """Generate card/account transactions."""
    txns = []
    now = datetime.now()
    cc_accounts = [a for a in accounts if a["product_id"].startswith("CC") and a["status"] == "open"]
    
    for _ in range(n):
        acct = random.choice(cc_accounts)
        mcc = random.choice(MCC_CATEGORIES)
        amt = round(random.gauss(mcc["avg_txn"], mcc["avg_txn"]*0.4), 2)
        if amt < 1: amt = round(random.uniform(1, 20), 2)
        ts = rts(now - timedelta(days=365), now)
        
        txns.append({
            "transaction_id": uid("TXN", len(txns)+1),
            "account_id": acct["account_id"],
            "customer_id": acct["customer_id"],
            "transaction_date": ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "post_date": (ts + timedelta(days=random.randint(0,2))).strftime("%Y-%m-%d"),
            "amount": abs(amt),
            "transaction_type": random.choices(["purchase","payment","refund","fee","interest","cash_advance"], weights=[70,15,5,4,4,2])[0],
            "mcc_code": mcc["mcc"],
            "merchant_category": mcc["category"],
            "merchant_name": f"{mcc['category']} Store #{random.randint(100,999)}",
            "channel": random.choices(["pos_chip","pos_contactless","online","mobile_wallet","atm"], weights=[30,25,30,10,5])[0],
            "currency": "USD",
            "rewards_earned": round(abs(amt) * random.uniform(0.01, 0.05), 2),
            "is_international": random.random() < 0.08,
            "is_disputed": random.random() < 0.02,
            "fraud_flag": random.random() < 0.008,
        })
    return txns

def gen_loan_payments(accounts):
    """Generate loan payment history."""
    payments = []
    now = datetime.now()
    loan_accts = [a for a in accounts if a["product_id"].startswith(("PL","AL")) and a["status"] != "closed"]
    
    for acct in loan_accts:
        open_dt = datetime.strptime(acct["open_date"], "%Y-%m-%d")
        payment_amt = acct["monthly_payment"]
        if payment_amt <= 0: continue
        
        d = open_dt + timedelta(days=30)
        while d < now:
            status = random.choices(["on_time","late_1_15","late_16_30","late_31_60","missed"], weights=[82,8,4,3,3])[0]
            actual_amt = payment_amt if status != "missed" else 0
            if status.startswith("late"):
                actual_amt = round(payment_amt * random.uniform(0.5, 1.0), 2)
            
            payments.append({
                "payment_id": uid("PMT", len(payments)+1),
                "account_id": acct["account_id"],
                "customer_id": acct["customer_id"],
                "due_date": d.strftime("%Y-%m-%d"),
                "payment_date": (d + timedelta(days={"on_time":random.randint(-5,0),"late_1_15":random.randint(1,15),"late_16_30":random.randint(16,30),"late_31_60":random.randint(31,60),"missed":0}[status])).strftime("%Y-%m-%d") if status != "missed" else "",
                "amount_due": round(payment_amt, 2),
                "amount_paid": round(actual_amt, 2),
                "payment_status": status,
                "payment_method": random.choice(["ach","debit_card","check","auto_pay"]),
                "principal_portion": round(actual_amt * 0.6, 2),
                "interest_portion": round(actual_amt * 0.4, 2),
            })
            d += timedelta(days=30)
    return payments

def gen_digital_events(customers, n=40000):
    """Generate digital banking / mobile app events."""
    events = []
    now = datetime.now()
    digital_custs = [c for c in customers if c["digital_enrolled"] and c["status"] == "active"]
    
    pages = [
        "/dashboard","/accounts","/transfer","/pay-bill","/rewards","/credit-score",
        "/apply/credit-card","/apply/loan","/statements","/settings","/support",
        "/invest","/auto-pay","/mobile-deposit","/card-controls","/alerts",
        "/spend-insights","/budgets","/savings-goals","/offers"
    ]
    
    for _ in range(n):
        cust = random.choice(digital_custs)
        ts = rts(now - timedelta(days=180), now)
        session = hashlib.md5(f"{cust['customer_id']}-{ts.strftime('%Y%m%d%H')}".encode()).hexdigest()[:12]
        
        events.append({
            "event_id": uid("EVT", len(events)+1),
            "customer_id": cust["customer_id"],
            "session_id": f"sess_{session}",
            "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "event_type": random.choices(["page_view","click","form_submit","api_call","error","feature_toggle"], weights=[40,25,15,10,5,5])[0],
            "page_url": random.choice(pages),
            "platform": "mobile_app" if cust["mobile_app_user"] and random.random() < 0.65 else "web",
            "device_type": random.choices(["ios","android","desktop","tablet"], weights=[35,30,25,10])[0],
            "os_version": random.choice(["iOS 17","iOS 18","Android 14","Android 15","Windows 11","macOS 14"]),
            "app_version": random.choice(["8.1.0","8.2.0","8.3.0","8.4.0","9.0.0"]),
            "screen_name": random.choice(pages).replace("/","").replace("-","_"),
            "duration_seconds": random.randint(2, 180),
            "referrer": random.choices(["direct","push_notification","email","search","social","partner_link"], weights=[35,20,15,15,10,5])[0],
            "conversion_event": random.random() < 0.03,
            "error_code": f"ERR_{random.randint(400,599)}" if random.random() < 0.02 else "",
            "geo_lat": round(random.uniform(25, 48), 4),
            "geo_lon": round(random.uniform(-122, -71), 4),
        })
    return events

def gen_fraud_alerts(transactions):
    """Generate fraud/AML alerts from transactions."""
    alerts = []
    flagged = [t for t in transactions if t["fraud_flag"] or t["amount"] > 500]
    
    for t in flagged[:800]:
        severity = random.choices(["critical","high","medium","low"], weights=[10,25,40,25])[0]
        alert_type = random.choices([
            "velocity_spike","geographic_anomaly","large_purchase","card_not_present_high_risk",
            "new_merchant_high_amount","international_unusual","multiple_declines","account_takeover_attempt",
            "structuring_pattern","unusual_time_pattern"
        ], weights=[15,12,15,12,10,8,8,8,6,6])[0]
        
        alerts.append({
            "alert_id": uid("FRD", len(alerts)+1),
            "transaction_id": t["transaction_id"],
            "account_id": t["account_id"],
            "customer_id": t["customer_id"],
            "alert_timestamp": t["transaction_date"],
            "alert_type": alert_type,
            "severity": severity,
            "risk_score": round(random.uniform(0.3, 1.0), 3),
            "amount": t["amount"],
            "merchant_category": t["merchant_category"],
            "detection_method": random.choice(["ml_model","rules_engine","velocity_check","geo_fence","network_analysis"]),
            "model_version": random.choice(["fraud_v3.2","fraud_v3.3","aml_v2.1"]),
            "status": random.choices(["open","investigating","confirmed_fraud","false_positive","closed"], weights=[15,20,10,40,15])[0],
            "assigned_to": f"analyst_{random.randint(1,20):03d}",
            "resolution_date": (datetime.strptime(t["transaction_date"][:10],"%Y-%m-%d") + timedelta(days=random.randint(1,30))).strftime("%Y-%m-%d") if random.random() > 0.3 else "",
            "loss_amount": round(t["amount"] * random.uniform(0, 1), 2) if random.random() < 0.1 else 0,
        })
    return alerts

def gen_partner_performance():
    """Generate partner/merchant performance data."""
    rows = []
    now = datetime.now()
    for partner in PARTNERS:
        for month_offset in range(12):
            m = now - timedelta(days=30 * month_offset)
            rows.append({
                "partner_id": partner["partner_id"],
                "partner_name": partner["name"],
                "partner_type": partner["type"],
                "partner_category": partner["category"],
                "month": m.strftime("%Y-%m"),
                "total_transactions": random.randint(5000, 150000),
                "total_spend": round(random.uniform(500000, 25000000), 2),
                "interchange_revenue": round(random.uniform(10000, 500000), 2),
                "rewards_cost": round(random.uniform(5000, 200000), 2),
                "new_accounts_sourced": random.randint(50, 2000),
                "active_cardholders": random.randint(10000, 500000),
                "avg_transaction_value": round(random.uniform(25, 200), 2),
                "customer_satisfaction": round(random.uniform(3.5, 4.9), 1),
                "contract_status": "active",
                "revenue_share_pct": round(random.uniform(0.5, 3.0), 2),
            })
    return rows

def gen_credit_risk_snapshot(customers, accounts):
    """Generate credit risk / delinquency snapshot."""
    rows = []
    now = datetime.now()
    
    for c in customers:
        if c["status"] == "closed": continue
        cust_accts = [a for a in accounts if a["customer_id"] == c["customer_id"]]
        total_balance = sum(a["balance"] for a in cust_accts)
        total_credit = sum(a["credit_limit"] for a in cust_accts if a["credit_limit"] > 0)
        
        dpd = 0
        if c["risk_tier"] in ["subprime","deep_subprime"]:
            dpd = random.choices([0,30,60,90,120,150], weights=[60,15,10,8,5,2])[0]
        elif c["risk_tier"] == "near_prime":
            dpd = random.choices([0,30,60,90], weights=[80,12,5,3])[0]
        else:
            dpd = random.choices([0,30,60], weights=[95,4,1])[0]
        
        rows.append({
            "customer_id": c["customer_id"],
            "snapshot_date": now.strftime("%Y-%m-%d"),
            "fico_score": c["fico_score"],
            "risk_tier": c["risk_tier"],
            "segment": c["segment"],
            "total_balance": round(total_balance, 2),
            "total_credit_limit": round(total_credit, 2),
            "utilization_pct": round((total_balance / total_credit * 100) if total_credit > 0 else 0, 1),
            "num_products": len(cust_accts),
            "days_past_due": dpd,
            "delinquency_status": {0:"current",30:"dpd_30",60:"dpd_60",90:"dpd_90"}.get(dpd, f"dpd_{dpd}"),
            "probability_of_default": round(min(dpd / 500 + random.uniform(0, 0.05), 1.0), 4),
            "loss_given_default": round(random.uniform(0.3, 0.8), 3),
            "expected_loss": round(total_balance * min(dpd / 500, 0.5) * random.uniform(0.3, 0.8), 2),
            "behavioral_score": random.randint(300, 850),
            "months_on_book": (now - datetime.strptime(c["acquisition_date"], "%Y-%m-%d")).days // 30,
        })
    return rows

def gen_realtime_metrics(n_hours=336):
    """Generate hourly real-time metrics (2 weeks)."""
    rows = []
    now = datetime.now()
    for h in range(n_hours):
        ts = now - timedelta(hours=h)
        hour = ts.hour
        # Simulate daily patterns
        activity_mult = 0.3 + 0.7 * math.sin(math.pi * (hour - 6) / 12) if 6 <= hour <= 22 else 0.2
        
        rows.append({
            "timestamp": ts.strftime("%Y-%m-%dT%H:00:00Z"),
            "active_digital_users": int(random.gauss(45000 * activity_mult, 5000)),
            "transactions_per_hour": int(random.gauss(12000 * activity_mult, 2000)),
            "card_approvals_per_hour": int(random.gauss(800 * activity_mult, 150)),
            "card_declines_per_hour": int(random.gauss(120 * activity_mult, 30)),
            "loan_apps_per_hour": int(random.gauss(200 * activity_mult, 40)),
            "fraud_alerts_per_hour": int(random.gauss(15, 5)),
            "api_latency_ms": int(random.gauss(180, 40)),
            "api_error_rate_pct": round(random.uniform(0.01, 0.5), 3),
            "mobile_app_crashes": int(random.gauss(3, 2)),
            "nps_score": round(random.gauss(72, 5), 1),
            "avg_transaction_amount": round(random.gauss(67, 15), 2),
            "total_deposits_hourly": round(random.gauss(2500000 * activity_mult, 500000), 2),
            "total_withdrawals_hourly": round(random.gauss(1800000 * activity_mult, 400000), 2),
            "rewards_redeemed_hourly": round(random.gauss(50000 * activity_mult, 10000), 2),
        })
    return rows

def gen_mdm_match_pairs(customers):
    """Generate MDM fuzzy match results."""
    pairs = []
    # Create candidate pairs from customers who might be duplicates
    for i in range(400):
        c1_idx = random.randint(0, len(customers)-1)
        c2_idx = random.randint(0, len(customers)-1)
        if c1_idx == c2_idx: continue
        c1, c2 = customers[c1_idx], customers[c2_idx]
        
        # Simulate match scores
        same_last = c1["last_name"] == c2["last_name"]
        name_score = random.uniform(0.85, 0.99) if same_last else random.uniform(0.1, 0.6)
        email_score = 1.0 if c1["email"] == c2["email"] else random.uniform(0.0, 0.3)
        phone_score = random.uniform(0.7, 1.0) if c1["phone"][:8] == c2["phone"][:8] else random.uniform(0.0, 0.3)
        addr_score = random.uniform(0.5, 0.95) if c1["state"] == c2["state"] else random.uniform(0.0, 0.4)
        xsys_score = random.uniform(0.0, 0.2)
        
        composite = round(name_score * 0.30 + email_score * 0.25 + phone_score * 0.20 + addr_score * 0.15 + xsys_score * 0.10, 4)
        
        if composite < 0.3: continue  # Skip obvious non-matches
        
        tier = "auto_merge" if composite >= 0.92 else ("review" if composite >= 0.75 else "no_match")
        
        pairs.append({
            "pair_id": uid("MPR", len(pairs)+1),
            "customer_id_1": c1["customer_id"],
            "source_system_1": c1["_source_system"],
            "customer_id_2": c2["customer_id"],
            "source_system_2": c2["_source_system"],
            "name_score": round(name_score, 4),
            "email_score": round(email_score, 4),
            "phone_score": round(phone_score, 4),
            "address_score": round(addr_score, 4),
            "cross_system_score": round(xsys_score, 4),
            "composite_score": composite,
            "match_tier": tier,
            "match_decision": random.choices(["merge","review","reject","pending"], weights=[40,25,25,10])[0] if tier != "no_match" else "reject",
            "decided_by": "system" if tier == "auto_merge" else ("steward" if random.random() < 0.6 else "pending"),
            "decided_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") if random.random() > 0.2 else "",
        })
    return pairs

def gen_dim_date():
    """Generate date dimension."""
    rows = []
    start = datetime(2023, 1, 1)
    for i in range(1095):  # 3 years
        d = start + timedelta(days=i)
        rows.append({
            "date_key": d.strftime("%Y-%m-%d"),
            "year": d.year,
            "quarter": (d.month - 1) // 3 + 1,
            "month": d.month,
            "month_name": d.strftime("%B"),
            "week": d.isocalendar()[1],
            "day_of_week": d.strftime("%A"),
            "is_weekend": d.weekday() >= 5,
            "is_holiday": d.month == 12 and d.day == 25,
            "fiscal_year": d.year if d.month >= 10 else d.year - 1,
            "fiscal_quarter": ((d.month - 10) % 12) // 3 + 1,
        })
    return rows

# ═══════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--company", default=COMPANY)
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"  {args.company} — MDM Lakehouse Data Generator")
    print(f"{'='*60}\n")
    
    # 1. Customers
    print("▶ Generating customers...")
    customers = gen_customers(2000)
    write_csv(out("gold", "dim_customer.csv"), customers)
    
    # 2. Bronze sources
    print("\n▶ Generating bronze source systems...")
    core, sfdc, fiserv = gen_bronze_sources(customers)
    write_csv(out("bronze", "core_banking_customers.csv"), core)
    write_csv(out("bronze", "salesforce_accounts.csv"), sfdc)
    write_csv(out("bronze", "fiserv_parties.csv"), fiserv)
    
    # 3. Accounts
    print("\n▶ Generating financial accounts...")
    accounts = gen_accounts(customers)
    write_csv(out("gold", "dim_account.csv"), accounts)
    
    # 4. Products — normalize to common schema
    print("\n▶ Writing product catalog...")
    all_keys = set()
    for p in ALL_PRODUCTS: all_keys.update(p.keys())
    normalized = [{k: p.get(k, "") for k in sorted(all_keys)} for p in ALL_PRODUCTS]
    write_csv(out("gold", "dim_product.csv"), normalized)
    
    # 5. Transactions
    print("\n▶ Generating card transactions...")
    txns = gen_transactions(accounts, 30000)
    write_csv(out("gold", "fact_transactions.csv"), txns)
    
    # 6. Loan payments
    print("\n▶ Generating loan payment history...")
    payments = gen_loan_payments(accounts)
    write_csv(out("gold", "fact_loan_payments.csv"), payments)
    
    # 7. Digital events
    print("\n▶ Generating digital/mobile events...")
    events = gen_digital_events(customers, 40000)
    write_csv(out("clickstream", "digital_events.csv"), events)
    
    # 8. Fraud alerts
    print("\n▶ Generating fraud/AML alerts...")
    alerts = gen_fraud_alerts(txns)
    write_csv(out("fraud", "fraud_alerts.csv"), alerts)
    
    # 9. Partners
    print("\n▶ Generating partner performance...")
    partners = gen_partner_performance()
    write_csv(out("partners", "partner_performance.csv"), partners)
    
    # 10. Credit risk
    print("\n▶ Generating credit risk snapshot...")
    risk = gen_credit_risk_snapshot(customers, accounts)
    write_csv(out("gold", "fact_credit_risk.csv"), risk)
    
    # 11. Real-time metrics
    print("\n▶ Generating real-time metrics...")
    metrics = gen_realtime_metrics(336)
    write_csv(out("realtime", "hourly_metrics.csv"), metrics)
    
    # 12. MDM match pairs
    print("\n▶ Generating MDM match pairs...")
    pairs = gen_mdm_match_pairs(customers)
    write_csv(out("mdm", "mdm_match_pairs.csv"), pairs)
    
    # 13. Date dimension
    print("\n▶ Generating date dimension...")
    dates = gen_dim_date()
    write_csv(out("gold", "dim_date.csv"), dates)
    
    # Summary
    total = len(customers) + len(core) + len(sfdc) + len(fiserv) + len(accounts) + len(ALL_PRODUCTS) + len(txns) + len(payments) + len(events) + len(alerts) + len(partners) + len(risk) + len(metrics) + len(pairs) + len(dates)
    
    print(f"\n{'='*60}")
    print(f"  GENERATION COMPLETE")
    print(f"  Company: {args.company}")
    print(f"  Total records: {total:,}")
    print(f"  CSV files: {sum(1 for r,d,f in os.walk(DATA) for fi in f if fi.endswith('.csv'))}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()

import { useState, useMemo } from "react";
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ComposedChart, Legend } from "recharts";

// ─── Color System ───
const C = {
  navy: "#0F172A", dark: "#1E293B", slate: "#334155", med: "#64748B", light: "#94A3B8",
  bg: "#F8FAFC", white: "#FFFFFF", amber: "#D97706", amberL: "#FEF3C7",
  teal: "#0D9488", tealL: "#CCFBF1", green: "#059669", greenL: "#D1FAE5",
  red: "#DC2626", redL: "#FEE2E2", blue: "#2563EB", blueL: "#DBEAFE",
  purple: "#7C3AED", purpleL: "#EDE9FE", cyan: "#0891B2",
};
const CHART_COLORS = [C.blue, C.teal, C.amber, C.purple, C.red, C.green, C.cyan, "#EC4899"];

// ─── Sample Data Generators ───
const months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
const revenueData = months.map((m,i) => ({
  month: m,
  interest: 42+Math.random()*15,
  fees: 12+Math.random()*5,
  interchange: 8+Math.random()*3,
  net: 35+Math.random()*12,
}));

const segmentData = [
  {name:"Mass Market",customers:840,revenue:28.5,products:1.8,color:C.blue},
  {name:"Mass Affluent",customers:620,revenue:42.3,products:2.4,color:C.teal},
  {name:"Affluent",customers:310,revenue:68.7,products:3.1,color:C.amber},
  {name:"HNW",customers:180,revenue:125.4,products:3.8,color:C.purple},
  {name:"Ultra HNW",customers:50,revenue:340.2,products:4.2,color:C.green},
];

const productPerf = [
  {product:"Venture Rewards",accounts:12500,spend:185,growth:12.3,nps:78},
  {product:"Unlimited Cash",accounts:28400,spend:92,growth:18.7,nps:72},
  {product:"Savor Dining",accounts:8200,spend:64,growth:22.1,nps:81},
  {product:"Elite Travel",accounts:3100,spend:420,growth:8.5,nps:85},
  {product:"Spark Business",accounts:5600,spend:210,growth:15.2,nps:74},
  {product:"Personal Loan",accounts:9800,balance:35200,growth:9.8,nps:68},
  {product:"Auto Loan New",accounts:7200,balance:28500,growth:6.4,nps:71},
  {product:"360 Savings",accounts:45000,balance:125000,growth:32.5,nps:82},
  {product:"12-Month CD",accounts:12000,balance:89000,growth:28.1,nps:76},
];

const riskDistrib = [
  {tier:"Super Prime",count:500,pct:25,dpd30:0.8,dpd60:0.2,dpd90:0.1,color:C.green},
  {tier:"Prime",count:700,pct:35,dpd30:2.1,dpd60:0.8,dpd90:0.3,color:C.teal},
  {tier:"Near Prime",count:400,pct:20,dpd30:5.4,dpd60:2.1,dpd90:1.2,color:C.amber},
  {tier:"Subprime",count:300,pct:15,dpd30:12.3,dpd60:5.8,dpd90:3.4,color:"#F59E0B"},
  {tier:"Deep Subprime",count:100,pct:5,dpd30:22.1,dpd60:12.4,dpd90:8.7,color:C.red},
];

const digitalData = months.map((m,i) => ({
  month: m,
  mobileUsers: 32000+i*2800+Math.random()*3000,
  webUsers: 18000+i*800+Math.random()*2000,
  branchVisits: 12000-i*400+Math.random()*1000,
}));

const fraudData = months.map((m,i) => ({
  month: m,
  alerts: 45+Math.random()*25,
  confirmed: 8+Math.random()*6,
  falsePositive: 28+Math.random()*15,
  lossAmount: 120000+Math.random()*80000,
}));

const partnerData = [
  {partner:"Costco",txns:142000,spend:18.5,interchange:324,satisfaction:4.6},
  {partner:"Amazon",txns:285000,spend:24.2,interchange:423,satisfaction:4.3},
  {partner:"Delta",txns:38000,spend:14.4,interchange:252,satisfaction:4.7},
  {partner:"Walmart",txns:198000,spend:12.8,interchange:224,satisfaction:4.1},
  {partner:"Uber",txns:165000,spend:4.1,interchange:72,satisfaction:4.2},
  {partner:"Marriott",txns:28000,spend:8.9,interchange:156,satisfaction:4.8},
  {partner:"Starbucks",txns:320000,spend:3.2,interchange:56,satisfaction:4.5},
];

const dqMetrics = {
  overallScore: 96.8,
  matchRate: 94.2,
  goldenCoverage: 97.5,
  freshnessHrs: 2.3,
  completeness: 98.1,
  accuracy: 97.3,
  consistency: 95.8,
  timeliness: 96.4,
  sources: [
    {name:"Core Banking",records:800,matched:762,quality:97.2},
    {name:"Salesforce",records:1200,matched:1128,quality:95.8},
    {name:"Fiserv",records:1000,matched:934,quality:94.2},
  ],
};

const acquisitionFunnel = [
  {stage:"Website Visits",count:850000,rate:100},
  {stage:"Started Application",count:125000,rate:14.7},
  {stage:"Completed App",count:68000,rate:8.0},
  {stage:"Approved",count:42000,rate:4.9},
  {stage:"Funded/Activated",count:28500,rate:3.4},
];

const channelCAC = [
  {channel:"Paid Search",cac:145,volume:8200,ltv:2400,roi:16.5},
  {channel:"Social Media",cac:89,volume:5400,ltv:1800,roi:20.2},
  {channel:"Direct Mail",cac:210,volume:3800,ltv:3200,roi:15.2},
  {channel:"Partner Referral",cac:62,volume:4200,ltv:2800,roi:45.2},
  {channel:"Branch Walk-in",cac:180,volume:2100,ltv:3800,roi:21.1},
  {channel:"Organic/SEO",cac:28,volume:6800,ltv:2200,roi:78.6},
];

const hourlyMetrics = Array.from({length:24},(_,h) => ({
  hour: `${h}:00`,
  users: Math.round(45000 * (0.3+0.7*Math.sin(Math.PI*(h-6)/12)) * (h>=6&&h<=22?1:0.3)),
  txns: Math.round(12000 * (0.3+0.7*Math.sin(Math.PI*(h-6)/12)) * (h>=6&&h<=22?1:0.3)),
  alerts: Math.round(3+Math.random()*8),
}));

// ─── Components ───
const KPI = ({label, value, sub, trend, color=C.blue}) => (
  <div className="bg-white rounded-lg p-4 shadow-sm border border-slate-100">
    <div className="text-xs font-medium text-slate-500 uppercase tracking-wide">{label}</div>
    <div className="text-2xl font-bold mt-1" style={{color}}>{value}</div>
    <div className="flex items-center mt-1 gap-1">
      {trend && <span className={`text-xs font-medium ${trend>0?'text-emerald-600':'text-red-500'}`}>{trend>0?'↑':'↓'} {Math.abs(trend)}%</span>}
      {sub && <span className="text-xs text-slate-400">{sub}</span>}
    </div>
  </div>
);

const SectionTitle = ({children, sub}) => (
  <div className="mb-4">
    <h2 className="text-lg font-bold text-slate-800">{children}</h2>
    {sub && <p className="text-xs text-slate-500 mt-0.5">{sub}</p>}
  </div>
);

const Badge = ({children, color=C.blue}) => (
  <span className="inline-block px-2 py-0.5 rounded-full text-xs font-medium text-white" style={{backgroundColor:color}}>{children}</span>
);

const MiniBar = ({value, max=100, color=C.blue}) => (
  <div className="w-full bg-slate-100 rounded-full h-2">
    <div className="h-2 rounded-full transition-all" style={{width:`${(value/max)*100}%`, backgroundColor:color}} />
  </div>
);

const fmt = (n, prefix="") => {
  if (n >= 1e9) return `${prefix}${(n/1e9).toFixed(1)}B`;
  if (n >= 1e6) return `${prefix}${(n/1e6).toFixed(1)}M`;
  if (n >= 1e3) return `${prefix}${(n/1e3).toFixed(1)}K`;
  return `${prefix}${typeof n === 'number' ? n.toFixed(n%1?1:0) : n}`;
};

// ─── Tab Panels ───
const ExecutivePulse = () => (
  <div>
    <SectionTitle sub="Real-time operational snapshot — Horizon Bank Holdings">Executive Pulse</SectionTitle>
    <div className="grid grid-cols-5 gap-3 mb-6">
      <KPI label="Assets Under Mgmt" value="$14.2B" trend={8.3} sub="vs last quarter" color={C.blue} />
      <KPI label="Active Accounts" value="124.8K" trend={12.1} sub="vs last year" color={C.teal} />
      <KPI label="Net Promoter Score" value="74" trend={3.2} sub="pts improvement" color={C.green} />
      <KPI label="30+ DPD Rate" value="3.8%" trend={-0.4} sub="improving" color={C.amber} />
      <KPI label="Digital Adoption" value="72.4%" trend={6.8} sub="mobile + web" color={C.purple} />
    </div>
    <div className="grid grid-cols-2 gap-4">
      <div className="bg-white rounded-lg p-4 shadow-sm border border-slate-100">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">Revenue Trend ($M)</h3>
        <ResponsiveContainer width="100%" height={200}>
          <AreaChart data={revenueData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="month" tick={{fontSize:10}} stroke="#94A3B8" />
            <YAxis tick={{fontSize:10}} stroke="#94A3B8" />
            <Tooltip contentStyle={{fontSize:11}} />
            <Area type="monotone" dataKey="interest" stackId="1" fill={C.blue} stroke={C.blue} fillOpacity={0.6} name="Interest" />
            <Area type="monotone" dataKey="fees" stackId="1" fill={C.teal} stroke={C.teal} fillOpacity={0.6} name="Fees" />
            <Area type="monotone" dataKey="interchange" stackId="1" fill={C.amber} stroke={C.amber} fillOpacity={0.6} name="Interchange" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
      <div className="bg-white rounded-lg p-4 shadow-sm border border-slate-100">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">Today's Activity (Hourly)</h3>
        <ResponsiveContainer width="100%" height={200}>
          <ComposedChart data={hourlyMetrics}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="hour" tick={{fontSize:9}} interval={3} stroke="#94A3B8" />
            <YAxis yAxisId="left" tick={{fontSize:10}} stroke="#94A3B8" />
            <YAxis yAxisId="right" orientation="right" tick={{fontSize:10}} stroke="#94A3B8" />
            <Tooltip contentStyle={{fontSize:11}} />
            <Bar yAxisId="left" dataKey="users" fill={C.blue} opacity={0.7} name="Active Users" />
            <Line yAxisId="right" type="monotone" dataKey="txns" stroke={C.amber} strokeWidth={2} dot={false} name="Transactions" />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  </div>
);

const RevenueTab = () => (
  <div>
    <SectionTitle sub="Interest income, fee income, net margin by product line">Revenue & Profitability</SectionTitle>
    <div className="grid grid-cols-4 gap-3 mb-6">
      <KPI label="Total Revenue" value="$748M" trend={11.2} sub="YTD" color={C.blue} />
      <KPI label="Interest Income" value="$512M" trend={8.7} sub="net interest margin 3.42%" color={C.teal} />
      <KPI label="Fee Income" value="$148M" trend={15.3} sub="interchange + annual fees" color={C.amber} />
      <KPI label="Net Income" value="$186M" trend={9.8} sub="24.9% net margin" color={C.green} />
    </div>
    <div className="grid grid-cols-2 gap-4">
      <div className="bg-white rounded-lg p-4 shadow-sm border border-slate-100">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">Monthly Revenue Mix ($M)</h3>
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={revenueData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="month" tick={{fontSize:10}} stroke="#94A3B8" />
            <YAxis tick={{fontSize:10}} stroke="#94A3B8" />
            <Tooltip contentStyle={{fontSize:11}} />
            <Legend wrapperStyle={{fontSize:11}} />
            <Bar dataKey="interest" fill={C.blue} name="Interest" stackId="a" />
            <Bar dataKey="fees" fill={C.teal} name="Fees" stackId="a" />
            <Bar dataKey="interchange" fill={C.amber} name="Interchange" stackId="a" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="bg-white rounded-lg p-4 shadow-sm border border-slate-100">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">Revenue by Segment</h3>
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={segmentData} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis type="number" tick={{fontSize:10}} stroke="#94A3B8" />
            <YAxis dataKey="name" type="category" tick={{fontSize:10}} width={85} stroke="#94A3B8" />
            <Tooltip contentStyle={{fontSize:11}} formatter={(v)=>`$${v}M`} />
            <Bar dataKey="revenue" fill={C.blue} name="Revenue ($M)">
              {segmentData.map((s,i)=> <Cell key={i} fill={s.color} />)}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  </div>
);

const Customer360 = () => {
  const [selected, setSelected] = useState(0);
  const cust = [
    {id:"CUST-00042",name:"Sarah Johnson",seg:"Affluent",fico:782,products:4,ltv:"$12,400",risk:"Prime",since:"2019",digital:true},
    {id:"CUST-00187",name:"Michael Chen",seg:"HNW",fico:810,products:5,ltv:"$28,900",risk:"Super Prime",since:"2017",digital:true},
    {id:"CUST-00523",name:"Maria Garcia",seg:"Mass Affluent",fico:720,products:3,ltv:"$6,800",risk:"Prime",since:"2021",digital:true},
  ];
  const c = cust[selected];
  return (
    <div>
      <SectionTitle sub="Unified golden record view — product holdings, LTV, risk profile">Customer 360</SectionTitle>
      <div className="flex gap-2 mb-4">
        {cust.map((cu,i) => (
          <button key={i} onClick={()=>setSelected(i)} className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${i===selected?'bg-blue-600 text-white':'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'}`}>
            {cu.name}
          </button>
        ))}
      </div>
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white rounded-lg p-4 shadow-sm border border-slate-100 col-span-1">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-lg" style={{backgroundColor:C.blue}}>{c.name.split(' ').map(n=>n[0]).join('')}</div>
            <div>
              <div className="font-bold text-slate-800">{c.name}</div>
              <div className="text-xs text-slate-500">{c.id}</div>
            </div>
          </div>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between"><span className="text-slate-500">Segment</span><Badge color={C.purple}>{c.seg}</Badge></div>
            <div className="flex justify-between"><span className="text-slate-500">FICO Score</span><span className="font-bold text-slate-800">{c.fico}</span></div>
            <div className="flex justify-between"><span className="text-slate-500">Risk Tier</span><Badge color={C.green}>{c.risk}</Badge></div>
            <div className="flex justify-between"><span className="text-slate-500">Products Held</span><span className="font-bold">{c.products}</span></div>
            <div className="flex justify-between"><span className="text-slate-500">Lifetime Value</span><span className="font-bold text-emerald-600">{c.ltv}</span></div>
            <div className="flex justify-between"><span className="text-slate-500">Customer Since</span><span>{c.since}</span></div>
            <div className="flex justify-between"><span className="text-slate-500">Digital</span><span>{c.digital?'✓ Enrolled':'—'}</span></div>
          </div>
        </div>
        <div className="bg-white rounded-lg p-4 shadow-sm border border-slate-100 col-span-2">
          <h3 className="text-sm font-semibold text-slate-700 mb-3">Product Holdings & Activity</h3>
          <div className="space-y-3">
            {[
              {prod:"Venture Rewards Card",bal:"$4,280",limit:"$15,000",util:28.5,status:"Active"},
              {prod:"360 Performance Savings",bal:"$48,200",limit:"-",util:0,status:"Active"},
              {prod:"Auto Loan (2023 Tesla)",bal:"$32,100",limit:"$45,000",util:71.3,status:"Current"},
              {prod:"12-Month CD",bal:"$25,000",limit:"-",util:0,status:"Locked"},
            ].slice(0, c.products).map((p,i) => (
              <div key={i} className="flex items-center gap-4 p-2 rounded-lg bg-slate-50">
                <div className="flex-1">
                  <div className="text-sm font-medium text-slate-800">{p.prod}</div>
                  <div className="text-xs text-slate-500">Balance: {p.bal} {p.limit!=="-"?`/ Limit: ${p.limit}`:""}</div>
                </div>
                {p.util > 0 && <div className="w-24"><MiniBar value={p.util} color={p.util>80?C.red:p.util>50?C.amber:C.green} /></div>}
                <Badge color={p.status==="Active"?C.green:p.status==="Current"?C.teal:C.blue}>{p.status}</Badge>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

const AcquisitionTab = () => (
  <div>
    <SectionTitle sub="CAC by channel, conversion funnel, campaign ROI">Customer Acquisition</SectionTitle>
    <div className="grid grid-cols-4 gap-3 mb-6">
      <KPI label="New Accounts (MTD)" value="4,280" trend={14.2} color={C.blue} />
      <KPI label="Avg CAC" value="$118" trend={-8.3} sub="improving" color={C.green} />
      <KPI label="Conversion Rate" value="3.4%" trend={0.6} sub="app → funded" color={C.teal} />
      <KPI label="Blended LTV:CAC" value="22.4x" trend={2.1} color={C.purple} />
    </div>
    <div className="grid grid-cols-2 gap-4">
      <div className="bg-white rounded-lg p-4 shadow-sm border border-slate-100">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">Acquisition Funnel</h3>
        <div className="space-y-2">
          {acquisitionFunnel.map((s,i) => (
            <div key={i}>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-slate-600">{s.stage}</span>
                <span className="font-bold">{fmt(s.count)} <span className="text-slate-400">({s.rate}%)</span></span>
              </div>
              <MiniBar value={s.rate} color={CHART_COLORS[i]} />
            </div>
          ))}
        </div>
      </div>
      <div className="bg-white rounded-lg p-4 shadow-sm border border-slate-100">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">CAC & ROI by Channel</h3>
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={channelCAC}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="channel" tick={{fontSize:9}} stroke="#94A3B8" />
            <YAxis tick={{fontSize:10}} stroke="#94A3B8" />
            <Tooltip contentStyle={{fontSize:11}} />
            <Bar dataKey="cac" fill={C.red} name="CAC ($)" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  </div>
);

const CreditRiskTab = () => (
  <div>
    <SectionTitle sub="30/60/90 DPD rates, risk tier distribution, expected losses">Credit Risk & Delinquency</SectionTitle>
    <div className="grid grid-cols-5 gap-3 mb-6">
      <KPI label="30+ DPD Rate" value="3.8%" trend={-0.4} sub="improving" color={C.amber} />
      <KPI label="60+ DPD Rate" value="1.6%" trend={-0.2} color={C.amber} />
      <KPI label="90+ DPD Rate" value="0.9%" trend={-0.1} color={C.red} />
      <KPI label="Net Charge-Offs" value="$18.2M" trend={-5.3} sub="YTD" color={C.red} />
      <KPI label="Loss Reserves" value="$124M" sub="1.8% of portfolio" color={C.blue} />
    </div>
    <div className="grid grid-cols-2 gap-4">
      <div className="bg-white rounded-lg p-4 shadow-sm border border-slate-100">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">Risk Tier Distribution</h3>
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={riskDistrib}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="tier" tick={{fontSize:9}} stroke="#94A3B8" />
            <YAxis tick={{fontSize:10}} stroke="#94A3B8" />
            <Tooltip contentStyle={{fontSize:11}} />
            <Bar dataKey="count" name="Customers">
              {riskDistrib.map((r,i) => <Cell key={i} fill={r.color} />)}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="bg-white rounded-lg p-4 shadow-sm border border-slate-100">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">Delinquency by Risk Tier (%)</h3>
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={riskDistrib}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="tier" tick={{fontSize:9}} stroke="#94A3B8" />
            <YAxis tick={{fontSize:10}} stroke="#94A3B8" />
            <Tooltip contentStyle={{fontSize:11}} />
            <Legend wrapperStyle={{fontSize:10}} />
            <Bar dataKey="dpd30" fill={C.amber} name="30 DPD %" />
            <Bar dataKey="dpd60" fill="#F59E0B" name="60 DPD %" />
            <Bar dataKey="dpd90" fill={C.red} name="90 DPD %" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  </div>
);

const ProductTab = () => (
  <div>
    <SectionTitle sub="Card spend velocity, loan origination, deposit growth, rewards">Product Performance</SectionTitle>
    <div className="grid grid-cols-4 gap-3 mb-6">
      <KPI label="Card Spend Vol" value="$2.8B" trend={14.5} sub="YTD" color={C.blue} />
      <KPI label="Loan Origination" value="$890M" trend={8.2} color={C.teal} />
      <KPI label="Total Deposits" value="$6.2B" trend={22.3} color={C.green} />
      <KPI label="Rewards Redeemed" value="$42M" trend={18.1} color={C.amber} />
    </div>
    <div className="bg-white rounded-lg p-4 shadow-sm border border-slate-100">
      <h3 className="text-sm font-semibold text-slate-700 mb-3">Product Leaderboard</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead><tr className="border-b border-slate-200">
            <th className="text-left py-2 text-xs font-medium text-slate-500">Product</th>
            <th className="text-right py-2 text-xs font-medium text-slate-500">Accounts</th>
            <th className="text-right py-2 text-xs font-medium text-slate-500">Spend/Bal ($M)</th>
            <th className="text-right py-2 text-xs font-medium text-slate-500">Growth %</th>
            <th className="text-right py-2 text-xs font-medium text-slate-500">NPS</th>
          </tr></thead>
          <tbody>
            {productPerf.map((p,i) => (
              <tr key={i} className="border-b border-slate-50 hover:bg-slate-50">
                <td className="py-2 font-medium text-slate-800">{p.product}</td>
                <td className="py-2 text-right text-slate-600">{fmt(p.accounts)}</td>
                <td className="py-2 text-right text-slate-600">${p.spend || p.balance ? fmt(p.spend||p.balance/1000) : '—'}M</td>
                <td className="py-2 text-right"><span className={`font-medium ${p.growth>15?'text-emerald-600':p.growth>10?'text-blue-600':'text-slate-600'}`}>+{p.growth}%</span></td>
                <td className="py-2 text-right"><span className={`font-medium ${p.nps>=80?'text-emerald-600':p.nps>=70?'text-blue-600':'text-amber-600'}`}>{p.nps}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  </div>
);

const DigitalTab = () => (
  <div>
    <SectionTitle sub="App sessions, feature adoption, digital vs branch transactions">Digital & Mobile Analytics</SectionTitle>
    <div className="grid grid-cols-4 gap-3 mb-6">
      <KPI label="Mobile MAU" value="68.2K" trend={24.5} color={C.blue} />
      <KPI label="Web MAU" value="42.1K" trend={12.3} color={C.teal} />
      <KPI label="Digital Txn Share" value="78.3%" trend={6.2} sub="vs branch" color={C.green} />
      <KPI label="App Rating" value="4.7★" trend={0.2} sub="App Store avg" color={C.amber} />
    </div>
    <div className="grid grid-cols-2 gap-4">
      <div className="bg-white rounded-lg p-4 shadow-sm border border-slate-100">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">Channel Migration (Monthly)</h3>
        <ResponsiveContainer width="100%" height={220}>
          <AreaChart data={digitalData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="month" tick={{fontSize:10}} stroke="#94A3B8" />
            <YAxis tick={{fontSize:10}} stroke="#94A3B8" />
            <Tooltip contentStyle={{fontSize:11}} formatter={(v)=>fmt(v)} />
            <Legend wrapperStyle={{fontSize:10}} />
            <Area type="monotone" dataKey="mobileUsers" fill={C.blue} stroke={C.blue} fillOpacity={0.5} name="Mobile" />
            <Area type="monotone" dataKey="webUsers" fill={C.teal} stroke={C.teal} fillOpacity={0.5} name="Web" />
            <Area type="monotone" dataKey="branchVisits" fill={C.amber} stroke={C.amber} fillOpacity={0.3} name="Branch" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
      <div className="bg-white rounded-lg p-4 shadow-sm border border-slate-100">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">Top Features by Adoption</h3>
        <div className="space-y-3">
          {[
            {feat:"Mobile Check Deposit",adopt:82,trend:"+12%"},
            {feat:"Bill Pay",adopt:74,trend:"+8%"},
            {feat:"Card Controls",adopt:68,trend:"+22%"},
            {feat:"Spend Insights",adopt:56,trend:"+31%"},
            {feat:"Savings Goals",adopt:42,trend:"+18%"},
            {feat:"Credit Score Check",adopt:71,trend:"+15%"},
          ].map((f,i) => (
            <div key={i}>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-slate-700 font-medium">{f.feat}</span>
                <span><span className="font-bold">{f.adopt}%</span> <span className="text-emerald-600">{f.trend}</span></span>
              </div>
              <MiniBar value={f.adopt} color={CHART_COLORS[i%CHART_COLORS.length]} />
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
);

const FraudTab = () => (
  <div>
    <SectionTitle sub="Alert volume, false positive rate, investigation pipeline, loss prevention">Fraud & AML Detection</SectionTitle>
    <div className="grid grid-cols-5 gap-3 mb-6">
      <KPI label="Active Alerts" value="128" sub="open cases" color={C.red} />
      <KPI label="False Positive Rate" value="42.3%" trend={-3.1} sub="improving" color={C.amber} />
      <KPI label="Avg Resolution" value="4.2 days" trend={-12} sub="faster" color={C.teal} />
      <KPI label="Prevented Losses" value="$8.4M" trend={22} sub="YTD" color={C.green} />
      <KPI label="Actual Losses" value="$2.1M" trend={-15} sub="declining" color={C.red} />
    </div>
    <div className="grid grid-cols-2 gap-4">
      <div className="bg-white rounded-lg p-4 shadow-sm border border-slate-100">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">Monthly Alert Volume</h3>
        <ResponsiveContainer width="100%" height={220}>
          <ComposedChart data={fraudData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="month" tick={{fontSize:10}} stroke="#94A3B8" />
            <YAxis tick={{fontSize:10}} stroke="#94A3B8" />
            <Tooltip contentStyle={{fontSize:11}} />
            <Legend wrapperStyle={{fontSize:10}} />
            <Bar dataKey="alerts" fill={C.red} opacity={0.7} name="Total Alerts" />
            <Bar dataKey="confirmed" fill="#991B1B" name="Confirmed Fraud" />
            <Line type="monotone" dataKey="falsePositive" stroke={C.amber} strokeWidth={2} dot={false} name="False Positives" />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
      <div className="bg-white rounded-lg p-4 shadow-sm border border-slate-100">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">Detection Methods</h3>
        <ResponsiveContainer width="100%" height={220}>
          <PieChart>
            <Pie data={[
              {name:"ML Model",value:45},{name:"Rules Engine",value:25},{name:"Velocity Check",value:15},{name:"Geo-Fence",value:10},{name:"Network",value:5}
            ]} cx="50%" cy="50%" outerRadius={80} dataKey="value" label={({name,percent})=>`${name} ${(percent*100).toFixed(0)}%`} labelLine={false}>
              {[C.blue,C.teal,C.amber,C.purple,C.green].map((c,i)=> <Cell key={i} fill={c} />)}
            </Pie>
            <Tooltip contentStyle={{fontSize:11}} />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  </div>
);

const PartnerTab = () => (
  <div>
    <SectionTitle sub="Co-brand performance, interchange revenue, merchant category spend">Partner & Merchant Analytics</SectionTitle>
    <div className="grid grid-cols-4 gap-3 mb-6">
      <KPI label="Total Interchange" value="$148M" trend={12.5} sub="YTD" color={C.blue} />
      <KPI label="Partner-Sourced Accts" value="18.2K" trend={22} color={C.teal} />
      <KPI label="Avg Partner NPS" value="4.5" sub="out of 5.0" color={C.green} />
      <KPI label="Revenue Share Paid" value="$22.4M" sub="to partners" color={C.amber} />
    </div>
    <div className="bg-white rounded-lg p-4 shadow-sm border border-slate-100">
      <h3 className="text-sm font-semibold text-slate-700 mb-3">Partner Leaderboard</h3>
      <table className="w-full text-sm">
        <thead><tr className="border-b border-slate-200">
          <th className="text-left py-2 text-xs font-medium text-slate-500">Partner</th>
          <th className="text-right py-2 text-xs font-medium text-slate-500">Transactions</th>
          <th className="text-right py-2 text-xs font-medium text-slate-500">Spend ($M)</th>
          <th className="text-right py-2 text-xs font-medium text-slate-500">Interchange ($K)</th>
          <th className="text-right py-2 text-xs font-medium text-slate-500">CSAT</th>
        </tr></thead>
        <tbody>
          {partnerData.map((p,i) => (
            <tr key={i} className="border-b border-slate-50 hover:bg-slate-50">
              <td className="py-2 font-medium text-slate-800">{p.partner}</td>
              <td className="py-2 text-right text-slate-600">{fmt(p.txns)}</td>
              <td className="py-2 text-right text-slate-600">${p.spend}M</td>
              <td className="py-2 text-right text-slate-600">${p.interchange}K</td>
              <td className="py-2 text-right"><span className={`font-medium ${p.satisfaction>=4.5?'text-emerald-600':'text-blue-600'}`}>{p.satisfaction}</span></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);

const MDMQualityTab = () => (
  <div>
    <SectionTitle sub="Match rates, golden record coverage, DQ scores, source system health">MDM & Data Quality Governance</SectionTitle>
    <div className="grid grid-cols-5 gap-3 mb-6">
      <KPI label="Overall DQ Score" value={`${dqMetrics.overallScore}%`} trend={1.2} color={C.green} />
      <KPI label="Match Rate" value={`${dqMetrics.matchRate}%`} trend={0.8} color={C.teal} />
      <KPI label="Golden Coverage" value={`${dqMetrics.goldenCoverage}%`} trend={0.5} color={C.blue} />
      <KPI label="Data Freshness" value={`${dqMetrics.freshnessHrs}hrs`} sub="avg lag" color={C.amber} />
      <KPI label="DQ Tests" value="34/34" sub="all passing" color={C.green} />
    </div>
    <div className="grid grid-cols-2 gap-4">
      <div className="bg-white rounded-lg p-4 shadow-sm border border-slate-100">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">Quality Dimensions</h3>
        <ResponsiveContainer width="100%" height={220}>
          <RadarChart data={[
            {dim:"Completeness",score:dqMetrics.completeness},
            {dim:"Accuracy",score:dqMetrics.accuracy},
            {dim:"Consistency",score:dqMetrics.consistency},
            {dim:"Timeliness",score:dqMetrics.timeliness},
            {dim:"Uniqueness",score:96.2},
            {dim:"Validity",score:97.8},
          ]}>
            <PolarGrid stroke="#E2E8F0" />
            <PolarAngleAxis dataKey="dim" tick={{fontSize:10}} stroke="#64748B" />
            <PolarRadiusAxis angle={30} domain={[90,100]} tick={{fontSize:9}} />
            <Radar name="Score" dataKey="score" stroke={C.blue} fill={C.blue} fillOpacity={0.3} />
          </RadarChart>
        </ResponsiveContainer>
      </div>
      <div className="bg-white rounded-lg p-4 shadow-sm border border-slate-100">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">Source System Health</h3>
        <div className="space-y-4">
          {dqMetrics.sources.map((s,i) => (
            <div key={i}>
              <div className="flex justify-between text-sm mb-1">
                <span className="font-medium text-slate-700">{s.name}</span>
                <span className="text-xs text-slate-500">{s.matched}/{s.records} matched <span className="font-bold ml-1" style={{color:s.quality>=96?C.green:s.quality>=94?C.amber:C.red}}>{s.quality}%</span></span>
              </div>
              <MiniBar value={s.quality} max={100} color={s.quality>=96?C.green:s.quality>=94?C.amber:C.red} />
            </div>
          ))}
        </div>
        <div className="mt-4 p-3 rounded-lg bg-slate-50">
          <div className="text-xs font-medium text-slate-600 mb-2">MDM Match Tier Distribution</div>
          <div className="flex gap-4 text-xs">
            <div><span className="inline-block w-2 h-2 rounded-full mr-1" style={{backgroundColor:C.green}}></span>Auto-Merge: 42%</div>
            <div><span className="inline-block w-2 h-2 rounded-full mr-1" style={{backgroundColor:C.amber}}></span>Review: 28%</div>
            <div><span className="inline-block w-2 h-2 rounded-full mr-1" style={{backgroundColor:C.red}}></span>No Match: 30%</div>
          </div>
        </div>
      </div>
    </div>
  </div>
);

// ─── Main App ───
const TABS = [
  {id:"exec",label:"Executive Pulse",icon:"📊"},
  {id:"revenue",label:"Revenue",icon:"💰"},
  {id:"c360",label:"Customer 360",icon:"👤"},
  {id:"acq",label:"Acquisition",icon:"🎯"},
  {id:"risk",label:"Credit Risk",icon:"⚠️"},
  {id:"product",label:"Products",icon:"💳"},
  {id:"digital",label:"Digital",icon:"📱"},
  {id:"fraud",label:"Fraud & AML",icon:"🛡️"},
  {id:"partner",label:"Partners",icon:"🤝"},
  {id:"dq",label:"MDM & DQ",icon:"✅"},
];

const TAB_CONTENT = {
  exec: ExecutivePulse, revenue: RevenueTab, c360: Customer360,
  acq: AcquisitionTab, risk: CreditRiskTab, product: ProductTab,
  digital: DigitalTab, fraud: FraudTab, partner: PartnerTab, dq: MDMQualityTab,
};

export default function App() {
  const [tab, setTab] = useState("exec");
  const Content = TAB_CONTENT[tab];
  
  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-slate-900 text-white px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-amber-500 flex items-center justify-center font-bold text-sm">HB</div>
          <div>
            <div className="text-sm font-bold">Horizon Bank Holdings</div>
            <div className="text-xs text-slate-400">Enterprise MDM Lakehouse — Idea to Display</div>
          </div>
        </div>
        <div className="flex items-center gap-4 text-xs text-slate-400">
          <span>103K+ records</span>
          <span>15 tables</span>
          <span>34/34 DQ tests</span>
          <span className="text-emerald-400">● Live</span>
        </div>
      </div>
      
      {/* Tab Bar */}
      <div className="bg-white border-b border-slate-200 px-4 flex gap-0.5 overflow-x-auto">
        {TABS.map(t => (
          <button key={t.id} onClick={()=>setTab(t.id)}
            className={`px-3 py-2.5 text-xs font-medium whitespace-nowrap transition border-b-2 ${
              tab===t.id ? 'border-amber-500 text-slate-900 bg-amber-50' : 'border-transparent text-slate-500 hover:text-slate-700 hover:bg-slate-50'
            }`}>
            <span className="mr-1">{t.icon}</span>{t.label}
          </button>
        ))}
      </div>
      
      {/* Content */}
      <div className="p-6 max-w-7xl mx-auto">
        <Content />
      </div>
      
      {/* Footer */}
      <div className="text-center py-3 text-xs text-slate-400 border-t border-slate-100">
        Simultaneous — "Idea to Display" — Built with Claude Opus 4.6 AI Agents
      </div>
    </div>
  );
}

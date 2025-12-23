import streamlit as st

# MUST be first Streamlit command
st.set_page_config(
    page_title="LoanGuardian AI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Navigation
st.sidebar.title("LoanGuardian AI")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Loan Evaluation", "Risk Dashboard", "Compliance Check", "Loan Monitoring"]
)
st.sidebar.markdown("---")
st.sidebar.markdown("**LMA EDGE Hackathon**")
st.sidebar.markdown("Commercial Lending & Risk")

# ========================================
# HOME PAGE
# ========================================
if page == "Home":
    st.title("LoanGuardian AI")
    st.subheader("Unified Risk, Compliance & Origination Engine")
    
    st.markdown("""
    **LoanGuardian AI** is an enterprise-grade platform designed to streamline commercial lending 
    operations by unifying risk assessment, compliance verification, and loan origination into a 
    single intelligent workflow.
    
    Built for banks, credit unions, and alternative lenders, LoanGuardian AI reduces manual review 
    time, minimizes regulatory risk, and improves portfolio quality through automated decision 
    support and continuous monitoring.
    """)
    
    st.markdown("---")
    st.markdown("### Key Performance Indicators")
    
    # KPI Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Loans Reviewed",
            value="1,247",
            delta="156 this month"
        )
    
    with col2:
        st.metric(
            label="Average Risk Score",
            value="68.5",
            delta="-3.2 (lower is better)",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="Compliance Pass Rate",
            value="94.3%",
            delta="+2.1%"
        )
    
    st.markdown("---")
    st.markdown("### Platform Capabilities")
    
    cap_col1, cap_col2 = st.columns(2)
    
    with cap_col1:
        st.markdown("**Risk Assessment**")
        st.markdown("- Multi-factor credit analysis")
        st.markdown("- Industry-specific risk scoring")
        st.markdown("- Default probability modeling")
        
        st.markdown("**Compliance Engine**")
        st.markdown("- Regulatory requirement validation")
        st.markdown("- KYC/AML screening integration")
        st.markdown("- Audit trail generation")
    
    with cap_col2:
        st.markdown("**Loan Origination**")
        st.markdown("- Streamlined application intake")
        st.markdown("- Document verification workflows")
        st.markdown("- Automated underwriting support")
        
        st.markdown("**Portfolio Monitoring**")
        st.markdown("- Early warning signals")
        st.markdown("- Covenant tracking")
        st.markdown("- Real-time alerts")

# ========================================
# LOAN EVALUATION PAGE
# ========================================
elif page == "Loan Evaluation":
    st.title("Loan Evaluation")
    st.markdown("Comprehensive risk assessment for commercial loan applications")
    
    st.markdown("---")
    st.subheader("Borrower Profile")
    
    profile_col1, profile_col2 = st.columns(2)
    
    with profile_col1:
        st.markdown("**Company Information**")
        st.markdown("- **Business Name:** Apex Manufacturing Inc.")
        st.markdown("- **Industry:** Industrial Equipment")
        st.markdown("- **Years in Business:** 12")
        st.markdown("- **Annual Revenue:** $8.5M")
        st.markdown("- **Employees:** 45")
    
    with profile_col2:
        st.markdown("**Loan Request**")
        st.markdown("- **Loan Amount:** $500,000")
        st.markdown("- **Purpose:** Equipment Purchase & Working Capital")
        st.markdown("- **Term:** 5 years")
        st.markdown("- **Collateral:** Manufacturing Equipment")
        st.markdown("- **Guarantor:** Personal Guarantee (Owner)")
    
    st.markdown("---")
    st.subheader("Risk Assessment Results")
    
    # Risk Score
    risk_score = 72
    st.markdown(f"**Overall Risk Score: {risk_score}/100**")
    st.progress(risk_score / 100)
    
    # Risk Label
    if risk_score < 50:
        st.success("Risk Level: LOW - Recommended for Approval")
    elif risk_score < 75:
        st.warning("Risk Level: MEDIUM - Additional Review Recommended")
    else:
        st.error("Risk Level: HIGH - Requires Senior Review")
    
    st.markdown("---")
    st.subheader("Risk Factor Breakdown")
    
    factor_col1, factor_col2 = st.columns(2)
    
    with factor_col1:
        st.markdown("**Credit History Score**")
        st.progress(0.65)
        st.markdown("65/100 - Satisfactory credit profile")
        
        st.markdown("**Financial Stability**")
        st.progress(0.78)
        st.markdown("78/100 - Strong cash flow position")
        
        st.markdown("**Collateral Coverage**")
        st.progress(0.82)
        st.markdown("82/100 - Adequate collateral value")
    
    with factor_col2:
        st.markdown("**Industry Risk**")
        st.progress(0.58)
        st.markdown("58/100 - Moderate industry outlook")
        
        st.markdown("**Management Experience**")
        st.progress(0.88)
        st.markdown("88/100 - Experienced leadership team")
        
        st.markdown("**Debt Service Coverage**")
        st.progress(0.75)
        st.markdown("75/100 - Acceptable DSCR of 1.45x")

# ========================================
# RISK DASHBOARD PAGE
# ========================================
elif page == "Risk Dashboard":
    st.title("Risk Dashboard")
    st.markdown("Portfolio-wide risk metrics and trend analysis")
    
    st.markdown("---")
    st.subheader("Portfolio Risk Distribution")
    
    st.markdown("""
    The risk dashboard provides a consolidated view of credit risk across your entire commercial 
    lending portfolio. Risk scores are calculated using a proprietary algorithm that weighs 
    financial metrics, industry factors, and borrower characteristics.
    """)
    
    st.markdown("---")
    st.markdown("### Risk Score Distribution")
    st.markdown("Percentage of portfolio by risk category:")
    
    # Risk distribution bars
    st.markdown("**Low Risk (0-50)**")
    st.progress(0.35)
    st.markdown("35% of portfolio - 437 loans")
    
    st.markdown("**Medium Risk (51-75)**")
    st.progress(0.52)
    st.markdown("52% of portfolio - 648 loans")
    
    st.markdown("**High Risk (76-100)**")
    st.progress(0.13)
    st.markdown("13% of portfolio - 162 loans")
    
    st.markdown("---")
    st.subheader("Industry Concentration")
    st.markdown("Top industries by loan volume:")
    
    st.markdown("**Manufacturing**")
    st.progress(0.28)
    st.markdown("28% - $142M exposure")
    
    st.markdown("**Real Estate**")
    st.progress(0.22)
    st.markdown("22% - $111M exposure")
    
    st.markdown("**Healthcare Services**")
    st.progress(0.18)
    st.markdown("18% - $91M exposure")
    
    st.markdown("**Professional Services**")
    st.progress(0.15)
    st.markdown("15% - $76M exposure")
    
    st.markdown("**Other Industries**")
    st.progress(0.17)
    st.markdown("17% - $86M exposure")

# ========================================
# COMPLIANCE CHECK PAGE
# ========================================
elif page == "Compliance Check":
    st.title("Compliance Check")
    st.markdown("Automated regulatory compliance verification")
    
    st.markdown("---")
    st.subheader("Compliance Checklist - Loan Application #LC-2024-0847")
    
    st.markdown("**Borrower:** Apex Manufacturing Inc.")
    st.markdown("**Review Date:** December 23, 2024")
    
    st.markdown("---")
    
    # Compliance checklist with hardcoded values
    checks = {
        "KYC Documentation Complete": True,
        "Business License Verified": True,
        "Tax Returns Reviewed (3 years)": True,
        "Financial Statements Audited": True,
        "AML Screening Passed": True,
        "OFAC Sanctions Check Clear": True,
        "Credit Report Obtained": True,
        "Collateral Appraisal Current": True,
        "Environmental Assessment Complete": False,
        "Insurance Coverage Verified": True,
        "Personal Guarantee Executed": True,
        "Loan Agreement Executed": False
    }
    
    passed_count = 0
    total_count = len(checks)
    
    st.markdown("### Required Checks")
    
    for check_name, is_passed in checks.items():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.checkbox(check_name, value=is_passed, disabled=True)
        with col2:
            if is_passed:
                st.success("PASS")
                passed_count += 1
            else:
                st.error("FAIL")
    
    st.markdown("---")
    st.subheader("Compliance Summary")
    
    compliance_rate = (passed_count / total_count) * 100
    st.progress(passed_count / total_count)
    st.markdown(f"**{passed_count}/{total_count} checks passed ({compliance_rate:.1f}%)**")
    
    if passed_count == total_count:
        st.success("**STATUS: FULLY COMPLIANT** - Application ready for underwriting")
    else:
        st.warning(f"**STATUS: PENDING** - {total_count - passed_count} item(s) require attention")
        st.markdown("**Outstanding Items:**")
        for check_name, is_passed in checks.items():
            if not is_passed:
                st.markdown(f"- {check_name}")

# ========================================
# LOAN MONITORING PAGE
# ========================================
elif page == "Loan Monitoring":
    st.title("Loan Monitoring")
    st.markdown("Continuous monitoring and early warning system for active loans")
    
    st.markdown("---")
    st.subheader("Early Warning Concept")
    
    st.markdown("""
    LoanGuardian AI continuously monitors active loans for signs of deteriorating credit quality 
    or covenant breaches. The early warning system tracks financial performance, payment history, 
    and external risk factors to identify loans requiring proactive intervention.
    
    **Monitoring Dimensions:**
    - Payment performance and delinquency trends
    - Financial covenant compliance
    - Credit rating changes
    - Industry stress indicators
    - Collateral value fluctuations
    """)
    
    st.markdown("---")
    st.subheader("Active Alerts")
    
    # Alert 1
    st.error("**HIGH PRIORITY ALERT**")
    st.markdown("**Loan ID:** LC-2023-0234")
    st.markdown("**Borrower:** Delta Logistics LLC")
    st.markdown("**Issue:** Payment 15 days past due, Second occurrence in 6 months")
    st.markdown("**Action Required:** Contact borrower for payment arrangement")
    
    st.markdown("---")
    
    # Alert 2
    st.warning("**MEDIUM PRIORITY ALERT**")
    st.markdown("**Loan ID:** LC-2022-0891")
    st.markdown("**Borrower:** Summit Hospitality Group")
    st.markdown("**Issue:** Debt Service Coverage Ratio below covenant threshold (1.15x vs 1.25x required)")
    st.markdown("**Action Required:** Request updated financial statements and remediation plan")
    
    st.markdown("---")
    
    # Alert 3
    st.warning("**MEDIUM PRIORITY ALERT**")
    st.markdown("**Loan ID:** LC-2023-0567")
    st.markdown("**Borrower:** Riverside Construction Corp")
    st.markdown("**Issue:** Industry downturn indicator - Construction sector experiencing headwinds")
    st.markdown("**Action Required:** Schedule quarterly review call")
    
    st.markdown("---")
    
    # Healthy Status
    st.success("**PERFORMING WELL**")
    st.markdown("**Loan ID:** LC-2024-0102")
    st.markdown("**Borrower:** Apex Manufacturing Inc.")
    st.markdown("**Status:** All covenants met, payments current, strong financial metrics")
    st.markdown("**Next Review:** March 2025")
    
    st.markdown("---")
    st.subheader("Monitoring Statistics")
    
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        st.metric("Total Active Loans", "1,247")
    
    with stat_col2:
        st.metric("Loans with Alerts", "47", delta="3.8%")
    
    with stat_col3:
        st.metric("High Priority", "8", delta="-2 this week", delta_color="inverse")

# Footer
st.markdown("---")
st.markdown("**LoanGuardian AI** | LMA EDGE Hackathon | Commercial Lending & Risk Management")

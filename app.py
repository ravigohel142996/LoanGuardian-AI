import streamlit as st

# MUST be first Streamlit command
st.set_page_config(
    page_title="LoanGuardian AI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enterprise dashboard styling and mobile responsiveness
st.markdown("""
<style>
    /* Main container padding and spacing */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 100%;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        /* Stack columns on mobile */
        .row-widget.stHorizontal {
            flex-direction: column;
        }
        
        /* Full width buttons on mobile */
        .stButton button {
            width: 100%;
        }
    }
    
    /* Typography improvements */
    h1 {
        color: #1E3A8A;
        font-weight: 700;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3B82F6;
        margin-bottom: 1.5rem;
    }
    
    h2 {
        color: #1E40AF;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #1E40AF;
        font-weight: 600;
        margin-top: 1rem;
    }
    
    /* Card-like sections */
    .stAlert {
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 500;
        color: #64748B;
    }
    
    /* Form styling */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        border-radius: 6px;
        border: 2px solid #E2E8F0;
        padding: 0.5rem;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #3B82F6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 6px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button[kind="primary"] {
        background-color: #3B82F6;
        border: none;
    }
    
    .stButton button[kind="primary"]:hover {
        background-color: #2563EB;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background-color: #3B82F6;
        border-radius: 4px;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 2px solid #E2E8F0;
    }
    
    [data-testid="stSidebar"] h1 {
        color: #1E3A8A;
        border-bottom: 2px solid #3B82F6;
        padding-bottom: 0.5rem;
    }
    
    /* Horizontal rules */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 2px solid #E2E8F0;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #F1F5F9;
        border-radius: 6px;
        font-weight: 600;
    }
    
    /* Success/Warning/Error message improvements */
    .stSuccess {
        background-color: #ECFDF5;
        border-left: 4px solid #10B981;
    }
    
    .stWarning {
        background-color: #FFFBEB;
        border-left: 4px solid #F59E0B;
    }
    
    .stError {
        background-color: #FEF2F2;
        border-left: 4px solid #EF4444;
    }
    
    .stInfo {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
    }
    
    /* Footer styling */
    footer {
        text-align: center;
        padding: 2rem 0;
        color: #64748B;
        font-size: 0.9rem;
    }
    
    /* Prevent horizontal scroll on mobile */
    .main {
        overflow-x: hidden;
    }
    
    /* Responsive tables and containers */
    @media (max-width: 768px) {
        .row-widget {
            overflow-x: auto;
        }
    }
</style>
""", unsafe_allow_html=True)

# Constants
INDUSTRY_OPTIONS = ["Manufacturing", "Retail", "Logistics", "Healthcare", "Real Estate"]
CREDIT_SCORE_DIVISOR = 5.5  # Normalizes credit score to 0-100 scale (850->100, 650->64)

# Initialize session state for user inputs
if 'business_name' not in st.session_state:
    st.session_state.business_name = ""
if 'industry' not in st.session_state:
    st.session_state.industry = "Manufacturing"
if 'annual_revenue' not in st.session_state:
    st.session_state.annual_revenue = 0
if 'loan_amount' not in st.session_state:
    st.session_state.loan_amount = 0
if 'credit_score' not in st.session_state:
    st.session_state.credit_score = 650
if 'years_in_business' not in st.session_state:
    st.session_state.years_in_business = 0
if 'collateral_available' not in st.session_state:
    st.session_state.collateral_available = False
if 'assessment_run' not in st.session_state:
    st.session_state.assessment_run = False

# Helper function to calculate risk score with feature importance
def calculate_risk_score(credit_score, annual_revenue, loan_amount, years_in_business, collateral_available, return_details=False):
    """Calculate risk score based on simple, explainable rules
    
    Args:
        credit_score: Borrower's credit score (300-850)
        annual_revenue: Annual business revenue in USD
        loan_amount: Requested loan amount in USD
        years_in_business: Years the business has been operating
        collateral_available: Whether collateral is available (boolean)
        return_details: If True, returns (score, feature_impacts, reasoning)
    
    Returns:
        If return_details=False: risk_score (int)
        If return_details=True: (risk_score, feature_impacts dict, reasoning list)
    """
    risk_score = 50  # Start at medium risk
    feature_impacts = {}
    reasoning = []
    
    # Credit score impact (weight: 30%)
    if credit_score >= 750:
        credit_impact = -15
        reasoning.append(f"✓ Excellent credit score ({credit_score}) reduces risk significantly")
    elif credit_score >= 650:
        credit_impact = -5
        reasoning.append(f"✓ Good credit score ({credit_score}) provides moderate risk reduction")
    elif credit_score >= 600:
        credit_impact = 5
        reasoning.append(f"⚠ Fair credit score ({credit_score}) slightly increases risk")
    else:  # credit_score < 600
        credit_impact = 15
        reasoning.append(f"✗ Low credit score ({credit_score}) significantly increases default risk")
    
    risk_score += credit_impact
    feature_impacts['Credit Score'] = credit_impact
    
    # Revenue vs loan amount ratio (weight: 25%)
    if loan_amount > 0 and annual_revenue > 0:
        ratio = annual_revenue / loan_amount
        if ratio >= 20:
            ratio_impact = -12
            reasoning.append(f"✓ Exceptional revenue coverage ({ratio:.1f}x) strongly reduces risk")
        elif ratio >= 10:
            ratio_impact = -8
            reasoning.append(f"✓ Strong revenue coverage ({ratio:.1f}x) reduces risk")
        elif ratio >= 5:
            ratio_impact = -3
            reasoning.append(f"✓ Adequate revenue coverage ({ratio:.1f}x) provides some risk reduction")
        elif ratio >= 3:
            ratio_impact = 8
            reasoning.append(f"⚠ Moderate revenue coverage ({ratio:.1f}x) increases risk")
        else:  # ratio < 3
            ratio_impact = 15
            reasoning.append(f"✗ Low revenue coverage ({ratio:.1f}x) significantly increases repayment risk")
    else:
        ratio_impact = 0
        reasoning.append("⚠ Insufficient financial data for revenue analysis")
    
    risk_score += ratio_impact
    feature_impacts['Revenue/Loan Ratio'] = ratio_impact
    
    # Years in business (weight: 20%)
    if years_in_business >= 10:
        years_impact = -10
        reasoning.append(f"✓ Well-established business ({years_in_business} years) reduces risk")
    elif years_in_business >= 5:
        years_impact = -5
        reasoning.append(f"✓ Mature business ({years_in_business} years) provides stability")
    elif years_in_business >= 2:
        years_impact = -2
        reasoning.append(f"✓ Established operations ({years_in_business} years) meets minimum threshold")
    else:  # years_in_business < 2
        years_impact = 10
        reasoning.append(f"✗ Limited operating history ({years_in_business} years) increases uncertainty")
    
    risk_score += years_impact
    feature_impacts['Business Maturity'] = years_impact
    
    # Collateral (weight: 15%)
    if collateral_available:
        collateral_impact = -8
        reasoning.append("✓ Collateral available reduces loss exposure")
    else:
        collateral_impact = 8
        reasoning.append("⚠ No collateral increases loss exposure in default scenarios")
    
    risk_score += collateral_impact
    feature_impacts['Collateral'] = collateral_impact
    
    # Keep score in valid range
    risk_score = max(0, min(100, risk_score))
    
    if return_details:
        return risk_score, feature_impacts, reasoning
    return risk_score

def get_risk_level(risk_score):
    """Convert risk score to risk level"""
    if risk_score < 50:
        return "LOW", "green"
    elif risk_score < 75:
        return "MEDIUM", "yellow"
    else:
        return "HIGH", "red"

def get_compliance_status(credit_score, annual_revenue, loan_amount, years_in_business):
    """Check compliance rules"""
    checks = {
        "Credit Score >= 650": credit_score >= 650,
        "Revenue >= Loan Amount": annual_revenue >= loan_amount,
        "Years in Business >= 2": years_in_business >= 2
    }
    return checks

# Sidebar Navigation
st.sidebar.title("LoanGuardian AI")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Loan Evaluation", "Risk Dashboard", "Compliance Check", "Loan Monitoring", "AI Copilot"]
)
st.sidebar.markdown("---")
st.sidebar.markdown("**LMA EDGE Hackathon**")
st.sidebar.markdown("Commercial Lending & Risk")

# ========================================
# HOME PAGE
# ========================================
if page == "Home":
    st.title("LoanGuardian AI")
    st.subheader("Interactive Risk, Compliance & Loan Decision Simulator")
    
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
    
    # KPI Cards - Dynamic based on user input
    col1, col2, col3 = st.columns(3)
    
    # Calculate dynamic values if assessment has been run
    if st.session_state.assessment_run:
        risk_score = calculate_risk_score(
            st.session_state.credit_score,
            st.session_state.annual_revenue,
            st.session_state.loan_amount,
            st.session_state.years_in_business,
            st.session_state.collateral_available
        )
        risk_level, _ = get_risk_level(risk_score)
        compliance_checks = get_compliance_status(
            st.session_state.credit_score,
            st.session_state.annual_revenue,
            st.session_state.loan_amount,
            st.session_state.years_in_business
        )
        compliance_rate = sum(compliance_checks.values()) / len(compliance_checks) * 100
        
        loan_status = "Approved" if risk_level == "LOW" else "Under Review" if risk_level == "MEDIUM" else "Declined"
    else:
        risk_score = 68.5
        compliance_rate = 94.3
        loan_status = "Pending"
    
    with col1:
        st.metric(
            label="Total Loans Reviewed",
            value="1,247",
            delta="156 this month"
        )
    
    with col2:
        st.metric(
            label="Average Risk Score",
            value=f"{risk_score:.1f}",
            delta="-3.2 (lower is better)",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="Compliance Pass Rate",
            value=f"{compliance_rate:.1f}%",
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
    st.markdown("Interactive Risk, Compliance & Loan Decision Simulator")
    
    st.markdown("---")
    st.subheader("Loan Application Form")
    
    # Input form
    with st.form("loan_application_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            business_name = st.text_input("Business Name", value=st.session_state.business_name)
            industry = st.selectbox(
                "Industry",
                INDUSTRY_OPTIONS,
                index=INDUSTRY_OPTIONS.index(
                    st.session_state.industry if st.session_state.industry in INDUSTRY_OPTIONS else "Manufacturing"
                )
            )
            annual_revenue = st.number_input("Annual Revenue (USD)", min_value=0, value=st.session_state.annual_revenue, step=10000)
            loan_amount = st.number_input("Loan Amount Requested (USD)", min_value=0, value=st.session_state.loan_amount, step=10000)
        
        with col2:
            credit_score = st.slider("Credit Score", min_value=300, max_value=850, value=st.session_state.credit_score)
            years_in_business = st.number_input("Years in Business", min_value=0, value=st.session_state.years_in_business, step=1)
            collateral_available = st.checkbox("Collateral Available", value=st.session_state.collateral_available)
        
        submitted = st.form_submit_button("Run Loan Assessment", type="primary")
        
        if submitted:
            # Save to session state
            st.session_state.business_name = business_name
            st.session_state.industry = industry
            st.session_state.annual_revenue = annual_revenue
            st.session_state.loan_amount = loan_amount
            st.session_state.credit_score = credit_score
            st.session_state.years_in_business = years_in_business
            st.session_state.collateral_available = collateral_available
            st.session_state.assessment_run = True
    
    # Display results if assessment has been run
    if st.session_state.assessment_run and st.session_state.business_name:
        st.markdown("---")
        st.subheader("Risk Assessment Results")
        
        # Calculate risk score with details
        risk_score, feature_impacts, reasoning = calculate_risk_score(
            st.session_state.credit_score,
            st.session_state.annual_revenue,
            st.session_state.loan_amount,
            st.session_state.years_in_business,
            st.session_state.collateral_available,
            return_details=True
        )
        
        risk_level, risk_color = get_risk_level(risk_score)
        
        # Risk Score Display
        score_col1, score_col2, score_col3 = st.columns([2, 1, 1])
        
        with score_col1:
            st.markdown(f"### Overall Risk Score: {risk_score}/100")
            st.progress(risk_score / 100)
        
        with score_col2:
            if risk_level == "LOW":
                st.markdown("### 🟢")
            elif risk_level == "MEDIUM":
                st.markdown("### 🟡")
            else:
                st.markdown("### 🔴")
        
        with score_col3:
            st.markdown(f"### {risk_level}")
        
        # Risk Level with detailed reasoning
        if risk_level == "LOW":
            st.success(f"✓ **Risk Level: {risk_level} - Recommended for Approval**")
            recommendation = "This loan application demonstrates strong creditworthiness and manageable risk. Proceed with standard approval process."
            st.markdown("**Key Strengths:**")
            for reason in reasoning:
                if "✓" in reason:
                    st.markdown(f"- {reason}")
        elif risk_level == "MEDIUM":
            st.warning(f"⚠ **Risk Level: {risk_level} - Additional Review Recommended**")
            recommendation = "This loan application requires additional due diligence. Consider requesting additional documentation or collateral to mitigate risk."
            st.markdown("**Risk Considerations:**")
            for reason in reasoning:
                st.markdown(f"- {reason}")
        else:
            st.error(f"✗ **Risk Level: {risk_level} - Requires Senior Review**")
            recommendation = "This loan application presents elevated risk factors. Senior underwriter review and enhanced monitoring protocols recommended."
            st.markdown("**Critical Risk Factors:**")
            for reason in reasoning:
                if "✗" in reason or "⚠" in reason:
                    st.markdown(f"- {reason}")
        
        st.info(f"**💡 Recommendation:** {recommendation}")
        
        st.markdown("---")
        st.subheader("📊 Feature Importance Analysis")
        st.markdown("*Understanding which factors drive the risk assessment*")
        
        # Display feature importance with visual bars
        st.markdown("#### Individual Factor Contributions to Risk Score")
        
        # Sort features by absolute impact
        sorted_features = sorted(feature_impacts.items(), key=lambda x: abs(x[1]), reverse=True)
        
        for feature_name, impact in sorted_features:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**{feature_name}**")
            
            with col2:
                # Show impact with color coding
                if impact < 0:
                    st.markdown(f"<span style='color: green; font-weight: bold;'>{impact:+.0f} points</span>", unsafe_allow_html=True)
                elif impact > 0:
                    st.markdown(f"<span style='color: red; font-weight: bold;'>{impact:+.0f} points</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<span style='color: gray; font-weight: bold;'>{impact:+.0f} points</span>", unsafe_allow_html=True)
            
            with col3:
                # Visual bar showing impact direction and magnitude
                if impact < 0:
                    # Negative impact (good) - show green bar
                    normalized = abs(impact) / 15.0  # Max impact is around 15
                    st.progress(min(1.0, normalized))
                elif impact > 0:
                    # Positive impact (bad) - show in metric
                    normalized = impact / 15.0
                    st.markdown(f"⚠️ {normalized*100:.0f}%")
        
        st.markdown("""
        **Legend:**
        - 🟢 **Negative values** (green) reduce risk and improve loan quality
        - 🔴 **Positive values** (red) increase risk and require mitigation
        - Base risk score starts at 50/100 (medium risk)
        """)
        
        st.markdown("---")
        st.subheader("🔮 What-If Simulation")
        st.markdown("*See how changes to loan parameters impact the risk assessment*")
        
        st.markdown("#### Adjust Parameters to See Impact")
        
        # What-if controls
        whatif_col1, whatif_col2 = st.columns(2)
        
        with whatif_col1:
            st.markdown("**Scenario: Adjust Loan Amount**")
            loan_adjustment = st.slider(
                "Loan Amount Adjustment (%)",
                min_value=-50,
                max_value=100,
                value=0,
                step=5,
                help="Adjust the requested loan amount to see impact on risk"
            )
            new_loan_amount = st.session_state.loan_amount * (1 + loan_adjustment / 100)
            st.markdown(f"New Loan Amount: **${new_loan_amount:,.0f}**")
        
        with whatif_col2:
            st.markdown("**Scenario: Adjust Annual Revenue**")
            revenue_adjustment = st.slider(
                "Annual Revenue Adjustment (%)",
                min_value=-50,
                max_value=100,
                value=0,
                step=5,
                help="Adjust annual revenue to see impact on risk"
            )
            new_annual_revenue = st.session_state.annual_revenue * (1 + revenue_adjustment / 100)
            st.markdown(f"New Annual Revenue: **${new_annual_revenue:,.0f}**")
        
        # Calculate new risk score with adjusted values
        if loan_adjustment != 0 or revenue_adjustment != 0:
            new_risk_score, new_impacts, new_reasoning = calculate_risk_score(
                st.session_state.credit_score,
                new_annual_revenue,
                new_loan_amount,
                st.session_state.years_in_business,
                st.session_state.collateral_available,
                return_details=True
            )
            
            new_risk_level, _ = get_risk_level(new_risk_score)
            
            st.markdown("---")
            st.markdown("#### 📈 Impact Analysis")
            
            # Show before/after comparison
            comp_col1, comp_col2, comp_col3 = st.columns(3)
            
            with comp_col1:
                st.markdown("**Original Assessment**")
                st.metric("Risk Score", f"{risk_score}/100")
                st.metric("Risk Level", risk_level)
                if st.session_state.loan_amount > 0 and st.session_state.annual_revenue > 0:
                    original_ratio = st.session_state.annual_revenue / st.session_state.loan_amount
                    st.metric("Revenue/Loan Ratio", f"{original_ratio:.2f}x")
            
            with comp_col2:
                st.markdown("**Simulated Assessment**")
                score_change = new_risk_score - risk_score
                st.metric("Risk Score", f"{new_risk_score}/100", delta=f"{score_change:+.0f} pts", delta_color="inverse")
                
                level_changed = "↑" if new_risk_level != risk_level and new_risk_score > risk_score else "↓" if new_risk_level != risk_level else "→"
                st.metric("Risk Level", new_risk_level, delta=level_changed)
                
                if new_loan_amount > 0 and new_annual_revenue > 0:
                    new_ratio = new_annual_revenue / new_loan_amount
                    ratio_change = new_ratio - original_ratio if st.session_state.loan_amount > 0 and st.session_state.annual_revenue > 0 else new_ratio
                    st.metric("Revenue/Loan Ratio", f"{new_ratio:.2f}x", delta=f"{ratio_change:+.2f}x")
            
            with comp_col3:
                st.markdown("**Outcome**")
                if score_change < 0:
                    st.success(f"✓ Risk Reduced by {abs(score_change):.0f} points")
                    st.markdown("**Impact:** Improved loan profile")
                elif score_change > 0:
                    st.error(f"✗ Risk Increased by {score_change:.0f} points")
                    st.markdown("**Impact:** Weakened loan profile")
                else:
                    st.info("→ No change in risk")
                    st.markdown("**Impact:** Neutral effect")
                
                # Show if risk level changed
                if new_risk_level != risk_level:
                    if new_risk_score < risk_score:
                        st.markdown(f"🎯 **Tier Change:** {risk_level} → {new_risk_level}")
                    else:
                        st.markdown(f"⚠️ **Tier Change:** {risk_level} → {new_risk_level}")
        
        else:
            st.info("💡 **Tip:** Adjust the sliders above to simulate different scenarios and see how they impact the risk assessment.")
        
        st.markdown("---")
        st.subheader("Risk Factor Breakdown")
        
        # Explain the factors
        st.markdown("**Key Factors Contributing to Risk Assessment:**")
        
        factor_col1, factor_col2 = st.columns(2)
        
        with factor_col1:
            # Credit Score Factor
            st.markdown("**Credit History Score**")
            # Normalize credit score to 0-100 scale using constant divisor
            credit_factor = 100 - abs(st.session_state.credit_score - 850) / CREDIT_SCORE_DIVISOR
            credit_factor = max(0, min(100, credit_factor))
            st.progress(credit_factor / 100)
            if st.session_state.credit_score >= 750:
                st.markdown(f"{credit_factor:.0f}/100 - Excellent credit profile")
            elif st.session_state.credit_score >= 650:
                st.markdown(f"{credit_factor:.0f}/100 - Good credit profile")
            else:
                st.markdown(f"{credit_factor:.0f}/100 - Credit needs improvement")
            
            # Financial Stability
            st.markdown("**Financial Stability**")
            if st.session_state.loan_amount > 0 and st.session_state.annual_revenue > 0:
                ratio = st.session_state.annual_revenue / st.session_state.loan_amount
                financial_factor = min(100, ratio * 5)
                st.progress(financial_factor / 100)
                st.markdown(f"{financial_factor:.0f}/100 - Revenue to Loan Ratio: {ratio:.1f}x")
            else:
                st.progress(0)
                st.markdown("0/100 - Insufficient financial data")
        
        with factor_col2:
            # Business Maturity
            st.markdown("**Business Maturity**")
            maturity_factor = min(100, st.session_state.years_in_business * 8)
            st.progress(maturity_factor / 100)
            st.markdown(f"{maturity_factor:.0f}/100 - {st.session_state.years_in_business} years of operational history")
            
            # Collateral Coverage
            st.markdown("**Collateral Coverage**")
            if st.session_state.collateral_available:
                st.progress(0.85)
                st.markdown("85/100 - Collateral available for security")
            else:
                st.progress(0.40)
                st.markdown("40/100 - No collateral provided")
    
    elif st.session_state.assessment_run:
        st.info("Please fill in the Business Name and click 'Run Loan Assessment' to see results.")
    else:
        st.info("Fill in the loan application form above and click 'Run Loan Assessment' to begin the evaluation.")

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
    st.markdown("Interactive Risk, Compliance & Loan Decision Simulator")
    
    st.markdown("---")
    
    if st.session_state.assessment_run and st.session_state.business_name:
        st.subheader(f"Compliance Checklist - {st.session_state.business_name}")
        
        st.markdown(f"**Business Name:** {st.session_state.business_name}")
        st.markdown(f"**Industry:** {st.session_state.industry}")
        
        st.markdown("---")
        
        # Get compliance status
        compliance_checks = get_compliance_status(
            st.session_state.credit_score,
            st.session_state.annual_revenue,
            st.session_state.loan_amount,
            st.session_state.years_in_business
        )
        
        st.markdown("### Required Compliance Checks")
        
        passed_count = 0
        total_count = len(compliance_checks)
        
        for check_name, is_passed in compliance_checks.items():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{check_name}**")
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
            for check_name, is_passed in compliance_checks.items():
                if not is_passed:
                    st.markdown(f"- {check_name}")
                    # Provide guidance
                    if "Credit Score" in check_name:
                        st.markdown("  *Borrower needs to improve credit score to at least 650*")
                    elif "Revenue" in check_name:
                        st.markdown("  *Loan amount exceeds annual revenue - consider reducing loan amount or providing additional financial documentation*")
                    elif "Years" in check_name:
                        st.markdown("  *Business must have at least 2 years of operational history*")
    else:
        st.info("Please complete a loan assessment in the 'Loan Evaluation' page first to see compliance results.")
        
        st.markdown("---")
        st.subheader("Compliance Framework")
        st.markdown("""
        The compliance engine automatically validates loan applications against key regulatory 
        and underwriting requirements:
        
        **Required Compliance Checks:**
        - **Credit Score >= 650:** Minimum creditworthiness threshold
        - **Revenue >= Loan Amount:** Ensures borrower has sufficient income capacity
        - **Years in Business >= 2:** Demonstrates operational stability
        
        These checks help ensure responsible lending practices and regulatory compliance.
        """)

# ========================================
# LOAN MONITORING PAGE
# ========================================
elif page == "Loan Monitoring":
    st.title("Loan Monitoring")
    st.markdown("Interactive Risk, Compliance & Loan Decision Simulator")
    
    st.markdown("---")
    
    if st.session_state.assessment_run and st.session_state.business_name:
        st.subheader(f"Monitoring Status - {st.session_state.business_name}")
        
        # Calculate current risk
        risk_score = calculate_risk_score(
            st.session_state.credit_score,
            st.session_state.annual_revenue,
            st.session_state.loan_amount,
            st.session_state.years_in_business,
            st.session_state.collateral_available
        )
        
        risk_level, _ = get_risk_level(risk_score)
        
        st.markdown("---")
        st.subheader("Current Loan Status")
        
        # Display status based on risk level
        if risk_level == "LOW":
            st.success("**Loan performing within expected parameters**")
            st.markdown("""
            **Performance Summary:**
            - All payment obligations current
            - Financial covenants met
            - No early warning indicators detected
            - Continue standard monitoring protocols
            
            **Next Review:** Quarterly
            """)
        elif risk_level == "MEDIUM":
            st.warning("**Monitor cash flow and covenant compliance**")
            st.markdown("""
            **Performance Summary:**
            - Payment performance requires monitoring
            - Some risk factors identified
            - Enhanced oversight recommended
            - Request updated financial statements
            
            **Next Review:** Monthly
            
            **Action Items:**
            - Schedule review call with borrower
            - Monitor payment patterns closely
            - Review financial performance monthly
            """)
        else:
            st.error("**Early warning triggered: elevated default risk**")
            st.markdown("""
            **Performance Summary:**
            - High risk indicators present
            - Immediate attention required
            - Senior management review needed
            - Consider risk mitigation strategies
            
            **Next Review:** Weekly
            
            **Urgent Action Items:**
            - Immediate contact with borrower required
            - Request current financial statements
            - Review collateral position
            - Evaluate workout or restructuring options
            - Escalate to special assets team
            """)
        
        st.markdown("---")
        st.subheader("Key Monitoring Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Risk Score", f"{risk_score}/100", delta=None)
        
        with col2:
            st.metric("Risk Level", risk_level)
        
        with col3:
            payment_status = "Current" if risk_level == "LOW" else "Watch" if risk_level == "MEDIUM" else "Alert"
            st.metric("Payment Status", payment_status)
    
    else:
        st.info("Please complete a loan assessment in the 'Loan Evaluation' page first to see monitoring results.")
        
        st.markdown("---")
        st.subheader("Loan Monitoring Framework")
        
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
        
        **Risk-Based Monitoring Frequency:**
        - **LOW RISK:** Quarterly reviews, standard monitoring
        - **MEDIUM RISK:** Monthly reviews, enhanced oversight
        - **HIGH RISK:** Weekly reviews, intensive management
        """)

# ========================================
# AI COPILOT PAGE
# ========================================
elif page == "AI Copilot":
    st.title("LoanGuardian Copilot")
    st.markdown("Explainable AI Assistant for Lending Decisions")
    
    st.markdown("---")
    
    if st.session_state.assessment_run and st.session_state.business_name:
        st.subheader("Ask LoanGuardian Copilot")
        
        # Display current application summary
        with st.expander("📊 Current Application Summary", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Business Name:** {st.session_state.business_name}")
                st.markdown(f"**Industry:** {st.session_state.industry}")
                st.markdown(f"**Annual Revenue:** ${st.session_state.annual_revenue:,.0f}")
                st.markdown(f"**Loan Amount:** ${st.session_state.loan_amount:,.0f}")
            with col2:
                st.markdown(f"**Credit Score:** {st.session_state.credit_score}")
                st.markdown(f"**Years in Business:** {st.session_state.years_in_business}")
                st.markdown(f"**Collateral:** {'Yes' if st.session_state.collateral_available else 'No'}")
                
                risk_score = calculate_risk_score(
                    st.session_state.credit_score,
                    st.session_state.annual_revenue,
                    st.session_state.loan_amount,
                    st.session_state.years_in_business,
                    st.session_state.collateral_available
                )
                risk_level, _ = get_risk_level(risk_score)
                st.markdown(f"**Risk Level:** {risk_level} ({risk_score}/100)")
        
        st.markdown("---")
        
        # Question selector
        question = st.selectbox(
            "What would you like to ask?",
            [
                "Why is this loan rated this risk level?",
                "What factors increased the risk score?",
                "How can the borrower reduce risk?",
                "Why did the compliance check fail?",
                "Is this loan suitable for secondary market trading?"
            ]
        )
        
        if st.button("Ask Copilot", type="primary"):
            st.markdown("---")
            st.subheader("Copilot Response")
            
            # Calculate current metrics
            risk_score = calculate_risk_score(
                st.session_state.credit_score,
                st.session_state.annual_revenue,
                st.session_state.loan_amount,
                st.session_state.years_in_business,
                st.session_state.collateral_available
            )
            risk_level, _ = get_risk_level(risk_score)
            
            compliance_checks = get_compliance_status(
                st.session_state.credit_score,
                st.session_state.annual_revenue,
                st.session_state.loan_amount,
                st.session_state.years_in_business
            )
            
            # Generate response based on question
            if "Why is this loan rated" in question:
                response = f"""Based on the current inputs, this loan has been assessed with a **{risk_level} RISK** rating (score: {risk_score}/100).

The system identified the following key drivers:

**Credit Profile:** The borrower's credit score of {st.session_state.credit_score} """
                
                if st.session_state.credit_score >= 750:
                    response += "demonstrates excellent creditworthiness, which reduces overall risk."
                elif st.session_state.credit_score >= 650:
                    response += "indicates satisfactory credit management, contributing to moderate risk."
                else:
                    response += "falls below optimal thresholds, elevating the risk profile."
                
                if st.session_state.loan_amount > 0 and st.session_state.annual_revenue > 0:
                    ratio = st.session_state.annual_revenue / st.session_state.loan_amount
                    response += f"\n\n**Financial Capacity:** The revenue-to-loan ratio is {ratio:.2f}x. "
                    if ratio >= 5:
                        response += "This strong coverage provides confidence in repayment capacity."
                    elif ratio >= 2:
                        response += "This indicates adequate but not exceptional repayment capacity."
                    else:
                        response += "This low ratio raises concerns about debt service ability."
                
                response += f"\n\n**Business Maturity:** With {st.session_state.years_in_business} years of operation, "
                if st.session_state.years_in_business >= 5:
                    response += "the business has demonstrated operational stability."
                elif st.session_state.years_in_business >= 2:
                    response += "the business has established a track record, though additional history would strengthen the profile."
                else:
                    response += "the business is relatively new, which increases uncertainty."
                
                response += f"\n\n**Collateral Position:** "
                if st.session_state.collateral_available:
                    response += "The availability of collateral provides additional security and reduces loss exposure in adverse scenarios."
                else:
                    response += "The absence of collateral increases exposure in default scenarios, requiring stronger cash flow coverage."
                
                st.info(response)
            
            elif "What factors increased" in question:
                response = "The system identified the following factors that contributed to increased risk:\n\n"
                
                risk_factors = []
                
                if st.session_state.credit_score < 650:
                    risk_factors.append(f"• **Credit Score Below Threshold:** At {st.session_state.credit_score}, the credit score falls below the 650 minimum, indicating elevated default probability")
                
                if st.session_state.loan_amount > 0 and st.session_state.annual_revenue > 0:
                    ratio = st.session_state.annual_revenue / st.session_state.loan_amount
                    if ratio < 3:
                        risk_factors.append(f"• **Low Revenue Coverage:** The {ratio:.2f}x revenue-to-loan ratio suggests limited financial cushion for debt service")
                
                if st.session_state.years_in_business < 2:
                    risk_factors.append(f"• **Limited Operating History:** {st.session_state.years_in_business} years in business is below the 2-year stability threshold")
                
                if not st.session_state.collateral_available:
                    risk_factors.append("• **Unsecured Loan Structure:** No collateral reduces recovery options in adverse scenarios")
                
                if risk_factors:
                    response += "\n".join(risk_factors)
                    response += "\n\nFrom a risk management perspective, these factors collectively elevate the probability of default and reduce potential recovery rates."
                else:
                    response += "This application demonstrates strong fundamentals across all evaluated dimensions. The risk rating reflects conservative underwriting standards rather than specific deficiencies."
                
                st.warning(response)
            
            elif "How can the borrower reduce" in question:
                response = "To improve loan eligibility and reduce the risk profile, the borrower should consider the following actions:\n\n"
                
                recommendations = []
                
                if st.session_state.credit_score < 750:
                    recommendations.append("• **Improve Credit Score:** Pay down existing debts, maintain payment schedules, and address any credit report inaccuracies. Target: 750+")
                
                if st.session_state.loan_amount > 0 and st.session_state.annual_revenue > 0:
                    ratio = st.session_state.annual_revenue / st.session_state.loan_amount
                    if ratio < 5:
                        recommendations.append(f"• **Strengthen Financial Position:** Current ratio is {ratio:.2f}x. Consider reducing loan amount or demonstrating revenue growth to achieve 5x+ coverage")
                
                if st.session_state.years_in_business < 5:
                    recommendations.append("• **Build Operating History:** Continue stable operations and maintain positive financial performance to demonstrate sustainability")
                
                if not st.session_state.collateral_available:
                    recommendations.append("• **Provide Collateral:** Offering equipment, real estate, or other assets as security can significantly reduce risk and improve terms")
                
                if recommendations:
                    response += "\n".join(recommendations)
                    response += "\n\n**Timeline:** Most improvements require 6-12 months of demonstrated performance. The borrower may reapply once these metrics improve."
                else:
                    response += "This application already demonstrates strong fundamentals. To further optimize, consider:\n\n"
                    response += "• Offering additional collateral for better pricing\n"
                    response += "• Providing detailed financial projections\n"
                    response += "• Establishing banking relationship history"
                
                st.success(response)
            
            elif "Why did the compliance" in question:
                failed_checks = [check for check, passed in compliance_checks.items() if not passed]
                
                if failed_checks:
                    response = "The compliance verification identified the following deficiencies:\n\n"
                    
                    for check in failed_checks:
                        if "Credit Score" in check:
                            response += f"• **{check}:** Current score of {st.session_state.credit_score} does not meet the minimum threshold of 650. This requirement ensures borrower creditworthiness and regulatory compliance.\n\n"
                        elif "Revenue" in check:
                            response += f"• **{check}:** The loan amount (${st.session_state.loan_amount:,.0f}) exceeds annual revenue (${st.session_state.annual_revenue:,.0f}). This indicates potential over-leverage and repayment risk.\n\n"
                        elif "Years" in check:
                            response += f"• **{check}:** {st.session_state.years_in_business} years of operation is below the 2-year minimum. This threshold ensures operational stability.\n\n"
                    
                    response += "**Regulatory Context:** These requirements align with prudent lending standards and risk management best practices. Applications must satisfy all compliance criteria before proceeding to underwriting."
                    
                    st.error(response)
                else:
                    response = "Based on the current inputs, this application has **PASSED** all compliance checks:\n\n"
                    response += f"✓ Credit Score ({st.session_state.credit_score}) meets minimum threshold\n"
                    response += f"✓ Revenue (${st.session_state.annual_revenue:,.0f}) adequately covers loan amount\n"
                    response += f"✓ Operating history ({st.session_state.years_in_business} years) demonstrates stability\n\n"
                    response += "The application is compliant and ready for risk-based underwriting review."
                    
                    st.success(response)
            
            elif "secondary market trading" in question:
                response = f"""From a risk management perspective, the secondary market viability of this loan depends on several factors:

**Current Risk Profile:** {risk_level} RISK (Score: {risk_score}/100)

**Secondary Market Assessment:**
"""
                
                if risk_level == "LOW":
                    response += """
This loan demonstrates strong fundamentals that would be attractive to secondary market investors:
• Investment-grade credit profile
• Strong coverage ratios
• Conservative loan structure

**Recommendation:** Suitable for secondary market sale. Expected pricing at or near par value, depending on market conditions and loan terms.
"""
                elif risk_level == "MEDIUM":
                    response += """
This loan presents moderate characteristics for secondary market placement:
• Acceptable but not optimal credit metrics
• May require credit enhancement or pricing adjustments
• Suitable for specialized loan buyers

**Recommendation:** Possible secondary market candidate with appropriate pricing discount. Consider portfolio diversification strategies or credit enhancements.
"""
                else:
                    response += """
This loan profile presents challenges for secondary market placement:
• Elevated risk indicators reduce investor appeal
• Limited buyer universe for high-risk assets
• Significant pricing discounts would be required

**Recommendation:** Not recommended for immediate secondary market sale. Consider portfolio retention with enhanced monitoring, or evaluate after performance improvement.
"""
                
                st.info(response)
    
    else:
        st.info("Please complete a loan assessment in the 'Loan Evaluation' page first to use the AI Copilot.")
        
        st.markdown("---")
        st.subheader("About LoanGuardian Copilot")
        
        st.markdown("""
        LoanGuardian Copilot is an explainable AI assistant designed to provide transparent, 
        business-friendly explanations of lending decisions.
        
        **Key Features:**
        - Clear explanations of risk assessments
        - Actionable recommendations for borrowers
        - Compliance guidance and regulatory context
        - Secondary market viability analysis
        
        **Transparency Commitment:**
        All responses are based on documented business rules and industry best practices. 
        The system provides full traceability of decision factors, enabling informed review 
        and regulatory compliance.
        """)

# Footer
st.markdown("---")
st.markdown("**LoanGuardian AI** | LMA EDGE Hackathon | Commercial Lending & Risk Management")

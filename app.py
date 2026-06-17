import streamlit as st
import pandas as pd
import time
import os
import plotly.express as px
from services.gemini_service import analyze_company
from services.scoring_service import calculate_lead_score

# 1. Page Config for Premium Theme
st.set_page_config(
    page_title="GTM Lead Scoring Tool",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Modern Styling (Premium Aesthetics)
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 4px;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Setup
with st.sidebar:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=60)
    st.title("GTM Lead Control")
    st.caption("Target Company Enrichment & Prioritization Engine")
    st.write("---")
    
    st.subheader("API Configuration")
    # Bring Your Own Key input field (Optional override)
    api_key_input = st.text_input(
        "Bring Your Own API Key (Optional)", 
        type="password", 
        placeholder="AIzaSy...",
        help="Paste your own Gemini API key to override the default system key."
    )
    
    # Read default key from environment
    default_key = os.getenv("GEMINI_API_KEY")
    
    if api_key_input:
        st.success("Custom Key Override Active")
        active_api_key = api_key_input
    elif default_key:
        st.info("Default Key Active (from .env)")
        active_api_key = default_key
    else:
        st.warning("No API Key detected! Please enter a key above or configure .env.")
        active_api_key = None
            
    st.write("---")
    st.markdown("### Expected Import Format")
    st.markdown("""
    Your CSV file must include:
    - **`Company`** (Name of the target company)
    - **`Website`** (Company domain/URL)
    """)
    st.caption("v1.2.0 • BYOK & Custom ICP Enabled")

# 4. Main Panel Header
st.title("🎯 GTM Lead Scoring Tool")
st.write("Prioritize outbound sales pipeline by running AI-driven enrichment and Ideal Customer Profile (ICP) alignment scoring.")

# Expandable ICP Targets Panel (Interactive Scoring Modification)
with st.expander("🎯 Customize Ideal Customer Profile (ICP) & Scoring Rules", expanded=True):
    st.markdown("Customize matching keywords to calculate the 100-point GTM prioritization score.")
    col_a, col_b = st.columns(2)
    with col_a:
        target_industries_input = st.multiselect(
            "Target Industries",
            options=["software", "saas", "technology", "fintech", "finance", "healthcare", "e-commerce", "biotech", "logistics", "retail", "education", "manufacturing", "marketing", "real estate"],
            default=["software", "saas", "technology", "fintech", "finance", "healthcare", "e-commerce", "biotech"]
        )
        target_sizes_input = st.multiselect(
            "Target Company Sizes (Employees)",
            options=["1-10", "11-50", "51-200", "201-500", "501-1000", "1000+", "10,000+"],
            default=["51-200", "201-500", "501-1000", "1000+", "10,000+"]
        )
    with col_b:
        target_growth_input = st.multiselect(
            "Growth Signals Keywords",
            options=["funding", "hiring", "expansion", "growth", "launch", "acquire", "raising", "raised", "partnership", "ipo", "profitability"],
            default=["funding", "hiring", "expansion", "growth", "launch", "acquire", "raising", "raised"]
        )
        target_roles_input = st.multiselect(
            "Target Buyer Roles",
            options=["cto", "vp of product", "head of engineering", "vp of finance", "director of product", "vp of sales", "coo", "head of partnerships", "cro", "cmo", "vp of marketing"],
            default=["cto", "vp of product", "head of engineering", "vp of finance", "director of product", "vp of sales", "coo", "head of partnerships"]
        )

# Prepare target profile dict for the scoring calculation
target_profile = {
    "target_industries": [ind.lower() for ind in target_industries_input],
    "target_sizes": target_sizes_input,
    "growth_keywords": [kw.lower() for kw in target_growth_input],
    "buyer_personas": [role.lower() for role in target_roles_input]
}

# Session state to store processed leads across streamlit reruns
if 'processed_leads' not in st.session_state:
    st.session_state.processed_leads = None

# 5. File Upload Section
st.subheader("📁 Upload Leads File")
uploaded_file = st.file_uploader(
    "Drag and drop your target companies CSV below. Must contain 'Company' and 'Website' columns.",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        # Load the uploaded file
        df = pd.read_csv(uploaded_file)
        
        # Validate columns
        required_cols = ["Company", "Website"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.error(f"❌ Verification failed! The uploaded CSV is missing the following required columns: {', '.join([f'`{c}`' for c in missing_cols])}")
            st.info("Please format your CSV file headers to match exactly 'Company' and 'Website'.")
        else:
            st.success("✅ File verified successfully. Columns 'Company' and 'Website' detected.")
            
            # Show Preview
            with st.expander("🔍 View Uploaded Data Preview", expanded=False):
                st.dataframe(df, use_container_width=True)
            
            st.write("---")
            
            # 6. Analysis Trigger
            col1, col2 = st.columns([1, 4])
            with col1:
                analyze_button = st.button("🚀 Analyze Leads", type="primary", use_container_width=True)
            
            if analyze_button:
                if not active_api_key:
                    st.error("❌ Cannot start analysis: No Gemini API Key is active. Please add a key in the sidebar.")
                else:
                    st.subheader("⚙️ Processing Leads Pipeline")
                    
                    # Setup progress tracking container
                    progress_bar = st.progress(0.0)
                    status_message = st.empty()
                    
                    total_rows = len(df)
                    enriched_rows = []
                    
                    # Prepare to process every row
                    for index, row in df.iterrows():
                        company_name = row['Company']
                        website = row['Website']
                        
                        status_message.markdown(f"**Processing {index+1}/{total_rows}:** Researching `{company_name}` ({website})...")
                        
                        # Wrap API call and scoring in error handling
                        try:
                            with st.spinner(f"Querying Gemini API for {company_name}..."):
                                # Call AI enrichment (passing custom API key override if present)
                                enriched_info = analyze_company(company_name, api_key_override=active_api_key)
                                
                                # Call lead scoring engine using the customizable target profile
                                scoring_results = calculate_lead_score(enriched_info, target_profile=target_profile)
                                
                            # Handle 503 rate limits / transient server overloads with automatic retry once
                            if "503" in str(enriched_info.get("reason_to_prioritize", "")):
                                status_message.warning(f"⚠️ Service busy. Retrying `{company_name}` in 3 seconds...")
                                time.sleep(3.0)
                                with st.spinner(f"Retrying Gemini API for {company_name}..."):
                                    enriched_info = analyze_company(company_name, api_key_override=active_api_key)
                                    scoring_results = calculate_lead_score(enriched_info, target_profile=target_profile)

                            enriched_rows.append({
                                "Company": company_name,
                                "Industry": enriched_info.get("industry", "Error / Unknown"),
                                "Buyer Persona": enriched_info.get("buyer_persona", "Error / Unknown"),
                                "Score": scoring_results.get("score", 0),
                                "Priority": scoring_results.get("priority", "Low"),
                                "Reason to Prioritize": enriched_info.get("reason_to_prioritize", "Failed to retrieve analysis")
                            })
                            
                        except Exception as row_error:
                            st.error(f"❌ Error processing `{company_name}`: {row_error}")
                            enriched_rows.append({
                                "Company": company_name,
                                "Industry": "Error / Unknown",
                                "Buyer Persona": "Error / Unknown",
                                "Score": 0,
                                "Priority": "Low",
                                "Reason to Prioritize": f"Analysis failed: {str(row_error)}"
                            })
                        
                        # Update progress bar
                        progress_percentage = float((index + 1) / total_rows)
                        progress_bar.progress(progress_percentage)
                    
                    status_message.success(f"🎉 Analysis complete! Successfully processed {total_rows} companies.")
                    
                    # Store results in session state
                    st.session_state.processed_leads = pd.DataFrame(enriched_rows)
                    
    except Exception as e:
        st.error(f"Error reading the CSV file: {e}")

# 7. Results Section
if st.session_state.processed_leads is not None:
    st.write("---")
    st.subheader("📊 GTM Lead Scoring Results")
    
    results_df = st.session_state.processed_leads
    
    # Dashboard KPI Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(results_df)}</div><div class="metric-label">Total Companies</div></div>', unsafe_allow_html=True)
    with m2:
        high_priority = len(results_df[results_df["Priority"] == "High"])
        st.markdown(f'<div class="metric-card"><div class="metric-value">{high_priority}</div><div class="metric-label">High Priority Leads</div></div>', unsafe_allow_html=True)
    with m3:
        avg_score = round(results_df["Score"].mean(), 1) if not results_df.empty else 0
        st.markdown(f'<div class="metric-card"><div class="metric-value">{avg_score}</div><div class="metric-label">Average ICP Score</div></div>', unsafe_allow_html=True)
    with m4:
        medium_priority = len(results_df[results_df["Priority"] == "Medium"])
        st.markdown(f'<div class="metric-card"><div class="metric-value">{medium_priority}</div><div class="metric-label">Medium Priority Leads</div></div>', unsafe_allow_html=True)
        
    st.write(" ")
    
    # Visualization Charts
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Lead Priority Tier Distribution")
        priority_counts = results_df["Priority"].value_counts().reset_index()
        fig_pie = px.pie(
            priority_counts, 
            names="Priority", 
            values="count", 
            hole=0.45,
            color="Priority",
            color_discrete_map={
                "High": "#137333",
                "Medium": "#b06000",
                "Low": "#c5221f"
            }
        )
        fig_pie.update_layout(margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.subheader("Lead Scores comparison")
        sorted_results = results_df.sort_values(by="Score", ascending=False)
        fig_bar = px.bar(
            sorted_results, 
            x="Company", 
            y="Score", 
            color="Priority",
            text="Score",
            color_discrete_map={
                "High": "#137333",
                "Medium": "#b06000",
                "Low": "#c5221f"
            }
        )
        fig_bar.update_layout(yaxis_range=[0, 100], margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_bar, use_container_width=True)
        
    st.subheader("📋 Prioritized Leads List")
    
    # Exact requested columns order in st.dataframe
    exact_table_df = results_df[[
        "Company", 
        "Industry", 
        "Buyer Persona", 
        "Score", 
        "Priority", 
        "Reason to Prioritize"
    ]]
    
    st.dataframe(exact_table_df, use_container_width=True)
    
    # Export options
    csv_data = exact_table_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Prioritized Leads (CSV)",
        data=csv_data,
        file_name="gtm_prioritized_leads.csv",
        mime="text/csv",
        type="primary"
    )
else:
    # Beautiful call to action if no analysis run yet
    st.info("💡 Upload a CSV file above and click **Analyze Leads** to run real-time AI enrichment, ICP scoring, and outbound prioritization.")

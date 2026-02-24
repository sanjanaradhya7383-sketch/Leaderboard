import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Lead Scoring Dashboard", layout="wide")


st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Glass Cards */
.card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: 0.3s;
}
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
}

.metric-number {
    font-size: 34px;
    font-weight: bold;
    color: #00f5d4;
}

.section-title {
    font-size: 26px;
    font-weight: 600;
    margin-top: 30px;
    margin-bottom: 15px;
}

.sidebar .sidebar-content {
    background: rgba(0,0,0,0.4);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>AI Lead Scoring Dashboard</h1>", unsafe_allow_html=True)

data = {
    "Name": ["Rahul Sharma", "Priya Verma", "Amit Kumar", "Sneha Reddy", "Karan Patel"],
    "Source": ["Referral", "Event", "Website", "LinkedIn", "Referral"],
    "Score": [88, 72, 45, 91, 60]
}

df = pd.DataFrame(data)


def category(score):
    if score >= 80:
        return "Hot"
    elif score >= 60:
        return "Warm"
    else:
        return "Cold"

df["Category"] = df["Score"].apply(category)


st.sidebar.header("🔎 Filter Leads")
selected_category = st.sidebar.selectbox("Select Category", ["All", "Hot", "Warm", "Cold"])

if selected_category != "All":
    filtered_df = df[df["Category"] == selected_category]
else:
    filtered_df = df


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"<div class='card'><div class='metric-number'>{len(df)}</div>Total Leads</div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='card'><div class='metric-number'>{len(df[df['Category']=='Hot'])}</div>Hot Leads</div>", unsafe_allow_html=True)

with col3:
    conversion = round((len(df[df['Category']=='Hot'])/len(df))*100)
    st.markdown(f"<div class='card'><div class='metric-number'>{conversion}%</div>Conversion Rate</div>", unsafe_allow_html=True)

with col4:
    avg_score = round(df["Score"].mean())
    st.markdown(f"<div class='card'><div class='metric-number'>{avg_score}</div>Avg Score</div>", unsafe_allow_html=True)


st.markdown("<div class='section-title'> Lead List</div>", unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True)


col1, col2 = st.columns(2)

with col1:
    fig1 = px.pie(df, names="Category", title="Lead Distribution")
    fig1.update_layout(template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(df, x="Name", y="Score", color="Category", title="Lead Score Analysis")
    fig2.update_layout(template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)


st.markdown("<div class='section-title'> Lead Details</div>", unsafe_allow_html=True)

selected_lead = st.selectbox("Select Lead", df["Name"])
lead_data = df[df["Name"] == selected_lead].iloc[0]

st.write(f"### {lead_data['Name']} ({lead_data['Category']})")
st.progress(lead_data["Score"]/100)

st.write("#### AI Reasoning:")
st.write("✔ High engagement")
st.write("✔ Recent activity")
st.write("✔ Suitable plan selection")

if st.button(" Schedule Call"):
    st.success("Call Scheduled Successfully!")
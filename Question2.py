import streamlit as st
import plotly.express as px
import pandas as pd

# Data Load and Cleanup
udash = pd.read_csv('university_student_dashboard_data.csv')

# Normalize percentage values
udash['Retention Rate (%)'] = udash['Retention Rate (%)'] / 100
udash['Student Satisfaction (%)'] = udash['Student Satisfaction (%)'] / 100

# Logo and Page Config
st.set_page_config(layout="wide", page_icon="SUNY-Poly-logo.png")
st.image("SUNY-Poly-logo.png", width=250)

# Title
st.title("Student Admissions Dashboard")

# Sidebar Filters
year_options = sorted(udash['Year'].unique())
term_options = sorted(udash['Term'].unique())

selected_year = st.sidebar.selectbox("Select Year", ["All"] + list(year_options))
selected_term = st.sidebar.selectbox("Select Term", ["All"] + list(term_options))

# Filter Data Based on Selections
udash_filtered = udash.copy()
if selected_year != "All":
    udash_filtered = udash_filtered[udash_filtered['Year'] == selected_year]
if selected_term != "All":
    udash_filtered = udash_filtered[udash_filtered['Term'] == selected_term]

# KPIs Section
st.header("Key Indicators")
st.metric("Total Applications", f"{udash_filtered['Applications'].sum():,}")
st.metric("Total Admitted", f"{udash_filtered['Admitted'].sum():,}")
st.metric("Total Enrolled", f"{udash_filtered['Enrolled'].sum():,}")

# Enrollment Trends
st.header("Student Enrollment Trends")
enrollment_yoy = udash.groupby('Year', as_index=False)['Enrolled'].sum()
fig_enrollment = px.bar(
    enrollment_yoy, x='Year', y='Enrolled',
    title="Student Enrollment Year-over-Year",
    labels={"Enrolled": "Total Enrolled"}
)
fig_enrollment.update_xaxes(tickmode='linear', dtick=1)
st.plotly_chart(fig_enrollment, use_container_width=True)

# Enrollment by Department
dept_totals = {
    'Engineering': udash_filtered['Engineering Enrolled'].sum(),
    'Business': udash_filtered['Business Enrolled'].sum(),
    'Arts': udash_filtered['Arts Enrolled'].sum(),
    'Science': udash_filtered['Science Enrolled'].sum()
}
dept_df = pd.DataFrame(list(dept_totals.items()), columns=['Department', 'Enrolled'])
dept_fig = px.pie(
    dept_df, values='Enrolled', names='Department',
    title='Enrollment by Department', hole=0.4
)
dept_fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(dept_fig, use_container_width=True)

# Retention and Satisfaction Trends
st.header("Retention & Student Satisfaction Trends")
trend_data = udash.groupby('Year', as_index=False)[['Retention_Rate', 'Student_Satisfaction']].mean()
fig_trend = px.line(
    trend_data, x='Year', y=['Retention_Rate (%)', 'Student_Satisfaction (%)'],
    title="Retention & Satisfaction Trends Over Time",
    labels={"Retention_Rate (%)": "Retention Rate", "Student Satisfaction (%)": "Student Satisfaction"}
)
fig_trend.update_yaxes(title_text="Rate (%)")
st.plotly_chart(fig_trend)

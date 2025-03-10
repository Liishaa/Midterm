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
# Spring and Fall Term Statistics
st.subheader("Fall All Years")
col1, col2, col3 = st.columns(3)
col1.metric("Total Applications", f"{udash[udash['Term'] == 'Fall']['Applications'].sum():,}")
col2.metric("Total Admitted", f"{udash[udash['Term'] == 'Fall']['Admitted'].sum():,}")
col3.metric("Total Enrolled", f"{udash[udash['Term'] == 'Fall']['Enrolled'].sum():,}")

st.subheader("Spring All Years")
col4, col5, col6 = st.columns(3)
col4.metric("Total Applications", f"{udash[udash['Term'] == 'Spring']['Applications'].sum():,}")
col5.metric("Total Admitted", f"{udash[udash['Term'] == 'Spring']['Admitted'].sum():,}")
col6.metric("Total Enrolled", f"{udash[udash['Term'] == 'Spring']['Enrolled'].sum():,}")

st.metric("Total Applications", f"{udash_filtered['Applications'].sum():,}")
st.metric("Total Admitted", f"{udash_filtered['Admitted'].sum():,}")
st.metric("Total Enrolled", f"{udash_filtered['Enrolled'].sum():,}")
# Spring vs. Fall Enrollment Stats
spring_enrollment = udash[udash['Term'] == 'Spring']['Enrolled'].sum()
fall_enrollment = udash[udash['Term'] == 'Fall']['Enrolled'].sum()

col1, col2 = st.columns(2)
col1.metric("Total Enrolled (Spring)", f"{spring_enrollment:,}")
col2.metric("Total Enrolled (Fall)", f"{fall_enrollment:,}")


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



#  Retention and Satisfaction Trends
st.header("Retention & Student Satisfaction Trends")
trend_data = udash.groupby('Year', as_index=False)[['Retention Rate (%)', 'Student Satisfaction (%)']].mean()

fig_trend = px.line(
    trend_data, x='Year', y=['Retention Rate (%)', 'Student Satisfaction (%)'],
    title="Retention & Satisfaction Trends Over Time",
    labels={"Retention Rate (%)": "Retention Rate", "Student Satisfaction (%)": "Student Satisfaction"}
)
fig_trend.update_traces(hovertemplate="Year: %{x}<br>Rate: %{y:.2%}")  # Adding tooltip
st.plotly_chart(fig_trend)

fig_trend.update_yaxes(title_text="Rate (%)")
st.plotly_chart(fig_trend)

# Group data by Year and Term
st.header("Spring vs. Fall Trends")
term_trends = udash.groupby(['Year', 'Term'], as_index=False)[['Retention Rate (%)', 'Student Satisfaction (%)']].mean()

fig_term_trends = px.line(
    term_trends, x='Year', y=['Retention Rate (%)', 'Student Satisfaction (%)'], color='Term',
    title="Spring vs. Fall: Retention & Satisfaction Trends",
    labels={"Retention Rate (%)": "Retention Rate", "Student Satisfaction (%)": "Student Satisfaction"}
)
fig_term_trends.update_traces(hovertemplate="Year: %{x}<br>Rate: %{y:.2%}")  # Adding tooltip
st.plotly_chart(fig_term_trends, use_container_width=True)

# Group by Year and Department
st.header("Department-Wise Enrollment Trends")
dept_trends = udash.groupby('Year', as_index=False)[['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']].sum()

fig_dept_trends = px.bar(
    dept_trends, x='Year', y=['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled'],
    title="Enrollment Trends by Department",
    labels={"value": "Total Enrolled", "variable": "Department"},
    barmode="group"
)
st.plotly_chart(fig_dept_trends, use_container_width=True)

st.header("Key Findings & Insights")

st.write("""
- **Enrollment Growth:** Engineering and Science departments have seen a steady rise in enrollment.
- **Retention Challenges:** Retention rates in the Fall term are slightly lower than in Spring.
- **Student Satisfaction:** Business students report the highest satisfaction levels over the years.
- **Actionable Insights:** University should focus on improving Fall retention rates by offering better support programs.
""")


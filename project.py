import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Indian Army Defence Equipment Analysis",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.main-title {
    font-size: 38px;
    font-weight: bold;
}

.subtitle {
    font-size: 17px;
    color: gray;
}

[data-testid="stMetric"] {
    border: 1px solid #dddddd;
    border-radius: 10px;
    padding: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">🛡️ Indian Army Defence Equipment & Modernization Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Interactive Defence Equipment Intelligence Dashboard</div>',
    unsafe_allow_html=True
)

st.write(
    """
    This dashboard analyzes Indian Army defence equipment based on
    categories, manufacturers, procurement quantity, estimated cost,
    origin, modernization status and induction trends.
    """
)

st.divider()

@st.cache_data
def load_data():
    file_path = "Indian Army Defence Equipment & Modernization Analysis.xlsx"
    data = pd.read_excel(file_path)
    return data

try:

    df = load_data()

except FileNotFoundError:

    st.error(
        "Excel file not found. Please check the file location."
    )

    st.stop()

except Exception as error:

    st.error(
        f"Error while loading the Excel file: {error}"
    )

    st.stop()

df = df.dropna(how="all").copy()

numeric_columns = [
    "Year_of_Induction",
    "Quantity_Procured",
    "Estimated_Unit_Cost_Cr_INR",
    "Total_Estimated_Value_Cr_INR"
]

for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

st.sidebar.title("🎛️ Dashboard Filters")

st.sidebar.write(
    "Select filters to explore the equipment data."
)

category_list = sorted(
    df["Category"]
    .dropna()
    .unique()
    .tolist()
)

selected_categories = st.sidebar.multiselect(
    "📂 Equipment Category",
    category_list,
    default=category_list
)

manufacturer_list = sorted(
    df["Primary_Manufacturer"]
    .dropna()
    .unique()
    .tolist()
)

selected_manufacturers = st.sidebar.multiselect(
    "🏭 Primary Manufacturer",
    manufacturer_list,
    default=manufacturer_list
)

origin_list = sorted(
    df["Origin_Type"]
    .dropna()
    .unique()
    .tolist()
)

selected_origins = st.sidebar.multiselect(
    "🌍 Origin Type",
    origin_list,
    default=origin_list
)

modernization_list = sorted(
    df["Modernization_Status"]
    .dropna()
    .unique()
    .tolist()
)

selected_modernization = st.sidebar.multiselect(
    "🔧 Modernization Status",
    modernization_list,
    default=modernization_list
)

role_list = sorted(
    df["Primary_Role"]
    .dropna()
    .unique()
    .tolist()
)

selected_roles = st.sidebar.multiselect(
    "🎯 Primary Operational Role",
    role_list,
    default=role_list
)

st.sidebar.divider()

min_year = int(
    df["Year_of_Induction"]
    .dropna()
    .min()
)

max_year = int(
    df["Year_of_Induction"]
    .dropna()
    .max()
)

selected_years = st.sidebar.slider(
    "📅 Induction Year",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

min_quantity = int(
    df["Quantity_Procured"]
    .dropna()
    .min()
)

max_quantity = int(
    df["Quantity_Procured"]
    .dropna()
    .max()
)

selected_quantity = st.sidebar.slider(
    "📦 Procurement Quantity",
    min_value=min_quantity,
    max_value=max_quantity,
    value=(min_quantity, max_quantity)
)

min_cost = float(
    df["Estimated_Unit_Cost_Cr_INR"]
    .dropna()
    .min()
)

max_cost = float(
    df["Estimated_Unit_Cost_Cr_INR"]
    .dropna()
    .max()
)

selected_cost = st.sidebar.slider(
    "💰 Unit Cost (₹ Crore)",
    min_value=min_cost,
    max_value=max_cost,
    value=(min_cost, max_cost)
)

filtered_df = df.copy()

filtered_df = filtered_df[
    filtered_df["Category"].isin(
        selected_categories
    )
]

filtered_df = filtered_df[
    filtered_df["Primary_Manufacturer"].isin(
        selected_manufacturers
    )
]

filtered_df = filtered_df[
    filtered_df["Origin_Type"].isin(
        selected_origins
    )
]

filtered_df = filtered_df[
    filtered_df["Modernization_Status"].isin(
        selected_modernization
    )
]

filtered_df = filtered_df[
    filtered_df["Primary_Role"].isin(
        selected_roles
    )
]

filtered_df = filtered_df[
    filtered_df["Year_of_Induction"].between(
        selected_years[0],
        selected_years[1]
    )
]

filtered_df = filtered_df[
    filtered_df["Quantity_Procured"].between(
        selected_quantity[0],
        selected_quantity[1]
    )
]

filtered_df = filtered_df[
    filtered_df["Estimated_Unit_Cost_Cr_INR"].between(
        selected_cost[0],
        selected_cost[1]
    )
]

st.sidebar.divider()

st.sidebar.success(
    f"{len(filtered_df):,} records selected"
)

st.sidebar.info(
    f"{len(df):,} total records"
)

st.subheader("📊 Key Performance Indicators")

metric1, metric2, metric3, metric4, metric5 = st.columns(5)

with metric1:

    st.metric(
        "Total Equipment",
        f"{len(filtered_df):,}"
    )

with metric2:

    total_quantity = filtered_df[
        "Quantity_Procured"
    ].sum()

    st.metric(
        "Quantity Procured",
        f"{total_quantity:,.0f}"
    )

with metric3:

    total_value = filtered_df[
        "Total_Estimated_Value_Cr_INR"
    ].sum()

    st.metric(
        "Estimated Value",
        f"₹ {total_value:,.2f} Cr"
    )

with metric4:

    st.metric(
        "Equipment Categories",
        filtered_df["Category"].nunique()
    )

with metric5:

    st.metric(
        "Manufacturers",
        filtered_df["Primary_Manufacturer"].nunique()
    )

st.divider()

st.subheader("📋 Equipment Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)

st.divider()

st.subheader("📊 Equipment Distribution by Category")

category_count = (
    filtered_df["Category"]
    .value_counts()
    .reset_index()
)

category_count.columns = [
    "Category",
    "Equipment_Count"
]

fig1 = px.bar(
    category_count,
    x="Category",
    y="Equipment_Count",
    text="Equipment_Count",
    title="Indian Army Equipment by Category"
)

fig1.update_layout(
    xaxis_title="Equipment Category",
    yaxis_title="Number of Equipment",
    height=500
)

fig1.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig1,
    use_container_width=True,
    key="category_chart"
)

st.divider()

st.subheader("🏭 Top Equipment Manufacturers")

manufacturer_count = (
    filtered_df["Primary_Manufacturer"]
    .value_counts()
    .head(10)
    .reset_index()
)

manufacturer_count.columns = [
    "Manufacturer",
    "Equipment_Count"
]

fig2 = px.bar(
    manufacturer_count,
    x="Equipment_Count",
    y="Manufacturer",
    orientation="h",
    text="Equipment_Count",
    title="Top 10 Equipment Manufacturers"
)

fig2.update_layout(
    xaxis_title="Number of Equipment",
    yaxis_title="Manufacturer",
    height=550
)

fig2.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig2,
    use_container_width=True,
    key="manufacturer_chart"
)

st.divider()

st.subheader("🌍 Indigenous vs Imported Equipment")

origin_count = (
    filtered_df["Origin_Type"]
    .value_counts()
    .reset_index()
)

origin_count.columns = [
    "Origin_Type",
    "Equipment_Count"
]

fig3 = px.pie(
    origin_count,
    names="Origin_Type",
    values="Equipment_Count",
    hole=0.45,
    title="Equipment Origin Distribution"
)

fig3.update_layout(
    height=500
)

st.plotly_chart(
    fig3,
    use_container_width=True,
    key="origin_chart"
)

st.divider()

st.subheader("🔧 Equipment Modernization Status")

modernization = (
    filtered_df["Modernization_Status"]
    .value_counts()
    .reset_index()
)

modernization.columns = [
    "Modernization_Status",
    "Equipment_Count"
]

fig4 = px.bar(
    modernization,
    x="Modernization_Status",
    y="Equipment_Count",
    text="Equipment_Count",
    title="Equipment by Modernization Status"
)

fig4.update_layout(
    xaxis_title="Modernization Status",
    yaxis_title="Number of Equipment",
    height=500
)

fig4.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig4,
    use_container_width=True,
    key="modernization_chart"
)

st.divider()

st.subheader("📅 Equipment Induction Trend")

year_data = (
    filtered_df
    .groupby("Year_of_Induction")
    .size()
    .reset_index(
        name="Equipment_Count"
    )
    .sort_values(
        "Year_of_Induction"
    )
)

fig5 = px.line(
    year_data,
    x="Year_of_Induction",
    y="Equipment_Count",
    markers=True,
    title="Equipment Induction Trend Over the Years"
)

fig5.update_layout(
    xaxis_title="Year of Induction",
    yaxis_title="Number of Equipment",
    height=500
)

st.plotly_chart(
    fig5,
    use_container_width=True,
    key="induction_chart"
)

st.divider()

st.subheader("🎯 Equipment Distribution by Primary Role")

role_data = (
    filtered_df["Primary_Role"]
    .value_counts()
    .reset_index()
)

role_data.columns = [
    "Primary_Role",
    "Equipment_Count"
]

fig6 = px.bar(
    role_data,
    x="Equipment_Count",
    y="Primary_Role",
    orientation="h",
    text="Equipment_Count",
    title="Equipment by Primary Operational Role"
)

fig6.update_layout(
    xaxis_title="Number of Equipment",
    yaxis_title="Primary Role",
    height=550
)

fig6.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig6,
    use_container_width=True,
    key="role_chart"
)

st.divider()

st.subheader("💰 Estimated Cost by Equipment Category")

cost_category = (
    filtered_df
    .groupby("Category")[
        "Total_Estimated_Value_Cr_INR"
    ]
    .sum()
    .reset_index()
    .sort_values(
        "Total_Estimated_Value_Cr_INR",
        ascending=False
    )
)

fig7 = px.bar(
    cost_category,
    x="Category",
    y="Total_Estimated_Value_Cr_INR",
    text_auto=".2f",
    title="Total Estimated Equipment Value by Category"
)

fig7.update_layout(
    xaxis_title="Equipment Category",
    yaxis_title="Total Estimated Value (₹ Crore)",
    height=550
)

st.plotly_chart(
    fig7,
    use_container_width=True,
    key="category_cost_chart"
)

st.divider()

st.subheader("💵 Top 10 Equipment by Estimated Unit Cost")

expensive = (
    filtered_df[
        [
            "Equipment_Name",
            "Category",
            "Estimated_Unit_Cost_Cr_INR"
        ]
    ]
    .sort_values(
        "Estimated_Unit_Cost_Cr_INR",
        ascending=False
    )
    .head(10)
)

fig8 = px.bar(
    expensive,
    x="Estimated_Unit_Cost_Cr_INR",
    y="Equipment_Name",
    orientation="h",
    text="Estimated_Unit_Cost_Cr_INR",
    title="Top 10 Equipment by Estimated Unit Cost"
)

fig8.update_layout(
    xaxis_title="Estimated Unit Cost (₹ Crore)",
    yaxis_title="Equipment",
    height=600
)

st.plotly_chart(
    fig8,
    use_container_width=True,
    key="unit_cost_chart"
)

st.divider()

st.subheader("📦 Top 10 Equipment by Quantity Procured")

quantity_data = (
    filtered_df[
        [
            "Equipment_Name",
            "Category",
            "Quantity_Procured"
        ]
    ]
    .sort_values(
        "Quantity_Procured",
        ascending=False
    )
    .head(10)
)

fig9 = px.bar(
    quantity_data,
    x="Quantity_Procured",
    y="Equipment_Name",
    orientation="h",
    text="Quantity_Procured",
    title="Top 10 Equipment by Quantity Procured"
)

fig9.update_layout(
    xaxis_title="Quantity Procured",
    yaxis_title="Equipment",
    height=600
)

st.plotly_chart(
    fig9,
    use_container_width=True,
    key="quantity_chart"
)

st.divider()

st.subheader("📈 Quantity Procured vs Estimated Unit Cost")

scatter_data = filtered_df.dropna(
    subset=[
        "Quantity_Procured",
        "Estimated_Unit_Cost_Cr_INR"
    ]
)

fig10 = px.scatter(
    scatter_data,
    x="Quantity_Procured",
    y="Estimated_Unit_Cost_Cr_INR",
    color="Category",
    hover_name="Equipment_Name",
    size="Quantity_Procured",
    title="Relationship Between Quantity Procured and Unit Cost"
)

fig10.update_layout(
    xaxis_title="Quantity Procured",
    yaxis_title="Estimated Unit Cost (₹ Crore)",
    height=600
)

st.plotly_chart(
    fig10,
    use_container_width=True,
    key="scatter_chart"
)

st.divider()

st.subheader("🏭 Manufacturer-wise Equipment Value")

manufacturer_value = (
    filtered_df
    .groupby("Primary_Manufacturer")[
        "Total_Estimated_Value_Cr_INR"
    ]
    .sum()
    .reset_index()
    .sort_values(
        "Total_Estimated_Value_Cr_INR",
        ascending=False
    )
    .head(10)
)

fig11 = px.bar(
    manufacturer_value,
    x="Total_Estimated_Value_Cr_INR",
    y="Primary_Manufacturer",
    orientation="h",
    text_auto=".2f",
    title="Top 10 Manufacturers by Total Estimated Equipment Value"
)

fig11.update_layout(
    xaxis_title="Total Estimated Value (₹ Crore)",
    yaxis_title="Manufacturer",
    height=600
)

st.plotly_chart(
    fig11,
    use_container_width=True,
    key="manufacturer_value_chart"
)

st.divider()

st.subheader("🌍 Origin Type vs Modernization Status")

origin_modernization = pd.crosstab(
    filtered_df["Origin_Type"],
    filtered_df["Modernization_Status"]
).reset_index()

melted_data = origin_modernization.melt(
    id_vars="Origin_Type",
    var_name="Modernization_Status",
    value_name="Equipment_Count"
)

fig12 = px.bar(
    melted_data,
    x="Origin_Type",
    y="Equipment_Count",
    color="Modernization_Status",
    barmode="stack",
    title="Modernization Status by Equipment Origin"
)

fig12.update_layout(
    xaxis_title="Origin Type",
    yaxis_title="Number of Equipment",
    height=550
)

st.plotly_chart(
    fig12,
    use_container_width=True,
    key="origin_modernization_chart"
)

st.divider()


st.subheader("🕰️ Equipment Distribution by Modernization Era")

era_data = (
    filtered_df["Modernization_Era"]
    .value_counts()
    .reset_index()
)

era_data.columns = [
    "Modernization_Era",
    "Equipment_Count"
]

fig13 = px.bar(
    era_data,
    x="Modernization_Era",
    y="Equipment_Count",
    text="Equipment_Count",
    title="Equipment Distribution Across Modernization Eras"
)

fig13.update_layout(
    xaxis_title="Modernization Era",
    yaxis_title="Number of Equipment",
    height=500
)

fig13.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig13,
    use_container_width=True,
    key="era_chart"
)

st.divider()

st.subheader("📦 Procurement Quantity Trend")

procurement_year = (
    filtered_df
    .groupby("Year_of_Induction")[
        "Quantity_Procured"
    ]
    .sum()
    .reset_index()
    .sort_values(
        "Year_of_Induction"
    )
)

fig14 = px.line(
    procurement_year,
    x="Year_of_Induction",
    y="Quantity_Procured",
    markers=True,
    title="Total Equipment Quantity Procured by Induction Year"
)

fig14.update_layout(
    xaxis_title="Year",
    yaxis_title="Total Quantity Procured",
    height=500
)

st.plotly_chart(
    fig14,
    use_container_width=True,
    key="procurement_chart"
)

st.divider()

st.subheader("🔍 Advanced Equipment Analysis")

st.markdown("### 💎 Top Equipment by Total Estimated Value")

top_value_equipment = (
    filtered_df[
        [
            "Equipment_Name",
            "Category",
            "Quantity_Procured",
            "Estimated_Unit_Cost_Cr_INR",
            "Total_Estimated_Value_Cr_INR"
        ]
    ]
    .sort_values(
        "Total_Estimated_Value_Cr_INR",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_value_equipment,
    use_container_width=True,
    hide_index=True
)

st.markdown("### 📊 Category-wise Performance")

category_analysis = (
    filtered_df
    .groupby("Category")
    .agg(
        Equipment_Count=("Equipment_Name", "count"),
        Total_Quantity=("Quantity_Procured", "sum"),
        Total_Value=("Total_Estimated_Value_Cr_INR", "sum"),
        Average_Unit_Cost=("Estimated_Unit_Cost_Cr_INR", "mean")
    )
    .reset_index()
    .sort_values(
        "Total_Value",
        ascending=False
    )
)

st.dataframe(
    category_analysis,
    use_container_width=True,
    hide_index=True
)

st.markdown("### 🏭 Manufacturer Performance")

manufacturer_analysis = (
    filtered_df
    .groupby("Primary_Manufacturer")
    .agg(
        Equipment_Count=("Equipment_Name", "count"),
        Total_Quantity=("Quantity_Procured", "sum"),
        Total_Value=("Total_Estimated_Value_Cr_INR", "sum"),
        Average_Unit_Cost=("Estimated_Unit_Cost_Cr_INR", "mean")
    )
    .reset_index()
    .sort_values(
        "Total_Value",
        ascending=False
    )
    .head(15)
)

st.dataframe(
    manufacturer_analysis,
    use_container_width=True,
    hide_index=True
)

st.markdown("### 🌍 Origin-wise Analysis")

origin_analysis = (
    filtered_df
    .groupby("Origin_Type")
    .agg(
        Equipment_Count=("Equipment_Name", "count"),
        Total_Quantity=("Quantity_Procured", "sum"),
        Total_Value=("Total_Estimated_Value_Cr_INR", "sum")
    )
    .reset_index()
    .sort_values(
        "Total_Value",
        ascending=False
    )
)

st.dataframe(
    origin_analysis,
    use_container_width=True,
    hide_index=True
)

st.markdown("### 🔧 Modernization Analysis")

modernization_analysis = (
    filtered_df
    .groupby("Modernization_Status")
    .agg(
        Equipment_Count=("Equipment_Name", "count"),
        Total_Quantity=("Quantity_Procured", "sum"),
        Total_Value=("Total_Estimated_Value_Cr_INR", "sum")
    )
    .reset_index()
    .sort_values(
        "Equipment_Count",
        ascending=False
    )
)

st.dataframe(
    modernization_analysis,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("🧠 Key Analytical Insights")

if not filtered_df.empty:

    insight1, insight2 = st.columns(2)

    with insight1:

        most_common_category = (
            filtered_df["Category"]
            .value_counts()
            .idxmax()
        )

        top_manufacturer = (
            filtered_df["Primary_Manufacturer"]
            .value_counts()
            .idxmax()
        )

        top_modernization = (
            filtered_df["Modernization_Status"]
            .value_counts()
            .idxmax()
        )

        st.info(
            f"""
            **Most Represented Category:**  
            {most_common_category}

            **Most Represented Manufacturer:**  
            {top_manufacturer}

            **Most Common Modernization Status:**  
            {top_modernization}
            """
        )

    with insight2:

        highest_value_row = filtered_df.loc[
            filtered_df[
                "Total_Estimated_Value_Cr_INR"
            ].idxmax()
        ]

        highest_value_equipment = (
            highest_value_row["Equipment_Name"]
        )

        highest_unit_cost = (
            filtered_df[
                "Estimated_Unit_Cost_Cr_INR"
            ].max()
        )

        st.success(
            f"""
            **Highest Total Value Equipment:**  
            {highest_value_equipment}

            **Highest Unit Cost:**  
            ₹ {highest_unit_cost:,.2f} Crore

            **Total Estimated Value:**  
            ₹ {total_value:,.2f} Crore
            """
        )

else:

    st.warning(
        "No equipment records match the selected filters."
    )

st.divider()

st.subheader("📥 Download Analysis Data")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Dataset",
    data=csv_data,
    file_name="indian_army_filtered_equipment_analysis.csv",
    mime="text/csv",
    use_container_width=True,
    key="download_csv"
)

st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:20px;">

    <h3>🛡️ Indian Army Defence Equipment & Modernization Analysis</h3>

    <p>
    Major Project using Python, Pandas, Plotly and Streamlit
    </p>

    <p>
    Data Analysis • Visualization • Procurement Analysis •
    Modernization Analysis • Interactive Dashboard
    </p>

    </div>
    """,
    unsafe_allow_html=True
)
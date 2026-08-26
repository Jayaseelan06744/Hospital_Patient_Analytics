import streamlit as st
import pandas as pd

from snowflake.snowpark.context import get_active_session


st.set_page_config(
    page_title="Hospital Patient Analytics",
    page_icon="🏥",
    layout="wide"
)

session = get_active_session()


query = """
SELECT
    PATIENT_ID,
    AGE,
    GENDER,
    CONDITION,
    MEDICATION,
    ADMISSION_DATE,
    DISCHARGE_DATE,
    PATIENT_STATE,
    YEAR_OF_ADMISSION,
    LENGTH_OF_STAY,
    READMISSION,
    OUTCOME,
    SATISFACTION,
    INSURANCE_CLAIMED,
    TOTAL_COST
FROM HOSPITAL_ANALYTICS.PUBLIC.HOSPITAL_PATIENTS_RAW
"""

df = session.sql(query).to_pandas()

st.title("🏥 Hospital Patient Analytics Dashboard")

st.markdown(
    "Interactive dashboard for analyzing hospital patient records "
    "using Snowflake and Streamlit."
)


st.divider()

st.subheader("🔍 Patient Search")

search_col1, search_col2 = st.columns([3, 1])


with search_col1:

    patient_id = st.text_input(
        "Enter Patient ID",
        placeholder="Example: 2"
    )


with search_col2:

    st.write("")
    st.write("")

    search_button = st.button(
        "🔎 Search Patient",
        use_container_width=True
    )


if search_button:

    if patient_id.strip() == "":
        
        st.warning(
            "⚠️ Please enter a Patient ID."
        )

    else:

        search_id = patient_id.strip().upper()

        patient_result = df[
            df["PATIENT_ID"]
            .astype(str)
            .str.upper()
            == search_id
        ]

        if patient_result.empty:

            st.error(
                f"❌ Patient ID '{search_id}' was not found."
            )

        else:

            st.success(
                f"✅ Patient '{search_id}' found!"
            )

            patient = patient_result.iloc[0]


            st.divider()

            st.subheader(
                f"👤 Patient Profile — {search_id}"
            )


            detail_col1, detail_col2, detail_col3 = st.columns(3)

            with detail_col1:

                st.markdown(
                    f"""
                    **Patient ID:**  
                    {patient["PATIENT_ID"]}

                    **Age:**  
                    {patient["AGE"]}

                    **Gender:**  
                    {patient["GENDER"]}

                    **Condition:**  
                    {patient["CONDITION"]}

                    **Medication:**  
                    {patient["MEDICATION"]}
                    """
                )

            with detail_col2:

                st.markdown(
                    f"""
                    **Admission Date:**  
                    {patient["ADMISSION_DATE"]}

                    **Discharge Date:**  
                    {patient["DISCHARGE_DATE"]}

                    **Patient State:**  
                    {patient["PATIENT_STATE"]}

                    **Year of Admission:**  
                    {patient["YEAR_OF_ADMISSION"]}

                    **Length of Stay:**  
                    {patient["LENGTH_OF_STAY"]} days
                    """
                )

            with detail_col3:

                st.markdown(
                    f"""
                    **Readmission:**  
                    {patient["READMISSION"]}

                    **Outcome:**  
                    {patient["OUTCOME"]}

                    **Insurance Claimed:**  
                    {patient["INSURANCE_CLAIMED"]}

                    **Satisfaction:**  
                    {patient["SATISFACTION"]}

                    **Total Cost:**  
                    ${patient["TOTAL_COST"]:,.0f}
                    """
                )

            st.divider()

            st.subheader(
                "📊 Patient Performance Indicators"
            )


            kpi1, kpi2, kpi3, kpi4 = st.columns(4)


            with kpi1:

                st.metric(
                    "🎂 Age",
                    f'{patient["AGE"]}'
                )


            with kpi2:

                st.metric(
                    "🛏️ Length of Stay",
                    f'{patient["LENGTH_OF_STAY"]} days'
                )


            with kpi3:

                st.metric(
                    "⭐ Satisfaction",
                    f'{patient["SATISFACTION"]:.1f}'
                )


            with kpi4:

                st.metric(
                    "💰 Total Cost",
                    f'${patient["TOTAL_COST"]:,.0f}'
                )

            patient_condition = patient["CONDITION"]


            condition_patients = df[
                df["CONDITION"]
                == patient_condition
            ]


            avg_condition_cost = (
                condition_patients["TOTAL_COST"]
                .mean()
            )


            avg_condition_stay = (
                condition_patients["LENGTH_OF_STAY"]
                .mean()
            )


            avg_condition_satisfaction = (
                condition_patients["SATISFACTION"]
                .mean()
            )

            st.divider()

            st.subheader(
                f"📈 Patient vs {patient_condition} Average"
            )


            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:

                st.markdown(
                    "### 💰 Cost Comparison"
                )


                cost_comparison = pd.DataFrame(
                    {
                        "Patient": [
                            patient["TOTAL_COST"]
                        ],

                        f"{patient_condition} Average": [
                            avg_condition_cost
                        ]
                    }
                )


                st.bar_chart(
                    cost_comparison.T,
                    use_container_width=True
                )


                st.caption(
                    f"Patient Cost: "
                    f"${patient['TOTAL_COST']:,.0f} | "
                    f"{patient_condition} Average: "
                    f"${avg_condition_cost:,.0f}"
                )

            with chart_col2:

                st.markdown(
                    "### 🛏️ Length of Stay Comparison"
                )


                stay_comparison = pd.DataFrame(
                    {
                        "Patient": [
                            patient["LENGTH_OF_STAY"]
                        ],

                        f"{patient_condition} Average": [
                            avg_condition_stay
                        ]
                    }
                )


                st.bar_chart(
                    stay_comparison.T,
                    use_container_width=True
                )


                st.caption(
                    f"Patient Stay: "
                    f"{patient['LENGTH_OF_STAY']:.1f} days | "
                    f"{patient_condition} Average: "
                    f"{avg_condition_stay:.1f} days"
                )
                
            st.markdown(
                "### ⭐ Satisfaction Comparison"
            )


            satisfaction_comparison = pd.DataFrame(
                {
                    "Patient": [
                        patient["SATISFACTION"]
                    ],

                    f"{patient_condition} Average": [
                        avg_condition_satisfaction
                    ]
                }
            )


            st.bar_chart(
                satisfaction_comparison.T,
                use_container_width=True
            )


            st.caption(
                f"Patient Satisfaction: "
                f"{patient['SATISFACTION']:.1f} | "
                f"{patient_condition} Average: "
                f"{avg_condition_satisfaction:.1f}"
            )

            st.divider()

            st.subheader(
                "📝 Patient Analytics Insights"
            )


            cost_difference = (
                patient["TOTAL_COST"]
                - avg_condition_cost
            )


            stay_difference = (
                patient["LENGTH_OF_STAY"]
                - avg_condition_stay
            )


            satisfaction_difference = (
                patient["SATISFACTION"]
                - avg_condition_satisfaction
            )


            insight_col1, insight_col2, insight_col3 = st.columns(3)


            with insight_col1:

                if cost_difference > 0:

                    st.warning(
                        f"""
                        💰 **Cost Insight**

                        Patient cost is
                        **${abs(cost_difference):,.0f} higher**
                        than the average cost for
                        {patient_condition} patients.
                        """
                    )

                elif cost_difference < 0:

                    st.success(
                        f"""
                        💰 **Cost Insight**

                        Patient cost is
                        **${abs(cost_difference):,.0f} lower**
                        than the average cost for
                        {patient_condition} patients.
                        """
                    )

                else:

                    st.info(
                        """
                        💰 **Cost Insight**

                        Patient cost is equal to
                        the condition average.
                        """
                    )


            with insight_col2:

                if stay_difference > 0:

                    st.warning(
                        f"""
                        🛏️ **Stay Insight**

                        Patient stayed
                        **{abs(stay_difference):.1f} days longer**
                        than the average for
                        {patient_condition} patients.
                        """
                    )

                elif stay_difference < 0:

                    st.success(
                        f"""
                        🛏️ **Stay Insight**

                        Patient stayed
                        **{abs(stay_difference):.1f} days less**
                        than the average for
                        {patient_condition} patients.
                        """
                    )

                else:

                    st.info(
                        """
                        🛏️ **Stay Insight**

                        Patient length of stay
                        is equal to the average.
                        """
                    )

            with insight_col3:

                if satisfaction_difference > 0:

                    st.success(
                        f"""
                        ⭐ **Satisfaction Insight**

                        Patient satisfaction is
                        **{abs(satisfaction_difference):.1f} points higher**
                        than the condition average.
                        """
                    )

                elif satisfaction_difference < 0:

                    st.warning(
                        f"""
                        ⭐ **Satisfaction Insight**

                        Patient satisfaction is
                        **{abs(satisfaction_difference):.1f} points lower**
                        than the condition average.
                        """
                    )

                else:

                    st.info(
                        """
                        ⭐ **Satisfaction Insight**

                        Patient satisfaction is
                        equal to the condition average.
                        """
                    )


            st.divider()

            st.subheader(
                "📋 Complete Patient Record"
            )


            st.dataframe(
                patient_result,
                use_container_width=True,
                hide_index=True
            )



st.sidebar.title("🔎 Filters")


conditions = ["All"] + sorted(
    df["CONDITION"]
    .dropna()
    .unique()
    .tolist()
)


selected_condition = st.sidebar.selectbox(
    "🏥 Condition",
    conditions
)
genders = ["All"] + sorted(
    df["GENDER"]
    .dropna()
    .unique()
    .tolist()
)


selected_gender = st.sidebar.selectbox(
    "⚥ Gender",
    genders
)

states = ["All"] + sorted(
    df["PATIENT_STATE"]
    .dropna()
    .unique()
    .tolist()
)


selected_state = st.sidebar.selectbox(
    "📍 Patient State",
    states
)

readmissions = ["All"] + sorted(
    df["READMISSION"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


selected_readmission = st.sidebar.selectbox(
    "🔄 Readmission",
    readmissions
)


filtered_df = df.copy()



if selected_condition != "All":

    filtered_df = filtered_df[
        filtered_df["CONDITION"]
        == selected_condition
    ]


if selected_gender != "All":

    filtered_df = filtered_df[
        filtered_df["GENDER"]
        == selected_gender
    ]

if selected_state != "All":

    filtered_df = filtered_df[
        filtered_df["PATIENT_STATE"]
        == selected_state
    ]



if selected_readmission != "All":

    filtered_df = filtered_df[
        filtered_df["READMISSION"]
        .astype(str)
        == selected_readmission
    ]

st.divider()

st.subheader(
    "📊 Key Performance Indicators"
)


col1, col2, col3, col4, col5 = st.columns(5)


total_patients = len(
    filtered_df
)
avg_age = (
    filtered_df["AGE"].mean()
    if len(filtered_df) > 0
    else 0
)

avg_stay = (
    filtered_df["LENGTH_OF_STAY"].mean()
    if len(filtered_df) > 0
    else 0
)


# ------------------------------------------------------------
# AVERAGE SATISFACTION
# ------------------------------------------------------------

avg_satisfaction = (
    filtered_df["SATISFACTION"].mean()
    if len(filtered_df) > 0
    else 0
)


# ------------------------------------------------------------
# TOTAL COST
# ------------------------------------------------------------

total_cost = (
    filtered_df["TOTAL_COST"].sum()
    if len(filtered_df) > 0
    else 0
)


# ------------------------------------------------------------
# DISPLAY KPIs
# ------------------------------------------------------------

col1.metric(
    "👥 Total Patients",
    f"{total_patients:,}"
)


col2.metric(
    "🎂 Average Age",
    f"{avg_age:.1f}"
)


col3.metric(
    "🛏️ Avg Length of Stay",
    f"{avg_stay:.1f} days"
)


col4.metric(
    "⭐ Avg Satisfaction",
    f"{avg_satisfaction:.1f}"
)


col5.metric(
    "💰 Total Cost",
    f"${total_cost:,.0f}"
)

st.divider()

st.subheader(
    "🏥 Patient Analysis"
)


chart_col1, chart_col2 = st.columns(2)

with chart_col1:

    condition_data = (
        filtered_df
        .groupby("CONDITION")
        .size()
        .reset_index(
            name="PATIENT_COUNT"
        )
        .sort_values(
            "PATIENT_COUNT",
            ascending=False
        )
    )


    st.markdown(
        "**Patients by Condition**"
    )


    st.bar_chart(
        condition_data.set_index(
            "CONDITION"
        )
    )


with chart_col2:

    gender_data = (
        filtered_df
        .groupby("GENDER")
        .size()
        .reset_index(
            name="PATIENT_COUNT"
        )
    )


    st.markdown(
        "**Patients by Gender**"
    )


    st.bar_chart(
        gender_data.set_index(
            "GENDER"
        )
    )

st.subheader(
    "💰 Cost & Hospital Stay Analysis"
)


chart_col3, chart_col4 = st.columns(2)

with chart_col3:

    cost_data = (
        filtered_df
        .groupby("CONDITION")["TOTAL_COST"]
        .mean()
        .reset_index()
        .sort_values(
            "TOTAL_COST",
            ascending=False
        )
    )


    st.markdown(
        "**Average Cost by Condition**"
    )


    st.bar_chart(
        cost_data.set_index(
            "CONDITION"
        )
    )


with chart_col4:

    stay_data = (
        filtered_df
        .groupby("CONDITION")["LENGTH_OF_STAY"]
        .mean()
        .reset_index()
        .sort_values(
            "LENGTH_OF_STAY",
            ascending=False
        )
    )


    st.markdown(
        "**Average Length of Stay by Condition**"
    )


    st.bar_chart(
        stay_data.set_index(
            "CONDITION"
        )
    )


st.subheader(
    "📅 Admission Analysis"
)


year_data = (
    filtered_df
    .groupby("YEAR_OF_ADMISSION")
    .size()
    .reset_index(
        name="PATIENT_COUNT"
    )
    .sort_values(
        "YEAR_OF_ADMISSION"
    )
)


st.line_chart(
    year_data.set_index(
        "YEAR_OF_ADMISSION"
    )
)


st.subheader(
    "🔄 Readmission Analysis"
)


readmission_data = (
    filtered_df
    .groupby("READMISSION")
    .size()
    .reset_index(
        name="PATIENT_COUNT"
    )
)


st.bar_chart(
    readmission_data.set_index(
        "READMISSION"
    )
)


st.subheader(
    "🏆 Patient Outcomes"
)


outcome_data = (
    filtered_df
    .groupby("OUTCOME")
    .size()
    .reset_index(
        name="PATIENT_COUNT"
    )
    .sort_values(
        "PATIENT_COUNT",
        ascending=False
    )
)


st.bar_chart(
    outcome_data.set_index(
        "OUTCOME"
    )
)


st.subheader(
    "👤 Patient Records"
)


st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)


st.divider()

st.caption(
    "Hospital Patient Analytics Dashboard | "
    "Powered by Snowflake Streamlit"
)

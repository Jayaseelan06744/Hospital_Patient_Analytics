# 🏥 Hospital Patient Analytics

An interactive **Hospital Patient Analytics Dashboard** built using **Snowflake, Snowpark, SQL, Python, and Streamlit**.

This project analyzes hospital patient data stored in Snowflake and presents useful patient-level and analytical insights through an interactive Streamlit dashboard.

---

## 📌 Project Overview

Hospital data contains valuable information about patients, medical conditions, admissions, treatments, outcomes, and hospital stays.

The goal of this project is to use **Snowflake for data storage and processing** and **Streamlit for interactive visualization** to create a simple and user-friendly hospital analytics application.

The dashboard allows users to explore patient information and analyze important hospital-related data.

---

## 🎯 Project Objectives

- Store and manage hospital patient data using Snowflake.
- Perform data analysis using SQL.
- Connect Snowflake data with a Streamlit application.
- Provide an interactive dashboard for exploring patient information.
- Display patient-level details in an easy-to-understand format.
- Demonstrate the use of Snowpark with Streamlit.
- Build a practical data analytics project using cloud technologies.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Snowflake** | Cloud data platform and data storage |
| **SQL** | Data creation, querying and analysis |
| **Python** | Application and data processing |
| **Snowpark** | Connecting Python applications with Snowflake |
| **Streamlit** | Interactive dashboard development |
| **Pandas** | Data manipulation and analysis |
| **Git & GitHub** | Version control and project management |

---

## 🏗️ Project Architecture

```text
                 ┌──────────────────────┐
                 │    Hospital Data     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │      Snowflake       │
                 │                      │
                 │  Database & Tables   │
                 │       SQL            │
                 └──────────┬───────────┘
                            │
                            │ Snowpark
                            ▼
                 ┌──────────────────────┐
                 │      Python          │
                 │     Application      │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │      Streamlit       │
                 │     Dashboard        │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Interactive Patient  │
                 │      Analytics       │
                 └──────────────────────┘

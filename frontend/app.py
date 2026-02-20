import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Employee Management System",
    page_icon="🧑🏻‍💼",
    layout="wide"
)


st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(to right, #eef2f3, #8e9eab);
}

/* Fix input labels (text above inputs) */
label {
    color: black !important;
    font-weight: 600 !important;
}

/* Fix subheaders */
h3 {
    color: #1e3c72 !important;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #1e3c72, #2a5298);
    color: white;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Title */
h1 {
    text-align: center;
    color: #1e3c72;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(to right, #4facfe, #00f2fe);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    background: linear-gradient(to right, #43e97b, #38f9d7);
    color: black;
}

/* Input fields */
.stTextInput>div>div>input,
.stNumberInput input {
    border-radius: 8px;
    border: 1px solid #2a5298;
}

/* Card container */
.card {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
            
</style>
""", unsafe_allow_html=True)


st.markdown("""
<h1 style='color:black;'>🧑🏻‍💼 Employee Management System</h1>
""", unsafe_allow_html=True)

st.markdown("---")


menu = st.sidebar.selectbox(
    "📌 Navigation Menu",
    ["📋 View Employees", "➕ Add Employee", "✅ Update Employee", "🗑️ Delete Employee"]
)


if menu == "📋 View Employees":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📋 Employee Records")

    response = requests.get(f"{API_URL}/employee")

    if response.ok:
        data = response.json()

        if len(data) == 0:
            st.warning("⚠ No Employees in the database")
        else:
           df = pd.DataFrame(data)
           df = df[["id", "name", "department", "experience", "salary"]]
           st.dataframe(df.sort_values("id"), width="stretch")

    else:
        st.error("Failed to fetch employees")

    st.markdown('</div>', unsafe_allow_html=True)



elif menu == "➕ Add Employee":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("➕ Add New Employee")

    name = st.text_input("Employee Name")
    department = st.text_input("Department")
    salary = st.number_input("Salary", min_value=0.0)
    experience = st.number_input("Experience", min_value=0)

    if st.button("Add Employee"):

        if name.strip() == "":
            st.markdown("""
                    <div style="
                        background-color:#fff8e1;
                        padding:15px;
                        border-left:6px solid #ffb300;
                        border-radius:10px;
                        color:#856404;
                        font-weight:600;
                    ">
                    ⚠ Employee Name cannot be empty
                    </div>
                    """, unsafe_allow_html=True)

        elif department.strip() == "":
            st.markdown("""
                    <div style="
                        background-color:#fff8e1;
                        padding:15px;
                        border-left:6px solid #ffb300;
                        border-radius:10px;
                        color:#856404;
                        font-weight:600;
                    ">
                    ⚠ Department Name cannot be empty
                    </div>
                    """, unsafe_allow_html=True)
        elif salary <= 0:
            st.markdown("""
                    <div style="
                        background-color:#fff8e1;
                        padding:15px;
                        border-left:6px solid #ffb300;
                        border-radius:10px;
                        color:#856404;
                        font-weight:600;">
                    ⚠ Salary must be greater than 0
                    </div>
                    """, unsafe_allow_html=True)
        else:
            payload = {
                "name": name,
                "department": department,
                "salary": salary,
                "experience": experience
            }

            response = requests.post(f"{API_URL}/employee", json=payload)

            if response.ok:
                st.markdown("""
                        <div style="
                            background-color:#e9f9ee;
                            padding:15px;
                            border-left:6px solid #28a745;
                            border-radius:10px;
                            color:#155724;
                            font-weight:600;
                        ">
                        ✅ Employee Added Successfully!
                        </div>
                        """, unsafe_allow_html=True)

                st.balloons()
            else:
                st.error(response.text)

    st.markdown('</div>', unsafe_allow_html=True)



elif menu == "✅ Update Employee":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("✅ Update Existing Employee")

    employee_id = st.number_input("Enter Employee ID", min_value=1)
    name = st.text_input("New Employee Name")
    department = st.text_input("New Department")
    salary = st.number_input("New Salary", min_value=0.0)
    experience = st.number_input("New Experience", min_value=0)

    if st.button("Update Employee"):

        payload = {
            "name": name,
            "department": department,
            "salary": salary,
            "experience": experience
        }

        response = requests.put(
            f"{API_URL}/employee/{employee_id}",
            json=payload
        )

        if response.ok:
            st.markdown("""
                        <div style="
                            background-color:#e9f9ee;
                            padding:15px;
                            border-left:6px solid #28a745;
                            border-radius:10px;
                            color:#155724;
                            font-weight:600;
                        ">
                         ✅ Employee Updated Successfully!
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.error("Employee Not Found!")

    st.markdown('</div>', unsafe_allow_html=True)




elif menu == "🗑️ Delete Employee":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🗑️ Delete Employee")

    employee_id = st.number_input("Enter Employee ID to Delete", min_value=1)

    if st.button("Delete Employee"):

        response = requests.delete(f"{API_URL}/employee/{employee_id}")

        if response.ok:
            st.markdown("""
                        <div style="
                            background-color:#e9f9ee;
                            padding:15px;
                            border-left:6px solid #28a745;
                            border-radius:10px;
                            color:#155724;
                            font-weight:600;
                        ">
                         ❌ Employee Deleted Successfully!
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.error("Employee Not Found!")

    st.markdown('</div>', unsafe_allow_html=True)


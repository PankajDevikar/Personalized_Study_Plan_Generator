import streamlit as st
import pulp as p

# Define the Linear Programming problem for optimization
def create_optimized_study_plan(total_time, min_physics, min_chemistry, min_biology, min_math, max_physics, max_chemistry, max_biology, max_math):
    # Define the Linear Programming problem: Maximizing the study effectiveness
    Lp_prob = p.LpProblem('Study_Plan_Optimization_Single_Student', p.LpMaximize)

    # Create decision variables for study hours in Physics, Chemistry, Biology, and Math
    Physics = p.LpVariable('Physics', lowBound=0)   # Minimum 0 hours for Physics
    Chemistry = p.LpVariable('Chemistry', lowBound=0)   # Minimum 0 hours for Chemistry
    Biology = p.LpVariable('Biology', lowBound=0)   # Minimum 0 hours for Biology
    Math = p.LpVariable('Math', lowBound=0)   # Minimum 0 hours for Math

    # Objective function: Maximize study effectiveness (using arbitrary weights for each subject)
    Lp_prob += 2 * Physics + 3 * Chemistry + 2 * Biology + 4 * Math, "Maximize Study Effectiveness"

    # Constraints:
    # Total available study hours
    Lp_prob += Physics + Chemistry + Biology + Math <= total_time, "Total Available Time"

    # Minimum hours required per subject
    Lp_prob += Physics >= min_physics, "Minimum Physics Study Hours"
    Lp_prob += Chemistry >= min_chemistry, "Minimum Chemistry Study Hours"
    Lp_prob += Biology >= min_biology, "Minimum Biology Study Hours"
    Lp_prob += Math >= min_math, "Minimum Math Study Hours"

    # Optional: Maximum study hours per subject
    Lp_prob += Physics <= max_physics, "Maximum Physics Study Hours"
    Lp_prob += Chemistry <= max_chemistry, "Maximum Chemistry Study Hours"
    Lp_prob += Biology <= max_biology, "Maximum Biology Study Hours"
    Lp_prob += Math <= max_math, "Maximum Math Study Hours"

    # Solve the problem
    status = Lp_prob.solve()

    # Check if the solution is optimal
    if p.LpStatus[status] == 'Optimal':
        return {
            "status": "Optimal",
            "Physics": p.value(Physics),
            "Chemistry": p.value(Chemistry),
            "Biology": p.value(Biology),
            "Math": p.value(Math),
            "Total_Study_Effectiveness": p.value(Lp_prob.objective)
        }
    else:
        return {
            "status": "Infeasible",
            "message": "No optimal solution found, please adjust the constraints."
        }

# Streamlit App interface
st.title("Personalized Study Plan Optimizer")

# Input fields for total available time and minimum/maximum study hours for each subject
total_time = st.number_input("Total Available Time (hours/day):", min_value=0, value=10)
min_physics = st.number_input("Minimum Physics Study Hours:", min_value=0, value=1)
min_chemistry = st.number_input("Minimum Chemistry Study Hours:", min_value=0, value=2)
min_biology = st.number_input("Minimum Biology Study Hours:", min_value=0, value=1)
min_math = st.number_input("Minimum Math Study Hours:", min_value=0, value=2)
max_physics = st.number_input("Maximum Physics Study Hours:", min_value=0, value=4)
max_chemistry = st.number_input("Maximum Chemistry Study Hours:", min_value=0, value=4)
max_biology = st.number_input("Maximum Biology Study Hours:", min_value=0, value=3)
max_math = st.number_input("Maximum Math Study Hours:", min_value=0, value=4)

# Button to calculate the optimized study plan
if st.button("Get Optimized Study Plan"):
    result = create_optimized_study_plan(
        total_time, min_physics, min_chemistry, min_biology, min_math, 
        max_physics, max_chemistry, max_biology, max_math
    )

    # Display the result
    if result["status"] == "Optimal":
        st.subheader("Optimized Study Plan (in hours per subject):")
        st.write(f"Physics: {result['Physics']} hours")
        st.write(f"Chemistry: {result['Chemistry']} hours")
        st.write(f"Biology: {result['Biology']} hours")
        st.write(f"Math: {result['Math']} hours")
        st.write(f"Total Study Effectiveness: {result['Total_Study_Effectiveness']}")
    else:
        st.error(result["message"])


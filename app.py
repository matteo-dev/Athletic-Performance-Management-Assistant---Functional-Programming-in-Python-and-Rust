# Main Streamlit application file for squat progression analysis and fatigue management.

# Import necessary modules
import streamlit as st # Framework to create interactive web apps in Python
from datetime import date
from models import WorkoutRecord
from analytics import extract_squat_progression, calculate_total_volume, calculate_1rm_epley, calculate_acwr, extract_bodyweight_trend, calculate_ewma, project_target_date

# Use st.cache_data to cache mock data to avoid recalculating on each interaction
@st.cache_data

# Function to load simulated workout data
def load_mock_data() -> tuple[WorkoutRecord, ...]:
    return (
        WorkoutRecord(date(2026, 9, 1), "Squat", 80.0, 5, 7, 67.0),
        WorkoutRecord(date(2026, 9, 8), "Squat", 85.0, 5, 8, 68.5),
        WorkoutRecord(date(2026, 9, 15), "Squat", 90.0, 3, 10, 69.5),
        WorkoutRecord(date(2026, 9, 22), "Squat", 90.0, 2, 10, 69.8),
        WorkoutRecord(date(2026, 9, 29), "Squat", 92.5, 3, 9, 70.1),
    )

# Main function of the Streamlit application
def main():
    st.title("🏋️‍♂️ Sports-Data & Biomechanics Assistant")
    st.write("100% Functional Architecture - Zero Mutability")
    
    history = load_mock_data()
    
    # Create Streamlit tabs
    tab1, tab2, tab3 = st.tabs(["📊 Progression & 1RM", "🧠 Fatigue & ACWR", "⚖️ Bodyweight (67 -> 70kg)"])
    
    with tab1:
        st.header("Strength Analysis (Squat)")
        total_volume = calculate_total_volume(history)
        squat_1rm_progression = extract_squat_progression(history)
        dates = tuple(map(lambda r: r.date, filter(lambda r: r.exercise == "Squat", history)))
        
        st.metric(label="Total Historical Volume", value=f"{total_volume} kg")
        st.line_chart({"Date": dates, "Estimated 1RM (kg)": squat_1rm_progression}, x="Date", y="Estimated 1RM (kg)")
        
    with tab2:
        st.header("Fatigue & Nervous System Management")
        st.write("The optimal ACWR ratio is between 0.8 and 1.3. Beyond this, the risk of injury and central nervous system fatigue increases (hitting 'the wall').")
        
        # Calculate ACWR on the date of the last workout
        last_workout_date = history[-1].date
        acwr_score = calculate_acwr(history, last_workout_date)
        
        st.metric(label="Current ACWR", value=f"{round(acwr_score, 2)}")
        if acwr_score > 1.3:
            st.warning("⚠️ Warning: Acute overload detected. The mental block on the squat is likely due to central nervous system fatigue. Reduce the volume.")
        else:
            st.success("✅ Optimal training load.")
            
    with tab3:
        st.header("⚖️ Bulking Trajectory (EWMA)")
        st.write("Goal: Reach 70kg in a controlled manner, filtered by exponential smoothing (EWMA, α=0.3).")
        
        # 1. Pure extraction of raw data
        dates_bw, weights = extract_bodyweight_trend(history)
        
        # 2. Mathematical model application (Data pipeline)
        ewma_weights = calculate_ewma(weights, alpha=0.3)
        target_date = project_target_date(dates_bw, ewma_weights, target_kg=70.0)
        
        # 3. Display KPIs
        current_weight = weights[-1]
        st.metric(
            label="Current Weight vs Goal (70kg)", 
            value=f"{current_weight} kg", 
            delta=f"{round(70.0 - current_weight, 1)} kg remaining",
            delta_color="off"
        )
        
        if target_date:
            st.success(f"📈 Mathematical projection: 70kg goal estimated for **{target_date.strftime('%d %B %Y')}**.")
        
        # 4. Comparative chart (Raw vs Smoothed)
        import pandas as pd
        # We temporarily use pandas just for the formatting expected by Streamlit (st.line_chart)
        chart_data = pd.DataFrame({
            "Date": dates_bw,
            "Raw Weight (kg)": weights,
            "EWMA Trend (kg)": ewma_weights
        }).set_index("Date")
        
        st.line_chart(chart_data)

if __name__ == "__main__":
    main()

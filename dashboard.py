import streamlit as st
import pandas as pd
import plotly.express as px

def show_dashboard(df: pd.DataFrame):
    st.subheader("📊 Data Dashboard")

    if df.empty:
        st.info("No data available for dashboard.")
        return

    # Identify column types
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    date_cols = df.select_dtypes(include=["datetime", "datetimetz"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    all_cols = df.columns.tolist()

    st.markdown("### Column Types")
    st.write(f"**Numeric:** {numeric_cols}")
    st.write(f"**Date/Datetime:** {date_cols}")
    st.write(f"**Categorical:** {categorical_cols}")

    # X-axis can be any column
    x_axis = st.selectbox("Select X-axis column", all_cols)

    # Y-axis can be numeric or None
    y_axis_options = ["None"] + numeric_cols
    y_axis = st.selectbox("Select Y-axis column (or None)", y_axis_options)

    chart_type = st.radio("Chart Type", ["Bar", "Line", "Scatter", "Histogram", "Boxplot"])

    try:
        # Auto-handle date columns
        if x_axis in date_cols:
            df[x_axis] = pd.to_datetime(df[x_axis], errors="coerce")

        # Prepare kwargs for Plotly
        plot_kwargs = {"x": x_axis}
        if y_axis != "None":
            plot_kwargs["y"] = y_axis
        if categorical_cols:
            plot_kwargs["color"] = categorical_cols[0]

        # Generate chart
        if chart_type == "Bar":
            fig = px.bar(df, **plot_kwargs)
        elif chart_type == "Line":
            fig = px.line(df, **plot_kwargs)
        elif chart_type == "Scatter":
            fig = px.scatter(df, **plot_kwargs)
        elif chart_type == "Histogram":
            fig = px.histogram(df, x=x_axis)
        elif chart_type == "Boxplot":
            fig = px.box(df, **plot_kwargs)

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error generating chart: {e}")

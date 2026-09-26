import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Smart Agriculture Analytics",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "clean_agriculture_data.csv"
)

CROP_MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "crop_recommendation_model.pkl"
)

CROP_ENCODER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "crop_label_encoder.pkl"
)

YIELD_MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "yield_prediction_model.pkl"
)

SQL_EXCEL_PATH = os.path.join(
    BASE_DIR,
    "excel",
    "agriculture_sql_analysis.xlsx"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .sub-title {
        font-size: 18px;
        margin-bottom: 25px;
    }

    .kpi-card {
        padding: 20px;
        border-radius: 15px;
        background: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.20);
        text-align: center;
        min-height: 130px;
    }

    .kpi-title {
        font-size: 15px;
        font-weight: 600;
    }

    .kpi-value {
        font-size: 28px;
        font-weight: 800;
        margin-top: 10px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 750;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .prediction-box {
        padding: 30px;
        border-radius: 18px;
        text-align: center;
        background: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.20);
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


df = load_data()

# =========================================================
# LOAD ML MODELS
# =========================================================

@st.cache_resource
def load_crop_model():

    model = joblib.load(CROP_MODEL_PATH)
    encoder = joblib.load(CROP_ENCODER_PATH)

    return model, encoder


@st.cache_resource
def load_yield_model():

    model = joblib.load(YIELD_MODEL_PATH)

    return model


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("# 🌾 Smart Agriculture")

st.sidebar.markdown(
    "### Analytics & ML Platform"
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📊 Data Analysis",
        "🌱 Crop Recommendation",
        "📈 Yield Prediction",
        "🧮 SQL Analytics",
        "📋 Dataset"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
    **Smart Agriculture Analytics**

    Python  
    SQL  
    Machine Learning  
    Streamlit
    """
)

# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">🌾 Smart Agriculture Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Data Analytics & Machine Learning Dashboard</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # FILTERS
    # -----------------------------------------------------

    st.sidebar.markdown("### 🔎 Dashboard Filters")

    selected_state = st.sidebar.selectbox(
        "State",
        ["All"] + sorted(df["State"].dropna().unique().tolist())
    )

    selected_crop = st.sidebar.selectbox(
        "Crop",
        ["All"] + sorted(df["Crop"].dropna().unique().tolist())
    )

    selected_season = st.sidebar.selectbox(
        "Season",
        ["All"] + sorted(df["Season"].dropna().unique().tolist())
    )

    filtered_df = df.copy()

    if selected_state != "All":

        filtered_df = filtered_df[
            filtered_df["State"] == selected_state
        ]

    if selected_crop != "All":

        filtered_df = filtered_df[
            filtered_df["Crop"] == selected_crop
        ]

    if selected_season != "All":

        filtered_df = filtered_df[
            filtered_df["Season"] == selected_season
        ]

    # -----------------------------------------------------
    # KPI
    # -----------------------------------------------------

    total_records = len(filtered_df)

    total_production = filtered_df[
        "Production_Tons"
    ].sum()

    average_yield = filtered_df[
        "Yield_Tons_Per_Hectare"
    ].mean()

    total_revenue = filtered_df[
        "Revenue"
    ].sum()

    st.markdown(
        '<div class="section-title">📊 Agriculture Overview</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">📋 Total Records</div>
                <div class="kpi-value">{total_records:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">🌾 Production</div>
                <div class="kpi-value">
                    {total_production:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">📈 Avg Yield</div>
                <div class="kpi-value">
                    {average_yield:.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">💰 Revenue</div>
                <div class="kpi-value">
                    ₹{total_revenue:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # CHARTS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">🌾 Production Analysis</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        crop_production = (
            filtered_df
            .groupby("Crop")["Production_Tons"]
            .sum()
            .sort_values(ascending=False)
        )

        st.markdown("#### Production by Crop")

        st.bar_chart(crop_production)

    with col2:

        crop_yield = (
            filtered_df
            .groupby("Crop")["Yield_Tons_Per_Hectare"]
            .mean()
            .sort_values(ascending=False)
        )

        st.markdown("#### Average Yield by Crop")

        st.bar_chart(crop_yield)

    col3, col4 = st.columns(2)

    with col3:

        state_production = (
            filtered_df
            .groupby("State")["Production_Tons"]
            .sum()
            .sort_values(ascending=False)
        )

        st.markdown("#### Production by State")

        st.bar_chart(state_production)

    with col4:

        season_production = (
            filtered_df
            .groupby("Season")["Production_Tons"]
            .sum()
            .sort_values(ascending=False)
        )

        st.markdown("#### Production by Season")

        st.bar_chart(season_production)

    # -----------------------------------------------------
    # IRRIGATION
    # -----------------------------------------------------

    irrigation_yield = (
        filtered_df
        .groupby("Irrigation")["Yield_Tons_Per_Hectare"]
        .mean()
        .sort_values(ascending=False)
    )

    st.markdown("#### 💧 Yield by Irrigation")

    st.bar_chart(irrigation_yield)

# =========================================================
# DATA ANALYSIS
# =========================================================

elif page == "📊 Data Analysis":

    st.title("📊 Data Analysis")

    st.write(
        "Explore agricultural performance across crops, states, seasons and irrigation."
    )

    # -----------------------------------------------------
    # CROP
    # -----------------------------------------------------

    st.subheader("🌾 Crop Performance")

    crop_summary = (
        df.groupby("Crop")
        .agg(
            Production=("Production_Tons", "sum"),
            Average_Yield=("Yield_Tons_Per_Hectare", "mean"),
            Revenue=("Revenue", "sum")
        )
        .sort_values(
            "Production",
            ascending=False
        )
    )

    st.dataframe(
        crop_summary,
        use_container_width=True
    )

    # -----------------------------------------------------
    # STATE
    # -----------------------------------------------------

    st.subheader("🗺️ State Performance")

    state_summary = (
        df.groupby("State")
        .agg(
            Production=("Production_Tons", "sum"),
            Average_Yield=("Yield_Tons_Per_Hectare", "mean"),
            Revenue=("Revenue", "sum")
        )
        .sort_values(
            "Production",
            ascending=False
        )
    )

    st.dataframe(
        state_summary,
        use_container_width=True
    )

    # -----------------------------------------------------
    # SEASON
    # -----------------------------------------------------

    st.subheader("🌦️ Seasonal Analysis")

    season_summary = (
        df.groupby("Season")
        .agg(
            Production=("Production_Tons", "sum"),
            Average_Yield=("Yield_Tons_Per_Hectare", "mean"),
            Revenue=("Revenue", "sum")
        )
    )

    st.dataframe(
        season_summary,
        use_container_width=True
    )

    # -----------------------------------------------------
    # CORRELATION
    # -----------------------------------------------------

    st.subheader("🔗 Numeric Correlation")

    numeric_df = df.select_dtypes(
        include=np.number
    )

    correlation = numeric_df.corr()

    st.dataframe(
        correlation.round(2),
        use_container_width=True
    )

# =========================================================
# CROP RECOMMENDATION
# =========================================================

elif page == "🌱 Crop Recommendation":

    st.title("🌱 Crop Recommendation")

    st.write(
        "Enter soil and environmental conditions to predict a suitable crop."
    )

    try:

        crop_model, crop_encoder = load_crop_model()

        col1, col2 = st.columns(2)

        with col1:

            soil_n = st.number_input(
                "Soil Nitrogen (N)",
                min_value=0.0,
                value=50.0
            )

            soil_p = st.number_input(
                "Soil Phosphorus (P)",
                min_value=0.0,
                value=40.0
            )

            soil_k = st.number_input(
                "Soil Potassium (K)",
                min_value=0.0,
                value=40.0
            )

            soil_ph = st.number_input(
                "Soil pH",
                min_value=0.0,
                max_value=14.0,
                value=6.5
            )

        with col2:

            temperature = st.number_input(
                "Temperature (°C)",
                value=25.0
            )

            humidity = st.number_input(
                "Humidity (%)",
                min_value=0.0,
                max_value=100.0,
                value=60.0
            )

            rainfall = st.number_input(
                "Rainfall (mm)",
                min_value=0.0,
                value=100.0
            )

        if st.button(
            "🌱 Recommend Crop",
            use_container_width=True
        ):

            input_data = pd.DataFrame(
                [[
                    soil_n,
                    soil_p,
                    soil_k,
                    temperature,
                    humidity,
                    rainfall,
                    soil_ph
                ]],
                columns=[
                    "Soil_N",
                    "Soil_P",
                    "Soil_K",
                    "Temperature_C",
                    "Humidity_Percent",
                    "Rainfall_mm",
                    "Soil_pH"
                ]
            )

            prediction = crop_model.predict(
                input_data
            )

            crop_name = crop_encoder.inverse_transform(
                prediction
            )[0]

            st.markdown(
                f"""
                <div class="prediction-box">

                <h2>🌱 Recommended Crop</h2>

                <h1>{crop_name}</h1>

                <p>
                Based on the entered soil and environmental conditions.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

    except Exception as e:

        st.error(
            f"Crop recommendation model error: {e}"
        )

# =========================================================
# YIELD PREDICTION
# =========================================================

elif page == "📈 Yield Prediction":

    st.title("📈 Yield Prediction")

    st.write(
        "Enter agricultural conditions to predict crop yield."
    )

    try:

        yield_model = load_yield_model()

        col1, col2, col3 = st.columns(3)

        with col1:

            area = st.number_input(
                "Area (Hectares)",
                min_value=0.1,
                value=10.0
            )

            rainfall = st.number_input(
                "Rainfall (mm)",
                min_value=0.0,
                value=100.0
            )

            temperature = st.number_input(
                "Temperature (°C)",
                value=25.0
            )

            humidity = st.number_input(
                "Humidity (%)",
                min_value=0.0,
                max_value=100.0,
                value=60.0
            )

        with col2:

            soil_n = st.number_input(
                "Soil N",
                min_value=0.0,
                value=50.0
            )

            soil_p = st.number_input(
                "Soil P",
                min_value=0.0,
                value=40.0
            )

            soil_k = st.number_input(
                "Soil K",
                min_value=0.0,
                value=40.0
            )

            soil_ph = st.number_input(
                "Soil pH",
                min_value=0.0,
                max_value=14.0,
                value=6.5
            )

        with col3:

            fertilizer = st.number_input(
                "Fertilizer (kg)",
                min_value=0.0,
                value=100.0
            )

            pesticide = st.number_input(
                "Pesticide (Liters)",
                min_value=0.0,
                value=10.0
            )

            market_price = st.number_input(
                "Market Price / Ton",
                min_value=0.0,
                value=20000.0
            )

            crop = st.selectbox(
                "Crop",
                sorted(df["Crop"].dropna().unique())
            )

            season = st.selectbox(
                "Season",
                sorted(df["Season"].dropna().unique())
            )

            irrigation = st.selectbox(
                "Irrigation",
                sorted(df["Irrigation"].dropna().unique())
            )

        if st.button(
            "📈 Predict Yield",
            use_container_width=True
        ):

            input_data = pd.DataFrame(
                [[
                    area,
                    rainfall,
                    temperature,
                    humidity,
                    soil_n,
                    soil_p,
                    soil_k,
                    soil_ph,
                    fertilizer,
                    pesticide,
                    market_price,
                    crop,
                    season,
                    irrigation
                ]],
                columns=[
                    "Area_Hectares",
                    "Rainfall_mm",
                    "Temperature_C",
                    "Humidity_Percent",
                    "Soil_N",
                    "Soil_P",
                    "Soil_K",
                    "Soil_pH",
                    "Fertilizer_kg",
                    "Pesticide_Liters",
                    "Market_Price_Per_Ton",
                    "Crop",
                    "Season",
                    "Irrigation"
                ]
            )

            prediction = yield_model.predict(
                input_data
            )[0]

            st.markdown(
                f"""
                <div class="prediction-box">

                <h2>📈 Predicted Yield</h2>

                <h1>{prediction:.2f} Tons / Hectare</h1>

                </div>
                """,
                unsafe_allow_html=True
            )

    except Exception as e:

        st.error(
            f"Yield prediction model error: {e}"
        )

# =========================================================
# SQL ANALYTICS
# =========================================================

elif page == "🧮 SQL Analytics":

    st.title("🧮 SQL Analytics")

    st.write(
        "Results generated from the SQLite agricultural database."
    )

    if os.path.exists(SQL_EXCEL_PATH):

        try:

            excel_file = pd.ExcelFile(
                SQL_EXCEL_PATH
            )

            selected_sheet = st.selectbox(
                "Select SQL Analysis",
                excel_file.sheet_names
            )

            sql_data = pd.read_excel(
                SQL_EXCEL_PATH,
                sheet_name=selected_sheet
            )

            st.dataframe(
                sql_data,
                use_container_width=True
            )

            csv_data = sql_data.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "⬇️ Download Analysis",
                csv_data,
                file_name=f"{selected_sheet}.csv",
                mime="text/csv"
            )

        except Exception as e:

            st.error(
                f"Unable to read SQL analysis: {e}"
            )

    else:

        st.warning(
            "SQL analysis Excel file was not found."
        )

# =========================================================
# DATASET
# =========================================================

elif page == "📋 Dataset":

    st.title("📋 Agriculture Dataset")

    st.write(
        f"Total records: **{len(df):,}**"
    )

    search = st.text_input(
        "🔎 Search dataset"
    )

    display_df = df.copy()

    if search:

        mask = display_df.astype(
            str
        ).apply(
            lambda row: row.str.contains(
                search,
                case=False,
                na=False
            ).any(),
            axis=1
        )

        display_df = display_df[mask]

    st.dataframe(
        display_df,
        use_container_width=True,
        height=550
    )

    csv = display_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Download Dataset",
        csv,
        file_name="agriculture_filtered_data.csv",
        mime="text/csv"
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <center>

    **🌾 Smart Agriculture Analytics**

    MSc Computer Science Project  
    Python • SQL • Machine Learning • Streamlit

    </center>
    """,
    unsafe_allow_html=True
)
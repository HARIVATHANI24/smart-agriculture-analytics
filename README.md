# 🌾 Smart Agriculture Analytics

## Project Overview

Smart Agriculture Analytics is a Python-based data analytics and machine learning project for analyzing agricultural production, crop performance, environmental conditions, irrigation, revenue, and crop yield.

The project combines Python, SQL, Machine Learning, and Streamlit to provide an interactive agriculture analytics platform.

## Objectives

- Analyze agricultural production data
- Analyze crop performance
- Analyze state-wise production
- Analyze seasonal production
- Analyze irrigation and yield
- Perform SQL-based analysis
- Recommend suitable crops using Machine Learning
- Predict agricultural yield using Machine Learning
- Build an interactive Streamlit dashboard

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SQLite
- SQL
- Scikit-learn
- Random Forest
- Joblib
- Streamlit
- Visual Studio Code

## Main Features

### 1. Data Analysis

The project analyzes:

- Crop production
- Average crop yield
- State-wise production
- Seasonal production
- Rainfall and yield
- Temperature and yield
- Irrigation and yield
- Fertilizer and yield
- Revenue by crop

### 2. SQL Analysis

SQLite is used to store and analyze agricultural data.

SQL analysis includes:

- Crop analysis
- State analysis
- Season analysis
- Irrigation analysis
- Agriculture KPIs
- Production analysis
- Yield analysis
- Revenue analysis

### 3. Crop Recommendation

A Random Forest Classification model is used to recommend a suitable crop based on:

- Soil Nitrogen
- Soil Phosphorus
- Soil Potassium
- Temperature
- Humidity
- Rainfall
- Soil pH

### 4. Yield Prediction

A Random Forest Regression model is used to predict crop yield.

The model uses:

- Area
- Rainfall
- Temperature
- Humidity
- Soil nutrients
- Soil pH
- Fertilizer
- Pesticide
- Market price
- Crop
- Season
- Irrigation

### 5. Streamlit Dashboard

The dashboard contains:

- Dashboard
- Data Analysis
- Crop Recommendation
- Yield Prediction
- SQL Analytics
- Dataset

## Dataset

The project uses approximately 5,000 agricultural records.

The dataset contains agricultural, environmental, soil, production, irrigation, and revenue information.

## Machine Learning Models

### Crop Recommendation Model

Algorithm:

Random Forest Classifier

Output:

Recommended Crop

### Yield Prediction Model

Algorithm:

Random Forest Regressor

Output:

Predicted Yield in Tons per Hectare

## Project Workflow

```text
Agricultural Dataset
        ↓
Data Cleaning
        ↓
Exploratory Data Analysis
        ↓
SQLite Database
        ↓
SQL Analysis
        ↓
Machine Learning
        ↓
Crop Recommendation
        ↓
Yield Prediction
        ↓
Streamlit Dashboard
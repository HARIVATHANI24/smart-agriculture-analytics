-- ============================================================
-- SMART AGRICULTURE ANALYTICS
-- SQL ANALYTICS MODULE
-- ============================================================


-- ============================================================
-- QUERY 1
-- TOTAL NUMBER OF FARM RECORDS
-- ============================================================

SELECT
    COUNT(*) AS Total_Records
FROM agriculture_data;


-- ============================================================
-- QUERY 2
-- TOTAL AGRICULTURAL PRODUCTION
-- ============================================================

SELECT
    ROUND(SUM(Production_Tons), 2)
        AS Total_Production_Tons
FROM agriculture_data;


-- ============================================================
-- QUERY 3
-- TOTAL AGRICULTURAL REVENUE
-- ============================================================

SELECT
    ROUND(SUM(Revenue), 2)
        AS Total_Revenue
FROM agriculture_data;


-- ============================================================
-- QUERY 4
-- PRODUCTION BY CROP
-- ============================================================

SELECT
    Crop,

    ROUND(
        SUM(Production_Tons),
        2
    ) AS Total_Production_Tons

FROM agriculture_data

GROUP BY Crop

ORDER BY
    Total_Production_Tons DESC;


-- ============================================================
-- QUERY 5
-- AVERAGE YIELD BY CROP
-- ============================================================

SELECT
    Crop,

    ROUND(
        AVG(Yield_Tons_Per_Hectare),
        2
    ) AS Average_Yield

FROM agriculture_data

GROUP BY Crop

ORDER BY
    Average_Yield DESC;


-- ============================================================
-- QUERY 6
-- REVENUE BY CROP
-- ============================================================

SELECT
    Crop,

    ROUND(
        SUM(Revenue),
        2
    ) AS Total_Revenue

FROM agriculture_data

GROUP BY Crop

ORDER BY
    Total_Revenue DESC;


-- ============================================================
-- QUERY 7
-- PRODUCTION BY STATE
-- ============================================================

SELECT
    State,

    ROUND(
        SUM(Production_Tons),
        2
    ) AS Total_Production

FROM agriculture_data

GROUP BY State

ORDER BY
    Total_Production DESC;


-- ============================================================
-- QUERY 8
-- AVERAGE YIELD BY STATE
-- ============================================================

SELECT
    State,

    ROUND(
        AVG(Yield_Tons_Per_Hectare),
        2
    ) AS Average_Yield

FROM agriculture_data

GROUP BY State

ORDER BY
    Average_Yield DESC;


-- ============================================================
-- QUERY 9
-- PRODUCTION BY SEASON
-- ============================================================

SELECT
    Season,

    ROUND(
        SUM(Production_Tons),
        2
    ) AS Total_Production

FROM agriculture_data

GROUP BY Season

ORDER BY
    Total_Production DESC;


-- ============================================================
-- QUERY 10
-- REVENUE BY SEASON
-- ============================================================

SELECT
    Season,

    ROUND(
        SUM(Revenue),
        2
    ) AS Total_Revenue

FROM agriculture_data

GROUP BY Season

ORDER BY
    Total_Revenue DESC;


-- ============================================================
-- QUERY 11
-- IRRIGATION PERFORMANCE
-- ============================================================

SELECT
    Irrigation,

    ROUND(
        AVG(Yield_Tons_Per_Hectare),
        2
    ) AS Average_Yield,

    ROUND(
        SUM(Production_Tons),
        2
    ) AS Total_Production

FROM agriculture_data

GROUP BY Irrigation

ORDER BY
    Average_Yield DESC;


-- ============================================================
-- QUERY 12
-- YEAR-WISE PRODUCTION
-- ============================================================

SELECT
    Year,

    ROUND(
        SUM(Production_Tons),
        2
    ) AS Total_Production

FROM agriculture_data

GROUP BY Year

ORDER BY Year;


-- ============================================================
-- QUERY 13
-- YEAR-WISE REVENUE
-- ============================================================

SELECT
    Year,

    ROUND(
        SUM(Revenue),
        2
    ) AS Total_Revenue

FROM agriculture_data

GROUP BY Year

ORDER BY Year;


-- ============================================================
-- QUERY 14
-- TOP 10 FARM RECORDS BY REVENUE
-- ============================================================

SELECT

    Record_ID,

    State,

    District,

    Crop,

    Area_Hectares,

    Production_Tons,

    Market_Price_Per_Ton,

    Revenue

FROM agriculture_data

ORDER BY
    Revenue DESC

LIMIT 10;


-- ============================================================
-- QUERY 15
-- TOP 10 HIGHEST YIELD RECORDS
-- ============================================================

SELECT

    Record_ID,

    State,

    District,

    Crop,

    Yield_Tons_Per_Hectare,

    Irrigation

FROM agriculture_data

ORDER BY
    Yield_Tons_Per_Hectare DESC

LIMIT 10;


-- ============================================================
-- QUERY 16
-- RAINFALL AND YIELD ANALYSIS
-- ============================================================

SELECT

    Crop,

    ROUND(
        AVG(Rainfall_mm),
        2
    ) AS Average_Rainfall,

    ROUND(
        AVG(Yield_Tons_Per_Hectare),
        2
    ) AS Average_Yield

FROM agriculture_data

GROUP BY Crop

ORDER BY
    Average_Yield DESC;


-- ============================================================
-- QUERY 17
-- SOIL ANALYSIS
-- ============================================================

SELECT

    Crop,

    ROUND(
        AVG(Soil_N),
        2
    ) AS Average_Nitrogen,

    ROUND(
        AVG(Soil_P),
        2
    ) AS Average_Phosphorus,

    ROUND(
        AVG(Soil_K),
        2
    ) AS Average_Potassium,

    ROUND(
        AVG(Soil_pH),
        2
    ) AS Average_pH

FROM agriculture_data

GROUP BY Crop;


-- ============================================================
-- QUERY 18
-- FERTILIZER VS YIELD
-- ============================================================

SELECT

    Crop,

    ROUND(
        AVG(Fertilizer_kg),
        2
    ) AS Average_Fertilizer,

    ROUND(
        AVG(Yield_Tons_Per_Hectare),
        2
    ) AS Average_Yield

FROM agriculture_data

GROUP BY Crop

ORDER BY
    Average_Yield DESC;


-- ============================================================
-- QUERY 19
-- PESTICIDE VS PRODUCTION
-- ============================================================

SELECT

    Crop,

    ROUND(
        AVG(Pesticide_Liters),
        2
    ) AS Average_Pesticide,

    ROUND(
        AVG(Production_Tons),
        2
    ) AS Average_Production

FROM agriculture_data

GROUP BY Crop;


-- ============================================================
-- QUERY 20
-- BEST CROP IN EACH STATE
-- ============================================================

WITH CropPerformance AS (

    SELECT

        State,

        Crop,

        AVG(
            Yield_Tons_Per_Hectare
        ) AS Average_Yield,

        SUM(
            Production_Tons
        ) AS Total_Production,

        SUM(
            Revenue
        ) AS Total_Revenue

    FROM agriculture_data

    GROUP BY
        State,
        Crop
)

SELECT

    State,

    Crop,

    ROUND(
        Average_Yield,
        2
    ) AS Average_Yield,

    ROUND(
        Total_Production,
        2
    ) AS Total_Production,

    ROUND(
        Total_Revenue,
        2
    ) AS Total_Revenue

FROM CropPerformance

ORDER BY
    State,
    Average_Yield DESC;


-- ============================================================
-- QUERY 21
-- HIGH PRODUCTIVITY FARMS
-- ============================================================

SELECT

    Record_ID,

    State,

    District,

    Crop,

    Area_Hectares,

    Yield_Tons_Per_Hectare,

    Production_Tons

FROM agriculture_data

WHERE
    Yield_Tons_Per_Hectare >
    (
        SELECT
            AVG(
                Yield_Tons_Per_Hectare
            )
        FROM agriculture_data
    )

ORDER BY
    Yield_Tons_Per_Hectare DESC;


-- ============================================================
-- QUERY 22
-- HIGH REVENUE FARMS
-- ============================================================

SELECT

    Record_ID,

    State,

    District,

    Crop,

    Revenue

FROM agriculture_data

WHERE Revenue >

    (
        SELECT
            AVG(Revenue)
        FROM agriculture_data
    )

ORDER BY
    Revenue DESC;


-- ============================================================
-- QUERY 23
-- PRODUCTION BY STATE AND CROP
-- ============================================================

SELECT

    State,

    Crop,

    ROUND(
        SUM(Production_Tons),
        2
    ) AS Total_Production

FROM agriculture_data

GROUP BY
    State,
    Crop

ORDER BY
    State,
    Total_Production DESC;


-- ============================================================
-- QUERY 24
-- CROP MARKET PRICE ANALYSIS
-- ============================================================

SELECT

    Crop,

    ROUND(
        AVG(Market_Price_Per_Ton),
        2
    ) AS Average_Market_Price,

    ROUND(
        MIN(Market_Price_Per_Ton),
        2
    ) AS Minimum_Price,

    ROUND(
        MAX(Market_Price_Per_Ton),
        2
    ) AS Maximum_Price

FROM agriculture_data

GROUP BY Crop

ORDER BY
    Average_Market_Price DESC;


-- ============================================================
-- QUERY 25
-- OVERALL AGRICULTURE KPI
-- ============================================================

SELECT

    COUNT(*) AS Total_Farms,

    COUNT(
        DISTINCT State
    ) AS Total_States,

    COUNT(
        DISTINCT Crop
    ) AS Total_Crops,

    ROUND(
        SUM(Area_Hectares),
        2
    ) AS Total_Area_Hectares,

    ROUND(
        SUM(Production_Tons),
        2
    ) AS Total_Production_Tons,

    ROUND(
        SUM(Revenue),
        2
    ) AS Total_Revenue,

    ROUND(
        AVG(Yield_Tons_Per_Hectare),
        2
    ) AS Average_Yield

FROM agriculture_data;
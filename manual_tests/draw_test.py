import pandas as pd
import sdmxthon
from src.draw import ChartGenerator



bl = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"
kpi1 = f"{bl}/TEICP000/M.CP00.I15.EA20?endPeriod=2022&lastNObservations=1"
kpi2 = f"{bl}/TEILM010/M.SA.TOTAL.T.THS_PER.EA20?endPeriod=2022&lastNObservations=1"
kpi3 = f"{bl}/TEILM310/Q.NSA.JOBRATE.TOTAL.B-S.EA20?endPeriod=2022&lastNObservations=1"
pie = f"{bl}/TPS00010/A..EA20?endPeriod=2022&lastNObservations=1"
bar = f"{bl}/TEIIS550/M.PSQM.F_CC1.I2015_SCA.BE+FR+ES+DE"
line = f"{bl}/TEICP000/M.CP00.I15.EA20+EU27_2020+FR+DE+IT+ES"

message = sdmxthon.read_sdmx(pie)
resource = message.payload[list(message.payload)[0]]
df = resource.data
df["OBS_VALUE"]
df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce")

ChartGenerator().calculate_kpi(df, xAxisConcept="TIME_PERIOD", yAxisConcept="OBS_VALUE")
ChartGenerator().pie_chart(
    df, xAxisConcept="indic_de", yAxisConcept="OBS_VALUE", legendLoc="BOTTOM"
)
ChartGenerator().bar_chart(df, xAxisConcept="TIME_PERIOD", yAxisConcept="OBS_VALUE")
ChartGenerator().time_series_chart(
    df, xAxisConcept="TIME_PERIOD", yAxisConcept="OBS_VALUE", color="geo"
)

# Example usage with a Pandas DataFrame
# TIME SERIES CHART (Multiline)
data = {
    "date": pd.date_range(start="2020-01-01", periods=20, freq="Q"),
    "value": [
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
    ],
    "category": [
        "A",
        "A",
        "B",
        "B",
        "C",
        "C",
        "A",
        "A",
        "B",
        "B",
        "C",
        "C",
        "A",
        "A",
        "B",
        "B",
        "C",
        "C",
        "A",
        "A",
    ],
}
df = pd.DataFrame(data)
df.set_index("date", inplace=True)
chart = ChartGenerator()
chart.time_series_chart(
    df, xAxisConcept="category", yAxisConcept="value", group_by="category"
)  # Create a multiline time series chart grouped by 'category'

# PIE CHART
chart = ChartGenerator()
chart.pie_chart(df, xAxisConcept=None, yAxisConcept="value", group_by="category")

# BAR CHART
chart = ChartGenerator()
chart.bar_chart(
    df, xAxisConcept="category", yAxisConcept="value", group_by=None, aggregation="mean"
)

# KPI CHART
data = {
    "Sales": [100, 150, 200, 120, 180],
    "Profit": [10, 15, 20, 12, 18],
    "Category": ["A", "A", "B", "B", "C"],
}
df = pd.DataFrame(data)
chart = ChartGenerator()
chart.calculate_kpi(df, "Sales", "mean", "Category")
chart.calculate_kpi(df, "Sales", "min", None)

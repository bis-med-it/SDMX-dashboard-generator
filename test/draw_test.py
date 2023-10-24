import pandas as pd
import plotly.graph_objects as go
from src.draw import ChartGenerator


def test_chart_generator_initialization():
    """This is a simple test to make sure the ChartGenerator class works as expected."""
    chart_generator = ChartGenerator()
    assert chart_generator is not None


def test_time_series_chart():
    """Tests the creation of a time series chart."""

    # ARRANGE:
    date_rng = pd.date_range(start="2021-01-01", end="2021-01-10", freq="D")
    df = pd.DataFrame({"date": date_rng, "data": list(range(1, 11))})
    chart_generator = ChartGenerator()

    # ACT:
    chart = chart_generator.time_series_chart(
        df, xAxisConcept="date", yAxisConcept="data"
    )

    # ASSERT
    assert isinstance(chart, go.Figure)
    assert isinstance(chart.data[0], go.Scatter)
    assert len(chart.data) == 1
    assert len(chart.data[0].x) == 10
    assert len(chart.data[0].y) == 10
    assert chart.data[0].y[0] == 1


def test_time_series_chart_with_group_by():
    """Tests the creation of a time series chart with grouping criteria."""

    # ARRANGE:
    date_rng = pd.date_range(start="2021-01-01", end="2021-01-10", freq="D")
    df = pd.DataFrame(
        {"date": date_rng, "data": list(range(1, 11)), "group": ["A", "B"] * 5}
    )
    chart_generator = ChartGenerator()

    # ACT:
    chart = chart_generator.time_series_chart(
        df, xAxisConcept="date", yAxisConcept="data", group_by="group"
    )

    # ASSERT
    assert isinstance(chart, go.Figure)
    assert isinstance(chart.data[0], go.Scatter)
    assert isinstance(chart.data[1], go.Scatter)
    assert len(chart.data) == 2
    assert len(chart.data[0].x) == 5
    assert len(chart.data[0].y) == 5
    assert chart.data[0].y[0] == 1
    assert len(chart.data[1].x) == 5
    assert len(chart.data[1].y) == 5
    assert chart.data[1].y[0] == 2


def test_pie_chart():
    """Tests the creation of a pie chart."""

    # ARRANGE:
    countries = ["USA", "Canada", "Germany", "France", "UK"]
    df = pd.DataFrame(
        {"country": countries, "population_millions": [331, 38, 84, 67, 68]}
    )
    chart_generator = ChartGenerator()

    # ACT:
    chart = chart_generator.pie_chart(
        df, xAxisConcept="country", yAxisConcept="population_millions"
    )

    # ASSERT
    assert isinstance(chart, go.Figure)
    assert isinstance(chart.data[0], go.Pie)
    assert len(chart.data) == 1


def test_bar_chart():
    """Tests the creation of a bar chart."""

    # ARRANGE:
    countries = ["USA", "Canada", "Germany", "France", "UK"]
    df = pd.DataFrame(
        {"country": countries, "population_millions": [331, 38, 84, 67, 68]}
    )
    chart_generator = ChartGenerator()

    # ACT:
    chart = chart_generator.bar_chart(
        df, xAxisConcept="country", yAxisConcept="population_millions"
    )

    # ASSERT
    assert isinstance(chart, go.Figure)
    assert isinstance(chart.data[0], go.Bar)
    assert len(chart.data) == 1

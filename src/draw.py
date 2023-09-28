"""Module providing graphing utilities"""
import functools

import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# Define the decorator function with legend positioning
def chart_style_decorator(func):
    """A decorator for applying chart styling and legend positioning to Plotly figures.

    :param func: function: the original function that generates a Plotly figure.
    :returns: function: a wrapped function that modifies the figure's style
        and legend positioning.

    This decorator is used to enhance the appearance of Plotly figures generated by
    other functions. It allows you to specify the positioning of the legend and applies
    various style modifications to the figure.

    Example:
        @chart_style_decorator
        def generate_plot(data, legendLoc="BOTTOM"):
            # Create a Plotly figure based on the input data
            fig = create_figure(data)
            return fig

        # Apply the decorator to the generate_plot function
        styled_fig = generate_plot(data, legendLoc="BOTTOM")

    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the legendLoc from kwargs (default to "HIDE" if not provided)
        legendLoc = kwargs.get("legendLoc", "HIDE")

        # Remove the legendLoc from kwargs before calling the original function
        if "legendLoc" in kwargs:
            del kwargs["legendLoc"]

        # Call the original function to obtain the figure object
        fig = func(*args, **kwargs)

        # Apply the legend positioning based on legendLoc
        if legendLoc == "HIDE":
            fig.update_layout(showlegend=False)  # Hide the legend
        else:
            if legendLoc == "BOTTOM":
                # Position the legend at the bottom, centered horizontally,
                # with a horizontal orientation
                fig.update_layout(
                    legend=dict(x=0.5, y=-0.2, xanchor="center", orientation="h")
                )
            elif legendLoc == "TOP":
                # Position the legend at the top, centered horizontally,
                # with a horizontal orientation
                fig.update_layout(
                    legend=dict(x=0.5, y=1.1, xanchor="center", orientation="h")
                )
            elif legendLoc == "LEFT":
                # Position the legend at the left, centered vertically,
                # with a vertical orientation
                fig.update_layout(
                    legend=dict(x=-0.1, y=0.5, xanchor="left", orientation="v")
                )
            elif legendLoc == "RIGHT":
                # Position the legend at the right, centered vertically,
                # with a vertical orientation
                fig.update_layout(
                    legend=dict(x=1.1, y=0.5, xanchor="right", orientation="v")
                )
            else:
                # Default to centering the legend horizontally,
                # with a horizontal orientation
                fig.update_layout(
                    legend=dict(x=-0.1, y=0.5, xanchor="center", orientation="h")
                )

        # Update layout properties for the figure
        fig.update_layout(
            plot_bgcolor="rgba(0, 0, 0, 0)",  # Set plot background color transparent
            paper_bgcolor="rgba(0, 0, 0, 0)",  # Set paper background color transparent
            margin=dict(l=20, r=20, t=0, b=20),  # Adjust margin settings
        )

        # Customize grid appearance for the x and y axes
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor="White")
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor="White")

        # Modify the visibility and tick labels for y-axis
        fig.update_layout(yaxis_visible=True, yaxis_showticklabels=True)

        # Modify the visibility and tick labels for x-axis, and remove the title
        fig.update_layout(xaxis_visible=True, xaxis_showticklabels=True)
        fig.update_xaxes(title="")  # Remove x-axis title

        return fig

    return wrapper


class ChartGenerator:
    """Initialize a ChartGenerator instance with an empty Plotly figure.

    This constructor initializes a ChartGenerator instance with an empty Plotly figure,
    which can be used to create various types of charts.

    """

    def __init__(self):
        self.fig = go.Figure()
        # Initialise to None attributes obtained with other methods
        self.kpi = None

    # Apply the decorator to a function that generates a Plotly figure
    @chart_style_decorator
    def time_series_chart(
        self, df, xAxisConcept, yAxisConcept, color=None, legend=None, group_by=None
    ):
        """Create a time series chart.

        :param df: DataFrame: the input DataFrame containing time series data.
        :param xAxisConcept: str: the concept for the x-axis data.
        :param yAxisConcept: str: the concept for the y-axis data.
        :param group_by: str, optional: the column to group by for multiline charts.
        :returns: self: the ChartGenerator instance.

        """
        # Check if the group_by parameter is provided (not None).
        if group_by:
            # Group the DataFrame df by the specified column (group_by).
            grouped_data = df.groupby(group_by)

            # Iterate through each group formed by grouping.
            for group_name, group_df in grouped_data:
                # Add a trace (line) to the chart for this group.
                self.fig.add_trace(
                    go.Scatter(
                        x=group_df.index,  # X-axis values from the group's index.
                        y=group_df[
                            yAxisConcept
                        ],  # Y-axis values from the specified concept.
                        mode="lines+markers",  # Use lines with markers to show data.
                        name=group_name,  # Set the name (legend label) for this group.
                    )
                )
        else:
            # If no group_by parameter is provided,
            # create a single-line time series chart.
            # Use Plotly Express (px) to create the chart.
            self.fig = px.line(df, x=xAxisConcept, y=yAxisConcept, color=color)

        # Return the created chart (Plotly figure) to the caller.
        return self.fig

    # Apply the decorator to a function that generates a Plotly figure
    @chart_style_decorator
    def pie_chart(
        self,
        df,
        xAxisConcept,
        yAxisConcept,
        group_by=None,
        LabelsYN=None,
        aggregation=None,
    ):
        """Create a pie chart.

        :param df: pd.DataFrame: the input DataFrame containing pie chart data.
        :param xAxisConcept: str: the concept for the x-axis data.
        :param yAxisConcept: str: the concept for the y-axis data.
        :param group_by: str, optional: the column to group by for multiple pie charts.
        :returns: self: the ChartGenerator instance.

        """

        # Check if 'group_by' parameter is provided
        if group_by is not None:
            if aggregation is None:
                raise ValueError(
                    "You must specify an aggregation function for yAxisConcept."
                )
            if aggregation not in ["sum", "mean", "max", "min", "std"]:
                raise ValueError(
                    "Invalid aggregation option. Supported options:\
                        'sum', 'mean', 'max', 'min', 'std'."
                )
            # Group the data by the specified column(s)
            grouped_data = (
                df.groupby(group_by).agg({yAxisConcept: aggregation}).reset_index()
            )

            if LabelsYN == "Yes":
                # Create a pie chart
                self.fig = go.Figure(
                    data=[
                        go.Pie(
                            labels=grouped_data[group_by],
                            values=grouped_data[yAxisConcept],
                            textinfo="percent+label",
                            hole=0.7,
                        )
                    ]
                )

                # Define a custom hovertemplate
                custom_hovertemplate = "group_by: %{label}\
                    <br>yAxisConcept: %{value}<br>Percent computed: %{percent}"

                # Update the hovertemplate for each trace in the pie chart
                for trace in self.fig.data:
                    trace.hovertemplate = custom_hovertemplate

            else:
                # Create a pie chart
                self.fig = go.Figure(
                    data=[go.Pie(values=grouped_data[yAxisConcept], hole=0.7)]
                )
                # Remove hover labels (tooltip) completely
                self.fig.update_layout(hovermode=False)

        else:
            if LabelsYN == "Yes":
                # Create a pie chart using Plotly Express
                self.fig = px.pie(
                    df,
                    values=df[yAxisConcept],
                    names=df[xAxisConcept],
                    labels=df[xAxisConcept],
                    hole=0.7,
                )

                # Define what to display on the donut
                self.fig.update_traces(textposition="inside", textinfo="percent")

                # Define a custom hovertemplate
                custom_hovertemplate = "xAxisConcept: %{label}\
                    <br>yAxisConcept: %{value}<br>Percent computed: %{percent}"

                # Update the hovertemplate for each trace in the pie chart
                for trace in self.fig.data:
                    trace.hovertemplate = custom_hovertemplate

            else:
                # Create a pie chart using Plotly Express
                self.fig = px.pie(
                    df, values=df[yAxisConcept], names=df[xAxisConcept], hole=0.7
                )
                # Remove hover labels (tooltip) completely
                self.fig.update_layout(hovermode=False)

        # Return the created chart (Plotly figure) to the caller.
        return self.fig

    # Apply the decorator to a function that generates a Plotly figure
    @chart_style_decorator
    def bar_chart(
        self,
        df,
        xAxisConcept,
        yAxisConcept,
        color=None,
        group_by=None,
        aggregation=None,
    ):
        """Create a bar chart.

        :param df: pd.DataFrame: the input containing bar chart data.
        :param xAxisConcept: str: the concept for the x-axis data.
        :param yAxisConcept: str: the concept for the y-axis data.
        :param group_by: str, optional: the column to group by for grouped bar charts.
        :returns: self: the ChartGenerator instance.

        """
        # Check if the group_by parameter is provided (not None).
        if group_by:
            # Group the DataFrame df by the specified column (group_by).
            grouped_data = df.groupby(group_by)

            # Initialize empty lists to store x and y values for the chart.
            x_values = []
            y_values = []

            # Iterate through each group formed by grouping.
            for group_name, group_df in grouped_data:
                # Append the group_name (x-axis value) to the x_values list.
                x_values.append(group_name)

                try:
                    # Attempt to calculate the aggregation of the yAxisConcept data
                    # within this group.
                    # If yAxisConcept contains numeric values,
                    # perform the specified aggregation (e.g., 'sum', 'mean').
                    # If it's not numeric, set the value to NaN.
                    y_values.append(
                        group_df[yAxisConcept].agg([aggregation]).reset_index()
                        if isinstance(group_df[yAxisConcept], (int, float))
                        else np.nan
                    )

                except Exception as e:
                    # Handle exceptions if the aggregation option is invalid.
                    print(
                        e,
                        "\n",
                        "Invalid aggregation option.\
                            Supported options: 'sum', 'mean', 'max', 'min', 'std'",
                    )
                    # Return None to indicate an error condition.
                    return None

        else:
            # If no group_by parameter is provided,
            # create a bar chart using Plotly Express (px).
            # Sort the DataFrame by the time series column (xAxisConcept)
            df = df.sort_values(by=xAxisConcept)
            self.fig = px.bar(df, x=xAxisConcept, y=yAxisConcept, color=color)

        # Return the created chart (Plotly figure) to the caller.
        return self.fig

    def calculate_kpi(
        self,
        df,
        yAxisConcept,
        xAxisConcept,
        legendConcept,
        decimals=2,
        aggregation=None,
        group_by=None,
    ):
        """Calculate Key Performance Indicators (KPIs) based on the provided DataFrame.

        :param df: pd.DataFrame: the DataFrame containing the data.
        :param xAxisConcept: str: the concept for the x-axis data.
        :param yAxisConcept: str: the concept for the y-axis data.
        :param legendConcept: str: the column name representing the legend
        :param group_by: str, optional: the column to group data by.
        :param decimals: int, optional: the number of decimals for rounding Y-axis
                                        (Default value = 2)
        :param aggregation: str, optional: the aggregation to apply to Y-axis data.
        :returns: dict: a dictionary containing legend values as keys
        :raises ValueError: If any of the specified columns are not found,
                            if 'legendConcept' is None,
                            or if invalid aggregation options are provided.

        """
        try:
            # Check if 'decimals' is an integer, if not, set it to default value 2.
            if not isinstance(decimals, int):
                print("Decimals need to be an integer. Setting to default")
                decimals = 2

            # Check if 'yAxisConcept' is a column in the DataFrame 'df'.
            if yAxisConcept not in df.columns:
                raise ValueError(f"Column '{yAxisConcept}' not found in the DataFrame.")

            # Check if 'xAxisConcept' is a column in the DataFrame 'df'.
            if xAxisConcept not in df.columns:
                raise ValueError(f"Column '{xAxisConcept}' not found in the DataFrame.")

            # Check if 'legendConcept' is not None.
            if legendConcept is None:
                raise ValueError("Column '{legendConcept}' not specified.")

            # If an aggregation function is specified:
            if aggregation:
                # If 'group_by' is specified:
                if group_by:
                    # Group the DataFrame by 'group_by',
                    # apply aggregation to 'yAxisConcept', and reset the index.
                    tmp = (
                        df.groupby(group_by)[yAxisConcept]
                        .agg([aggregation])
                        .reset_index()
                    )
                    # Depending on the aggregation function,
                    # perform additional operations.
                    if aggregation in ["min", "max"]:
                        tmp = df.merge(tmp, on=group_by)
                        tmp = tmp[tmp[yAxisConcept] == tmp[aggregation]]
                    elif aggregation in ["mean", "sum", "std"]:
                        tmp[xAxisConcept] = df[xAxisConcept].unique().tolist()[0]
                        tmp[legendConcept] = df[legendConcept].unique().tolist()[0]
                        tmp[yAxisConcept] = tmp[aggregation]
                    else:
                        raise ValueError(
                            "Invalid aggregation option.\
                            Supported options: 'sum', 'mean', 'max', 'min', 'std'"
                        )
                else:
                    # Depending on the aggregation function,
                    # perform additional operations.
                    if aggregation in ["min", "max"]:
                        tmp = df.copy()
                        tmp[aggregation] = df[yAxisConcept].agg(aggregation)
                        tmp = tmp[tmp[yAxisConcept] == tmp[aggregation]]
                    elif aggregation in ["mean", "sum", "std"]:
                        tmp = df[yAxisConcept].agg(aggregation)
                        tmp[xAxisConcept] = df[xAxisConcept].unique().tolist()[0]
                        tmp[legendConcept] = df[legendConcept].unique().tolist()[0]
                        tmp[yAxisConcept] = tmp[aggregation]

                    else:
                        raise ValueError(
                            "Invalid aggregation option.\
                            Supported options: 'sum', 'mean', 'max', 'min', 'std'"
                        )
            else:
                # If no aggregation is specified:
                if group_by:
                    # If 'group_by' is specified without aggregation, raise an error.
                    raise ValueError("Column '{aggregation}' not specified.")
                # If neither 'aggregation' nor 'group_by' is specified,
                # create a copy of 'df' as 'tmp'.
                tmp = df.copy()

            # Create a format pattern for formatting 'yAxisConcept' values
            # with the specified number of decimals.
            user_format_pattern = f"{{0:.{decimals}f}}"
            # Apply the format pattern to 'yAxisConcept' values in 'tmp'.
            tmp[yAxisConcept] = tmp[yAxisConcept].apply(
                lambda x: user_format_pattern.format(x)
            )

            # Create a dictionary 'self.kpi' with legend values as keys
            # and corresponding data as values.
            self.kpi = {
                key: tmp[tmp[legendConcept] == key][[xAxisConcept, yAxisConcept]]
                .values.flatten()
                .tolist()
                for key in tmp[legendConcept].unique()
            }

            # Return the created 'self.kpi' dictionary.
            return self.kpi

        except Exception as e:
            # If any exception occurs during the execution,
            # print an error message and return a default empty dictionary.
            print(f"Error calculating KPIs: {str(e)}")
            # Return a default empty dictionary as a placeholder
            return {"": ["", ""]}

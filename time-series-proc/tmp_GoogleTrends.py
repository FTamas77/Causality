import os
from pathlib import Path

import pandas as pd
import matplotlib
from matplotlib import pyplot as plt

import causalimpact


import statsmodels.api as sm
from statsmodels.formula.api import ols
import statsmodels.formula.api as smf


def read_and_filter_datasets(intervention_file, control_file, selected_parameters):

    def read_and_filter(file, selected_parameters):
        data = pd.read_csv(file)

        print(f"Columns in {file}:")
        print(data.columns.tolist())

        # Strip any extra whitespace from column names
        data.columns = data.columns.str.strip()

        # Ensure selected_parameters are in the columns
        missing_cols = [col for col in selected_parameters if col not in data.columns]
        if missing_cols:
            raise KeyError(f"Missing columns in {file}: {missing_cols}")

        # Convert 'Month' column to datetime
        if "Month" in data.columns:
            data["Month"] = pd.to_datetime(data["Month"], format="%Y-%m")
        else:
            raise KeyError("The 'Month' column is missing from the data.")

        # Filter data based on selected parameters
        filtered_data = data[selected_parameters]
        print(f"Filtered data from {file}:")
        print(filtered_data.head())

        return filtered_data

    intervention_data = read_and_filter(intervention_file, selected_parameters)

    control_data = read_and_filter(control_file, selected_parameters)

    # Debugging
    print("Intervention Data:")
    print(intervention_data)

    print("Control Data:")
    print(control_data)

    return intervention_data, control_data


def plot_data(intervention_data, control_data, intervention_start_date):

    # Ensure that 'Month' is the index for both DataFrames
    intervention_data = intervention_data.set_index("Month")
    control_data = control_data.set_index("Month")

    # Create the plot
    plt.figure(figsize=(12, 6))

    # Plot the intervention data
    plt.plot(
        intervention_data.index,
        intervention_data["Number"],
        color="blue",
        label="Intervention",
    )

    # Plot the control data
    plt.plot(
        control_data.index,
        control_data["Number"],
        linestyle="dotted",
        color="green",
        label="Control",
    )

    # Add a vertical line to indicate the intervention start date
    plt.axvline(
        x=pd.to_datetime(intervention_start_date),
        color="red",
        linestyle=":",
        alpha=0.5,
        linewidth=2,
        label="Intervention Start Date",
    )

    # Set titles and labels
    plt.title("Intervention vs. Control Group Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend(loc="upper right", edgecolor="red", shadow=True, title="Group")

    # Show the plot
    plt.show()


def prepare_data(intervention_data, control_data, index_column="Month"):

    # Ensure 'Month' is set as the index for both DataFrames
    if intervention_data.index.name != index_column:
        if index_column in intervention_data.columns:
            intervention_data.set_index(index_column, inplace=True)
        else:
            raise KeyError(f"{index_column} is not in intervention_data columns")

    if control_data.index.name != index_column:
        if index_column in control_data.columns:
            control_data.set_index(index_column, inplace=True)
        else:
            raise KeyError(f"{index_column} is not in control_data columns")

    # Ensure that the index is in datetime format
    if not pd.api.types.is_datetime64_any_dtype(intervention_data.index):
        intervention_data.index = pd.to_datetime(intervention_data.index)

    if not pd.api.types.is_datetime64_any_dtype(control_data.index):
        control_data.index = pd.to_datetime(control_data.index)

    # Combine the intervention and control data into a single DataFrame
    data = pd.DataFrame(
        {"y": intervention_data["Number"], "x1": control_data["Number"]}
    )

    print(data.head())

    return data


def plot_prepared_data(prepared_data):
    if prepared_data.empty:
        print("The DataFrame is empty. No data to plot.")
        return

    plt.figure(figsize=(10, 6))
    for column in prepared_data.columns:
        plt.plot(prepared_data.index, prepared_data[column], label=column)

    plt.title("Prepared Data Over Time")
    plt.xlabel("Time")
    plt.ylabel("Values")
    plt.legend()
    plt.show()


def perform_did_analysis(intervention_data, control_data, intervention_start_date):

    # Combine intervention and control DataFrames
    combined_df = pd.concat(
        [intervention_data, control_data], keys=["intervention", "control"]
    )

    combined_df.reset_index(level=1, inplace=True)

    # Print the first few rows to inspect the DataFrame
    print("Combined DataFrame Preview:")
    print(combined_df.head())

    print("Columns in Combined DataFrame:")
    print(combined_df.columns)

    # Check if conversion to datetime was successful
    print("Data Types After Conversion:")
    print(combined_df.dtypes)

    # Add 'post' column
    combined_df["post"] = combined_df["Month"] >= pd.to_datetime(
        intervention_start_date
    )

    # Add 'intervention' column to indicate intervention group
    combined_df["intervention"] = (
        combined_df.index.get_level_values(0) == "intervention"
    )

    # Fit the DiD model
    formula = "Number ~ post * intervention"
    did_model = smf.ols(formula, data=combined_df).fit()

    # Print the summary of the model
    print(did_model.summary())

    return combined_df, did_model


def plot_did_results(combined_df, intervention_start_date):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Use 'intervention' and 'post' columns for grouping
    for key, grp in combined_df.groupby(["intervention", "post"]):
        label = f"Intervention: {key[0]}, Post: {key[1]}"
        ax.plot(grp["Month"], grp["Number"], label=label)

    # Add a vertical line for the intervention start date
    plt.axvline(
        x=pd.to_datetime(intervention_start_date),
        color="red",
        linestyle="--",
        label="Intervention",
    )

    plt.title("Difference-in-Differences Analysis")
    plt.xlabel("Date")
    plt.ylabel("End Trip Number")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    selected_parameters = ["Month", "Number"]

    root_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent

    intervention_file = os.path.join(
        root_dir, "datasets", "googleTrends", "ds2_ce_g.csv"
    )

    control_file = os.path.join(root_dir, "datasets", "googleTrends", "ds1_ce_usa.csv")

    intervention_data, control_data = read_and_filter_datasets(
        intervention_file, control_file, selected_parameters
    )

    # Define the intervention start date
    intervention_start_date = "2015-06-01"

    # Plot the data
    plot_data(intervention_data, control_data, intervention_start_date)

    # Prepare data for causal impact analysis
    prepared_data = prepare_data(
        intervention_data=intervention_data,
        control_data=control_data,
        index_column="Month",
    )

    plot_prepared_data(prepared_data)

    pre_period = ("2004-04-01", "2015-06-01")
    post_period = ("2015-07-01", "2024-07-01")

    impact = causalimpact.fit_causalimpact(
        data=prepared_data, pre_period=pre_period, post_period=post_period
    )

    chart = causalimpact.plot(impact)
    script_dir = os.path.dirname(__file__)
    full_file_path = os.path.join(script_dir, "causal_impact_plot_for_trends.html")
    chart.save(full_file_path)
    plt.show()

    # Further logs
    print(causalimpact.summary(impact, output_format="summary"))
    print(causalimpact.summary(impact, output_format="report"))

    # DiD Analysis
    combined_df, did_model = perform_did_analysis(
        intervention_data, control_data, intervention_start_date
    )

    plot_did_results(combined_df, intervention_start_date)

    print("\nend of script")

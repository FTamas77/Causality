import os
from pathlib import Path

import pandas as pd
import matplotlib
from matplotlib import pyplot as plt

import causalimpact


import statsmodels.api as sm
from statsmodels.formula.api import ols
import statsmodels.formula.api as smf

import tmp_bubi_days


def read_and_filter_dataset(selected_parameters, input_data_file):
    # selected_parameters: for causal impact it should be only one parameter
    # station_name: if we want to filter on stations
    # ts_0: for resampling

    # reading the dataset
    bubi = pd.read_csv(input_data_file)
    print(bubi)

    return bubi


def filter_groups(
    bubi,
    selected_parameters,
    ts_param,
    station_prefixes_intervention,
    station_prefixes_control,
):
    # bubi_intervention -> filter on station_name + add selected parameters + add ts_param
    # bubi_control -> filter on station_name + add selected parameters + add ts_param

    def filter_by_stations(station_prefixes):
        return bubi.loc[
            bubi.station_name.apply(
                lambda name: any(name.startswith(prefix) for prefix in station_prefixes)
            ),
            selected_parameters + [ts_param],
        ]

    bubi_intervention = filter_by_stations(station_prefixes_intervention)
    print(bubi_intervention)

    bubi_control = filter_by_stations(station_prefixes_control)
    print(bubi_control)

    return bubi_intervention, bubi_control


def resample_data(bubi_intervention, bubi_control):
    def resample(df):
        df["ts_0"] = pd.to_datetime(df["ts_0"])
        return df.resample("D", on="ts_0").sum()

    bubi_intervention_resampled = resample(bubi_intervention)
    print(bubi_intervention_resampled)

    bubi_control_resampled = resample(bubi_control)
    print(bubi_control_resampled)

    return bubi_intervention_resampled, bubi_control_resampled


def filter_by_date(bubi_intervention, bubi_control, start_date, end_date):
    def filter_df(df):
        query_string = f"ts_0 >= '{start_date}' and ts_0 < '{end_date}'"
        filtered_df = df.query(query_string)
        print(filtered_df)
        return filtered_df

    bubi_intervention_filtered = filter_df(bubi_intervention)
    print(bubi_intervention_filtered)

    bubi_control_filtered = filter_df(bubi_control)
    print(bubi_control_filtered)

    return bubi_intervention_filtered, bubi_control_filtered


def plot_data(
    intervention_data,
    control_data,
    intervention_start_date,
    start_date_filter,
    end_date_filter,
):
    # Filter the data based on the provided start and end date filters
    intervention_data = intervention_data[
        (intervention_data.index >= start_date_filter)
        & (intervention_data.index <= end_date_filter)
    ]
    control_data = control_data[
        (control_data.index >= start_date_filter)
        & (control_data.index <= end_date_filter)
    ]

    ax = intervention_data.plot(color="blue", label="Intervention")
    control_data.plot(ax=ax, linestyle="dotted", color="green", label="Control")

    plt.axvline(
        x=pd.to_datetime(intervention_start_date),
        color="red",
        linestyle=":",
        alpha=0.5,
        linewidth=2,
        label="Intervention Start Date",
    )

    plt.title("Intervention vs. Control Group Over Time")
    plt.xlabel("Date")
    plt.ylabel("End Trip Number")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend(loc="upper right", edgecolor="red", shadow=True, title="Group")

    plt.show()


def prepare_data(bubi_intervention, bubi_control, index_column, interest_column):
    if bubi_intervention.index.name != index_column:
        if index_column in bubi_intervention.columns:
            bubi_intervention.set_index(index_column, inplace=True)
        else:
            raise KeyError(f"{index_column} is not in bubi_intervention columns")

    if bubi_control.index.name != index_column:
        if index_column in bubi_control.columns:
            bubi_control.set_index(index_column, inplace=True)
        else:
            raise KeyError(f"{index_column} is not in bubi_control columns")

    data = pd.DataFrame(
        {"y": bubi_intervention[interest_column], "x1": bubi_control[interest_column]}
    )

    return data


def plot_prepared_data(prepared_data, start_date_filter, end_date_filter):
    if prepared_data.empty:
        print("The DataFrame is empty. No data to plot.")
        return

    # Filter the DataFrame for the specified date range
    prepared_data = prepared_data[
        (prepared_data.index >= start_date_filter)
        & (prepared_data.index <= end_date_filter)
    ]

    plt.figure(figsize=(10, 6))
    for column in prepared_data.columns:
        plt.plot(prepared_data.index, prepared_data[column], label=column)

    plt.title("Prepared Data Over Time")
    plt.xlabel("Time")
    plt.ylabel("Values")
    plt.legend()
    plt.show()


def manual_plot(
    impact, intervention_start_date, file_name="manual_causal_impact_plot.png"
):
    plt.figure(figsize=(10, 6))
    plt.plot(impact.series.index, impact.series["observed"], label="Observed")
    plt.plot(impact.series.index, impact.series["posterior_mean"], label="Predicted")
    plt.fill_between(
        impact.series.index,
        impact.series["posterior_lower"],
        impact.series["posterior_upper"],
        color="gray",
        alpha=0.2,
    )
    plt.axvline(
        x=pd.to_datetime(intervention_start_date),
        color="red",
        linestyle="--",
        label="Intervention",
    )
    plt.xlabel("Date")
    plt.ylabel("End Trip Number")
    plt.title("Causal Impact Analysis")
    plt.legend()
    plt.savefig(file_name)
    plt.show()


def manual_plot(impact, intervention_start_date):
    plt.figure(figsize=(10, 6))
    plt.plot(impact.series.index, impact.series["observed"], label="Observed")
    plt.plot(impact.series.index, impact.series["posterior_mean"], label="Predicted")
    plt.fill_between(
        impact.series.index,
        impact.series["posterior_lower"],
        impact.series["posterior_upper"],
        color="gray",
        alpha=0.2,
    )
    plt.axvline(
        x=pd.to_datetime(intervention_start_date),
        color="red",
        linestyle="--",
        label="Intervention",
    )
    plt.xlabel("Date")
    plt.ylabel("End Trip Number")
    plt.title("Causal Impact Analysis")
    plt.legend()
    plt.show()


def perform_did_analysis(bubi_intervention, bubi_control, intervention_start_date):
    # Combine intervention and control DataFrames
    combined_df = pd.concat(
        [bubi_intervention, bubi_control], keys=["intervention", "control"]
    )

    # Reset the index to make 'ts_0' a column
    combined_df.reset_index(level=1, inplace=True)

    # Print the first few rows to inspect the DataFrame
    print("Combined DataFrame Preview:")
    print(combined_df.head())

    # Print the columns to check if 'ts_0' is present
    print("Columns in Combined DataFrame:")
    print(combined_df.columns)

    # Convert 'ts_0' to datetime if it's not already
    combined_df["ts_0"] = pd.to_datetime(combined_df["ts_0"])

    # Check if conversion to datetime was successful
    print("Data Types After Conversion:")
    print(combined_df.dtypes)

    # Add 'post' column
    combined_df["post"] = combined_df["ts_0"] >= pd.to_datetime(intervention_start_date)

    # Add 'intervention' column to indicate intervention group
    combined_df["intervention"] = (
        combined_df.index.get_level_values(0) == "intervention"
    )

    # Fit the DiD model
    formula = "end_trip_no ~ post * intervention"
    did_model = smf.ols(formula, data=combined_df).fit()

    # Print the summary of the model
    print(did_model.summary())

    return combined_df, did_model


def plot_did_results(combined_df, intervention_start_date):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Use 'intervention' and 'post' columns for grouping
    for key, grp in combined_df.groupby(["intervention", "post"]):
        label = f"Intervention: {key[0]}, Post: {key[1]}"
        ax.plot(grp["ts_0"], grp["end_trip_no"], label=label)

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

    # Parameters:
    # "end_trip_no",
    # "temperature",
    # "max_wind_speed",
    # "start_trip_no",
    # "precipitation",

    # Sources:
    # bubi-weather_export_2212-2312.csv
    # LARGE_bubi-weather_export_2206-2406.csv

    ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
    INPUT_DATA_FILE = os.path.join(
        ROOT_DIR, "datasets", "bubi", "LARGE_bubi-weather_export_2206-2406.csv"
    )

    selected_parameters = ["end_trip_no"]
    bubi = read_and_filter_dataset(selected_parameters, INPUT_DATA_FILE)

    index_column = "ts_0"
    station_intervention = ["0507", "0103"]
    station_control = ["0515", "1101"]
    bubi_intervention, bubi_control = filter_groups(
        bubi,
        selected_parameters,
        index_column,
        station_intervention,
        station_control,
    )

    bubi_intervention, bubi_control = resample_data(bubi_intervention, bubi_control)

    start_date_filter = "2023-05-01"
    end_date_filter = "2023-08-01"
    bubi_intervention_filtered, bubi_control_filtered = filter_by_date(
        bubi_intervention, bubi_control, start_date_filter, end_date_filter
    )

    # Plot data
    plot_date = "2023-06-15"
    plot_data(
        bubi_intervention, bubi_control, plot_date, start_date_filter, end_date_filter
    )

    # Prepare data for causal impact analysis
    interest_column = "end_trip_no"
    prepared_data = prepare_data(
        bubi_intervention, bubi_control, index_column, interest_column
    )
    print(prepared_data.head())

    # plot_prepared_data(prepared_data, start_date_filter, end_date_filter)

    pre_period = ("2023-05-01", "2023-06-15")
    post_period = ("2023-06-16", "2023-09-01")

    impact = causalimpact.fit_causalimpact(
        data=prepared_data, pre_period=pre_period, post_period=post_period
    )

    print(" ---------------- Causal Impact Analysis ---------------- ")

    # FIXME: https://github.com/google/tfp-causalimpact/issues/36
    chart = causalimpact.plot(impact)
    script_dir = os.path.dirname(__file__)
    full_file_path = os.path.join(script_dir, "causal_impact_plot.html")
    chart.save(full_file_path)
    plt.show()

    # OR DO THIS:
    # fig = causalimpact.plot(
    #    impact, backend="matplotlib", chart_width=1000, chart_height=200
    # )
    # fig.save("causal_impact_plot.png")
    # plt.show()

    # Further logs
    print(causalimpact.summary(impact, output_format="summary"))
    print(causalimpact.summary(impact, output_format="report"))

    # Manual Plot using the function
    # manual_plot(impact, intervention_start_date="2023-06-16")

    print(" ---------------- DiD Analysis ---------------- ")

    # DiD Analysis
    combined_df, did_model = perform_did_analysis(
        bubi_intervention_filtered, bubi_control_filtered, plot_date
    )
    plot_did_results(combined_df, plot_date)

    print("end")

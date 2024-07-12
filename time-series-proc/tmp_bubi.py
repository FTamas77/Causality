import os
from pathlib import Path

import pandas as pd
import matplotlib
from matplotlib import pyplot as plt

import causalimpact


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
    station_prefix_intervention,
    station_prefix_control,
):
    # bubi_intervention -> filter on station_name + add selected parameters + add ts_param
    # bubi_control -> filter on station_name + add selected parameters + add ts_param

    def filter_by_station(station_prefix):
        return bubi.loc[
            bubi.station_name.str.startswith(station_prefix),
            selected_parameters + [ts_param],
        ]

    bubi_intervention = filter_by_station(station_prefix_intervention)
    print(bubi_intervention)

    bubi_control = filter_by_station(station_prefix_control)
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


def plot_data(intervention_data, control_data, intervention_start_date):
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


if __name__ == "__main__":

    # Possible parameters:
    # "end_trip_no",
    # "temperature",
    # "max_wind_speed",
    # "start_trip_no",
    # "precipitation",

    ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
    INPUT_DATA_FILE = os.path.join(
        ROOT_DIR, "datasets", "bubi", "bubi-weather_export_2212-2312.csv"
    )

    selected_parameters = ["end_trip_no"]
    bubi = read_and_filter_dataset(selected_parameters, INPUT_DATA_FILE)

    index_column = "ts_0"
    station_intervention = "0507"
    station_control = "0508"
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
    plot_data(bubi_intervention, bubi_control, plot_date)

    # Prepare data for causal impact analysis
    interest_column = "end_trip_no"
    prepared_data = prepare_data(
        bubi_intervention, bubi_control, index_column, interest_column
    )
    print(prepared_data.head())

    plot_prepared_data(prepared_data)

    pre_period = ("2023-05-01", "2023-06-15")
    post_period = ("2023-06-16", "2023-09-01")

    impact = causalimpact.fit_causalimpact(
        data=prepared_data, pre_period=pre_period, post_period=post_period
    )

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

    print("end")

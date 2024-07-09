import os
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
INPUT_DATA_FILE = os.path.join(
    ROOT_DIR, "datasets", "bubi", "bubi-weather_export_2212-2312.csv"
)


def read_and_filter_dataset(selected_parameters, input_data_file=INPUT_DATA_FILE):
    # selected_parameters: for causal impact it should be only one parameter
    # station_name: if we want to filter on stations
    # ts_0: for resampling

    # reading the dataset
    bubi = pd.read_csv(INPUT_DATA_FILE)
    print(bubi)

    return bubi


def filter_groups(bubi, selected_parameters):
    # bubi_intervention -> filter on station_name
    # bubi_control -> filter on station_name
    # keep all selected parameters
    # keep ts_0 for resampling (start of the interval)

    def filter_by_station(station_prefix):
        return bubi.loc[
            bubi.station_name.str.startswith(station_prefix),
            selected_parameters + ["ts_0"],
        ]

    bubi_intervention = filter_by_station("0507")
    print(bubi_intervention)

    bubi_control = filter_by_station("0508")
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

    # from this point we don't need ts_0 and station_name
    return bubi_intervention_resampled, bubi_control_resampled


def filter_by_date(bubi_intervention, bubi_control):
    def filter_df(df):
        filtered_df = df.query("ts_0 >= '2023-05-01' and ts_0 < '2023-08-01'")
        print(filtered_df)
        return filtered_df

    bubi_intervention_filtered = filter_df(bubi_intervention)
    print(bubi_intervention_filtered)

    bubi_control_filtered = filter_df(bubi_control)
    print(bubi_control_filtered)

    return bubi_intervention_filtered, bubi_control_filtered


def plot_data(intervention_data, control_data):
    ax = intervention_data.plot(color="blue", label="Intervention")
    control_data.plot(ax=ax, linestyle="dotted", color="green", label="Control")

    plt.axvline(
        x=pd.to_datetime("2023-06-15"),
        color="red",
        linestyle=":",
        alpha=0.5,
        linewidth=2,
        label="Key Date",
    )

    plt.title("Intervention vs. Control Group Over Time")
    plt.xlabel("Date")
    plt.ylabel("End Trip Number")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend(loc="upper right", edgecolor="red", shadow=True, title="Group")

    plt.show()


if __name__ == "__main__":

    selected_parameters_all = [
        "end_trip_no",
        "temperature",
        "max_wind_speed",
        "start_trip_no",
        "precipitation",
    ]

    selected_parameters__only_end_trip = ["end_trip_no"]

    bubi = read_and_filter_dataset(selected_parameters__only_end_trip, INPUT_DATA_FILE)

    bubi_intervention, bubi_control = filter_groups(
        bubi, selected_parameters__only_end_trip
    )

    bubi_intervention, bubi_control = resample_data(bubi_intervention, bubi_control)

    bubi_intervention, bubi_control = filter_by_date(bubi_intervention, bubi_control)

    plot_data(bubi_intervention, bubi_control)

    print("end")

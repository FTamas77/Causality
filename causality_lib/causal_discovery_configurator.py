import os
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt


class config:
    pass


class config_bubi(config):
    __ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
    __INPUT_DATA_FILE = os.path.join(
        __ROOT_DIR, "dataset", "bubi-weather_export_2212-2312.csv"
    )

    #        "temperature",
    #       "max_wind_speed",

    # start_trip_no
    selected_parameters = ["end_trip_no"]

    def prepare_dataset(self):
        # , nrows=3000
        bubi = pd.read_csv(self.__INPUT_DATA_FILE)
        print(bubi)

        # Filter on stations
        bubi = bubi[self.selected_parameters + ["station_name", "ts_0"]]

        bubi_intervention = bubi[bubi.station_name.str.startswith("0507")]
        print(bubi_intervention)

        bubi_control = bubi[bubi.station_name.str.startswith("0508")]
        print(bubi_control)

        bubi_intervention = bubi_intervention[self.selected_parameters + ["ts_0"]]
        print(bubi_intervention)

        bubi_control = bubi_control[self.selected_parameters + ["ts_0"]]
        print(bubi_control)

        # Resample on days
        bubi_intervention["ts_0"] = pd.to_datetime(bubi_intervention["ts_0"])
        bubi_intervention = bubi_intervention.resample("D", on="ts_0").sum()
        print(bubi_intervention)

        bubi_control["ts_0"] = pd.to_datetime(bubi_control["ts_0"])
        bubi_control = bubi_control.resample("D", on="ts_0").sum()
        print(bubi_control)

        # Filter between two dates
        bubi_intervention = bubi_intervention.query(
            "ts_0 >= '2023-05-01' and ts_0 < '2023-08-01'"
        )
        print(bubi_intervention)

        bubi_control = bubi_control.query(
            "ts_0 >= '2023-05-01' and ts_0 < '2023-08-01'"
        )
        print(bubi_control)

        # plot
        ax = bubi_intervention.plot(color="blue")
        ax.set_prop_cycle(None)
        bubi_control.plot(ax=ax, linestyle="dotted", color="green")

        plt.axvline(x="2023-06-15", color="red", linestyle=":", alpha=0.5, linewidth=3)

        ax.set_xlabel("date")
        ax.set_ylabel("end trip number")

        plt.legend(
            ["intervented", "control"], loc="upper right", edgecolor="red", shadow=True
        )
        plt.show()

        return bubi_control


class config_co2mpas(config):
    __ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
    __INPUT_DATA_FILE = os.path.join(
        __ROOT_DIR, "co2mpas", "output", "20231118_142209-co2mpas_conventional.xlsx"
    )

    # TODO: outcome: co2_emissions
    # temporally removed:
    # "engine_temperature_derivatives",
    # "wheel_speeds",
    #  "motor_p1_maximum_powers",
    # "active_cylinders",
    #  it is in different file: "velocities",

    # TODO: temporally copied here from ontology.py
    selected_parameters = [
        "engine_temperatures",
        "motor_p0_speeds",
        "engine_powers_out",
        "co2_emissions",
        "fuel_consumptions_liters_value",
    ]

    def prepare_dataset(self):
        nedc_h = pd.read_excel(
            self.__INPUT_DATA_FILE,
            sheet_name="output.prediction.nedc_h.ts",
            skiprows=1,
            index_col="times",  # TODO: ?
            nrows=1500,
        )

        return nedc_h[self.selected_parameters]


if __name__ == "__main__":
    my_run = config_bubi()
    my_run.prepare_dataset()
    print("end")

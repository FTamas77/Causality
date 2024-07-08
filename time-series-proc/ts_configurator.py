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

    # TODO: default parameters
    selected_parameters = [
        "end_trip_no",
        "temperature",
        "max_wind_speed",
        "start_trip_no",
        "precipitation",
    ]

    def read_causal_discovery_dataset(self, selected_parameters=None, resample=True):
        """
        Returns multiple feautures, according to the selected parameters
        """

        if selected_parameters is not None:
            self.selected_parameters = selected_parameters

        # , nrows=3000
        bubi = pd.read_csv(self.__INPUT_DATA_FILE)

        # Filter on stations
        bubi = bubi[self.selected_parameters + ["station_name", "ts_0"]]
        bubi = bubi[bubi.station_name.str.startswith("0507")]
        print(bubi)

        # Resample on days
        if resample is True:
            bubi["ts_0"] = pd.to_datetime(bubi["ts_0"])
            bubi = bubi.resample("D", on="ts_0").sum()
            print(bubi)
        else:
            print("There is no resample.")

        # remove helper data (station and time)
        bubi = bubi[self.selected_parameters]
        print(bubi)

        return bubi

    def read_causal_impact_dataset(self, selected_parameters=None):
        """
        Read two time lines: control and intervention
        """

        if selected_parameters is not None:
            self.selected_parameters = selected_parameters

        # , nrows=3000
        bubi = pd.read_csv(self.__INPUT_DATA_FILE)
        print(bubi)

        # Filter on stations, first add the station to the all set
        bubi = bubi[self.selected_parameters + ["station_name", "ts_0"]]

        # Intervention, filter then remove it
        bubi_intervention = bubi[bubi.station_name.str.startswith("0507")]
        print(bubi_intervention)
        bubi_intervention = bubi_intervention[self.selected_parameters + ["ts_0"]]
        print(bubi_intervention)

        # Control
        bubi_control = bubi[bubi.station_name.str.startswith("0508")]
        print(bubi_control)
        bubi_control = bubi_control[self.selected_parameters + ["ts_0"]]
        print(bubi_control)

        # Resample on days
        # intervention
        bubi_intervention["ts_0"] = pd.to_datetime(bubi_intervention["ts_0"])
        bubi_intervention = bubi_intervention.resample("D", on="ts_0").sum()
        print(bubi_intervention)

        # control
        bubi_control["ts_0"] = pd.to_datetime(bubi_control["ts_0"])
        bubi_control = bubi_control.resample("D", on="ts_0").sum()
        print(bubi_control)

        # Filter between two dates
        # invervention
        bubi_intervention = bubi_intervention.query(
            "ts_0 >= '2023-05-01' and ts_0 < '2023-08-01'"
        )
        print(bubi_intervention)

        # control
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

        return bubi_intervention, bubi_control


class config_co2mpas(config):
    __ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
    __INPUT_DATA_FILE = os.path.join(
        __ROOT_DIR, "co2mpas", "output", "20231118_142209-co2mpas_conventional.xlsx"
    )

    # temporally removed:
    # "engine_temperature_derivatives",
    # "wheel_speeds",
    # "motor_p1_maximum_powers",
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

    def prepare_dataset(self, selected_parameters=None):

        if selected_parameters is not None:
            self.selected_parameters = selected_parameters

        nedc_h = pd.read_excel(
            self.__INPUT_DATA_FILE,
            sheet_name="output.prediction.nedc_h.ts",
            skiprows=1,
            index_col="times",  # TODO: ?
            nrows=1500,
        )

        return nedc_h[self.selected_parameters]


class config_mav(config):
    pass


if __name__ == "__main__":
    # my_run = config_bubi()

    # bubi_data = my_run.read_causal_discovery_dataset()
    # print(bubi_data)

    # selected_parameters = ["end_trip_no"]
    # bubi_intervention, bubi_control = my_run.read_causal_impact_dataset(
    #    selected_parameters
    # )

    my_run = config_co2mpas()
    data = my_run.prepare_dataset()
    print(data)

    print("end")

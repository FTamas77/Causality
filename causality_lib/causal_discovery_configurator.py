import os
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt

import numpy as np
from sklearn.linear_model import LinearRegression

import datetime as dt

from statsmodels.tsa.seasonal import seasonal_decompose


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

        return bubi_intervention, bubi_control

    def regression(self, bubi_intervention, bubi_control):
        bubi_control.reset_index()  # Is it needed?

        bubi_control["ts_0"] = bubi_control.index
        bubi_control.index = range(len(bubi_control))

        plt.scatter(
            bubi_control[["ts_0"]], bubi_control[["end_trip_no"]], color="black"
        )
        plt.show()

        x = pd.to_numeric(bubi_control.ts_0, downcast="float").to_numpy().reshape(-1, 1)
        y = pd.to_numeric(bubi_control.end_trip_no, downcast="float")

        print(x)
        print(y)

        model = LinearRegression()
        model.fit(x, y)
        r_sq = model.score(x, y)

        print(f"coefficient of determination: {r_sq}")
        print(f"intercept: {model.intercept_}")
        print(f"slope: {model.coef_}")

        dt_obj = dt.datetime.strptime("2023-08-01", "%Y-%m-%d")
        numpy_array = np.array([dt_obj.timestamp()]).reshape(-1, 1)
        print(numpy_array)
        y_pred = model.predict(numpy_array)
        print(f"predicted response:\n{y_pred}")

        # https://realpython.com/linear-regression-in-python/
        y_pred = model.intercept_ + model.coef_ * numpy_array
        print(y_pred)
        return

    def decomposition(self, bubi_intervention, bubi_control):
        """
        trend, seasonality, and residual
        https://medium.com/@vaibhav1403/decomposition-in-time-series-analysis-c7b03c5a1ea2
        """
        bubi_intervention.plot()

        bubi_intervention_before = bubi_control.query(
            "ts_0 >= '2023-05-01' and ts_0 < '2023-06-15'"
        )
        bubi_intervention_before.plot()

        bubi_intervention_after = bubi_control.query(
            "ts_0 > '2023-06-15' and ts_0 <= '2023-08-01'"
        )
        bubi_intervention_after.plot()

        result_mul = seasonal_decompose(
            bubi_intervention["end_trip_no"],
            model="multiplicative",
            extrapolate_trend="freq",
        )
        result_add = seasonal_decompose(
            bubi_intervention["end_trip_no"], model="additive", extrapolate_trend="freq"
        )

        plt.rcParams.update({"figure.figsize": (20, 10)})
        result_mul.plot().suptitle("Multiplicative Decompose", fontsize=30)
        result_add.plot().suptitle("Additive Decompose", fontsize=30)
        plt.show()


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
    bubi_intervention, bubi_control = my_run.prepare_dataset()
    # my_run.regression(bubi_intervention, bubi_control)
    my_run.decomposition(bubi_intervention, bubi_control)
    print("end")

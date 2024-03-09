import pandas as pd
from matplotlib import pyplot as plt

import numpy as np
from sklearn.linear_model import LinearRegression

import datetime as dt

from statsmodels.tsa.seasonal import seasonal_decompose


class ts_utils:

    @staticmethod
    def decomposition(time_series_data, column_name):
        """
        trend, seasonality, and residual
        https://medium.com/@vaibhav1403/decomposition-in-time-series-analysis-c7b03c5a1ea2
        """

        time_series_data.plot()

        result_mul = seasonal_decompose(
            time_series_data[column_name],
            model="multiplicative",
            extrapolate_trend="freq",
        )

        result_add = seasonal_decompose(
            time_series_data[column_name], model="additive", extrapolate_trend="freq"
        )

        plt.rcParams.update({"figure.figsize": (20, 10)})
        result_mul.plot().suptitle("Multiplicative Decompose", fontsize=30)
        result_add.plot().suptitle("Additive Decompose", fontsize=30)
        plt.show()

    @staticmethod
    def regression(time_series_data, column_name):
        """
        https://realpython.com/linear-regression-in-python/
        """

        # reset index renames the earlier index to index by default
        time_series_data.reset_index().plot.scatter(x="index", y="A")

        x = (
            pd.to_numeric(time_series_data.index, downcast="float")
            .to_numpy()
            .reshape(-1, 1)
        )
        y = pd.to_numeric(time_series_data.A, downcast="float")

        print(x)
        print(y)

        model = LinearRegression()
        model.fit(x, y)
        r_sq = model.score(x, y)

        print(f"coefficient of determination: {r_sq}")
        print(f"intercept: {model.intercept_}")
        print(f"slope: {model.coef_}")

        # convert date to numerical value:
        # https://stackoverflow.com/a/40217971/23111804
        dt_obj = dt.datetime.strptime("2023-08-01", "%Y-%m-%d")
        numpy_array = np.array([dt_obj.timestamp()]).reshape(-1, 1)
        print(numpy_array)
        y_pred = model.predict(numpy_array)
        print(f"predicted response:\n{y_pred}")

        y_pred = model.intercept_ + model.coef_ * numpy_array
        print(y_pred)
        return


if __name__ == "__main__":
    date = pd.date_range("1/1/2020", periods=1000, freq="W-SUN")
    long_df = pd.DataFrame(
        np.random.randint(low=1, high=100, size=(1000, 4), dtype="int"),
        index=date,
        columns=list("ABCD"),
    )
    long_df.head()
    print(long_df)

    # ts_utils.decomposition(long_df, "A")

    # ts_utils.regression(long_df, "A")

    print("...")

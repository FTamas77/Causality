import matplotlib
import matplotlib.pyplot as plt

from ts_configurator import config_bubi


class ts_granger:
    def __init__(self, config) -> None:
        self.config = config

    def prepare_input_dataset(self):
        self.intervention, self.control = self.config.read_causal_impact_dataset(
            [
                "end_trip_no",
            ]
        )

    def plot_prepared_data(self):
        plt.figure("Prepared input data")

        # plot the intervention and the control
        fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True)

        axs[0].set_title("intervention")
        axs[0].plot(self.intervention, color="tab:green")

        axs[1].set_title("control")
        axs[1].plot(self.control, color="tab:blue")


if __name__ == "__main__":
    config = config_bubi()

    my_run = ts_granger(config)
    my_run.prepare_input_dataset()
    my_run.plot_prepared_data()
    print("end")

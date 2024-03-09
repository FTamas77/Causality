# from causalimpact import CausalImpact

#
# There are two possible libraries:
# https://github.com/google/tfp-causalimpact
# https://github.com/WillianFuks/tfcausalimpact
#

#
# TODO: use this example
# https://github.com/google/tfp-causalimpact/blob/main/docs/quickstart.ipynb
#

import causalimpact

import matplotlib
import matplotlib.pyplot as plt

from ts_configurator import config_bubi
from ts_configurator import config_co2mpas


class ts_causalimpact:
    def __init__(self, config) -> None:
        self.config = config

    def prepare_input_dataset(self):
        self.intervention, self.control = self.config.read_causal_impact_dataset(
            [
                "end_trip_no",
            ]
        )

    def apply_granger_causality(self):



if __name__ == "__main__":
    config = config_bubi()

    my_run = ts_causalimpact(config)
    my_run.prepare_input_dataset()
    my_run.apply_granger_causality()
    print("end")

from causality_lib.causality_ts_configurator import config_bubi
from causality_lib.causality_ts_configurator import config_co2mpas


class Causal_discovery_tfp_causalimpact:
    def prepare_input_dataset(self):
        self.config = config_bubi()


if __name__ == "__main__":
    my_run = Causal_discovery_tfp_causalimpact()
    my_run.prepare_input_dataset()

    print("...")

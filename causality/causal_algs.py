from causal_inference import Causal_inference
from causal_discovery import Causal_discovery
from logger import logger as l
from configurator import configurator
from data_reader import data_reader


class causal_algs:

    @staticmethod
    def causal_inference(progressBar):

        #l = logger.get_instance()
        l.print_log("Causal_inference is called")
        l.print_log("Reading input data started")

        c = configurator()
        df = data_reader.read_input_data(c.get_causal_inference_keep_cols(),
                                         c.get_applied_input_files())
        progressBar.config(value=20)
        l.print_log("Reading input data completed")

        causality = Causal_inference()
        progressBar.config(value=10)

        l.print_log("Create the model")
        model = causality.create_model(df)
        progressBar.config(value=30)
        l.print_log("The model has been created")

        l.print_log("Identify effect")
        estimand = causality.identify_effect(model)
        progressBar.config(value=40)
        l.print_log("Identify effect is done")

        l.print_log("Estimate effect")
        estimate = causality.estimate_effect(model, estimand)
        progressBar.config(value=80)

        l.print_log("Estimate effect is done")

        l.print_log("Refute")
        causality.refute(model, estimand, estimate)
        progressBar.config(value=100)
        l.print_log("Refute is done, computation completed")

    @staticmethod
    def causal_discovery(progressBar):

        #l = logger.get_instance()
        l.print_log("Discovery is called")
        l.print_log("Read the input data")

        c = configurator()
        df = data_reader.read_input_data(c.get_causal_discovery_keep_cols(),
                                         c.get_applied_input_files())
        l.print_log("Read the input data is done")
        progressBar.config(value=20)

        causality = Causal_discovery()
        progressBar.config(value=40)

        l.print_log("Run pc alg")
        causality.calculate_pc(df)
        progressBar.config(value=60)
        l.print_log("Run pc alg is done")

        l.print_log("Run fci alg")
        causality.calculate_fci(df)
        progressBar.config(value=80)
        l.print_log("Run fci alg is done")

        l.print_log("Run ges")
        causality.calculate_ges(df)
        progressBar.config(value=100)
        l.print_log("Run ges is done")

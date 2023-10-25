

from data_reader import data_reader

from causal_inference import Causal_inference
from causal_discovery import Causal_discovery


class causal_algs:
    """
    It has only static members since it only implements algoritms
    Has no data
    """

    @staticmethod
    def causal_inference(applied_input_files, progressBar, write_log):
        write_log.print_log("Causal_inference is called")

        keep_cols = ["teljesítmény", "CO2 kibocsátás gkm V7",
                     "hengerűrtartalom", "Elhaladási zaj dBA"]

        reader = data_reader(applied_input_files)
        df = reader.read_input_data(keep_cols)

        causality = Causal_inference()
        progressBar.config(value=10)

        write_log.print_log("Reading input data")
        # df = causality.read_input_data()
        progressBar.config(value=20)

        write_log.print_log("Create the model")
        model = causality.create_model(df)
        progressBar.config(value=30)

        write_log.print_log("Identify effect")
        estimand = causality.identify_effect(model)
        progressBar.config(value=40)

        write_log.print_log("Estimate effect")
        estimate = causality.estimate_effect(model, estimand)
        progressBar.config(value=80)
        # dowhy.plotter.plot_causal_effect(
        # estimate, df["teljesítmény"], df["CO2 kibocsátás gkm V7"])

        write_log.print_log("Refute")
        causality.refute(model, estimand, estimate)
        progressBar.config(value=100)

    @staticmethod
    def causal_discovery(applied_input_files, progressBar, write_log):
        write_log.print_log("Discovery is called")

        # simple or extended
        keep_cols = ["teljesítmény", "CO2 kibocsátás gkm V7",
                     "hengerűrtartalom", "Elhaladási zaj dBA",
                     "Összevont átlagfogy", "Korr abszorp együttható", "kilométeróra állás", "gy fogy ért orszúton"]

        keep_cols_label = ["Performance", "CO2 emission",
                           "Cylinder cap.", "Passing noise",
                           "Sum. consumption", "Corr. abs. co.", "Actual kilometers", "Cons. on roads"]

        reader = data_reader(applied_input_files)
        df = reader.read_input_data(keep_cols)

        causality = Causal_discovery()
        progressBar.config(value=20)

        write_log.print_log("read input data")
        # df = causality.read_input_data()
        progressBar.config(value=40)

        write_log.print_log("pc")
        causality.calculate_pc(df)
        progressBar.config(value=60)

        write_log.print_log("fci")
        causality.calculate_fci(df)
        progressBar.config(value=80)

        write_log.print_log("ges")
        causality.calculate_ges(df)
        progressBar.config(value=100)

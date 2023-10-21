from causallearn.search.ScoreBased.GES import ges
from causallearn.search.FCMBased.lingam.utils import make_dot
from causallearn.search.FCMBased import lingam
from causallearn.search.ConstraintBased.FCI import fci
from causallearn.search.ConstraintBased.PC import pc
from causallearn.utils.GraphUtils import GraphUtils

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

import io
import os
from pathlib import Path
import networkx as nx

from utils import read_input_data

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent


class Causal_discovery:
    """Causal discovery class:
    only the configuration is stored, calculated causal discovery object are not """

    def __init__(self, input_files):
        self.input_files = input_files

        # simple or extended
        self.keep_cols = ["teljesítmény", "CO2 kibocsátás gkm V7",
                          "hengerűrtartalom", "Elhaladási zaj dBA"]
        #   "Összevont átlagfogy", "Korr abszorp együttható", "kilométeróra állás", "gy fogy ért orszúton"]

        self.keep_cols_label = ["Performance", "CO2 emission",
                                "Cylinder cap.", "Passing noise"]
        # "Sum. consumption", "Corr. abs. co.", "Actual kilometers", "Cons. on roads"]

    def read_input_data(self):
        df = read_input_data(self.keep_cols, self.input_files)

        print("\nSize of the input data: " +
              str(df.shape[0]) + "x" + str(df.shape[1]) + "\n\nAnd the input data:\n")

        print(df)

        print("**** Header:\n")
        print(df.head())

        print("**** Numpy:\n")
        print(df.to_numpy())

        return df

    def calculate_pc(self, df):
        cg = pc(df.to_numpy())

        # visualization using pydot
        # cg.draw_pydot_graph()

        pyd = GraphUtils.to_pydot(cg.G, labels=self.keep_cols_label)

        PC_FILE = os.path.join(ROOT_DIR, 'doc', 'pc.png')
        pyd.write_png(PC_FILE)
        # tmp_png = pyd.create_png(f="png")
        # fp = io.BytesIO(tmp_png)
        # img = mpimg.imread(fp, format='png')
        # plt.axis('off')
        # plt.imshow(img)
        # plt.show()

        # visualization using networkx
        # cg.to_nx_graph()
        # cg.draw_nx_graph(skel=False)

    def calculate_fci(self, df):

        # default parameters
        g, edges = fci(df.to_numpy())

        # visualization
        pdy = GraphUtils.to_pydot(g, labels=self.keep_cols_label)

        FCI_FILE = os.path.join(ROOT_DIR, 'doc', 'fci.png')
        pdy.write_png(FCI_FILE)

    def calculate_ges(self, df):
        # default parameters
        Record = ges(df.to_numpy())

        # Visualization using pydot

        pyd = GraphUtils.to_pydot(Record['G'])
        tmp_png = pyd.create_png(f="png")
        fp = io.BytesIO(tmp_png)
        img = mpimg.imread(fp, format='png')
        plt.axis('off')
        plt.imshow(img)
        plt.show()

        # or save the graph
        GES_FILE = os.path.join(ROOT_DIR, 'doc', 'ges.png')
        pyd.write_png(GES_FILE)

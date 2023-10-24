from causallearn.search.ScoreBased.GES import ges
from causallearn.search.FCMBased.lingam.utils import make_dot
from causallearn.search.FCMBased import lingam
from causallearn.search.ConstraintBased.FCI import fci
from causallearn.search.ConstraintBased.PC import pc
from causallearn.utils.GraphUtils import GraphUtils

import matplotlib.pyplot as plt
import io
import os
from pathlib import Path
import networkx as nx

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent


class Causal_discovery:
    def __init__(self):
        # simple or extended
        self.keep_cols = ["teljesítmény", "CO2 kibocsátás gkm V7",
                          "hengerűrtartalom", "Elhaladási zaj dBA",
                          "Összevont átlagfogy", "Korr abszorp együttható", "kilométeróra állás", "gy fogy ért orszúton"]
        self.keep_cols_label = ["Performance", "CO2 emission",
                                "Cylinder cap.", "Passing noise",
                                "Sum. consumption", "Corr. abs. co.", "Actual kilometers", "Cons. on roads"]

    def calculate_pc(self, df):
        cg = pc(df.to_numpy())
        pyd = GraphUtils.to_pydot(cg.G, labels=self.keep_cols_label)
        PC_FILE = os.path.join(ROOT_DIR, 'doc', 'pc.png')
        pyd.write_png(PC_FILE)

    def calculate_fci(self, df):
        g, edges = fci(df.to_numpy())
        pdy = GraphUtils.to_pydot(g, labels=self.keep_cols_label)
        FCI_FILE = os.path.join(ROOT_DIR, 'doc', 'fci.png')
        pdy.write_png(FCI_FILE)

    def calculate_ges(self, df):
        Record = ges(df.to_numpy())
        pyd = GraphUtils.to_pydot(Record['G'], labels=self.keep_cols_label)
        GES_FILE = os.path.join(ROOT_DIR, 'doc', 'ges.png')
        pyd.write_png(GES_FILE)

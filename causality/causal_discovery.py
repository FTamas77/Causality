from causallearn.search.ScoreBased.GES import ges
from causallearn.search.ConstraintBased.FCI import fci
from causallearn.search.ConstraintBased.PC import pc
from causallearn.utils.GraphUtils import GraphUtils

import os

from configurator import configurator


class Causal_discovery:

    def calculate_pc(self, df):
        cg = pc(df.to_numpy())

        c = configurator()
        pyd = GraphUtils.to_pydot(
            cg.G, labels=c.get_causal_discovery_keep_cols_labels())

        PC_FILE = os.path.join(c.get_ROOT_DIR(), 'doc', 'pc.png')
        pyd.write_png(PC_FILE)

    def calculate_fci(self, df):
        g, edges = fci(df.to_numpy())

        c = configurator()
        pdy = GraphUtils.to_pydot(
            g, labels=c.get_causal_discovery_keep_cols_labels())

        FCI_FILE = os.path.join(c.get_ROOT_DIR(), 'doc', 'fci.png')
        pdy.write_png(FCI_FILE)

    def calculate_ges(self, df):
        Record = ges(df.to_numpy())

        c = configurator()
        pyd = GraphUtils.to_pydot(
            Record['G'], labels=c.get_causal_discovery_keep_cols_labels())

        GES_FILE = os.path.join(c.get_ROOT_DIR(), 'doc', 'ges.png')
        pyd.write_png(GES_FILE)

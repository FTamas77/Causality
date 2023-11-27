# In this file I apply causal discovery and interferenc on time-series data.
# There is no intervention here.
#

import os
from pathlib import Path

import pandas as pd
import numpy as np

import matplotlib
from matplotlib import pyplot as plt

import sklearn

import tigramite
from tigramite import data_processing as pp
from tigramite.toymodels import structural_causal_processes as toys

from tigramite import plotting as tp
from tigramite.pcmci import PCMCI
from tigramite.lpcmci import LPCMCI

from tigramite.independence_tests.parcorr import ParCorr
from tigramite.independence_tests.robust_parcorr import RobustParCorr
from tigramite.independence_tests.parcorr_wls import ParCorrWLS
#from tigramite.independence_tests.gpdc import GPDC
from tigramite.independence_tests.cmiknn import CMIknn
from tigramite.independence_tests.cmisymb import CMIsymb
from tigramite.independence_tests.gsquared import Gsquared
from tigramite.independence_tests.regressionCI import RegressionCI

__ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
__INPUT_DATA_FILE = os.path.join(__ROOT_DIR, 'co2mpas', 'output',
                                 '20231118_142209-co2mpas_conventional.xlsx')

# output.prediction.nedc_h.ts
nedc_h = pd.read_excel(__INPUT_DATA_FILE,
                       sheet_name="output.prediction.nedc_h.ts",
                       skiprows=1,
                       index_col="times",
                       nrows=1500)

# the selected sub data set
var_names = [
    'co2_emissions', 'motor_p2_planetary_speeds', 'engine_temperatures'
]
print(nedc_h[var_names].to_string(index=True, max_rows=10))
nedc_h = nedc_h[var_names]

fig, axs = plt.subplots(nrows=3, ncols=1, sharex=True)
fig.suptitle('Selected features')

axs[0].set_title('co2_emissions')
axs[0].plot(nedc_h["co2_emissions"], 'tab:green')

axs[1].set_title('motor_p2_planetary_speeds')
axs[1].plot(nedc_h["motor_p2_planetary_speeds"], 'tab:orange')

axs[2].set_title('engine_temperatures')
axs[2].plot(nedc_h["engine_temperatures"], 'tab:blue')

# plt.show()

# Causal discovery

dataframe = pp.DataFrame(nedc_h.to_numpy(), var_names=var_names)

#tp.plot_timeseries(dataframe)
#plt.show()

# Partial correlation test.
parcorr = ParCorr(significance='analytic')

# PCMCI causal discovery for time series datasets.
pcmci = PCMCI(dataframe=dataframe, cond_ind_test=parcorr, verbosity=1)

# Unconditional lagged independence tests.
correlations = pcmci.get_lagged_dependencies(tau_max=20,
                                             val_only=True)['val_matrix']

matrix_lags = None  #np.argmax(np.abs(correlations), axis=2)
tp.plot_scatterplots(dataframe=dataframe,
                     add_scatterplot_args={'matrix_lags': matrix_lags})
#plt.show()

#tp.plot_densityplots(dataframe=dataframe, add_densityplot_args={'matrix_lags': matrix_lags})
#plt.show()

parcorr = ParCorr(significance='analytic')
pcmci = PCMCI(dataframe=dataframe, cond_ind_test=parcorr, verbosity=1)

correlations = pcmci.get_lagged_dependencies(tau_max=20,
                                             val_only=True)['val_matrix']
lag_func_matrix = tp.plot_lagfuncs(val_matrix=correlations,
                                   setup_args={
                                       'var_names': var_names,
                                       'x_base': 5,
                                       'y_base': .5
                                   })

pcmci.verbosity = 1
results = pcmci.run_pcmci(tau_max=8, pc_alpha=None, alpha_level=0.01)

print("p-values")
print(results['p_matrix'].round(3))
print("MCI partial correlations")
print(results['val_matrix'].round(2))

q_matrix = pcmci.get_corrected_pvalues(p_matrix=results['p_matrix'],
                                       tau_max=8,
                                       fdr_method='fdr_bh')
pcmci.print_significant_links(p_matrix=q_matrix,
                              val_matrix=results['val_matrix'],
                              alpha_level=0.01)
graph = pcmci.get_graph_from_pmatrix(p_matrix=q_matrix,
                                     alpha_level=0.01,
                                     tau_min=0,
                                     tau_max=8,
                                     link_assumptions=None)
results['graph'] = graph

tp.plot_graph(val_matrix=results['val_matrix'],
              graph=results['graph'],
              var_names=var_names,
              link_colorbar_label='cross-MCI',
              node_colorbar_label='auto-MCI',
              show_autodependency_lags=False)

tp.plot_time_series_graph(
    figsize=(6, 4),
    val_matrix=results['val_matrix'],
    graph=results['graph'],
    var_names=var_names,
    link_colorbar_label='MCI',
)

plt.show()

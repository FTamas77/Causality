# General notes:

* 3.10.6 seems to work with pygraphviz
  * Graphviz must be added to the path
  * This was also missing after install IPython and DoWhy: `pip install openpyxl`
  * On my work machine: `python -m pip install --use-pep517 --config-setting="--global-option=build_ext" --config-setting="--global-option=-IC:\Program Files\Graphviz\include" --config-setting="--global-option=-LC:\Program Files\Graphviz\lib" pygraphviz -vvv`
  * On my school machine: `pip install pygraphviz-1.9-cp310-cp310-win_amd64.whl`

# Working environment:

* **Create an environment to a specific python version:** `virtualenv causalityEnv -p python3.11`
* **Activate the created environment:** `.\causalityEnv\Scripts\activate`
* **Get the package list:** `python -m pip freeze > requirements.txt`
* **Install the package list:** `python -m pip install -r requirements.txt`
* **Deactivate the environment:** `deactivate`

# Programming:

## Sample causal inference computation (skeleton):

```
from dowhy import CausalModel
import dowhy

import numpy as np
import pandas as pd

from IPython.display import Image, display

sample_size = 1000
W = np.random.randn(sample_size)
X = 0.3*W + np.random.randn(sample_size)
Y = 0.45*W + 0.87*X + 0.4*np.random.randn(sample_size)

# Note that we pass all the variables to the dataframe
data_1 = pd.DataFrame(np.vstack([X, W, Y]).T, columns=['X', 'W', 'Y'])
print(data_1)

# Create the graph
graph_1 = """graph [directed 1 node [id "X" label "X"] node [id "W" label "W"] node [id "Y" label "Y"]
edge [source "W" target "X"] edge [source "W" target "Y"] edge [source "X" target "Y"]]"""

# Instantiate the CausalModel object
model_1 = CausalModel(
    data=data_1,
    treatment='X',
    outcome='Y',
    graph=graph_1
)

print(model_1.view_model())

estimand_1 = model_1.identify_effect()
print(estimand_1)

estimate_1 = model_1.estimate_effect(
    identified_estimand=estimand_1,
    method_name='backdoor.linear_regression')
```

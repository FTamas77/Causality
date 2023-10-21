# Dev environment:

* 3.10.6 seems to work with pygraphviz
  * Graphviz must be added to the path
  * This was also missing after install IPython and DoWhy: `pip install openpyxl`
  * On my work machine: `python -m pip install --use-pep517 --config-setting="--global-option=build_ext" --config-setting="--global-option=-IC:\Program Files\Graphviz\include" --config-setting="--global-option=-LC:\Program Files\Graphviz\lib" pygraphviz -vvv`
  * On my school machine: `pip install pygraphviz-1.9-cp310-cp310-win_amd64.whl` and this was downloaded from here: `https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygraphviz`

# Useful comments:

* **Create an environment to a specific python version:** `virtualenv causalityEnv3.10 -p python3.10`
* **Activate the created environment:** `.\causalityEnv3.10\Scripts\activate`
* **Get the package list:** `python -m pip freeze > requirements3.10.txt`
* **Install the package list:** `python -m pip install -r requirements3.10.txt`
* **Deactivate the environment:** `deactivate`

# Causality:

* Further technical [utils](./causality/index.md).

# Packaging:

* Create package [tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
  * Build: `py -m build`
* Test to upload [test_pypi](https://test.pypi.org/account/register/https://test.pypi.org/account/register/)
  * Upload: `py -m twine upload --repository testpypi dist/*`


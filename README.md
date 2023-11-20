# Table of Contents

- [Table of Contents](#table-of-contents)
- [General](#general)
  - [Dev environment-related useful notes](#dev-environment-related-useful-notes)
  - [Packaging](#packaging)
  - [git related useful commands](#git-related-useful-commands)
- [Applied dataset](#applied-dataset)
- [Causality package](#causality-package)
  - [Configuration](#configuration)
- [Ontology package](#ontology-package)
- [CO2MPAS sim](#co2mpas-sim)
- [Test](#test)

---

# General

There are two packages:

* Causality with a GUI
* Ontology with a web

## Dev environment-related useful notes

Setting up:

* **Create an environment to a specific python version:** `virtualenv causalityEnv3.10 -p python3.10`
* **Activate the created environment:** `.\causalityEnv3.10\Scripts\activate`
* **Get the package list:** `python -m pip freeze > requirements3.10.txt`
* **Install the package list:** `python -m pip install -r requirements3.10.txt`
* **Deactivate the environment:** `deactivate`

3.10.6 seems to work with pygraphviz:

* Graphviz must be added to the path
* This was also missing after install IPython and DoWhy: `pip install openpyxl`
* On my work machine: `python -m pip install --use-pep517 --config-setting="--global-option=build_ext" --config-setting="--global-option=-IC:\Program Files\Graphviz\include" --config-setting="--global-option=-LC:\Program Files\Graphviz\lib" pygraphviz -vvv`
* On my school machine: `pip install pygraphviz-1.9-cp310-cp310-win_amd64.whl` and this was downloaded from here: `https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygraphviz`

## Packaging

* Create package [tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
  * Build: `py -m build`
* Test to upload [test_pypi](https://test.pypi.org/account/register/https://test.pypi.org/account/register/)
  * Upload: `py -m twine upload --repository testpypi dist/*`

## git related useful commands

* Create tag: `git tag `<tagname>
* Push tags: `git push origin --tags`
* Move tags, steps:
  * git tag -d <tagname>                  # delete the old tag locally
  * git push origin :refs/tags/<tagname>  # delete the old tag remotely
  * git tag <tagname> <commitId>          # make a new tag locally
  * git push origin <tagname>             # push the new local tag to the remote

# Applied dataset

* Added as a submodule
* [https://github.com/FTamas77/dataset](https://github.com/FTamas77/datasethttps:/)

---

# Causality package

* Further technical/coding-related notes [dev](./causality/dev.md)

## Configuration

* **Example:** measurement_config.json
* **Schema:** measurement_config_schema.json

---

# Ontology package

* Dev details [here](./ontology/dev.md)

---

# CO2MPAS sim

* Dev details [here](./co2mpas/dev.md)

---

# Test

* Dev details [here](./test/dev.md)

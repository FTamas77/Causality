
# General

## Setting up:

* **Create an environment to a specific python version:** `virtualenv causalityEnv3.10 -p python3.10`
* **Activate the created environment:** `.\causalityEnv3.10\Scripts\activate`
* **Get the package list:** `python -m pip freeze > requirements3.10.txt`
* **Install the package list:** `python -m pip install -r requirements3.10.txt`
* **Deactivate the environment:** `deactivate`

## Packaging

* Create package [tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
  * Build: `py -m build`
* Test to upload [test_pypi](https://test.pypi.org/account/register/https://test.pypi.org/account/register/)
  * Upload: `py -m twine upload --repository testpypi dist/*`

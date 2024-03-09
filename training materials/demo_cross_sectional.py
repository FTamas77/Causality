from dowhy import CausalModel
import dowhy, dowhy.plotter

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


def scatter_plot_with_correlation_line(x, y):
    plt.scatter(x, y, c="#c23424")

    axes = plt.gca()
    m, b = np.polyfit(x, y, 1)
    X_plot = np.linspace(axes.get_xlim()[0], axes.get_xlim()[1], 100)

    plt.xlabel("X")
    plt.ylabel("Y")

    plt.plot(X_plot, m * X_plot + b, "-")
    plt.show()


sample_size = 1000

W = np.random.randn(sample_size)
# X --> Y
X = 0.3 * W + np.random.randn(sample_size)
# Y is only partially dependent on X: 0.87
Y = 0.45 * W + 0.87 * X + 0.4 * np.random.randn(sample_size)
data = pd.DataFrame(np.vstack([X, W, Y]).T, columns=["X", "W", "Y"])

scatter_plot_with_correlation_line(data["X"], data["Y"])
print(data.head(10))

graph_1 = """graph [directed 1 node [id "X" label "X"] node [id "W" label "W"] node [id "Y" label "Y"]
edge [source "W" target "X"] edge [source "W" target "Y"] edge [source "X" target "Y"]]"""

model = CausalModel(data=data, treatment="X", outcome="Y", graph=graph_1)
model.view_model()

estimand = model.identify_effect()
print(estimand)

estimate = model.estimate_effect(
    identified_estimand=estimand, method_name="backdoor.linear_regression"
)
print(estimate)


res_random = model.refute_estimate(
    estimand, estimate, method_name="random_common_cause"
)
print(res_random)

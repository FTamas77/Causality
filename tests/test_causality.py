import sys
import pytest
import json
import os
from pathlib import Path

from configurator import configurator
from data_reader import data_reader


@pytest.mark.skip(reason="TODO")
def test_configurator_default_config():
    c = configurator()
    c.default()

    assert c.get_causal_discovery_keep_cols() == [
        "teljesítmény", "CO2 kibocsátás gkm V7", "hengerűrtartalom",
        "Elhaladási zaj dBA", "Összevont átlagfogy", "Korr abszorp együttható",
        "kilométeróra állás", "gy fogy ért orszúton"
    ]

    assert c.get_causal_discovery_keep_cols_labels() == [
        "Performance", "CO2 emission", "Cylinder cap.", "Passing noise",
        "Sum. consumption", "Corr. abs. co.", "Actual kilometers",
        "Cons. on roads"
    ]

    assert c.get_causal_inference_keep_cols() == [
        "teljesítmény", "CO2 kibocsátás gkm V7", "hengerűrtartalom",
        "Elhaladási zaj dBA"
    ]

    assert c.get_applied_input_files() == ["KV-41762_202301_test.xlsx"]


def test_data_reader_simple():
    c = configurator()
    c.default()
    c.default_causal_graph()

    c.get_outcome()
    c.get_treatment()
    c.get_causal_graph()

    d = data_reader()
    causal_inference_data = d.read_input_data("Causal inference")
    causal_discovery_data = d.read_input_data("Causal discovery")

    assert causal_inference_data.head != causal_discovery_data.head

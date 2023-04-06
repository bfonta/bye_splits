# coding: utf-8

_all_ = []

import os
import sys

parent_dir = os.path.abspath(__file__ + 2 * "/..")
sys.path.insert(0, parent_dir)

from utils import params

import os
import yaml
import numpy as np
import pandas as pd


def binConv(vals, dist, amin):
    """
    Converts bin indexes back to values (central values in the bin).
    Assumes equally-spaced bins.
    """
    return (vals * dist) + (dist / 2) + amin


def calcRzFromEta(eta):
    """R/z = tan(theta) [theta is obtained from pseudo-rapidity, eta]"""
    _theta = 2 * np.arctan(np.exp(-1 * eta))
    return np.tan(_theta)

def create_dir(p):
    if not os.path.exists(p):
        os.makedirs(p)

class dot_dict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def fill_path(base_path, data_dir=params.LocalStorage, ext="hdf5", **kw):
    """Create unique file name base on user input parameters."""

    with open(params.CfgPath, 'r') as afile:
        cfg = yaml.safe_load(afile)
        base_path += '_' + cfg['base']['FesAlgo']
    
    def add_if_exists(s, prefix):
        nonlocal base_path
        if s in kw:
            base_path += "_" + prefix + "_" + str(kw[s]).replace(".", "p")

    strings = {
        "sel": "SEL",
        "reg": "REG",
        "seed_window": "SW",
        "smooth_kernel": "SK",
        "cluster_algo": "CA",
    }

    for k, v in strings.items():
        add_if_exists(k, v)

    base_path += "." + ext
    return os.path.join(data_dir, base_path)


class SupressSettingWithCopyWarning:
    """
    Temporarily supress pandas SettingWithCopyWarning.
    It is known to ocasionally provide false positives.
    https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas
    """

    def __init__(self, chained=None):
        acceptable = [None, "warn", "raise"]
        assert chained in acceptable, "chained must be in " + str(acceptable)
        self.swcw = chained

    def __enter__(self):
        self.saved_swcw = pd.options.mode.chained_assignment
        pd.options.mode.chained_assignment = self.swcw
        return self

    def __exit__(self, *args):
        pd.options.mode.chained_assignment = self.saved_swcw


def get_detector_region_mask(df, region):
    """
    Obtain a mask to filter a specific detector region.
    subdetectors: - ECAL (1)
                  - HCAL silicon (2)
                  - HCAL scintillator (10)
    """
    if region == "Si":
        subdetCond = (df.subdet == 1) | (df.subdet == 2)
    elif region == "ECAL":
        subdetCond = df.subdet == 1
    elif region == "HCAL":
        subdetCond = (df.subdet == 2) | (df.subdet == 10)
    elif region == "MaxShower":
        subdetCond = (df.subdet == 1) & (df.layer >= 8) & (df.layer <= 15)
    elif region == "ExcludeMaxShower":
        subdetCond = (df.subdet == 1) & (df.layer < 8) | (df.layer > 15)

    df = df.drop(["subdet"], axis=1)
    return df, subdetCond

def print_histogram(arr):
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if arr[i, j] == 0:
                print("-", end="|")
            else:
                print("X", end="|")
        print()

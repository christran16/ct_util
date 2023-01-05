import os
import logging
import pandas as pd
import re
import numpy as np
from datetime import datetime
from pathlib import Path


today = datetime.today().strftime("%Y-%m-%d/")
hour_min = datetime.today().strftime("%H-%M")


def check_dir(path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:
            pass


def make_logger(
    name=__name__,
    logname=None,
    level=logging.INFO,
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filemode="a",
):
    logger = logging.getLogger(name)
    logging.basicConfig(level=level, format=fmt, datefmt=datefmt)
    if logname is not None:
        if "logs" not in logname:
            logname = "logs/" + logname
        if ".log" not in logname:
            logname = logname + ".log"
        check_dir(logname)
        formatter = logging.Formatter(fmt, datefmt=datefmt)
        file_handler = logging.FileHandler(logname, mode=filemode)
        file_handler.setFormatter(formatter)
        # stream_handler = logging.StreamHandler()
        for old_handler in logger.handlers:
            logger.removeHandler(old_handler)
        logger.addHandler(file_handler)
        # logger.addHandler(stream_handler)
    return logging.getLogger(name)


def one_hot_df(data, cols, drop=True):
    for col in cols:
        data[col] = pd.Categorical(data[col])
        df_dummies = pd.get_dummies(data[col], prefix=col)
        data = pd.concat([data, df_dummies], axis=1)
        if drop:
            data = data.drop(col, axis=1)
    return data


def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
    return sorted(l, key=alphanum_key)


def export_legend(legend, filename="results/legend.pdf"):
    fig = legend.figure
    fig.canvas.draw()
    bbox = legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(filename, dpi=200, bbox_inches=bbox)


def get_home():

    home = str(Path.home())
    return home


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

from indicators.SMA import SMA
import plotly
import plotly.graph_objs as go
import random
import math
from threading import Thread
from multiprocessing import Process, Manager
from main import start
file = "EURUSDFEB.csv"
indicators = {"smallSMA": [SMA,"EUR/USD", 70], "largeSMA": [SMA, "EUR/USD", 399]}
start(100000, 15, file, True, True, indicators)

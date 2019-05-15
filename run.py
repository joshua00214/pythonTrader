from indicators.SMA import SMA
import plotly
import plotly.graph_objs as go
import random
import math
from threading import Thread
from multiprocessing import Process, Manager
from main import start
file = "EURUSD2018.csv"
indicators = {"smallSMA": [SMA,"EUR/USD", 100], "largeSMA": [SMA, "EUR/USD", 200]}
start(100000, 15, file, True, True, indicators)

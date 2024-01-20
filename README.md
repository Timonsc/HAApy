# Hybrid Asset Allocation
haapy - a python implementation of Hybrid Asset Allocation


# Description
Hybrid Asset Allocation is a tactical investing strategy designed by Wouter J. Keller and Jan Willem Keuning [1, 2]. The strategy combines dual momentum with canary momentum. This script implements the G8/T4 variant and calculates the investment signals.

## The HAA Algorithm
1. Calculate the 12631U momentum scores of all assets.
2. First trading day of the month:
   * If the TIP momentum score is positive buy the 4 highest momentum assets from the offensive universe (SPY, IWM, VEA, VWO, DBC, VNQ, IEF, TLT) in equal proportion and hold until the end of the month. 
   * If the TIP score is negative, buy the highest momentum asset from the defensive universe (IEF, BIL) 
3. Sell all assets and calculate the next holdings.
See [1, 2] for further explanations.

# Usage
There's two options to run this script.
## 1. Docker Compose
Requirements: docker compose

* `docker compose up --build`
## 2. Python
Requirements: python 3.10.2
* `pip install poetry==1.7.1`
* `poetry shell`
* `python ./src/haapy`


# References
1. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4346906
2. https://indexswingtrader.blogspot.com/2023/02/introducing-hybrid-asset-allocation-haa.html?m=1

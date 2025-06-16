# print("Hello world from Docker!")

import datetime
from time import sleep

import pandas as pd

while True:
    df = pd.DataFrame(
        data={
            "timestamp": [datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2)],
            "col2": [3, 4],
        }
    )

    print(f"{df}")
    sleep(2)

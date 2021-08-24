from random import randint
import time
import os

def refresher(seconds):
    while True:
        mainDir = os.path.dirname(__file__)
        filePath = os.path.join(mainDir, 'dummy.py')
        with open(filePath, 'w') as f:
            f.write(f'variable= {randint(0, 10000)}')
        time.sleep(seconds)

refresher(3)
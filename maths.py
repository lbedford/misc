#!/usr/bin/env python3

import datetime
import random
import time

start = datetime.datetime.now()

correct = 0
incorrect = 0

random.seed()

A_VALUES = [ 1, 2, 3, 5, 10]
while True:
    a = random.choice(A_VALUES)
    max_b = 12
    b = random.randint(1, max_b)

    switcher = random.randint(0, 100) % 4

    if switcher == 0:
      print(f"{a} * {b} = ?")
      expected = a * b
    elif switcher == 1:
      print(f"{b} * {a} = ?")
      expected = a * b
    elif switcher == 2:
      print(f"? * {b} = {a * b}")
      expected = a
    else:
      print(f"{a} * ? = {a * b}")
      expected = b

    answer = input()
    
    if str(expected) == answer:
        correct = correct + 1
    else:
        incorrect = incorrect + 1
        print(f"Falsch! Richtig ist {expected}")

    delta = datetime.datetime.now() - start
    if delta.seconds > 60:
        break

print(f"Du hast {correct} richtige, und {incorrect} falsche Antworten gegeben.") 

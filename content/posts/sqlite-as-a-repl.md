---
date: 2023-10-10
title: SQLite as a Data REPL
description: If I have some large csv of data that I need to look at, I've typically reached first for pandas, served via a standard python or ipython repl - but I'm writing this to remember to consider looking at sqlite instead.
license: commercial
---

If I have some large csv of data that I need to look at, I've typically reached first for pandas, served via a standard python or ipython repl - but I'm writing this to remember to consider looking at sqlite instead.

Anecdotally (I'm typing it at the command-line now), the sqlite3 cli starts up much faster than python3 repl. Add in the cost of `import pandas as pd`, and you've probably already taken like 6-8 seconds. Reading in data with sqlite3 seems much quicker than `pd.read_csv`, and I get the benefit of easy persistance with `.backup FILE` instead of saving a bunch of additional csv files with the results of different filters.

`.import FILENAME TABLE --csv` is all you need to read a csv file as a new table, so give it a shot next time you find yourself with the need to munge some data quickly




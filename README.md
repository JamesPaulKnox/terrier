# What is Terrier?
An experimental algorithmic trading utility tool. For use with 
Interactive Brokers. Coded in Python 3.7.1 - uses the ib_insync API 
wrapper to make communication with the IB API many times easier.

# Important Notice
Looking for a working version? Look in the subdir v0 - you'll find some 
code there. I want to rework how I organize things and change some core 
ideas about how data is handled within individual scripts. v0 feels 
clunky and I don't like it.

## The Flow
There are three main steps.
1. (feed.py) Get data as fast & frequently as possible. Save this data 
to a file.
2. (algo.py) Interpret the data in the file to make a decision. Save the 
decision 
to another file.
3. (order.py) If my position in IB isn't matching what step 2 thinks, 
make it 
happen. So read the file, check to see if it matches current positions, 
and execute an order to reconcile the difference.

Each step is given its own file. This way, one step can never block the 
next from happening. Each step will therfore run as fast as it is 
individually capable, without concern for the other steps.

## Proposed Changes
* I dislike that order.py simply searches for files matching a certain 
pattern. I think it would be better if instead it attempted to open 
files that should exist based on the ./stock file. That way, the ./stock 
file can be updated and the ordering program knows immediately to stop 
trying to send orders for a stock no longer being updated.
* I dislike that all the looping is done within the non-master algo & 
feed. I think it would be better if instead the looping mechanism lives 
within the master_algo and master_feed files.
* I am unsure how I feed about the ./stocks file being plaintext. A npy 
file may be more useful if I decide to implement a screener in the 
future, BUT it would also be more annoying to test if its working 
proper.

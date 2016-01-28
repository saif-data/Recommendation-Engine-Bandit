## Recommendation Engine Bandit

Designed a simple Epsilon Greedy Bandit algorithm, to dynamically compare and optimize for the performance of selected recommendation engines.

Once the algorithm in integrated, and the decay rate specified, the best performing recommendation engine will be used ( decay / (total pageviews + decay) ) proportion of the time, while the remaining proportion will be filled by an equal distribution (p = 1 / number of recommendation engines) of all algorithms.

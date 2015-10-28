# Assignment 6: Bayes Net
Adrian Chen
## Usage
```
python main.py <insert flags here>
```
Possible flags are:
-p set a prior
-m marginal probability
-g conditional probability
-j joint probability
### Functionality
These are the programmed functionalities of the program:

-mD is the marginal probability distribution of Dyspnoea

-jPSC is the joint probabilities for all possible combinations of cancer, smoking and pollution

-jpsc is the joint probability for pollution = low, smoker = true, cancer = true

-j~p~s~c is the joint probability for pollution = high, smoker = false, cancer = false

-g"c|s" is the conditional probability for Cancer given that someone is a smoker.

-pS=0.40 sets the probability that smoking is True to .40.

-pP=0.80 sets the probability that pollution is Low to .80.

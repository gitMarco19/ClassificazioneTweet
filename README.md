## Description
Twitter has become an important communication channel in times of emergency.<br>
The ubiquitousness of smartphones enables people to announce an emergency they’re observing in real-time. Because of this, more agencies are interested in programatically monitoring Twitter (i.e. disaster relief organizations and news agencies).

## Goal
Predict which Tweets are about real disasters and which ones are not.

## Files
### pulisciParole.py
This file cleans all tweets from unuseful tags, emojis, URL and all kinds of like stuff which could create some problems to classify correctly the tweets.

### findModello.py
This file makes a comparison between some classification models by doing the cross validation and computing the score for each model. <br>
In the end, is choseen the model with the highest scoreto classify the tweets.

### SVC_formula.py
This file implements the SVC model by using the theory formulas of the Support Vector Machine.

## File directory
In this directory there are:
- *train.csv*: tweets train set.  
- *test.csv*: tweets test set.
- *train_cleaned.csv*: it is the train set which will be used to train the model. It comes from the clean of the file train.csv used in input of "pulisciParole.py"; 
- *test_cleaned.csv*: it is the test set which will be used to test the model. It comes from the clean of the file test.csv used in input of "pulisciParole.py"
- *sample_submission.csv*: file which will be used to make the real submission file.
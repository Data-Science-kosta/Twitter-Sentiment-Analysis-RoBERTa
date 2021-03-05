# Twitter-Sentiment-Analysis-RoBERTa
Sentiment Analysis of tweets written in underused Slavic languages (Serbian, Bosnian and Croatian) using pretrained multilingual RoBERTa based model XLM-R.

# Data
Sentiment Analysis is performed on 2 different datasets separately (I decided not to join the datasets, because I wanted to compare my results with the similar work):<br />
*1. CLARIN.SI - Twitter sentiment for 15 European languages:<br />

*2. doiSerbia:
This dataset is collected by Ljajić Adela and Marović Ulfeta and there work on the same problem can be found [here](http://www.doiserbia.nb.rs/img/doi/1820-0214/2019/1820-02141800013L.pdf). Dataset is balanced and it consists out of only **1152** labeled tweets. The labels are 0 = positive, 2 = neutral and 4 = negative. Text of the tweets is not provided and can be extracted through the [Twitter API](https://developer.twitter.com/en/docs/twitter-api) using tweet ids.

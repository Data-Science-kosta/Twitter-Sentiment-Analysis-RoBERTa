# Twitter-Sentiment-Analysis-RoBERTa
Sentiment Analysis of tweets written in underused Slavic languages (Serbian, Bosnian and Croatian) using pretrained multilingual RoBERTa based model XLM-R.

# Data
Sentiment Analysis is performed on 2 different datasets separately (I decided not to join the datasets, because I wanted to compare my results with the similar work):<br />
1. **CLARIN.SI** - Twitter sentiment for 15 European languages:<br />
Dataset can be found [here](https://www.clarin.si/repository/xmlui/handle/11356/1054). It consits of tweet IDs (which can be used for extraction of tweets through the [Tweeter API](https://developer.twitter.com/en/docs/twitter-api)) and corresponding labels (positive, negative or neutral). From this dataset only Serbian, Croatian and Bosnian tweets were used.<br />
**Note** that this dataset is 5 years old so we won't be able to extract the large number of tweets, because they are deleted.
**Similar work** on the same dataset can be found [here](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0155036). They achieved 55.9% accuracy on the dataset that consits of 193827 Serbian, Bosnian and Croatian tweets. 
2. **doiSerbia**:<br />
This dataset is collected by Ljajić Adela and Marović Ulfeta and there work on the same problem can be found [here](http://www.doiserbia.nb.rs/img/doi/1820-0214/2019/1820-02141800013L.pdf). Dataset is balanced and it consists out of only **1152** labeled tweets. The labels are 0 = positive, 2 = neutral and 4 = negative. Text of the tweets is not provided and can be extracted through the [Twitter API](https://developer.twitter.com/en/docs/twitter-api) using tweet ids.

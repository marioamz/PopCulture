# PopCulture

This project uses a basic machine learning bag of words model to do sentiment analysis on best-selling books, movies, and songs in order to gauge sentiment over the last 70 years.

## Getting Started

These instructions will get you a copy of the project running on your local machine. 

### Step-by-Step Instructions

#### Step 0: Get Installed

Make sure to install the following:

```
pip3 install sklearn
pip3 install nltk
pip3 install jellyfish
pip3 install django
pip3 install wikipedia
pip3 install xlrd
```

#### Step 1: Get Git

Make sure to add the movies_metadata.csv file from dropbox/google drive file and then pull all the necessary files into a new directory on your machine by running the following command. The movies_metadata.csv must be within the git repository. 

```
git clone https://github.com/marioamz/PopCulture
```

#### Step 2: Get Data
 
In iPython3, run the file called condensed_db to process the books, songs, and movies data. This takes about 15 seconds.

The output file will be called final_media_df.csv

```
import condensed_db
run condensed_db
result = create_file()
```

#### Step 3: Get Emotions

In iPython3, run our machine learning algorithm to determine frequencies of emotions for each year. This takes about three minutes. Downloading the nltk library takes about 10 minutes. 

The output file will be called emotions.csv

```
import nltk
nltk.download()
import nltk_ml_final
run nltk_ml_final
analyze_total_nonuniq = analyze_model("emotions.csv", result, 1, 1, None, True, False, True, False)
```
Here's what those inputs mean:

```
"emotions.csv" = csv file being created
result = dataframe being used as a comparison in the model
1 = level of analysis (1 for all content, 2 just for songs, 3 just for movies and books)
1 = model running (1 for bag of words, 2 for clustering)
None = number of clusters to be used (integer if model = 2)
True = stemmed tokens
False = keep unique tokens for a string
True = remove stopwords
False = no topic analysis included
```

#### Step 4: Get Events

Still in iPython3, pull events for the relevant years by running the following. This takes about three minutes.

The output file will be called final_events.csv

```
import wiki_data
run wiki_data
create_events_df(1945, 2017)
```

#### Step 5: Get a Website!

On the command line, navigate to the popsite directory and run the following commands to create an instance of the website.

```
cd popsite
python3 manage.py runserver
***add /popsents to the end of the URL in the web browser***
```

## Running Additional Models

The primary model is a bag of words that counts frequently occurring emotions in the summaries of top grossing movies, lyrics from songs in the Billboard Top 100, and abstracts from best-selling books for any given year.

We also developed an additional model: an unsupervised clustering model that attempted to cluster songs based on similarities that could be associated with emotions.

### Clustering model

To run this alternative model, follow these commands in place of Step 3 above.

```
import nltk
nltk.download()
import nltk_ml
run nltk_ml
analyze_total_nonuniq = analyze_model("emotions.csv", result, 1, 2, 8, True, False, True, False)
```
Please note this model does not cluster successfully, as the output does not vary much based on emotion.

## Topic Analysis 
```
analyze_total_nonuniq = analyze_model("emotions.csv", result, 1, 2, 8, True, False, True, False)
```
To run topic analysis, the last boolean parameter for the analyze_model command should be set to True. This will print out a message with the components of the topics on the terminal screen. Aditional parameters to change the defaults for number of words per topics and Vectorizing methods can be set as additional parameters as indicated in the header for the function on the .py file. 


## Authors

``` 
Cristina Mac Gregor -- worked on condensed_db and nltk_ml_final
Mario Moreno -- worked on condensed_db and nltk_ml_final
Hye Yeon Chang -- worked on popsite, wiki_data, visualizations
```

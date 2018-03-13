# PopCulture

This project uses a basic machine learning word count model to analyze popular culture in order to gauge sentiment over the last 50 years.

## Getting Started

These instructions will get you a copy of the project running on your local machine. 

###Step-by-Step Instructions

####Step 0: Get Installed

Make sure to install the following:

```
pip3 install sklearn
pip3 install nltk
pip3 install jellyfish
pip3 install django
pip3 install wikipedia
pip3 install xlrd
```

####Step 1: Get Git

Make sure to add the movies_metadata.csv file from dropbox and then pull all the necessary files into a new directory on your machine by running the following command.

```
git clone https://github.com/marioamz/PopCulture
```

####Step 2: Get Data
 
In iPython3, run the file called condensed_db to obtain a dataframe with books, songs, and movies. This takes about 15 seconds.

```
import condensed_db
run condensed_db
result = create_file()
```

####Step 3: Get Emotions

In iPython3, run our machine learning algorithm to output a new CSV file that returns frequencies of emotions for each year. This takes about three minutes.

The output file will be called emotions.csv

```
import nltk
nltk.download()
import nltk_ml
run nltk_ml
analyze_total_nonuniq = analyze_model("emotions.csv", result, 1, 1, None, True, False, True)
```

####Step 4: Get Events

Still in iPython3, pull events for the relevant years by running the following. This takes about three minutes.

The output file will be called final_events.csv

```
import wiki_data
run wiki_data
create_events_df(1945, 2017)
```

####Step 5: Get a Website!

On the command line, navigate to the popsite directory and run the following commands to create an instance of the website.

```
cd popsite
python3 manage.py runserver
add /popsents to the end of the URL
```




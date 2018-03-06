# import nltk and download all relevant packages
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import csv
import pandas as pd


primary_emotions = {"anticipation":["vigilance", "interest", "optimism", "aggressiveness", "anticipation"],
                    "anger":["rage", "annoyance", "aggressiveness", "contempt", "anger"],
                    "joy":["ecstasy", "serenity", "optimism", "love", "joy"],
                    "trust":["admiration", "acceptance", "love", "submission", "trust"],
                    "fear":["terror", "apprehension", "submission", "awe", "fear"],
                    "surprise":["amazement", "distraction", "awe", "disapproval", "surprise"],
                    "sadness":["pensiveness", "grief", "remorse", "disapproval", "sadness"],
                    "disgust":["loathing", "boredom", "contempt", "remorse", "disgust"]}


def create_csv(primary_emotions, emotion_d):
    '''
    Inputs emotion dictionary -> returns CSV
    Creates a CSV file that can be then linked to Django.
    '''

    #data = process_frame(primary_emotions, p_df)

    csvfile = open("test.csv", 'w')
    filewriter = csv.writer(csvfile, delimiter=",", quotechar=",")

    for year, sentiments in emotion_d.items():
        print(year)

        list_for_csv =[]
        list_for_csv.append(int(year))

        emotions, sent = sentiments
        top_e = sorted(emotions.items(), key = lambda x:-x[1])[:3]
        total = sum(emotions.values())

        for tup in top_e:
            emotion, freq  = tup
            freq = freq/total * 100
            list_for_csv.append(emotion)
            list_for_csv.append(freq)

            #move top 3 into columns

        order = ('compound', 'pos', 'neu', 'neg')
        for val in order:
            if val in sent:
                list_for_csv.append(sent[val])
            else:
                list_for_csv.append(0)

        filewriter.writerow((list_for_csv))


def process_frame(primary_emotions, p_df):
    '''
    Takes a dataframe. Using all observations corresponding to a given year,
    it will update a dictionary counting how many times words related to a
    given feeling show up..

    '''
    feels = synonyms(primary_emotions)
    d_year_feels = {}
    list_years = list(p_df.Year.unique())

    for i in list_years:

        yearly_df = p_df[(p_df.Year== i)]
        d_sents = sentiments(yearly_df)
        d_feels = {}
        for row in yearly_df.iterrows():
            process_text(row[1].Plot, feels, d_feels)
        d_year_feels[i] = (d_feels, d_sents)

    return d_year_feels


# def get_predominant(year_dict):
#     pred_feels = {}
#     for year in year_dict:
#
#         predominant = ""
#         mfreq = 0
#         for sent, freq in year.items():
#             if freq > mfreq:
#                 predominant = sent
#         pred_feels[year] = predominant
#
#     return d_year_feels, pred_feels


def process_text(target_text, feels, d_updt):
    '''
    Performs three basic steps:
    1. tokenize text.
    2. remove stopwords
    3. get frequency of feeling per text.
    '''
    if type(target_text) is str:
        list_words = tokenize(target_text)
        clean_list_w = rm_stopwords(list_words)
        basic_counts(clean_list_w, feels,  d_updt)


    else:
        return "as"

# FUNCTIONS TO MEASURE SENTIMENT INTENSITY

def sentiments(yearly_df):
    '''
    This function takes in a dataframe segregated by year. It
    pulls out the plot for each year, calculates it's sentiment
    using SentimentIntensityAnalyzer, aggregates sentiments for
    all plots in the year in question, and then takes the average
    of those figures.
    '''

    sent_dict = {}
    sentiment = {}
    sid = SentimentIntensityAnalyzer()

    for row in yearly_df.iterrows():
        if type(row[1].Plot) is str:
            ####
            tokenized = tokenize(row[1].Plot)
            no_stops = rm_stopwords(tokenized)
            plots = ' '.join(no_stops)

            sentiment = sid.polarity_scores(plots)

        for sent, score in sentiment.items():
            if sent not in sent_dict:
                sent_dict[sent] = score
            else:
                sent_dict[sent] += score

    for s, sc in sent_dict.items():
        sent_dict[s] = sc / len(yearly_df)

    return sent_dict


#FUNCTIONS TO CLEAN BASE FEELINGS
def synonyms(wrds):
    '''
    Returns a list of all synonyms
    '''
    synonyms = {}
    for primary, feeling in wrds.items():
        feelings_syn = []
        for f in feeling:
            for syn in wordnet.synsets(f):
                for lemma in syn.lemmas():
                    if f not in synonyms:
                        synonyms[primary] = feelings_syn
                        if lemma.name() not in feelings_syn:
                            feelings_syn.append(lemma.name())

    return synonyms

def add_stem_words(d_words):
    '''
    Generates a list with stem-words for the words in the synonym list for each
    feeling
    '''
    stems_f = {}
    lemmatizer = WordNetLemmatizer()
    for w, syn in d_words.items():
        for i in syn:
            # still unsure if this is the right loop
            if lemmatizer.lemmatize(i) not in syn:
                # this isn't working because you need to a positional
                # value to lemmatize (word, 'v')
                stems_f[i] = lemmatizer.lemmatize(i)
                # do we incorporate this into the broader dictionary here or later?
    return stems_f

# FUNCTIONS TO CLEAN PLOT

def tokenize(text):
    '''
    Takes a string and returns list of words used.
    '''
    t_words = word_tokenize(text)
    return t_words

def rm_stopwords(toks):
    '''
    to be applied with a loop to every plot item in dataframe. Given tokenized
    words, returns lists of tokens without stop words.

    '''
    clean_tokens = toks[:]

    stop_words = stopwords.words('english')
    for token in toks:
        if token in stop_words:
            clean_tokens.remove(token)

    return clean_tokens

def basic_counts(words_lst, syn, target_dict):
    '''
    This function tokenizes all the lyrics, and compares them to synonyms of
    our primal emotions
    '''
    for word in words_lst:
        for i, ls in syn.items():
            if word in ls:
                if i not in target_dict:
                    target_dict[i] = 0
                target_dict[i] +=1
                continue
    return target_dict

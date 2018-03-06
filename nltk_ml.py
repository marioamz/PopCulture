import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer


import sklearn
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import pandas as pd
import numpy as np
import condensed_db as cdb
import re

primary_emotions = {"anticipation":["vigilance", "interest", "optimism", "aggressiveness", "anticipation"],
                    "anger":["rage", "annoyance", "aggressiveness", "contempt", "anger"],
                    "joy":["ecstasy", "serenity", "optimism", "love", "joy"],
                    "trust":["admiration", "acceptance", "love", "submission", "trust"],
                    "fear":["terror", "apprehension", "submission", "awe", "fear"],
                    "surprise":["amazement", "distraction", "awe", "disapproval", "surprise"],
                    "sadness":["pensiveness", "grief", "remorse", "disapproval", "sadness"],
                    "disgust":["loathing", "boredom", "contempt", "remorse", "disgust"]}


def modeling(p_df, clusters, model = 1, stem = True, unique = True, nstopwords = True):
    '''
    Classifies in clusters.
    '''
    p_clean = p_df[p_df.Plot !=  None]
    p_clean = p_clean[p_df.Plot !=  "None"]
    p_clean = p_clean.dropna(axis = 0, how="any")
    p_clean.reset_index(inplace= True)
    plots = list(p_clean.Plot)

    #MODEL 1
    if model == 1:
        #VECTORIZING USING ALL AVAILABLE INFORMATION
        clust_labs = tfidf_km(plots, clusters)

        #print(m.groupby(['Clust']).Year.max())
        #print(m.groupby(['Clust']).Year.min())
        #print(m.groupby(['Clust']).Year.mean())
        #print(m.groupby(['Type']).Clust.mean())

    #MODEL 2
    if model == 2:
        #Did not work
        dict_feels = get_feelings_dict()
        l_feels = []
        for i in dict_feels:
            l_feels.append(i)
        #Can only pass on lists, 8 primary are not enough
        clust_labs = tfidf_km(plots, clusters, l_feels)

    #MODEL 3
    if model != 3:
        for inx, clust in enumerate(clust_labs):
            p_clean.loc[inx, "Clust"] = clust

    p_clean.loc[:, "Clean_tokens"] = ""
    for row in p_clean.iterrows():
        if type(row[1].Plot) is str:
            x = process_text(row[1].Plot, stem, unique, nstopwords)
            p_clean.at[row[0], "Clean_tokens"] = x

    return p_clean


def main8_frequencies(modeled_frame):
    '''
    Gets frequencies for each of the eight main feelings, given a particular
    dataframe
    '''
    feels_d = get_feelings_dict()

    main_8 = [["anticipation", 0, 0], ["anger", 0, 0], ["joy",0, 0],
            ["trust",0, 0],["fear", 0, 0],["surprise", 0, 0], ["sadness", 0, 0],
            ["disgust", 0, 0]]
    tot = 0
    for FEELING in main_8:
        for row in modeled_frame.iterrows():

            for i in row[1].Clean_tokens:
                if i in feels_d[FEELING[0]]:
                    FEELING[1] += 1
        tot += FEELING[1]
    for i in main_8:
        i[2] = (i[1] / tot) *100


    return sorted(main_8)


def analyze_model(comp_frame, clusters, model = 1, stem = True, unique = True, nstopwords = True):
    '''
    From a frame created by condensed_db.py, analyze_model does the following:
    1. Runs model returning frame with new columns: tokenized text, and cluster.
    2. Gets statistics for each cluster according to the songs classified as
        part of it
    3. Gets, for any given year, the predominant cluster, and its corresponding
        characteristics.

    Models:
    -Clustering vectorizing on a matrix using all content of the plots. We do so
    in order to contextualize each word and move beyond a bag of words approach.

    -Clustering vectorizing on lexicus only related to feelings.

    -Not clusterizing, getting general statistics per year. (bag of words
        approach)
    '''
    model_f = modeling(comp_frame, clusters, model, stem, unique, nstopwords)

    lst_freqs = []
    if model !=3:
        for i in range(clusters):
            temp = model_f[model_f.Clust == i]
            l = main8_frequencies(temp)
            lst_freqs.append((i, l))

    list_years = list(model_f.Year.unique())
    yr_d = {}
    for yr in list_years:
        yearly_df = model_f[(model_f.Year== yr)]

        if model !=3:
            most_freq_cluster = yearly_df.Clust.mode().loc[0]
            most_freq_cluster = float(most_freq_cluster)

            for stats in lst_freqs:
                if stats[0] == most_freq_cluster:
                    thisispryr = stats[1]
                    break

        elif model == 3:
            thisispryr = main8_frequencies(yearly_df)

        #Revise where we are getting sentiment per year to abstract and
        #avoid iterating twice in file.
        sent = sentiments(yearly_df)
        yr_d[yr] = (thisispryr, sent)
        #ADDITIONALLY, FOR YEAR, REGARDLESS OF MODEL, GETTING SENTIMENTS.

    return yr_d

def tfidf_km(plots, clusters, vocbs = None):
    '''
    We worked on process_text funciton, follow source for other parts of process.
    #add reference.
    '''
    tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=5000,
                                 min_df=0.2, use_idf=True,
                                 vocabulary = vocbs, tokenizer=process_text,
                                 ngram_range=(1,3))

    tfidf_matrix = tfidf_vectorizer.fit_transform(plots)

    dist = 1 - cosine_similarity(tfidf_matrix)

    km_model = KMeans(n_clusters=clusters)
    km_model.fit(tfidf_matrix)
    clusters = km_model.labels_.tolist()
    return clusters

#INCORPORATE TO ANALYZE MODEL
def sentiments(yearly_df):
    '''
    This function takes in a dataframe segregated by year. It
    pulls out the plot for each year, calculates it's sentiment
    using SentimentIntensityAnalyzer, aggregates sentiments for
    all plots in the year in question, and then takes the average
    of those figures.
    '''

    sent_dict = {}
    sid = SentimentIntensityAnalyzer()

    for row in yearly_df.iterrows():
        if type(row[1].Plot) is str:
            sentiment = sid.polarity_scores(row[1].Plot)

        for sent, score in sentiment.items():
            if sent not in sent_dict:
                sent_dict[sent] = score
            else:
                sent_dict[sent] += score

    for s, sc in sent_dict.items():
        sent_dict[s] = sc / len(yearly_df)

    return sent_dict

def process_text(text, stem = True, unique = True, nstopwords = True):
    '''
    '''
    text.lower()
    text = text.encode('ascii', 'ignore').decode('ascii')
    tokens = word_tokenize(text)
    if stem:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(t) for t in tokens]

    clean_tokens = tokens[:]
    stop_words = ["i", "me", "my", "myself", "we", "our,ours",
                  "ourselves","you", "your", "yours", "yourself", "yourselves",
                  "he", "him", "his", "himself", "she", "her", "hers",
                  "herself", "it", "its", "itself", "they", "them", "their",
                  "theirs", "themselves", "what", "which", "who", "whom",
                  "this", "that", "these", "those", "am", "is", "are", "was",
                  "were", "be", "been", "being", "doing", "a", "an", "the",
                  "and", "but","if", "or", "because", "as", "until", "while",
                  "of", "at", "by", "for", "with", "about", "against",
                  "between", "into", "through", "during", "before", "after",
                  "above", "below",  "to", "from", "up", "down", "in", "out",
                  "on", "off", "over", "under", "again", "further", "then",
                  "once", "here", "there", "when", "where", "why", "how", "all",
                  "any", "both", "each", "few", "more", "most", "other", "some",
                  "such", "only", "own", "same", "so", "than", "too", "very",
                  "s", "tm", "can", "will", "just", "don", "should", "now"]

                  #NLTK stopwords removed from stopword list:
                  #Have "have", "has", "had", "having", "do", "does", "did"
                  #"no", "nor", "not",

    if nstopwords:
        for token in tokens:
            if token in stop_words:
                clean_tokens.remove(token)
    if unique:
        clean_tokens = list(set(clean_tokens))
        return clean_tokens

    return clean_tokens

#NOT USED
def tokeize_frame(p_df, stem = True, unique = True, nstopwords = True):
    '''
    Takes a dataframe. Generates a new column with tokens with the following
    properties:
    -stem
    -uniques
    -nstopwords
    '''
    p_df.loc[:, "Clean_tokens"] = ""
    for row in p_df.iterrows():
        if type(row[1].Plot) is str:
            x = process_text(row[1].Plot, stem, unique, nstopwords)
            p_df.at[row[0], "Clean_tokens"] = x

    return p_df

#NOT USED
def get_allvocab(p_df):
    '''
    Gets all the potential words from all plots available.
    '''
    p_df.Plot.fillna("")
    x = vocab
    for row in p_df.iterrows():
        if type(row[1].Plot) is str:
            x = process_text(row[1].Plot, stem, unique, nstopwords)
            vocab.append(x)

    return vocab

def get_feelings():

    stemmer = PorterStemmer()
    feelings = synonyms(primary_emotions)
    feels = []
    for i, val in feelings.items():
        feels.append(stemmer.stem(i))
        for x in val:
            feels.append(stemmer.stem(x)
    total_feelings = list(set(feels))
    return total_feelings

def get_feelings_dict():
    stemmer = PorterStemmer()
    feelings = synonyms(primary_emotions)
    feelings_stemmed  = {}
    for i, val in feelings.items():
        feelings_stemmed[i] = [stemmer.stem(i)]
        for x in val:
            k  = stemmer.stem(x)
            feelings_stemmed[i] += [k]
        i = stemmer.stem(i)

    return feelings_stemmed

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

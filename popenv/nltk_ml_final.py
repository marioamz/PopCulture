import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import PorterStemmer

import sklearn
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.datasets import fetch_20newsgroups
import pandas as pd
import numpy as np
import condensed_db as cdb
import re
import csv

#Primary emotions dictionary maps basic 8 sentiments to those
#related to them by theory, according to topic analysis, and
#by analyzing the input data.

primary_emotions = {"anticipation":["vigilance", "interest", "optimism",
                        "aggressiveness", "anticipation", "worrisome",
                        "anxiety", "anxious", "paranoia" "paranoid",
                        "expectation", "nervous", "wait", "waiting"],
                    "anger":["rage", "annoyance", "aggressiveness", "contempt",
                        "anger", "havoc", "angry", "mad", "hell", "kill",
                        "vengeance", "revenge", "rogue", "rant", "trash",
                        "bitch"],
                    "joy":["ecstasy", "serenity", "optimism", "love", "joy",
                        "smile","heart", "sunshine", "warmth", "warm",
                        "rainbows","paradise", "bloom", "welcome", "friend",
                        "smile","cool", "inspire", "happy", "laugh",
                        "laughter","bliss", "fun", "beautiful", "awesome",
                        "dope","excitement"],
                    "trust":["admiration", "acceptance", "love", "submission",
                        "trust", "yours", "protection", "believe", "open",
                        "alright", "comfort", "friend", "cool", "team",
                        "strong", "strength"],
                    "fear":["terror", "apprehension", "submission", "awe",
                        "fear", "posttraumatic", "trauma", "traumatic",
                        "anxiety", "anxious", "nervous", "refuge",
                        "escap", "escape", "shook"],
                    "surprise":["amazement", "distraction", "awe",
                        "disapproval", "surprise", "wild", "bewild",
                        "believe", "unexpected", "shock",
                        "back", "strarstruck"],
                "sadness":["pensiveness", "grief", "remorse", "disapproval",
                        "sadness", "hurt", "forsaken" "emotionless",
                        "cry", "cri", "broken", "tear", "tears", "cloud",
                        "clouds", "cold", "blues", "blue", "gloom", "rain",
                        "goodbye", "numb", "die", "surrend", "kill", "death"
                        , "hunger", "wish"],
                    "disgust":["loathing", "boredom", "contempt", "remorse",
                        "disgust", "hell", "vomit", "nausea", "unacceptable"
                        ,"ugly", "nasty", "horrible", "naughty", "ew",
                        "ugh"]}

stop_words = ["i", "me", "my", "myself", "we", "our","ours",
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

COL_HEADERS = ["Year", "anticipation count","anticipation percentage",
        "anger count", "anger percentage", "joy count", "joy percentage",
        "trust count", "trust percentage", "fear count",
        "fear percentage", "surprise count", "surprise percentage",
        "sadness count", "sadness percentage",
        "disgust count", "disgust percentage", "compound", "pos", "neu",
        "neg"]

def analyze_model(csv_file, comp_frame, level = 1, model = 1, clusters = 8,
                        stem = True, unique = True, nstopwords = True, topics = True, ntopwords = 40, n_components = 10, n_features = 50000):
    '''
    From a frame created by condensed_db.py, analyze_model does the following:

    Gets the statistics per year according to the plots and in line with specified model with inputs.

    Inputs:
        -csv_file: (str) - name of output csv
        -comp_frame: (pandas dataframe) - Pandas df used for inputs.

        -level: (int) - level of analysis.
            - 1: All categories
            - 2: Only songs
            - 3: Only movies and books

        model: (int) - model ran for information about years.
            - 1: Getting general statistics per year. (bag of words
                    approach
            - 2: Clustering - vectorizing on a matrix using all content of the plots. We do so in order to contextualize each word and move beyond a bag of words approach. It gets the cluster mode per year and gets the statistics for that cluster as representative for the year. (UNSUCCESFUL APPROACH - CLUSTERS ARE TOO RANDOM)

        -clusters: (int) number of clusters to be used if model 1 is specified
        -stem: (boolean) True if we want stemmed tokens
        -unique: (boolean) True if we want to keep unique tokens for a string.
        -nstopwords: (boolean) True if we want to remove stopwords.

        -topics: (boolean) True if topic analysis is ran.
        -ntopwords: top words to show by topic (if topics)
        -n_components: number of topics (if topics).
        -n_features: number of features in CountVectorizer matrix (if topics).

    Outputs:
        -csv file with statistics per year according to the specified model
        -frame containing all the information from the model.
        -if topic analysis specified, message printed on scren.

    '''
    #Set CSV defaults.
    csvfile = open(csv_file, 'w')
    filewriter = csv.writer(csvfile, delimiter=",", quotechar=",")
    filewriter.writerow(COL_HEADERS)
    #Filter according to level
    feels_d = get_feelings_dict()

    if level != 1:
        if level == 2:
            comp_frame = comp_frame[(comp_frame.Type== "Song")]
        elif level == 3:
            comp_frame = comp_frame[(comp_frame.Type!= "Song")]

    #Complete frame with tokens per plot and cluster if specified.
    clean_f = updating_frame(comp_frame, clusters, model, stem, unique, nstopwords)

    if model == 2:
        lst_freqs = get_stats_perclust(clusters, clean_f, feels_d)

    #Get yearly stats and print on csv.
    list_years = list(clean_f.Year.unique())
    yr_d = {}

    for yr in list_years:
        if model ==  1:
            csv_list = compute_stats_list(clean_f, yr, model, feels_d)
        else:
            csv_list = compute_stats_list(clean_f, yr, model, feels_d, lst_freqs)

        filewriter.writerow(csv_list)

    #If topic analysis specified, print topics results on screen.
    if topics:
        topic = topic_analysis(clean_f, ntopwords, n_components, n_features)
        print(topic)

    return clean_f


def updating_frame(p_df, clusters, model = 1, stem = True, unique = True,
                nstopwords = True):
    '''
    Cleans and updates the dataframe with new variables needed for the analysis (tokens, feelings-related tokens, cluster (if model = 2))

    Inputs:
        -p_df
        -clusters: (int) number of clusters to be used if model 1 is specified
        -model (int)
        -stem: (boolean) True if we want stemmed tokens
        -unique: (boolean) True if we want to keep unique tokens for a string.
        -nstopwords: (boolean) True if we want to remove stopwords.

    Ouptuts: Updated dataframe
    '''
    #Making sure there are no None values in plot data
    p_clean = p_df[p_df.Plot !=  None]
    p_clean = p_clean[p_clean.Plot !=  "None"]
    p_clean = p_clean.dropna(axis = 0, how="any")
    p_clean.reset_index(inplace= True)
    plots = list(p_clean.Plot)


    p_clean.loc[:, "Clean_tokens"] = ""
    p_clean.loc[:, "Total_tokens"] = 0

    for row in p_clean.iterrows():
        if type(row[1].Plot) is str:
            x = process_text(row[1].Plot, stem, unique, nstopwords)
            p_clean.at[row[0], "Clean_tokens"] = x
            p_clean.at[row[0], "Total_tokens"] = len(x)

    #MODEL 2 CLUSTERS  #VECTORIZING USING ALL AVAILABLE INFORMATION

    if model == 2:

        p_clean.loc[:, "Clust"] = 0
        clust_labs = tfidf_km(plots, clusters)
        for inx, clust in enumerate(clust_labs):
            p_clean.loc[inx, "Clust"] = clust

    return p_clean

def compute_stats_list(frame, year, mdl, d, lst_freqs = None):
    '''
    Creates a list with the statistics for a given year.
    Inputs:
        frame: (pandas dataframe)
        year: (int) year to filter for.
        mdl: (int)model being specified
        lst_freqs: (list of tuples) list of frequencies per cluster (if model2)
    '''
    yearly_df = frame[(frame.Year== year)]

    if mdl == 1:
        freq_pyear, sent_intensity = sentiment_statistics(yearly_df, d)

    elif mdl == 2:
        most_freq_cluster = yearly_df.Clust.mode().loc[0]
        most_freq_cluster = float(most_freq_cluster)

        for stats in lst_freqs:
            if stats[0] == most_freq_cluster:
                freq_pyear, sent_intensity = stats[1], stats[2]
                break

    csv_list = [year]
    for i in freq_pyear:
        csv_list.append(i[1])
        csv_list.append(i[2])

    #ADDITIONALLY, FOR YEAR, REGARDLESS OF MODEL, GETTING SENTIMENTS.
    order = ('compound', 'pos', 'neu', 'neg')

    for val in order:
        if val in sent_intensity:
            csv_list.append(sent_intensity[val])
        else:
            csv_list.append(0)

    return csv_list

def get_stats_perclust(clusters, frame, d):
    lst_freqs = []
    for i in range(clusters):
        temp = frame[frame.Clust == i]
        l, s = sentiment_statistics(temp, d)
        lst_freqs.append((i, l, s))

    return lst_freqs

def sentiment_statistics(modeled_frame, d):
    '''
    Gets frequencies for each of the eight main feelings, considering all the observations in a given dataframe.

    Inputs: (frame) a pandas dataframe

    Output: (list) list of lists, one for each feeling, with three items in
            each:   item 0: name of feeling
                    item 1: number of counts for tokens related to given feeling.
                    item 2: percentage of words assigned to the feeling,    related to those assigned to other feelings.
    '''

    tot = 0
    feeling = 0
    sent_dict = None

    main_8_counts = [["anticipation", 0, 0], ["anger", 0, 0], ["joy",0, 0],
        ["trust",0, 0],["fear", 0, 0],["surprise", 0, 0], ["sadness", 0,0],
        ["disgust", 0, 0]]

    for FEELING in main_8_counts:
        for row in modeled_frame.iterrows():

            #Update feelings frequencies
            for i in row[1].Clean_tokens:
                if i in d[FEELING[0]]:
                    FEELING[1] += 1

            #Sentiment polarity: Only created in first loop
            if not sent_dict:
                plot = row[1].Plot
                sent_dict = sentiment_polarity(plot, len(modeled_frame))

        tot += FEELING[1]

    for i in main_8_counts:
        if tot !=0:
            i[2] = (i[1] / tot) * 100
        else:
            i[2] = 0

    return main_8_counts, sent_dict

def sentiment_polarity(plot, length):
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

    sentiment = sid.polarity_scores(plot)
    for sent, score in sentiment.items():
        if sent not in sent_dict:
            sent_dict[sent] = score
        else:
            sent_dict[sent] += score

    for s, sc in sent_dict.items():
        sent_dict[s] = sc / length

    return sent_dict

def tfidf_km(plots, clusters, vocbs = None):
    '''
    Creates a term-frequency inverse document frequency matrix weighting words for documents, and clusters all plots through a kmeans model.

    Inputs:
        - Plots: (list of strings)
        - Clusters: (int)
        - vocbs: list of vocabulary to be used in tfidf (if None, uses all vocabulary created by plots)

    Outputs:
        - list of clusters per document.

    Follows: http://brandonrose.org/clustering; Tokenizer tools are custion made and also follow SciKit documentation.

    '''
    tfidf_v = TfidfVectorizer(max_df=0.8, max_features=5000,
                                 min_df=0.05, use_idf=True,
                                 vocabulary = vocbs, tokenizer=process_text,
                                 ngram_range=(1,3))
    tfidf_matrix = tfidf_v.fit_transform(plots)

    #K means model
    km_model = KMeans(n_clusters=clusters)
    km_model.fit(tfidf_matrix)

    clusters = km_model.labels_.tolist()
    return clusters

def topic_analysis(p_df, ntopwords, n_components = 10, n_features = 50000 ):
    '''
    Given a dataframe and a number of words per topic specified, returns a string with topics obtained by a group of documents.
    Inputs:
        - p_df: (frame) Pandas dataframe.
        -topw: (int) Number of words to be returned in the topic string.
    Outputs: (str) topics.

    Following scikit documentation (LDA and CountVectorizer) - LDA topic extraction example by authors Olivier Grisel <olivier.grisel@ensta.org & Lars Buitinck & Chyi-Kwei Yau <chyikwei.yau@gmail.com>. Found in:  http://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html#sphx-glr-auto-examples-applications-plot-topics-extraction-with-nmf-lda-py

    '''
    plots = list(p_df.Plot)
    lda, featnames = tf_topwords(plots, ntopwords, n_components, n_features)
    tf_topics = get_message(lda, featnames, ntopwords)

    return tf_topics



def tf_topwords(plots, ntopwords, n_components = 10, n_features = 50000):
    '''
    Given a list of plots, number of topwords, components and maximum number of features, creates a matrix (which size will be equal or less to the number of features) that counts words used per document; models a LatentDirichletAllocation model, and returns list of topics used.


    Inputs:
        -plots (list of strings): "documnets" used for analysis.
        -ntopwords (int): words per topic in return message
        -n_components (int): Components for LatentDirichletAllocation
        -n_features (int): max size of matrix.

    Outputs: (object) LatentDirichletAllocation fitted model; -feature_names: (list) list of all vocabulary used in documents inputed for the LDA model.

    '''
    tf_v = CountVectorizer(max_features=20000,
                            analyzer = 'word', tokenizer = process_text)

    tf_matrix = tf_v.fit_transform(plots)
    featnames = tf_v.get_feature_names()

    #LDA model
    lda = LatentDirichletAllocation(n_components=n_components, max_iter=10,
                                    learning_method='online',
                                    learning_offset=50.,random_state=0)
    lda.fit(tf_matrix)

    return lda, featnames

def get_message(model, feature_names, n_top_words = 20):
    '''
    Takes an LDA modeled after a count matrix and a list of featured vocabulary and returns a string containing the main topics extracted by the LatentDirichletAllocation fit.

    Inputs:
        -model: (object) LatentDirichletAllocation fitted model
        -feature_names: (list) list of all vocabulary used in documents inputed for the LDA model.
        -n_top_words: (int) Number of words to be returned in the topic string.

    Outputs: (str) topics.
    '''

    message = ""
    for topic_idx, topic in enumerate(model.components_):
        message += " Topic #%d: " % topic_idx
        message += " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
    return message


def process_text(text, stem = True, unique = True, nstopwords = True):
    '''
    Takes a string and returns a list of corresponding clean tokens.

    Inputs:
        text: (str) text to be tokenized
        stem: (boolean) True if we want stemmed tokens
        unique: (boolean) True if we want to keep unique tokens for a string.
        nstopwords: (boolean) True if we want to remove stopwords.

    Outputs: (list) Clean tokens.

    '''
    text.lower()
    text = text.encode('ascii', 'ignore').decode('ascii')
    tokens = word_tokenize(text)
    if stem:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(t) for t in tokens]

    clean_tokens = tokens[:]

    if nstopwords:
        clean_tokens = rm_stopwords(clean_tokens)

    if unique:
        clean_tokens = list(set(clean_tokens))
        return clean_tokens

    return clean_tokens

def get_feelings_dict():
    '''
    Maps primary feelings to all its stemmed synonyms for all the related words to it.

    Inputs: (None) - map of feelings given as a global.
    Output: (dict) - Feelings dictionary.

    '''
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
    Returns a dictionary with all possible synonyms given a word and its corresponding lemmas.

    Inputs: (dict) - Feelings dictionary
    Returns: (dict) - Feelings dicionary extended with synonyms.

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

def make_list(dict_):
    '''
    Transforms a dict into a dictionary

    Inputs: (dict)
    Returns: (list)

    '''
    ls = []
    for i, x in dict_.items():
        if i not in ls:
            ls.append(i)
        if x not in ls:
            ls+=x
    return ls

def rm_stopwords(tokens):
    '''
    Removes stopwords specified in global list.

    Inputs: (list) Tokens
    Returns: (list) Filtered tokens

    '''
    clean_tokens = tokens[:]
    for token in tokens:
        if token in stop_words:
            clean_tokens.remove(token)

    return clean_tokens

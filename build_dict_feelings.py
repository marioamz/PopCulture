# import nltk and download all relevant packages
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd


# Robert Plutchik's 8 primary emotions and extensions
base_feelings = ['anger', 'anticipation', 'joy', 'disgust', 'sadness',
                'suprise', 'fear', 'trust', 'rage', 'loathing', 'grief',
                'amazement', 'terror', 'admiration', 'ecstasy', 'vigilance',
                'serenity', 'interest' 'annoyance', 'boredom', 'pensiveness',
                'distraction', 'apprehension' 'acceptance', 'optimism',
                'love', 'submission', 'awe', 'disapproval', 'remorse']


# sample lyric
lyric = "the beau brummels miscellaneous just a little just a little beau brummels ahhhhhhhhhhhhhhhhhhhhhhhh i cant stay yes i know you know i hate to go but goodbye love was sweet i was kind never mean so ill cry just a little cause i love you so and ill die just a little cause i have to go away cant you see how i feel when i say loves unreal so goodbye its been sweet even though incomplete so ill cry just a little cause i love you so and ill die just a little cause i have to go away instrumental interlude every night i still hear oh your sighs very near now its gone gone away as i once heard you say now ill cry just a little cause i love you so and ill die just a little cause i have to go away ahhhhhhhhhhhhhhhhhhhhhhhhh tmazanec1junocom or joy tom mazanec to humans"


'''
METHODOLOGY TO DECIDE:
    1. should we make a mega string per year and tokenize and clean that one
    2. OR get main feelings by song and decide check total frequencies

'''

def process_frame(base_feelings, p_df):
    '''
    Takes a dataframe. Using all observations corresponding to a given year,
    it will update a dictionary counting how many times words related to a
    given feeling show up.

    '''
    feels = synonyms(base_feelings)
    d_year_feels = {}
    list_years = list(p_df.Year.unique())

    for i in list_years:

        yearly_df = p_df[(p_df.Year== i)]
        d_feels = {}
        d_sents = {}
        for row in yearly_df.iterrows():
            process_text(row[1].Plot, feels, d_feels)
            #sentiments(row[1].Plot, d_sents)
        #print(i, d_feels)
        d_year_feels[i] = d_feels, d_sents

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

def sentiments(text, d_sts):
    
    sid = SentimentIntensityAnalyzer()
    
    if type(text) is str:
        sentiment = sid.polarity_scores(text)
    
    for sent, score in sentiment.items():
        if sent not in d_sts:
            d_sts[sent] = score
        else:
            d_sts[sent] += score
    
    return d_sts

#FUNCTIONS TO CLEAN BASE FEELINGS
def synonyms(wrds):
    '''
    Returns a list of all synonims
    '''
    synonyms = {}
    for feeling in wrds:
        feelings_syn = []
        for syn in wordnet.synsets(feeling):
            for lemma in syn.lemmas():
                if feeling not in synonyms:
                    synonyms[feeling] = feelings_syn
                if lemma.name() not in feelings_syn:
                    feelings_syn.append(lemma.name())

    return synonyms

def add_stem_words(d_words):
    '''
    Generates a list with stem-words for the words in the synonim list for each
    feeling
    '''
    stems_f = {}
    stemmer = PorterStemmer()
    for w, syn in d_words.items():
        for i in syn:
            if stemmer.stem(i) not in syn:
                stems_f[i] = stemmer.stem(i)
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

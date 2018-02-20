# import nltk and download all relevant packages
import nltk
nltk.download()
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize


# Robert Plutchik's 8 primary emotions and extensions
base_feelings = ['anger', 'anticipation', 'joy', 'disgust', 'sadness', \
'suprise', 'fear', 'trust', 'rage', 'loathing', 'grief', 'amazement', \
'terror', 'admiration', 'ecstasy', 'vigilance', 'serenity', 'interest' \
'annoyance', 'boredom', 'pensiveness', 'distraction', 'apprehension' \
'acceptance', 'optimism', 'love', 'submission', 'awe', 'disapproval' \
'remorse', '']

synonyms = {}

# sample lyric
lyric = "the beau brummels miscellaneous just a little just a little beau brummels ahhhhhhhhhhhhhhhhhhhhhhhh i cant stay yes i know you know i hate to go but goodbye love was sweet i was kind never mean so ill cry just a little cause i love you so and ill die just a little cause i have to go away cant you see how i feel when i say loves unreal so goodbye its been sweet even though incomplete so ill cry just a little cause i love you so and ill die just a little cause i have to go away instrumental interlude every night i still hear oh your sighs very near now its gone gone away as i once heard you say now ill cry just a little cause i love you so and ill die just a little cause i have to go away ahhhhhhhhhhhhhhhhhhhhhhhhh tmazanec1junocom or joy tom mazanec to humans"

for feeling in base_feelings:
    feelings_syn = []
    for syn in wordnet.synsets(feeling):
        for lemma in syn.lemmas():
            feelings_syn.append(lemma.name())
            if feeling not in synonyms:
                synonyms[feeling] = feelings_syn

# we're going to need to calculate jaro winkler scores
# on these feelings since they're not going to match
# exactly with what will be in lyrics, etc...
# or maybe we can use stemming like the below, or a combination of the two


# this function tokenizes all the lyrics, and compares them to synonyms of our primal emotions
words = word_tokenize(lyric)

for word in words:
    for primary, synonyms in synonyms.items():
        if word in synonyms:
            print(word)

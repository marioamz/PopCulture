# import nltk and download all packages
import nltk
nltk.download()

# Robert Plutchik's 8 primary emotions
base_feelings = ['anger', 'anticipation', 'joy', 'disgust', 'sadness', 'suprise', 'fear', 'trust']

synonyms = {}

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

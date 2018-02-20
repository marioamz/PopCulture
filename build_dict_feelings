# import nltk and download all packages
import nltk
nltk.download()

base_feelings = ['happy', 'sad', 'angry', 'scared']

synonyms = {}

for feeling in base_feelings:
    feelings_syn = []
    for syn in wordnet.synsets(feeling):
        for lemma in syn.lemmas():
            feelings_syn.append(lemma.name())
            if feeling not in synonyms:
                synonyms[feeling] = feelings_syn

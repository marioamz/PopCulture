# ORIGINAL
# DATA DUMP INTO SQL

from .models import *


EVENTS_FILENAME = '../final_events.csv'
MEDIA_FILENAME = '../final_media_df.csv'
RESULTS_FILENAME = '../emotions.csv'

def construct_db():
    '''
    Wipes out DB, Creates and Saves New Data Points
    '''

    Media.objects.all().delete()
    Event.objects.all().delete()
    TopSents.objects.all().delete()
    CompoundSents.objects.all().delete()

    create_event_table(EVENTS_FILENAME)
    create_media_table(MEDIA_FILENAME)
    create_sentiment_tables(RESULTS_FILENAME)


def create_event_table(filename):
    '''
    Creates and Saves Event Objects in DB
    '''
    
    df = pd.read_csv(filename, header=0,
                    names=['idx', 'year', 'month', 'event'],
                    index_col='idx')

    for idx, row in df.iterrows():
        event = Event(year=row.year, month=row.month, text=row.event)
        event.save()
    event.objects.filter(event='WWII:').delete()


def create_media_table(filename):
    '''
    Creates and Saves Media Objects in DB
    '''

    df = pd.read_csv(filename, header=0)
    df.Year = df.Year.apply(int)
    for i, row in df.iterrows():
        media = Media(year=row.Year, media_type=row.Type, title=row.Title, author=row.Author)
        media.save()


def create_sentiment_tables(filename):
    '''
    Creates and Saves TopSents, CompSents Objects in DB
    '''

    df = pd.read_csv(filename)
    df.Year = df.Year.apply(int)
    FEELS = ["anticipation", "anger", "joy", "trust", "fear",
             "surprise", "sadness", "disgust"]

    for i, row in df.iterrows():
        for f in FEELS:
            intense = "{} percentage".format(f)
            sent = TopSents(year=int(row.Year), emotion=f, intensity=row[intense])
            sent.save()
        c = CompoundSents(year=int(row.Year), compound=row['compound'],
                          positive=row.pos, neutral=row.neu, negative=row.neg)
        c.save()

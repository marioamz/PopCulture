from .models import *

########################
#  DATA DUMP INTO SQL  #
########################

EVENTS_FILENAME = '../all_events.csv'
MEDIA_FILENAME = '../final_media_df_UPDT.csv'
RESULTS_FILENAME = '../model_wordcounts_nonuniq.csv'

def construct_db():
    '''
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
    '''
    df = pd.read_csv(filename, header=0,
                    names=['idx', 'year', 'month', 'event'],
                    index_col='idx')

    for idx, row in df.iterrows():
        event = Event(year=row.year, month=row.month, text=row.event)
        event.save()


def create_media_table(filename):
    '''
    '''
    df = pd.read_csv(filename, header=0)
    df.Year = df.Year.apply(int)
    for i, row in df.iterrows():
        print(row.Year)
        media = Media(year=row.Year, media_type=row.Type, title=row.Title, author=row.Author)
        media.save()


def create_sentiment_tables(filename):
    '''
    '''
    df = pd.read_csv(filename)
    df.Year = df.Year.apply(int)
    FEELS = ["anticipation", "anger", "joy", "trust", "fear", "surprise", "sadness", "disgust"]

    for i, row in df.iterrows():
        for f in FEELS:
            intense = "{} percentage".format(f)
            sent = TopSents(year=int(row.Year), emotion=f, intensity=row[intense])
            sent.save()
        c = CompoundSents(year=int(row.Year), compound=row['compound'], positive=row.pos,
                      neutral=row.neu, negative=row.neg)
        c.save()

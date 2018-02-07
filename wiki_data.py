
# coding: utf-8

# ## Aggregating Major Events by Year Using Wikipedia Data
# - Uses the [Wikipedia](https://github.com/goldsmith/Wikipedia) python wrapper by Jonathan Goldsmith

# In[1]:


cd Wikipedia


# In[2]:


import wikipedia as wiki
import re
import pandas


# In[3]:


MONTHS = ['January', 'February', 'March', 'April',
          'May', 'June', 'July', 'August',
          'September', 'October', 'November', 'December']


# In[4]:


def get_all_events(start, end):
    '''
    Gathers list of all events for given date range
    Inputs: a pair of (integers)
    Returns:
        (list) of (tuples) of form (year, month, date)
    '''
    
    all_events = []
    for i in range(start, end + 1):
        year = str(i)
        all_events += get_year_month_events(year)
    return all_events

def get_year_month_events(year):
    '''
    Parses Wikipedia page for given year and creates a list of events
    Inputs:
        (string) of year
    Returns: 
        (list) of (tuple) of the form (year, month, event)
    '''

    page = wiki.WikipediaPage(title=year)
    content = page.content
    events = re.search("== Events ==(.|\n)*== Births ==", content).group()
    
    event_list = []
    for month in MONTHS:    
        lines = re.finditer("(({}) [0-9 ]*(–|-) )[^\n]*".format(month), events)
        for line in lines:
            actual_event = re.search("(–|-) .*", line.group(0)).group()[2:]
            event_list.append((year, month, actual_event))

    return event_list

### CURRENTLY NOT USING
def get_yearly_events(year):
    '''
    Parses Wikipedia page for given year and creates a list of events
    Inputs:
        (string) of year
    Returns: 
        (list) of (tuple) of the form (year, event)
    '''
    
    page = wiki.WikipediaPage(title=year)
    content = page.content
    events = re.search("== Events ==(.|\n)*== Births ==", content).group()
    lines = re.finditer("(({}) [0-9 ]*(–|-) )[^\n]*".format('|'.join(MONTHS)), events)
    event_list = []
    for line in lines:
        actual_event = re.search("(–|-) .*", line.group(0)).group()[2:]
        event_list.append((year, actual_event))
    
    return event_list


# In[5]:


events_data = get_all_events(1958, 1963)


# In[6]:


events_df = pandas.DataFrame(events_data, columns=['Year', 'Month', 'Event'])


# In[7]:


events_df[:10]


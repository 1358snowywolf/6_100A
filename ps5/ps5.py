# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    
    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

class PhraseTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger.lower()
    
    def is_phrase_in(self, text):
        updatedText = self.getRidOfPunctuation(text)
        
        firstIndex = updatedText.find(self.trigger)
        
        if(firstIndex == -1):
            return False
        
        if(firstIndex >= 1 and updatedText[firstIndex - 1] != ' '):
            return False
        
        finalIndex = firstIndex + len(self.trigger) - 1
        
        if(finalIndex < len(updatedText) - 1 and updatedText[finalIndex + 1] != ' '):
            return False
        
        return True
    
    #helper methods
    def getRidOfPunctuation(self, text):
        text = text.lower()
        
        for i in range (len(string.punctuation)):
            text = text.replace(string.punctuation[i], ' ')
        
        text = " ".join(tuple(text.split()))
        
        return text

# Problem 3

class TitleTrigger(PhraseTrigger):
    def evaluate(self, newsStory):
        return self.is_phrase_in(newsStory.get_title())

# Problem 4

class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, newsStory):
        return self.is_phrase_in(newsStory.get_description())

# TIME TRIGGERS

# Problem 5
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self, time):
        #12 Oct 2016 23:59:59
        self.date = datetime.strptime(time, "%d %b %Y %H:%M:%S")
        self.date = self.date.replace(tzinfo=pytz.timezone("EST"))

# Problem 6

class BeforeTrigger(TimeTrigger):
    def evaluate(self, newsStory):
        local_time = newsStory.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
        return self.date > local_time

class AfterTrigger(TimeTrigger):
    def evaluate(self, newsStory):
        local_time = newsStory.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
        return self.date < local_time

# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, other_trigger):
        self.trigger = other_trigger
        
    def evaluate(self, newsStory):
        return not self.trigger.evaluate(newsStory)
    
# Problem 8

class AndTrigger(Trigger):
    def __init__(self, other_trigger, other_other_trigger):
        self.trigger1 = other_trigger
        self.trigger2 = other_other_trigger

    def evaluate(self, newsStory):
        return self.trigger1.evaluate(newsStory) and self.trigger2.evaluate(newsStory)

# Problem 9

class OrTrigger(Trigger):
    def __init__(self, other_trigger, other_other_trigger):
        self.trigger1 = other_trigger
        self.trigger2 = other_other_trigger

    def evaluate(self, newsStory):
        return self.trigger1.evaluate(newsStory) or self.trigger2.evaluate(newsStory)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    
    triggeredStories = []
    
    for i in stories:
        for j in triggerlist:
            if(j.evaluate(i)):
                triggeredStories.append(i)
                break
    
    return triggeredStories

#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    triggerList = {}
    finalTriggerList = []
    
    for currentLine in lines:
        if(currentLine == ""):
            continue
        
        if(currentLine[0] == '/' and currentLine[1] == '/'):
            continue
        
        commands = currentLine.split(',')
        
        if(commands[0] == "ADD"):
            for triggerName in commands:
                if(triggerName == "ADD"):
                    continue
                
                finalTriggerList.append(triggerList[triggerName])
        else:
            triggerType = commands[1]
            
            if(triggerType == "TITLE"):
                value = DescriptionTrigger(commands[2])
                triggerList[commands[0]] = value
            elif(triggerType == "DESCRIPTION"):
                value = TitleTrigger(commands[2])
                triggerList[commands[0]] = value
            elif(triggerType == "AFTER"):
                value = AfterTrigger(commands[2])
                triggerList[commands[0]] = value
            elif(triggerType == "BEFORE"):
                value = BeforeTrigger(commands[2])
                triggerList[commands[0]] = value
            elif(triggerType == "NOT"):
                currentTrigger = triggerList[commands[2]]
                value = NotTrigger(currentTrigger)
                triggerList[commands[0]] = value
            elif(triggerType == "AND"):
                currentTrigger1 = triggerList[commands[2]]
                currentTrigger2 = triggerList[commands[3]]
                value = AndTrigger(currentTrigger1, currentTrigger2)
                triggerList[commands[0]] = value
            elif(triggerType == "OR"):
                currentTrigger1 = triggerList[commands[2]]
                currentTrigger2 = triggerList[commands[3]]
                value = OrTrigger(currentTrigger1, currentTrigger2)
                triggerList[commands[0]] = value
            else:
                print("Congratulations! You reached the unreachable line!")
                return None

    # print(lines) # for now, print it so you see what it contains!
    return finalTriggerList


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    # root = Tk()
    # root.title("Some RSS parser")
    # t = threading.Thread(target=main_thread, args=(root,))
    # t.start()
    # root.mainloop()
    
    triggerList = read_trigger_config("triggers.txt")
    print((triggerList))
    pass
    


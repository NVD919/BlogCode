import string
import time
import operator
import dateutil.parser as dateparser
from sklearn.feature_extraction.text import TfidfVectorizer

lines = open('2015-08-01.txt').read().splitlines();       # Load the file to study
corpus = [];                                              # Will store the messages
counter = {};                                             # Count the number of posts per user (this is a dictionary)
oncecorpus = {};                                          # Dictionary to store the messages for those who post only once

for l in lines:
   j = [word for word in l.split()]                       # Extract words from the message

   usr = j[3][:-1];                                       # The user is always the fourth word, take off the trailing semicolon

   # The following stores time information (was not used for the blug post)
   #tstamp = j[0].strip(string.punctuation)+" "+j[1].strip(string.punctuation);
   #dt = dateparser.parse(tstamp)
   #timestamp = int(time.mktime(dt.timetuple()))

   s = " ";
   toAppend = s.join(j[4:]);                              # Extract the message, and turn words back into a string
   corpus.append((usr,toAppend));                         # Corpus will store user and the message

   if usr in counter:                                     # Check if the user is already in the dictionary
      counter[usr] += 1;                                  # Increase number of messages by 1
      if(counter[usr]==2):                                # Delete multiple message people from oncecorpus
         del oncecorpus[usr];
   else:                                                  # User is not in the dictionary
      counter[usr] = 1;                                   # Add the user to dictionary with one post
      oncecorpus[usr] = toAppend;                         # Store the one message in oncecorpus
 
#manycorpus = [];                                         # Will store messages for people who post many times
#distinctppl = {};                                        # This will store users who post many times

#for c in corpus:                                         # Loop through all messsages
#   if(counter[c[0]]>=10):                                # Did they post more than 10 posts?
#      manycorpus.append(c[1]);                           # Add message to manycorpus
#      distinctppl[c[0]] = True;                          # Add user to the dictionary (does nothing if user already there)

#ucorpus = [];                                            # Will store messages that reference a user
#for j in range(len(corpus)):                             # Loop through all messages
#   for u in counter.keys():                              # Loop through all users
#      if(u.lower() in corpus[j][1].lower()):             # Is the user in the message?
#         ucorpus.append(corpus[j][1]);                   # Append the message to the list
#         break;

#print len(ucorpus)                                       # How many of those posts were there?

profanity = open('bad.csv').read().splitlines();          # Load up profanity list

ucorpus = [];                                             # Will store messages with profanity
for j in range(len(corpus)):                              # Loop through all messages
   for u in profanity:                                    # Loop through all profane words
      if(u.lower() in corpus[j][1].lower()):              # Is the word in the message?
         ucorpus.append(corpus[j][1]);                    # Append the message to the list
         break;

print len(ucorpus)                                        # How many of those posts were there?

# Use scikit-learn's implementation of tf-idf, we allow for single words and two word phrases
vectorizer = TfidfVectorizer(min_df=5, max_df = 0.5,sublinear_tf=True,use_idf=True,stop_words='english',ngram_range=(1,2))
X = vectorizer.fit_transform(ucorpus);

# Sort and print the vocabulary by tf-idf score
lfreqs = [(word, X.getcol(idx).sum()) for word, idx in vectorizer.vocabulary_.items()]
lfreqs = sorted (lfreqs, key = lambda x: -x[1]);

for l in lfreqs:
   print l

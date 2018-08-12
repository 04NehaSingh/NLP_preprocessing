__author__ = "Nehas"
# coding: utf-8

####################################
# # # Cleaning junks from dataset
####################################

import pandas as pd
import re

#1. Load the dataset into dataframe df
df = pd.read_csv("input_file.csv")
pd.options.display.max_colwidth = 100

print(df.head(10))
print('\ntotal entries =' +str(df.shape))

column_name = (df.columns.values)
print(column_name)


#2. creating a copy of original df_cpy for manipulation 
df_cpy = df.copy()
df_cpy.rename(columns=lambda x: x.strip(), inplace=True)

# Create an empty datafame df_new for updating with new value
# df_new = pd.DataFrame(columns=column_name)
# print(df_new.shape)

#dropping unnecessary columns and rows
df_cpy = df_cpy.drop(df_cpy.columns[[5, 6]], axis=1) 
df_cpy = df_cpy.dropna()

#drop unnecessary rows:
#df_cpy = df_cpy.drop(df_cpy[df_cpy.Tag== 'col1_name'].index)
#df_cpy = df_cpy.drop(df_cpy[df_cpy.Tag == 'col2_name'].index)

#print('\ntotal entries =' +str(df_cpy.shape))

# sorting 
df_cpy = df_cpy[df_cpy['issueType']=="Defect"]
print(df_cpy.head(10))
print('\ntotal entries =' +str(df_cpy.shape))


# merging 2 cols into new one 
# df_cpy['summary_description'] = df_cpy['summary'].astype(str) + df_cpy['description']
# print(df_cpy['summary_description'].head(100))


# A list of contractions from http://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python
contractions = { 
"ain't": "am not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he's": "he is",
"how'd": "how did",
"how'll": "how will",
"how's": "how is",
"i'd": "i would",
"i'll": "i will",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'll": "it will",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"must've": "must have",
"mustn't": "must not",
"needn't": "need not",
"oughtn't": "ought not",
"shan't": "shall not",
"sha'n't": "shall not",
"she'd": "she would",
"she'll": "she will",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"that'd": "that would",
"that's": "that is",
"there'd": "there had",
"there's": "there is",
"they'd": "they would",
"they'll": "they will",
"they're": "they are",
"they've": "they have",
"wasn't": "was not",
"we'd": "we would",
"we'll": "we will",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"where'd": "where did",
"where's": "where is",
"who'll": "who will",
"who's": "who is",
"won't": "will not",
"wouldn't": "would not",
"you'd": "you would",
"you'll": "you will",
"you're": "you are"
}


#3. iterate the row of df_cpy, clean it and save it into df_new
# Cleaning : to_lower

import csv
import string
import wordninja
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 

#clean emojis
def clean_emoji(sen): 
    sen = ''.join(c for c in sen if c <= '\uFFFF')
    return sen.replace("  ", " ")

#further cleaning
def clean(sen,remove_stopwords = True, contraction = True, pun= True,lemma_= True):

    sen = re.sub(r'https?:\/\/.*[\r\n]*', '', sen, flags=re.MULTILINE)
    sen = re.sub(r'\<a href', ' ', sen)
    sen = re.sub(r'&amp;', '', sen) 
    sen = re.sub(r'[_"\-;%()|+&=*%.,!?:#$@\[\]/]', ' ', sen)
    sen = re.sub(r'<br />', ' ', sen)
    sen = re.sub(r"[:()]", "", sen) #remove () 
    sen = re.sub('\s+$|^\s+', '', sen) #remove whitespace from start of the line and end of the line
    sen = re.sub(r'[^\x00-\x7f]', r'', sen) #a single character in the range between  (index 0) and  (index 127) (case sensitive)
    sen = sen.strip(""" '!:?-_().,'"[]{};*""")
    sen = ' '.join([w.strip(""" '!:?-_().,'"[]{};*""") for w in re.split(' ', sen)])
   
    # spliting words
    string = []
    for x in sen.split():
        if len(x)>6:
            for i in wordninja.split(x):
                if len(i)>2:
                    string.append(i)
        else:
            string.append(x)
    sen = " ".join(string)
    
    contraction  
    new_text = []
    for word in sen.split():
        if word in contractions:
            new_text.append(contractions[word])
        else:
            new_text.append(word)
    sen = " ".join(new_text)

    sen = re.sub(r"[^A-Za-z0-9:(),\'\`]", " ", sen)
    sen = re.sub(r"\b\d+\b", "", sen)  #remove numbers 
    sen = re.sub('\s+',  ' ', sen) #matches any whitespace characte
    sen = re.sub(r'(?:^| )\w(?:$| )', ' ', sen).strip() #removing single character
   
     # Optionally, remove stop words
    if remove_stopwords:
        sen = " ".join([i for i in sen.split() if i not in stop])
       
    # Optionally emove puncuations 
    if pun:
        sen = ''.join(ch for ch in sen if ch not in exclude)
    
    # Optionally lemmatiztion  
    if lemma_:
        normalized = " ".join(WordNetLemmatizer().lemmatize(word) for word in sen.split())        
        
    return sen.strip().lower()

# Cleaning the dataset 
clean_data = []
for index, row in df_cpy['description'][:10].iteritems():
    row = clean_emoji(str(row))
    row = clean(row,remove_stopwords=False)
    #print(row)
    clean_data.append(row)

#print(df_cpy['description'][:50])


# Inspect the cleaned summaries and texts to ensure they have been cleaned well
for i in range(10):
    print("Clean Review #",i+1)
    print(clean_data[i])
    print()


# 4 saving the dataset 
df2 = pd.DataFrame(data={'description':clean_data})
print(df2)
df2.to_csv("cleaned_data.csv", index=False , encoding='utf-8')
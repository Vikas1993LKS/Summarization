# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 12:45:42 2021

@author: Vikas.gupta
"""

import nltk
import os
import re
import math
import operator
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.stem.porter import PorterStemmer
import spacy
import json
nlp = spacy.load('en_core_web_sm')
Stopwords = set(stopwords.words('english'))
wordlemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
from Legislation_Generator import entityextraction


def lemmatize_words(words):
    lemmatized_words = []
    for word in words:
       lemmatized_words.append(wordlemmatizer.lemmatize(word))
    return lemmatized_words
def stem_words(words):
    stemmed_words = []
    for word in words:
       stemmed_words.append(stemmer.stem(word))
    return stemmed_words
def remove_special_characters(text):
    regex = r'[^a-zA-Z0-9\s]'
    text = re.sub(regex,'',text)
    return text
def freq(words):
    words = [word.lower() for word in words]
    dict_freq = {}
    words_unique = []
    for word in words:
       if word not in words_unique:
           words_unique.append(word)
    for word in words_unique:
       dict_freq[word] = words.count(word)
    return dict_freq
def pos_tagging(text):
    pos_tag = nltk.pos_tag(text.split())
    pos_tagged_noun_verb = []
    for word,tag in pos_tag:
        if tag == "NN" or tag == "NNP" or tag == "NNS" or tag == "VB" or tag == "VBD" or tag == "VBG" or tag == "VBN" or tag == "VBP" or tag == "VBZ":
             pos_tagged_noun_verb.append(word)
    return pos_tagged_noun_verb
def tf_score(word,sentence):
    freq_sum = 0
    word_frequency_in_sentence = 0
    len_sentence = len(sentence)
    for word_in_sentence in sentence.split():
        if word == word_in_sentence:
            word_frequency_in_sentence = word_frequency_in_sentence + 1
    tf =  word_frequency_in_sentence/ len_sentence
    return tf
def idf_score(no_of_sentences,word,sentences):
    no_of_sentence_containing_word = 0
    for sentence in sentences:
        sentence = remove_special_characters(str(sentence))
        sentence = re.sub(r'\d+', '', sentence)
        sentence = sentence.split()
        sentence = [word for word in sentence if word.lower() not in Stopwords and len(word)>1]
        sentence = [word.lower() for word in sentence]
        sentence = [wordlemmatizer.lemmatize(word) for word in sentence]
        if word in sentence:
            no_of_sentence_containing_word = no_of_sentence_containing_word + 1
    idf = math.log10(no_of_sentences/no_of_sentence_containing_word)
    return idf
def tf_idf_score(tf,idf):
    return tf*idf
def word_tfidf(dict_freq,word,sentences,sentence):
    word_tfidf = []
    tf = tf_score(word,sentence)
    idf = idf_score(len(sentences),word,sentences)
    tf_idf = tf_idf_score(tf,idf)
    return tf_idf
def sentence_importance(sentence,dict_freq,sentences):
     sentence_score = 0
     sentence = remove_special_characters(str(sentence)) 
     sentence = re.sub(r'\d+', '', sentence)
     pos_tagged_sentence = [] 
     no_of_sentences = len(sentences)
     pos_tagged_sentence = pos_tagging(sentence)
     for word in pos_tagged_sentence:
          if word.lower() not in Stopwords and word not in Stopwords and len(word)>1: 
                word = word.lower()
                word = wordlemmatizer.lemmatize(word)
                sentence_score = sentence_score + word_tfidf(dict_freq,word,sentences,sentence)
     return sentence_score


def summary_generator(list1):
    for file_name in list1:
        legal_entities = []
        legislation_entities = []
        text = ""
        legal_entities_cleaned = ""
        regular_expression = re.compile(r'^([\d]+\.?\)?([\d]+\.?\)?)?)$', re.IGNORECASE)
        #file = open(file_name, 'r', encoding = "utf-8")
        with open(file_name, 'rb') as fp:
            json_text = json.load(fp)
        sentence = ""
        for value in json_text:
            if (regular_expression.search(value['Line_Data']['Value'].strip())):
                pass
            elif (value['Line_Data']['leftpoint_x'] < 210):
                sentence =  sentence + value['Line_Data']['Value'].replace("\n", " ") 
        filename = file_name.split("\\")[-1]
        print (filename)
        # text_original = file.read()
        text = re.sub('  +', " ", sentence)
        text_1 = text.replace("Ld.", "Ld").replace("w.e.f.", "with effective from").replace("Ors.", "others").replace("viz.", "viz").replace("i.e.", "ie").replace("Anr.","another").replace("ors.", "others").replace("anr.","another").replace("Sq. ft,", "square feet").replace("u/s.", "under section").replace("r.w.r.", "read with rule").replace("Pr.", "Pr").replace("addl. CIT", "additional commisioner of income tax").replace("ld.", "ld").replace("Nos.", "numbers").replace("nos.", "numbers").replace("no.", "number").replace("No.", "Number").replace("Sh.", "Shri").replace("Inv.", "Invested").replace("Del.", "Delhi").replace("Bom.", "Bombay").replace("Smt.", "Shri Mati").replace("A.Y.", "Annual Year").replace("F.Y.", "Financial Year").replace("D.R.", "DR").replace("Pvt.", "private").replace("pvt.", "private").replace("ltd.", "limited").replace("Sec.", "Section").replace("I.T.", "Income Tax").replace("A.O.", "Assesse Officer").replace("r.w.s." , "read with section").replace("Vs.", "Vs").replace("Id.", "Id").replace("i.e.", "").replace("Rs.", "Rupees ").replace("ltd.", "limited").replace("Ltd.", "limited").replace("M/s.", "M/s").replace("O/o.", "O/o").replace("u/s", "under section").replace("U/S", "under section").replace("M/S.", "M/S").split("Sd/-")[0]
        tokenized_sentence = sent_tokenize(text_1)
        #text = remove_special_characters(str(text_1))
        print (len(tokenized_sentence))
        #print (text)
        legislation_entities = entityextraction(str(text))
        print (legislation_entities)
        for values in legislation_entities:
            if (values['Txt'].replace("  "," ").strip() not in legal_entities and "rule" in values['Txt'].lower() or "ita " in values['Txt'].lower()  or "act" in values['Txt'].lower() or "notification" in values['Txt'] or "section" in values['Txt'].lower() or "article" in values['Txt'].lower()) and len(values['Txt']) < 60:
                legal_entities.append(values['Txt'].replace("  "," ").strip())
        legal_entities_cleaned = "\n".join(legal_entities)
        text = re.sub(r'\d+', '', text)
        tokenized_words_with_stopwords = word_tokenize(text)
        tokenized_words = [word for word in tokenized_words_with_stopwords if word not in Stopwords]
        tokenized_words = [word for word in tokenized_words if len(word) > 1]
        tokenized_words = [word.lower() for word in tokenized_words]
        tokenized_words = lemmatize_words(tokenized_words)
        word_freq = freq(tokenized_words)
        if len(tokenized_sentence) > 350:
            input_user = 10
        elif 350 > len(tokenized_sentence) > 250:
            input_user = 15
        elif 250 > len(tokenized_sentence) > 150:
            input_user = 20
        else:
            input_user = 30
        no_of_sentences = int((input_user * len(tokenized_sentence))/100)
        print(no_of_sentences)
        c = 1
        #print (text_1)
        sentence_with_importance = {}
        #spacy_tokenization = nlp(text_1).sents
        #print (tokenized_sentence)
        #print ("----------------------Spacy Tokenization----------------------")
        #print (spacy_tokenization)
        #for i, sentence in enumerate(nlp(text_1).sents):
            #print("Sentence %d: %s" % (i, sentence.text))
        Sentence_test = ""
        for sent in tokenized_sentence:
                digit_list = re.findall(r'(\d+(,)?\d+)', sent)
                if (len(digit_list) < 10) and "INCOME TAX APPELLATE TRIBUNAL" not in sent and "BEFORE SHRI JUSTICE" not in sent:
                    Sentence_test = Sentence_test + "Sentence: " + sent + "\n"
                    sentenceimp = sentence_importance(sent,word_freq,tokenized_sentence)
                    sentence_with_importance[c] = sentenceimp
                    c = c+1
        with open(locationofjson + "/" + filename + "sentence.txt", "w", encoding="utf-8") as f:
            f.write(Sentence_test)
        sentence_with_importance = sorted(sentence_with_importance.items(), key=operator.itemgetter(1),reverse=True)
        cnt = 0
        summary = []
        sentence_no = []
        for word_prob in sentence_with_importance:
            if cnt < no_of_sentences:
                sentence_no.append(word_prob[0])
                cnt = cnt+1
            else:
              break
        sentence_no.sort()
        cnt = 1
        for sentence in tokenized_sentence:
            if cnt in sentence_no:
                summary.append(sentence)
            cnt = cnt+1
        summary = " ".join(summary)
        legal_entities_cleaned = "Legal_Entities" + "\n" + legal_entities_cleaned.lower().replace("u / s", "under section") + "\n"
        if len(legal_entities_cleaned.strip()) != 0:
            summary_final = legal_entities_cleaned + "\n" + "Summary" + "\n" + "\n" + summary
            with open(locationofjson + "/" + filename + '_summary.txt',"w", encoding = "utf-8") as f:
                f.write(summary_final)


list1 = []
def PDFLocation(pathofPDF):
    for dirpath, dirname, filenames in os.walk(pathofPDF):
        for file in filenames:
            try:
                #if file.lower().endswith(".txt") and "paragraph" not in file.lower():
                if file.lower().endswith(".json"):
                    path = os.path.abspath(os.path.join(dirpath, file))
                    list1.append(path)
                else:
                    continue
            except (FileNotFoundError, IOError):
                print("runtime exception")
    
locationofpdf = input("Please enter the location of input pdf :\n")
locationofjson = input("Please enter the location of output JSON :\n")
PDFLocation(locationofpdf)

summary_generator(list1)
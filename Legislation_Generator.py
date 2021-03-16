# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 17:37:46 2020

@author: Aditya
"""


from flair.models import SequenceTagger
from flair.data import Sentence
import re

tagger = SequenceTagger.load("ner-ontonotes-fast")


FileName = []
Sections = []


def entityextraction(text):
    # for i in list1:
    #     Starting_Ending_Index = []
    #     Spacy_Data = []
    #     with open(i, "rb") as f:
    #         jsonfilename = i.split("\\")[-1]
    #         print (jsonfilename)
    #         data = json.load(f)
    #         for j in range(len(data)):
    #             starting_position = 0
    #             ending_position = 0
    #             starting_text = ""
    #             text = data[j]["Paragraph_data"]["paragraph_value"]
    #             #                data = text.split("\\r\\n")
                starting_position = 0
                ending_position = 0
                starting_text = ""
                Starting_Ending_Index = []
                starting_string = "<B-LAW>"
                text = re.sub(r"(Page\s\d\sof\s\d+)", "", text)                       
                sentence = Sentence(text)
                tagger.predict(sentence)
                tagged_data = sentence.to_tagged_string()
                links = re.findall(
                    r"((<B-LAW>)(.+?)(<E-LAW>))",
                    tagged_data,
                )
                #links = [(tuple(str(x) if len(x.strip())>0 else x for x in _ if x)) for _ in links]
                for link in links:
                        link_text = sentence.to_tagged_string().split(" ")
                        for i in range(len(link_text)):
                            if link_text[i] == starting_string:
                                if link[0].split(" ")[0] == link_text[i]:
                                    if i > starting_position and i > ending_position:
                                        starting_position = i
                                        starting_text = link_text[i-1]
                                        break
                        Start_End_Index = {
                                "Txt": re.sub(
                                    r"<.*?>",
                                    "",
                                    starting_text + link[0],
                                    ).strip()
                                }
                        Starting_Ending_Index.append(Start_End_Index)
                return Starting_Ending_Index
import csv
import os
import re
import html as ihtml
import re

import pandas as pd
from bs4 import BeautifulSoup

input_dir = '/Users/jarman/PycharmProjects/QnA/data/'

stackoverflow_row_data = pd.read_csv(os.path.join(input_dir, 'stackoverflow.csv'))
collected_row_data = pd.read_csv(os.path.join(input_dir, 'javafqs.csv'))
merged_data = pd.concat([stackoverflow_row_data, collected_row_data])


# print(collected_row_data.tail())
# nothing here
# sample_text = stackoverflow_stackoverflow_row_data.loc[425,"abody"]
# print(sample_text)


def clean_text(text):
    text = BeautifulSoup(ihtml.unescape(text), "lxml").text
    text = re.sub(r"http[s]?://\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    text = text.replace("'", "").replace('"', '').replace("\\", "")
    # text = re.escape(text)
    return text


answers = collected_row_data.loc[~collected_row_data["abody"].isnull(), "abody"].apply(clean_text)
questions = collected_row_data.loc[~collected_row_data["qbody"].isnull(), "qbody"].apply(clean_text)
print((answers.tail()))
answers2 = stackoverflow_row_data.loc[~stackoverflow_row_data["abody"].isnull(), "abody"].apply(clean_text)
questions2 = stackoverflow_row_data.loc[~stackoverflow_row_data["qbody"].isnull(), "qbody"].apply(clean_text)
print(answers2.tail())
with open(input_dir + 'cleaned_data.csv', 'w') as csvfile:
    fieldnames = ['title', 'paragraphs']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for rows in questions2.index:
        writer.writerow({'title': questions2[rows], 'paragraphs': "['" + answers2[rows] + "']"})

    for row in questions.index:
        writer.writerow({'title': questions[row], 'paragraphs': "['" + answers[row] + "']"})

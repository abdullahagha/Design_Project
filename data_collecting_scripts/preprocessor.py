import re
import string
import pickle
import os
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize


#Parse the translate file inside the translates_path directory to the output_path directory
def parse_raw_translates(translates_path, output_path):
    file_number = 1
    
    for directory_name in os.listdir(translates_path):
        translate_file_name = os.listdir(os.path.join(translates_path, directory_name))[0]
        film_rating = directory_name.split("_")[0]
        print(film_rating)

        read_file = open(os.path.join(translates_path, directory_name, translate_file_name), encoding = "utf-8", errors="ignore")
        write_file = open(os.path.join(output_path, film_rating + "_" + str(file_number)), "w")
        file_number +=1

        write_buffer = ""
        lines_count = 0
        lines = []

        for line in read_file:
            line=str(line)
            if line[0] == '\n':
                for i, already_read_lines in enumerate(lines):
                    if i != 0 and i !=1:
                        already_read_lines = already_read_lines.split('\n')[0]
                        write_buffer = write_buffer + already_read_lines
                        write_buffer = write_buffer + " "

                lines = []
            else:
                lines.append(line)

        write_file.write(write_buffer)

        read_file.close()
        write_file.close()

def clean_text(text):
    """
    Remove "(strings)" or "<string>" from text file.
    """
    regex = re.compile('(<.*?>)|(\(.*?\))')
    cleantext = re.sub(regex, '', text)
    return cleantext


def clean_tokens(tokens_list):
    """
    General purpose tokens cleaning function.
    Note : The order of the functions is important.
    """

    #To lowercase
    cleaned_tokens = [token.lower() for token in tokens_list]

    #Remove numbers, punctuation marks or words contains non-characters like "don`t"
    cleaned_tokens = [token for token in cleaned_tokens if token.isalpha()]

    #Remove stop words
    stop_words = set(stopwords.words('english'))
    cleaned_tokens = [token for token in cleaned_tokens if not token in stop_words]

    #Remove words with one character
    cleaned_tokens = [token for token in cleaned_tokens if len(token) > 1]

    """ #Words stemming
    porter = PorterStemmer()
    cleaned_tokens = [porter.stem(token) for token in cleaned_tokens] 
    """
    return cleaned_tokens

""" for file_name in os.listdir("./subtitles-dataset/preprocessed_files/"):
    print(file_name)
    output =  open("./pickle_files/" + file_name + '.pkl', 'wb')
    file_dic = {}
    file = open("./subtitles-dataset/preprocessed_files/" + file_name, "r")
    text = file.read()
    cleaned_text = clean_text(text)    
    file_sentences = sent_tokenize(cleaned_text)

    sentence_number = 0
    for sentence in file_sentences:
        tokens = word_tokenize(sentence)
        cleaned_tokens = clean_tokens(tokens)
        if len(cleaned_tokens) != 0 :
            file_dic[sentence_number] = cleaned_tokens
            sentence_number += 1

    sentence_number = 0
    pickle.dump(file_dic, output,protocol=pickle.HIGHEST_PROTOCOL)

    file.close()
    output.close()
 """




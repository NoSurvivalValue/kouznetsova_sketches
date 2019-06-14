import os
import time
from convert_msd import convert_morph

def convert_sentence_msd(sentence):

    words = sentence.split('\n')

    conll_sentence = ''

    n_token = 1

    for w in words:
        
        parts = w.split()
        
        if len(parts) != 0:
            if len(parts) > 3:

                if parts[3] != '[]':
                    if '#' in parts[3]:
                        normal_form = parts[2]
                    else:
                        normal_form = parts[3][1:-1]
                else:
                    normal_form = parts[2]


                conll_sentence += '{}\t{}\t{}\t{}\t_\t{}\t_\t_\t_\t_\n'.format(n_token, parts[2], normal_form, convert_morph(w)[0], convert_morph(w)[1])
            else:
                conll_sentence += '{}\t{}\t{}\tPUNCT\t_\t_\t_\t_\t_\t_\n'.format(n_token, parts[2], parts[2])
            n_token += 1

    return conll_sentence
    

def split_into_sentences(text):

    sentences = text.split('\n\n')
    conll_sentences = []

    for s in sentences:
        conll_sentences.append(convert_sentence_msd(s))

    return conll_sentences


def convert_file_msd(file, folder, new_folder):

    f = open(folder + file, 'r', encoding = 'utf-8')
    g = open(new_folder + file[:-3] + 'conll', 'w', encoding = 'utf-8')
    
    text = ''

    for line in f:

        if line.startswith('TEXTID') == True:

            try:
                sentences = split_into_sentences(text)
                for s in sentences:
                    if len(s) != 0:
                        g.write(s + '\n')
            except UnboundLocalError:
                pass
            
            text = ''

        else:

            text += line

    sentences = split_into_sentences(text)
    for s in sentences:
        if len(s) != 0:
            g.write(s + '\n')

def convert_corpora_msd(folder, new_folder):

    files = os.listdir(folder)

    for f in files:

        print(f)

        convert_file_msd(f, folder, new_folder)

convert_corpora_msd('./Media Corpora/', './CONLL MSD Corpora/')

import os

def get_morph(morph):

    new_morph = '_'
    pos = '_'

    if morph[0] == 'N':
        if morph[6] == 'y':
            new_morph = 'Animacy=Anim|'
        if morph[6] == 'n':
            new_morph = 'Animacy=Inan|'
        if morph[1] == 'p':
            pos = 'PROPN'
            
    if morph[0] == 'V':
        if morph[9] == 'p':
            new_morph = 'Aspect=Perf|'
        if morph[9] == 'i':
            new_morph = 'Aspect=Imp|'

    return new_morph, pos

def convert_sentence(sentence):

    words = sentence.split('\n')

    conll_sentence = ''

    n_token = 1

    for w in words:
        
        parts = w.split()
        
        if len(parts) != 0:
            if len(parts) > 3:
                conll_sentence += '{}\t{}\t_\t{}\t_\t{}\t_\t_\t_\t_\n'.format(n_token, parts[2], get_morph(parts[4])[1], get_morph(parts[4])[0])
            else:
                conll_sentence += '{}\t{}\t_\t_\t_\t_\t_\t_\t_\t_\n'.format(n_token, parts[2])
            n_token += 1

    return conll_sentence
    

def split_into_sentences(text):

    sentences = text.split('\n\n')
    conll_sentences = []

    for s in sentences:
        conll_sentences.append(convert_sentence(s))

    return conll_sentences


def convert_file(file, folder, new_folder):

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

def convert_corpora(folder, new_folder):

    files = os.listdir(folder)

    for f in files:

        convert_file(f, folder, new_folder)

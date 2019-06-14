import os
from rnnmorph.predictor import RNNMorphPredictor
import warnings

warnings.simplefilter('ignore')

predictor = RNNMorphPredictor(language="ru")

# Функция для прогона файла через морфологический анализатор RNNMorph

def morph_analyze_file(file, folder, new_folder):
    f = open(folder + file, 'r', encoding = 'utf-8')
    g = open(new_folder + file, 'w', encoding = 'utf-8')
    sentence = []
    cconj = ['только', 'ни', 'причем', 'иль', 'и', 'либо', 'и/или', 'иначе', 'а', 'зато', 'но', 'или', 'да', 'х', 'ан']
    first_line = 0
    extra_morph = {}
    new_pos = {}
    for line in f:
        line = line.strip()
        parts = line.split('\t')
        if len(parts) > 1:
            extra_morph[parts[1]] = parts[5]
            new_pos[parts[1]] = parts[3]
            if parts[0] == '1':
                forms = predictor.predict(sentence)
                n = 1
                for m in forms:
                    
                    if m.pos == 'CONJ' and m.normal_form in cconj:
                        m.pos = 'CCONJ'
                    if m.pos == 'CONJ' and m.normal_form not in cconj:
                        m.pos = 'SCONJ'
                    
                    try:
                        if extra_morph[m.word] != '_':
                            m.tag = extra_morph[m.word] + m.tag
                    except IncorrectKeyError:
                        pass
                    
                    try:
                        if new_pos[m.word] == 'PROPN':
                            m.pos = 'PROPN'
                    except IncorrectKeyError:
                        pass
                    
                    g.write('{}\t{}\t{}\t{}\t_\t{}\t_\t_\t_\t_\n'.format(n, sentence[n - 1], m.normal_form, m.pos, m.tag))
                    n += 1
                if first_line != 0:
                    g.write('\n')
                sentence = []
            sentence.append(parts[1])
        first_line += 1
    forms = predictor.predict(sentence)
    n = 1
    for m in forms:
        if m.pos == 'CONJ' and m.normal_form in cconj:
            m.pos = 'CCONJ'
        if m.pos == 'CONJ' and m.normal_form not in cconj:
            m.pos = 'SCONJ'
        try:
            if extra_morph[m.word] != '_':
                m.tag = extra_morph[m.word] + m.tag
        except IncorrectKeyError:
            pass
        g.write('{}\t{}\t{}\t{}\t_\t{}\t_\t_\t_\t_\n'.format(n, sentence[n - 1], m.normal_form, m.pos, m.tag))
        n += 1
        
    f.close()
    g.close()

# Функция для прогона всего корпуса через морфологический анализатор RNNMorph

def morph_analyze_corpora(folder, new_folder):
    files = os.listdir(folder)
    for file in files:
        if file.endswith('.conll') == True:
            morph_analyze_file(file, folder, new_folder)


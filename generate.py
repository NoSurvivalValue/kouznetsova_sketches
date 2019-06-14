import collections
from convert_to_conll import convert_corpora
from convert_msd_to_conll import convert_corpora_msd
import csv
import math
from metrics import calculate_pmd_2, calculate_md_2, calculate_lfmd_2, calculate_t_score_2, calculate_x_sq_2, calculate_dice_2, calculate_jaccard_2, calculate_poisson_2
from metrics import calculate_pmd_3, calculate_poisson_3
from morph_analyze import morph_analyze_corpora
import os
import re
from synt_parse import synt_parse_corpora, synt_parse_corpora_w_morph

# Сохранение всех интересующих синтаксических отношений из файлов в программу

rels_2 = {}

f = open('2gramms.txt', 'r', encoding = 'utf-8-sig')

for line in f:
    line = line.strip()
    words = line.split('\t')
    rels_2[tuple([words[0], words[1], words[2]])] = words[3]

f.close()

rels_3 = {}

f = open('3gramms.txt', 'r', encoding = 'utf-8-sig')
for line in f:
    line = line.strip()
    words = line.split('\t')
    rels_3[tuple([words[0], words[1], words[2], words[3], words[4]])] = words[5]

f.close()

sketch_repr = {}

# Класс биграммы, у которой есть словоформа, лемма и часть речи обоих слов,
# вид синтаксической связи и то, как эта биграмма будет отображаться      
                 
class gramm_2:

    def __init__(self, word_1, lemma_1, pos_1, syntax, word_2, lemma_2, pos_2):
        self.word_1 = word_1
        self.lemma_1 = lemma_1
        self.pos_1 = pos_1
        self.syntax = syntax
        self.word_2 = word_2
        self.lemma_2 = lemma_2
        self.pos_2 = pos_2
        rel = tuple([pos_1, syntax, pos_2])
        if tuple([self.lemma_1, self.lemma_2, syntax]) in sketch_repr:
            self.sketch = sketch_repr[tuple([self.lemma_1, self.lemma_2, syntax])]
        else:
            if rels_2[rel] == 'agr':
                self.sketch = self.lemma_1 + ' ' + self.lemma_2
            if rels_2[rel] == 'gov':
                self.sketch = self.lemma_1 + ' ' + self.lemma_2
            if rels_2[rel] == 'head':
                self.sketch = self.lemma_2 + ' ' + self.lemma_2

# Класс триграммы, у которой есть словоформа, лемма и часть речи всех трех слов,
# оба вида синтаксической связи и то, как эта триграмма будет отображаться

class gramm_3:

    def __init__(self, word_1, lemma_1, pos_1, syntax_1, word_2, lemma_2, pos_2, syntax_2, word_3, lemma_3, pos_3):
        self.word_1 = word_1
        self.lemma_1 = lemma_1
        self.pos_1 = pos_1
        self.syntax_1 = syntax_1
        self.word_2 = word_2
        self.lemma_2 = lemma_2
        self.pos_2 = pos_2
        self.syntax_2 = syntax_2
        self.word_3 = word_3
        self.lemma_3 = lemma_3
        self.pos_3 = pos_3
        rel = tuple([pos_1, syntax_1, pos_2, syntax_2, pos_3])
        if rels_3[rel] == 'agr':
            self.sketch = self.lemma_1 + ' ' + self.lemma_3 + ' ' + self.lemma_2
        if rels_3[rel] == 'gov':
            self.sketch = self.lemma_1 + ' ' + self.word_3 + ' ' + self.word_2

# Класс леммы, для которого определена лемма и часть речи
            
class lem:

    def __init__(self, lemma, pos):

        self.lemma = lemma
        self.pos = pos

# Функция для нахождения всех зависимых слова

def find_dep(word, sent):

    dep = []

    for s in sent:
        
        if sent[s][4] == word:

            dep.append(sent[s][5])

    return dep

# Функция для нахождения всех биграмм интересующих синтаксических отношений

def find_gramms_2(sent):

    gramms_2 = []

    for s in sent:

        word_1 = sent[sent[s][4]][0]
        lemma_1 = sent[sent[s][4]][1]
        pos_1 = sent[sent[s][4]][2]
        syntax = sent[s][5]
        word_2 = sent[s][0]
        lemma_2 = sent[s][1]
        pos_2 = sent[s][2]

        dep = find_dep(s, sent)

        if 'case' not in dep:

            try:

                gramms_2.append(gramm_2(word_1, lemma_1, pos_1, syntax, word_2, lemma_2, pos_2))

            except KeyError:

                pass

    return gramms_2

# Функция для нахождения всех триграмм интересующих синтаксических отношений

def find_gramms_3(sent):

    gramms_3 = []

    for s in sent:
        
        word_1 = sent[sent[sent[s][4]][4]][0]
        lemma_1 = sent[sent[sent[s][4]][4]][1]
        pos_1 = sent[sent[sent[s][4]][4]][2]
        syntax_1 = sent[sent[s][4]][5]
        word_2 = sent[sent[s][4]][0]
        lemma_2 = sent[sent[s][4]][1]
        pos_2 = sent[sent[s][4]][2]
        syntax_2 = sent[s][5]
        word_3 = sent[s][0]
        lemma_3 = sent[s][1]
        pos_3 = sent[s][2]

        try:

            gramms_3.append(gramm_3(word_1, lemma_1, pos_1, syntax_1, word_2, lemma_2, pos_2, syntax_2, word_3, lemma_3, pos_3))

        except KeyError:

            pass

    return gramms_3

# Функция для нахождения всех лемм помимо пунктуации

def find_lemmas(sent):

    lemmas = []

    for s in sent:

        lemma = sent[s][1]
        pos = sent[s][2]

        if pos != 'PUNCT':
            lemmas.append(lem(lemma, pos))

    return lemmas

# Функция генерации скетчей для одного файла

def generate_sketches_file(file):

    print(file)
    print('generating')

    all_gramms_2 = []
    all_gramms_3 = []
    all_lemmas = []
    all_rels_2 = 0
    all_rels_3 = 0

    f = open(file, 'r', encoding = 'utf-8-sig')

    for line in f:

        line = re.sub('\ufeff', '', line)
        parts = line.split('\t')

        if parts != [] and '#' not in parts and line != '\n':
            
            if parts[0] == '1':

                try:
                    
                    for gramm_2 in find_gramms_2(sent):
                        all_gramms_2.append(gramm_2)

                except (UnboundLocalError, KeyError) as e:

                    pass

                try:
                    
                    for gramm_3 in find_gramms_3(sent):
                        all_gramms_3.append(gramm_3)

                except (UnboundLocalError, KeyError) as e:

                    pass

                try:

                    found_lemmas = find_lemmas(sent)
                    for lemma in found_lemmas:
                        all_lemmas.append(lemma)
                    all_rels_2 += len(found_lemmas) - 1
                    all_rels_3 += len(found_lemmas) - 2

                except UnboundLocalError:

                    pass
                
                sent = {'0': ['_', '_', '_', '_', '-1', '_'],
                        '-1': ['_', '_', '_', '_', '0', '_']}

            if '.' not in parts[0]:
                try:
                    sent[parts[0]] = [parts[1], parts[2], parts[3], parts[5], parts[6], parts[7]]
                except IndexError:
                    print(parts)

    f.close()

    return(all_gramms_2, all_gramms_3, all_lemmas, all_rels_2, all_rels_3)

folder = '../corpora/'

# Функция генерации скетчей для всего корпуса

def generate_sketches_corpora(folder_path):

    files = os.listdir(folder_path)

    corpora_gramms_2 = collections.Counter()
    corpora_gramms_3 = collections.Counter()
    corpora_lemmas = collections.Counter()
    corpora_rels_2 = 0
    corpora_rels_3 = 0

    for f in files:

        all_gramms_2, all_gramms_3, all_lemmas, all_rels_2, all_rels_3 = generate_sketches_file(folder_path + f)

        for a in all_gramms_2:
            corpora_gramms_2[tuple([a.sketch, a.lemma_1, a.pos_1, a.lemma_2, a.pos_2, a.syntax])] +=1

        for a in all_gramms_3:
            corpora_gramms_3[tuple([a.sketch, a.lemma_1, a.pos_1, a.lemma_2, a.pos_2, a.lemma_3, a.pos_3, a.syntax_1, a.syntax_2])] +=1

        for a in all_lemmas:
            corpora_lemmas[tuple([a.lemma, a.pos])] += 1

        corpora_rels_2 += all_rels_2
        corpora_rels_3 += all_rels_3

    print('generated')

    return(corpora_gramms_2, corpora_gramms_3, corpora_lemmas, corpora_rels_2, corpora_rels_3)

# Функция для записи всех найденных лемм, биграмм и триграмм в отдельные файлы

def write_sketches(folder, new_folder):

    corpora_gramms_2, corpora_gramms_3, corpora_lemmas, corpora_rels_2, corpora_rels_3 = generate_sketches_corpora(folder)

    print('Lemmas - ' + str(sum(corpora_lemmas.values())))
    print('Sketches 2 - ' + str(corpora_rels_2))
    print('writing sketches 2')

    f = open(new_folder + 'gramms_2.txt', 'w', encoding = 'utf-8')

    f.write('LEMMA\tPOS\tSKETCH\tTYPE\tSYNTAX\tLEMMA_2\tPOS_2\tFreq\tPMI\tMD\tLFMD\tT-Score\tX-Squared\tDice\tJaccard\tPoisson\n')

    for c in corpora_gramms_2.most_common():
        pmd = calculate_pmd_2(c, corpora_lemmas, corpora_rels_2)
        md = calculate_md_2(c, corpora_lemmas, corpora_rels_2)
        lfmd = calculate_lfmd_2(c, corpora_lemmas, corpora_rels_2)
        t_score = calculate_t_score_2(c, corpora_lemmas, corpora_rels_2)
        x_sq = calculate_x_sq_2(c, corpora_lemmas, corpora_rels_2)
        dice = calculate_dice_2(c, corpora_lemmas, corpora_rels_2)
        jaccard = calculate_jaccard_2(c, corpora_lemmas, corpora_rels_2)
        poisson = calculate_poisson_2(c, corpora_lemmas, corpora_rels_2)
        f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(c[0][1], c[0][2], c[0][0], 'head', c[0][5], c[0][3], c[0][4], c[1], pmd, md, lfmd, t_score, x_sq, dice, jaccard, poisson))
        f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(c[0][3], c[0][4], c[0][0], 'dep', c[0][5], c[0][1], c[0][2], c[1], pmd, md, lfmd, t_score, x_sq, dice, jaccard, poisson))

    f.close()

    print('writing sketches 3')

    f = open(new_folder + 'gramms_3.txt', 'w', encoding = 'utf-8')

    f.write('LEMMA\tPOS\tSKETCH\tTYPE\tSYNTAX\tLEMMA_2\tPOS_2\tFreq\tPMI\tPoisson-Stirling\n')

    for c in corpora_gramms_3.most_common():
        pmd = calculate_pmd_3(c, corpora_lemmas, corpora_rels_3)
        poisson = calculate_poisson_3(c, corpora_lemmas, corpora_rels_3)
        f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(c[0][1], c[0][2], c[0][0], 'head', c[0][7] + '|' + c[0][8], c[0][3], c[0][4], c[1], pmd, poisson))
        f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(c[0][3], c[0][4], c[0][0], 'dep', c[0][7] + '|' + c[0][8], c[0][1], c[0][2], c[1], pmd, poisson))


    f.close()

    print('writing lemmas')

    f =open(new_folder + 'lemmas.txt', 'w', encoding = 'utf-8')

    for c in corpora_lemmas:
        f.write('{}\t{}\t{}\n'.format(c[0], c[1], corpora_lemmas[c]))

    f.close()

# Главная функция для генерации скетчей

def generate_sketches():

    morph = input('Choose a morphological analyzer (Udpipe, Rnnmorph, MSD or nothing): ')
    corpora = './Media Corpora/'

    if morph == 'MSD' or morph == '':

        conll_folder = './CONLL MSD Corpora/'
        convert_corpora_msd(corpora, conll_folder)
        
        syntax_folder = './Synt Corpora MSD/'
        
        synt_parse_corpora(conll_folder, syntax_folder)
        
        sketch_folder = './Sketches MSD/'
        
        write_sketches(syntax_folder, sketch_folder)

    else:

        conll_folder = './CONLL Corpora/'
        convert_corpora(corpora, conll_folder)
        
        if morph == 'Rnnmorph':
            
            morph_folder = './Morph Corpora/'
            morph_analyze_corpora(conll_folder, morph_folder)
            
            syntax_folder = './Synt Corpora Rnnmorph/'
            synt_parse_corpora(morph_folder, syntax_folder)
            
            sketch_folder = './Sketches Rnnmorph/'
        
            write_sketches(syntax_folder, sketch_folder)
            
        if morph == 'Udpipe':
            
            syntax_folder = './Synt Corpora Udpipe/'
            synt_parse_corpora_w_morph(conll_folder, syntax_folder)
            
            sketch_folder = './Sketches Udpipe/'
        
            write_sketches(syntax_folder, sketch_folder)
        
            

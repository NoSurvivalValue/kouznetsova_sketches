import re
import operator
import os

metrics_2 = {'PMI': 8,
           'MD': 9,
           'LFMD': 10,
           'T-Score': 11,
           'X_Squared': 12,
           'Dice': 13,
           'Jaccard': 14,
           'Poisson': 15}

metrics_3 = {'PMI': 8,
             'Poisson': 9}

#metric_3 = {

class sketch_search:

    def __init__(self, lemma, pos):
        self.lemma = lemma
        self.pos = pos
        self.sketches_2 = {}
        self.sketches_3 = {}
        self.names_2 = {}
        self.names_3 = {}

        try:
            f = open('./POS_classes/' + pos + '_2.txt', 'r', encoding = 'utf-8')
            for line in f:
                line = line.strip()
                line = re.sub('\ufeff', '', line)
                parts = line.split('\t')
                self.sketches_2[tuple([parts[0], parts[1]])] = {}
                self.names_2[tuple([parts[0], parts[1]])] = parts[2]
            f.close()

            f = open('./POS_classes/' + pos + '_3.txt', 'r', encoding = 'utf-8')
            for line in f:
                line = line.strip()
                line = re.sub('\ufeff', '', line)
                parts = line.split('\t')
                self.sketches_3[parts[0]] = {}
                self.names_3[parts[0]] = parts[1]
            f.close()

        except FileNotFoundError:
            pass
        

def find_lemma(variant, lemma, pos = ''):

    lemmas = []

    f = open('./Sketches ' + variant + '/lemmas.txt', 'r', encoding = 'utf-8')

    for line in f:
        line = line.strip()
        parts = line.split()
        if pos != '':
            lemmas.append(sketch_search(lemma, pos))
            break
        else:
            if parts[0] == lemma:
                lemmas.append(sketch_search(lemma, parts[1]))

    f.close()
    
    return lemmas

def find_sketches_2(variant, sketch_search, metric_2):

    if metric_2 == '':
        metric_2 = 'Dice'

    print(sketch_search.lemma + ' (' + sketch_search.pos + ')\n')

    f = open('./Sketches ' + variant + '/gramms_2.txt', 'r', encoding = 'utf-8')

    for line in f:
        line = line.strip()
        parts = line.split('\t')
        if parts[0] == sketch_search.lemma and parts[1] == sketch_search.pos:
            try:
                sketch_search.sketches_2[tuple([parts[4], parts[3]])][parts[2]] = float(parts[metrics_2[metric_2]])
            except KeyError:
                pass
    f.close()

def find_sketches_3(variant, sketch_search, metric_3):

    if metric_3 == '':
        metric_3 = 'Poisson'

    f = open('./Sketches ' + variant + '/gramms_3.txt', 'r', encoding = 'utf-8')

    for line in f:
        line = line.strip()
        parts = line.split('\t')
        if parts[0] == sketch_search.lemma and parts[1] == sketch_search.pos:
            try:
                sketch_search.sketches_3[parts[4]][parts[2]] = float(parts[metrics_3[metric_3]])
            except KeyError:
                pass
    f.close()

def find_all_sketches():

    variant = input('Input the morphology variant (Rnnmorph, Udpipe, MSD): ')
    lemma = input('Input the lemma: ')
    pos = input('Input the part of speech (or nothing): ')
    metric_2 = input('Input the desired metric (PMI, MD, LFMD, T-Score, X_Squared, Dice, Jaccard, Poisson or nothing): ')
    metric_3 = input('Input the desired metric (PMI, Poisson or nothing): ')

    lemmas = find_lemma(variant, lemma, pos)

    for l in lemmas:

        f = open('./Results/' + l.lemma + '_' + l.pos + '_' + variant + '.txt', 'w', encoding = 'utf-8')
    
        find_sketches_2(variant, l, metric_2)

        for e in l.sketches_2:

            if len(l.sketches_2[e]) != 0:
                print(l.names_2[tuple([e[0], e[1]])])
                f.write('\n' + l.names_2[tuple([e[0], e[1]])] + '\n\n')

                for k in sorted(l.sketches_2[e].items(), key=operator.itemgetter(1), reverse=True):
                    print('{}\t({})'.format(k[0], k[1]))
                    f.write('{}\t({})\n'.format(k[0], k[1]))
                print('')

        find_sketches_3(variant, l, metric_3)

        for e in l.sketches_3:

            if len(l.sketches_3[e]) != 0:

                print(l.names_3[e])
                f.write('\n' + l.names_3[e] + '\n\n')

                for k in sorted(l.sketches_3[e].items(), key=operator.itemgetter(1), reverse=True):
                    print('{}\t({})'.format(k[0], k[1]))
                    f.write('{}\t({})\n'.format(k[0], k[1]))
                print('')

find_all_sketches()     
    
        
    

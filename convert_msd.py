def convert_noun(old_tag):

    parts = list(old_tag)

    tag = []

    if parts[1] == 'p':
        pos = 'PROPN'
    if parts[1] == 'c':
        pos = 'NOUN'

    if parts[6] == 'n':
        tag.append('Animacy=Inan')
    if parts[6] == 'y':
        tag.append('Animacy=Anim')

    if parts[4] == 'n':
        tag.append('Case=Nom')
    if parts[4] == 'g':
        tag.append('Case=Gen')
    if parts[4] == 'd':
        tag.append('Case=Dat')
    if parts[4] == 'a':
        tag.append('Case=Acc')
    if parts[4] == 'i':
        tag.append('Case=Ins')
    if parts[4] == 'l':
        tag.append('Case=Loc')
    if parts[4] == 'v':
        tag.append('Case=Voc')

    if parts[2] == 'm':
        tag.append('Gender=Masc')
    if parts[2] == 'f':
        tag.append('Gender=Fem')
    if parts[2] == 'n':
        tag.append('Gender=Neut')
    if parts[2] == 'c':
        tag.append('Gender=Com')

    if parts[3] == 's':
        tag.append('Number=Sing')
    if parts[3] == 'p':
        tag.append('Number=Plur')

    if len(tag) == 0:
        tag.append('_')

    return(pos, '|'.join(tag))

def convert_verb(old_tag):

    parts = list(old_tag)

    tag = []

    if parts[9] == 'p':
        tag.append('Aspect=Perf')
    if parts[9] == 'i':
        tag.append('Aspect=Imp')

    if parts[2] == 'm':
        tag.append('Gender=Masc')
    if parts[2] == 'f':
        tag.append('Gender=Fem')
    if parts[2] == 'n':
        tag.append('Gender=Neut')
    if parts[2] == 'c':
        tag.append('Gender=Com')

    if parts[1] == 'i':
        tag.append('Mood=Ind')
        tag.append('VerbForm=Fin')
    if parts[1] == 'm':
        tag.append('Mood=Imp')
        tag.append('VerbForm=Fin')
    if parts[1] == 'n':
        tag.append('VerbForm=Inf')
    if parts[1] == 'g':
        tag.append('VerbForm=Conv')
    if parts[1] == 'p':
        tag.append('VerbForm=Part')

    if parts[3] == 's':
        tag.append('Number=Sing')
    if parts[3] == 'p':
        tag.append('Number=Plur')

    if parts[4] == 'n':
        tag.append('Case=Nom')
    if parts[4] == 'g':
        tag.append('Case=Gen')
    if parts[4] == 'd':
        tag.append('Case=Dat')
    if parts[4] == 'a':
        tag.append('Case=Acc')
    if parts[4] == 'i':
        tag.append('Case=Ins')
    if parts[4] == 'l':
        tag.append('Case=Loc')
    if parts[4] == 'v':
        tag.append('Case=Voc')

    if parts[5] == '1':
        tag.append('Person=1')
    if parts[5] == '2':
        tag.append('Person=2')
    if parts[5] == '3':
        tag.append('Person=3')

    if parts[6] == 'p':
        tag.append('Tense=Pres')
    if parts[6] == 's':
        tag.append('Tense=Past')
    if parts[6] == 'f':
        tag.append('Tense=Fut')

    if parts[8] == 'a':
        tag.append('Voice=Act')
    if parts[8] == 'p' or parts[8] == 's':
        tag.append('Voice=Pass')

    if parts[11] == 's':
        tag.append('Variant=Short')

    if len(tag) == 0:
        tag.append('_')

    return('VERB', '|'.join(tag))

def convert_adj(old_tag):

    parts = list(old_tag)

    tag = []

    if parts[1] == 'p':
        tag.append('Degree=Pos')
    if parts[1] == 'c':
        tag.append('Degree=Cmp')
    if parts[1] == 's':
        tag.append('Degree=Sup')

    if parts[2] == 'm':
        tag.append('Gender=Masc')
    if parts[2] == 'f':
        tag.append('Gender=Fem')
    if parts[2] == 'n':
        tag.append('Gender=Neut')

    if parts[3] == 's':
        tag.append('Number=Sing')
    if parts[3] == 'p':
        tag.append('Number=Plur')

    if parts[4] == 'n':
        tag.append('Case=Nom')
    if parts[4] == 'g':
        tag.append('Case=Gen')
    if parts[4] == 'd':
        tag.append('Case=Dat')
    if parts[4] == 'a':
        tag.append('Case=Acc')
    if parts[4] == 'i':
        tag.append('Case=Ins')
    if parts[4] == 'l':
        tag.append('Case=Loc')
    
    if parts[5] == 's':
        tag.append('Variant=Short')

    if len(tag) == 0:
        tag.append('_')

    return('ADJ', '|'.join(tag))

def convert_adv(old_tag):

    parts = list(old_tag)

    tag = []

    if parts[1] == 'p':
        tag.append('Degree=Pos')
    if parts[1] == 'c':
        tag.append('Degree=Cmp')
    if parts[1] == 's':
        tag.append('Degree=Sup')

    if len(tag) == 0:
        tag.append('_')

    return('ADV', '|'.join(tag))

def convert_pred(word):

    return('VERB', '_')

def convert_pron(old_tag):

    parts = list(old_tag)

    tag = []

    if parts[2] == 'm':
        tag.append('Gender=Masc')
    if parts[2] == 'f':
        tag.append('Gender=Fem')
    if parts[2] == 'n':
        tag.append('Gender=Neut')

    if parts[3] == 's':
        tag.append('Number=Sing')
    if parts[3] == 'p':
        tag.append('Number=Plur')

    if parts[4] == 'n':
        tag.append('Case=Nom')
    if parts[4] == 'g':
        tag.append('Case=Gen')
    if parts[4] == 'd':
        tag.append('Case=Dat')
    if parts[4] == 'a':
        tag.append('Case=Acc')
    if parts[4] == 'i':
        tag.append('Case=Ins')
    if parts[4] == 'l':
        tag.append('Case=Loc')

    if len(tag) == 0:
        tag.append('_')

    return('PRON', '|'.join(tag))

def convert_num(old_tag):

    parts = list(old_tag)

    tag = []

    if parts[2] == 'm':
        tag.append('Gender=Masc')
    if parts[2] == 'f':
        tag.append('Gender=Fem')
    if parts[2] == 'n':
        tag.append('Gender=Neut')

    if parts[3] == 's':
        tag.append('Number=Sing')
    if parts[3] == 'p':
        tag.append('Number=Plur')

    if parts[4] == 'n':
        tag.append('Case=Nom')
    if parts[4] == 'g':
        tag.append('Case=Gen')
    if parts[4] == 'd':
        tag.append('Case=Dat')
    if parts[4] == 'a':
        tag.append('Case=Acc')
    if parts[4] == 'i':
        tag.append('Case=Ins')
    if parts[4] == 'l':
        tag.append('Case=Loc')

    if len(tag) == 0:
        tag.append('_')

    return('NUM', '|'.join(tag))

def convert_conj(word):

    cconj = ['только', 'ни', 'причем', 'иль', 'и', 'либо', 'и/или', 'иначе', 'а', 'зато', 'но', 'или', 'да', 'х', 'ан']

    if word in cconj:
        pos = 'CCONJ'
         
    else:
        pos = 'SCONJ'

    return(pos, '_')

def convert_adp(old_tag):

    return('ADP', '_')

def convert_h(old_tag):

    return('ADV', '_')

def convert_intj(old_tag):

    return('INTJ', '_')

def convert_part(old_tag):

    return('PART', '_')

def convert_x(old_tag):

    return('X', '_')

def convert_morph(msd):

    msd = msd.strip()
    parts = msd.split()

    msd_word = parts[2]
    msd_tag = parts[4]
    msd_pos = msd_tag[0]
    
    if msd_pos == 'N':
        pos, tag = convert_noun(msd_tag)

    if msd_pos == 'V':
        pos, tag = convert_verb(msd_tag)

    if msd_pos == 'A':
        pos, tag = convert_adj(msd_tag)

    if msd_pos == 'R':
        pos, tag = convert_adv(msd_tag)

    if msd_pos == 'W':
        pos, tag = convert_pred(msd_word)

    if msd_pos == 'P':
        pos, tag = convert_pron(msd_tag)

    if msd_pos == 'M':
        pos, tag = convert_num(msd_tag)

    if msd_pos == 'C':
        pos, tag = convert_conj(msd_word)

    if msd_pos == 'S':
        pos, tag = convert_adp(msd_word)

    if msd_pos == 'H':
        pos, tag = convert_h(msd_word)

    if msd_pos == 'I':
        pos, tag = convert_intj(msd_word)

    if msd_pos == 'Q':
        pos, tag = convert_part(msd_word)

    if msd_pos == 'X':
        pos, tag = convert_x(msd_word)

    return(pos, tag)

    


        
    
    
    
        
        
        

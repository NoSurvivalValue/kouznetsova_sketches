import collections
import math

def calculate_pmd_2(gramm_2, corpora_lemmas, corpora_rels_2):

    freq_sketch = gramm_2[1]/corpora_rels_2
    freq_lemma_1 = corpora_lemmas[tuple([gramm_2[0][1], gramm_2[0][2]])] / sum(corpora_lemmas.values())
    freq_lemma_2 = corpora_lemmas[tuple([gramm_2[0][3], gramm_2[0][4]])] / sum(corpora_lemmas.values())
    pmd = math.log(freq_sketch / (freq_lemma_1 * freq_lemma_2), 2)

    return round(pmd, 2)

def calculate_md_2(gramm_2, corpora_lemmas, corpora_rels_2):

    freq_sketch = gramm_2[1]/corpora_rels_2
    freq_lemma_1 = corpora_lemmas[tuple([gramm_2[0][1], gramm_2[0][2]])] / sum(corpora_lemmas.values())
    freq_lemma_2 = corpora_lemmas[tuple([gramm_2[0][3], gramm_2[0][4]])] / sum(corpora_lemmas.values())
    md = math.log((freq_sketch ** 2)/ (freq_lemma_1 * freq_lemma_2), 2)

    return round(md, 2)

def calculate_lfmd_2(gramm_2, corpora_lemmas, corpora_rels_2):

    md = calculate_md_2(gramm_2, corpora_lemmas, corpora_rels_2)
    freq_sketch = gramm_2[1]/corpora_rels_2

    lfmd = md + math.log(freq_sketch, 2)

    return round(lfmd, 2)

def calculate_t_score_2(gramm_2, corpora_lemmas, corpora_rels_2):

    freq_sketch = gramm_2[1]/corpora_rels_2
    freq_lemma_1 = corpora_lemmas[tuple([gramm_2[0][1], gramm_2[0][2]])] / sum(corpora_lemmas.values())
    freq_lemma_2 = corpora_lemmas[tuple([gramm_2[0][3], gramm_2[0][4]])] / sum(corpora_lemmas.values())
 
    t_score = (freq_sketch - (freq_lemma_1 * freq_lemma_2)) / ((freq_sketch * (1 - freq_sketch)) / sum(corpora_lemmas.values()) ** 0.5)

    return round(t_score, 2)
                                                               

def calculate_x_sq_2(gramm_2, corpora_lemmas, corpora_rels_2):

    freq_sketch = gramm_2[1]/corpora_rels_2
    freq_lemma_1 = corpora_lemmas[tuple([gramm_2[0][1], gramm_2[0][2]])] / sum(corpora_lemmas.values())
    freq_lemma_2 = corpora_lemmas[tuple([gramm_2[0][3], gramm_2[0][4]])] / sum(corpora_lemmas.values())

    a = ((freq_sketch - (freq_lemma_1 * freq_lemma_2)) ** 2) / (freq_lemma_1 * freq_lemma_2)

    freq_sketch_b = (corpora_lemmas[tuple([gramm_2[0][1], gramm_2[0][2]])] - gramm_2[1]) / corpora_rels_2
    freq_lemma_1_b = freq_lemma_1
    freq_lemma_2_b = 1 - freq_lemma_2

    b = ((freq_sketch_b - (freq_lemma_1_b * freq_lemma_2_b)) ** 2) / (freq_lemma_1_b * freq_lemma_2_b)

    freq_sketch_c = (corpora_lemmas[tuple([gramm_2[0][3], gramm_2[0][4]])] - gramm_2[1]) / corpora_rels_2
    freq_lemma_1_c = 1 - freq_lemma_1
    freq_lemma_2_c = freq_lemma_2

    c = ((freq_sketch_c - (freq_lemma_1_c * freq_lemma_2_c)) ** 2) / (freq_lemma_1_c * freq_lemma_2_c)

    freq_sketch_d = 1 - freq_sketch - freq_sketch_b - freq_sketch_c
    freq_lemma_1_d = freq_lemma_1_c
    freq_lemma_2_d = freq_lemma_2_b

    d = ((freq_sketch_d - (freq_lemma_1_d * freq_lemma_2_d)) ** 2) / (freq_lemma_1_d * freq_lemma_2_d)

    return round(a + b + c + d, 5)

def calculate_log_likelihood_2(gramm_2, corpora_lemmas, corpora_rels_2):
    
    freq_sketch = gramm_2[1]/corpora_rels_2
    freq_lemma_1 = corpora_lemmas[tuple([gramm_2[0][1], gramm_2[0][2]])] / sum(corpora_lemmas.values())
    freq_lemma_2 = corpora_lemmas[tuple([gramm_2[0][3], gramm_2[0][4]])] / sum(corpora_lemmas.values())

    a = freq_sketch * math.log(freq_sketch / (freq_lemma_1 * freq_lemma_2), 2)

    freq_sketch_b = (corpora_lemmas[tuple([gramm_2[0][1], gramm_2[0][2]])] - gramm_2[1]) / corpora_rels_2
    freq_lemma_1_b = freq_lemma_1
    freq_lemma_2_b = 1 - freq_lemma_2

    b = freq_sketch_b * math.log(freq_sketch_b / float(freq_lemma_1_b * freq_lemma_2_b), 2)

    freq_sketch_c = (corpora_lemmas[tuple([gramm_2[0][3], gramm_2[0][4]])] - gramm_2[1]) / corpora_rels_2
    freq_lemma_1_c = 1 - freq_lemma_1
    freq_lemma_2_c = freq_lemma_2

    c = freq_sketch_c * math.log(freq_sketch_c / float(freq_lemma_1_c * freq_lemma_2_c), 2)

    freq_sketch_d = 1 - freq_sketch - freq_sketch_b - freq_sketch_c
    freq_lemma_1_d = freq_lemma_1_c
    freq_lemma_2_d = freq_lemma_2_b

    d = freq_sketch_c * math.log(freq_sketch_d / float(freq_lemma_1_d * freq_lemma_2_d), 2)

    return round(2 * (a + b + c + d), 5)

def calculate_dice_2(gramm_2, corpora_lemmas, corpora_rels_2):

    freq_sketch = gramm_2[1]/corpora_rels_2
    freq_lemma_1 = corpora_lemmas[tuple([gramm_2[0][1], gramm_2[0][2]])] / sum(corpora_lemmas.values())
    freq_lemma_2 = corpora_lemmas[tuple([gramm_2[0][3], gramm_2[0][4]])] / sum(corpora_lemmas.values())

    dice = (2 * freq_sketch) / (freq_lemma_1 + freq_lemma_2)

    return round(dice, 5)

def calculate_jaccard_2(gramm_2, corpora_lemmas, corpora_rels_2):

    freq_sketch = gramm_2[1]/corpora_rels_2
    freq_sketch_b = (corpora_lemmas[tuple([gramm_2[0][1], gramm_2[0][2]])] - gramm_2[1]) / corpora_rels_2
    freq_sketch_c = (corpora_lemmas[tuple([gramm_2[0][3], gramm_2[0][4]])] - gramm_2[1]) / corpora_rels_2

    jaccard = freq_sketch / (freq_sketch + freq_sketch_b + freq_sketch_c)

    return round(jaccard, 3)

def calculate_poisson_2(gramm_2, corpora_lemmas, corpora_rels_2):

    freq_sketch = gramm_2[1]/corpora_rels_2
    freq_lemma_1 = corpora_lemmas[tuple([gramm_2[0][1], gramm_2[0][2]])] / sum(corpora_lemmas.values())
    freq_lemma_2 = corpora_lemmas[tuple([gramm_2[0][3], gramm_2[0][4]])] / sum(corpora_lemmas.values())

    poisson = freq_sketch * (math.log(freq_sketch, 2) - math.log(freq_lemma_1 * freq_lemma_2) - 1)

    return round(poisson, 5)

def calculate_pmd_3(gramm_3, corpora_lemmas, corpora_rels_3):

    freq_sketch = gramm_3[1]/corpora_rels_3
    freq_lemma_1 = corpora_lemmas[tuple([gramm_3[0][1], gramm_3[0][2]])] / sum(corpora_lemmas.values())
    freq_lemma_2 = corpora_lemmas[tuple([gramm_3[0][3], gramm_3[0][4]])] / sum(corpora_lemmas.values())
    freq_lemma_3 = corpora_lemmas[tuple([gramm_3[0][5], gramm_3[0][6]])] / sum(corpora_lemmas.values())

    pmd = freq_sketch / (freq_lemma_1 * freq_lemma_2 * freq_lemma_3)

    return round(pmd, 2)

def calculate_poisson_3(gramm_3, corpora_lemmas, corpora_rels_3):

    freq_sketch = gramm_3[1]/corpora_rels_3
    freq_lemma_1 = corpora_lemmas[tuple([gramm_3[0][1], gramm_3[0][2]])] / sum(corpora_lemmas.values())
    freq_lemma_2 = corpora_lemmas[tuple([gramm_3[0][3], gramm_3[0][4]])] / sum(corpora_lemmas.values())
    freq_lemma_3 = corpora_lemmas[tuple([gramm_3[0][5], gramm_3[0][6]])] / sum(corpora_lemmas.values())

    poisson = freq_sketch * (math.log(freq_sketch, 2) - math.log(freq_lemma_1 * freq_lemma_2 * freq_lemma_3, 2) - 1)

    return round(poisson, 5)
    



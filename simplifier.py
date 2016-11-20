from sets import Set


def simplify_word(word):
    sim_word = word
    if word[0:4] == 'The ' or word[0:4] == 'the ':
        sim_word = word[4:]
    elif word[0:2] == 'A ' or word[0:2] == 'a ':
        sim_word = word[2:]
    elif word[0:3] == 'An ' or word[0:3] == 'an ':
        sim_word = word[3:]
    return sim_word


def simplify_candidates(candidate):
    sim_candidate = candidate
    for i in range(0, 2):
        sim_candidate[i] = simplify_word(candidate[i])
    return sim_candidate


# candidates is a list of size 2, pronoun is the word, sent is a list of dict
def break_by_conn(origin_candidates, candidates, tokens, c1_name, c2_name):
    can_1 = False
    can_2 = False
    conn_found = False
    sent1 = []
    sent2 = []

    for i in range(0, len(tokens)):
        if tokens[i]['pos'] == '.' or tokens[i]['word'] == ',':
            continue
        if conn_found and tokens[i]['word'] != ',':
            sent2.append(tokens[i])
        elif tokens[i]['pos'] in Set(["IN", "CC"]) and (can_1 + can_2) == 2:
            conn_found = True
            conn = tokens[i]
        else:
            if (tokens[i]['word'] in candidates[0] and c1_name) or (tokens[i]['word'] == candidates[0]):
                can_1 = True
            if (tokens[i]['word'] in candidates[1] and c2_name) or (tokens[i]['word'] == candidates[1]):
                can_2 = True
            sent1.append(tokens[i])
    if conn_found == False:
        conn = 'GG'
    # sent1 and sent2 are list of dict from token. conn is the dict of conn from tokens
    return sent1, sent2, conn


def query_type(words, dict_key, dict_value):
    for i in range(0, len(words)-1):
        if words[i][dict_key] == dict_value:
            return True, i
    return False, -1

def check_candidate_name(candidate_list, tokens):
    c1_name = False
    c2_name = False
    for i in range(0, len(tokens)):
        if tokens[i]['ner'] == 'PERSON':
            if tokens[i]['word'] in candidate_list[0]:
                c1_name = True
            if tokens[i]['word'] in candidate_list[1]:
                c2_name = True

    return c1_name, c2_name
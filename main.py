import data_provider
import simplifier
import search


def list_to_string(list):
    sent = ""
    for i in range(0, len(list)):
        sent = sent + list[i] + ' '
    return sent


if __name__ == '__main__':

    num_of_sentences, sent_list, pronoun_list, origin_candidate_list, answer_list = data_provider.read_data()
    full_tokens, depend_list = data_provider.get_json_sent(num_of_sentences, sent_list)

    candidate_list = []
    for i in range(0, num_of_sentences):
        candidate_list.append(simplifier.simplify_candidates(origin_candidate_list[i]))

    # broken_sent_list a list(sent) of list(word) of dict
    # broken_sent_list a list of strings
    # BROKEN means # needs * 2!
    broken_sent_list = []
    broken_sent_string_list = []
    f = open('data/broken_sent.txt', 'w+')
    for i in range(0, num_of_sentences):
        print "Sentence #", i
        sent1, sent2, conn_dict = simplifier.break_by_conn(candidate_list[i], full_tokens[i])
        broken_sent_list.append(sent1)
        broken_sent_list.append(sent2)

        sent1_string = ""
        sent2_string = ""
        for j in range(0, len(sent1)):
            f.write(sent1[j]['word']+' ')
            sent1_string = sent1_string + sent1[j]['word'] + ' '
        sent1_string += '.'
        broken_sent_string_list.append(sent1_string)
        f.write('.\n')

        for j in range(0, len(sent2)):
            f.write(sent2[j]['word']+' ')
            sent2_string = sent2_string + sent2[j]['word'] + ' '
        broken_sent_string_list.append(sent2_string)
        f.write('.\n\n')

    f.close()
    broken_tokens, broken_depend_list = data_provider.get_json_broken_sent(num_of_sentences*2, broken_sent_string_list)

    print broken_tokens
    print broken_depend_list

    feature = []

    for i in range(0, num_of_sentences):
        be_sentence = False

        be_sentence, be_index = simplifier.query_type(broken_tokens[i*2+1], 'lemma', 'be')
        _, pronoun_index = simplifier.query_type(broken_tokens[i*2+1], 'word', pronoun_list[i])

        latter_sent = []
        for j in range(0, len(broken_tokens[i*2+1])-1):
            latter_sent.append(str(broken_tokens[i*2+1][j]['word']))

        latter_sent[pronoun_index] = candidate_list[i][0]
        C0_BJ = search.google_search("Lions are predators.")
        latter_sent[pronoun_index] = candidate_list[i][1]
        C1_BJ = search.google_search(list_to_string(latter_sent))

        if C0_BJ > C1_BJ * (1 + 0.2):
            feature[i][1][0] = [1, 0]
        elif C1_BJ > C0_BJ * (1 + 0.2):
            feature[i][1] = [0, 1]
        else:
            feature[i][1] = [0, 0]


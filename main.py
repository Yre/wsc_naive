import data_provider
import simplifier

if __name__ == '__main__':

    num_of_sentences, sent_list, pronoun_list, origin_candidate_list, answer_list = data_provider.read_data()
    full_tokens, depend_list = data_provider.get_json_sent(num_of_sentences, sent_list)

    print "Dependency list:\n", depend_list
    print "All tokens:\n", full_tokens

    candidate_list = []
    for i in range(0, num_of_sentences):
        candidate_list.append(simplifier.simplify_candidates(origin_candidate_list[i]))

    # broke_sent[0] is a list of length 2: two small sentences
    broken_2_sent = []
    for i in range(0, num_of_sentences):
        print "Sentence #", i
        sent1, sent2, conn_dict = simplifier.break_by_conn(candidate_list[i], full_tokens[i])
        broken_2_sent.append([sent1, sent2])
        # print "Full tokens:\n", full_tokens[i]
        # simplified_sent_list.append(simplifier.basic_structure(full_tokens[i], depend_list[i]))
        # print broken_2_sent
        for j in range(0, len(broken_2_sent[i][0])):
            print broken_2_sent[i][0][j]['word'],
        print ' '
        for j in range(0, len(broken_2_sent[i][1])):
            print broken_2_sent[i][1][j]['word'],
        print '\n'
        # print sent1
        # print sent2


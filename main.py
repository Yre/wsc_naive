import data_provider
import simplifier
import search
import evaluate
# import run_shell
# # import sys
# from GoogleScraper import scrape_with_config, GoogleSearchError
# from GoogleScraper.utils import get_some_words


def list_to_string(list):
    sent = ""
    for i in range(0, len(list)):
        sent = sent + list[i] + ' '
    return sent


if __name__ == '__main__':

    num_of_sentences, sent_list, pronoun_list, origin_candidate_list, key_list = data_provider.read_data()
    full_tokens, depend_list = data_provider.get_json_sent(num_of_sentences, sent_list)

    candidate_list = []
    for i in range(0, num_of_sentences): # get rid of the/a
        candidate_list.append(simplifier.simplify_candidates(origin_candidate_list[i]))

    ############################################################
    # Break sentences

    # broken_sent_list a list(sent) of list(word) of dict
    # broken_sent_list a list of strings
    # BROKEN means # needs * 2!
    broken_sent_list = []
    broken_sent_string_list = []
    f = open('data/broken_sent.txt', 'w+')
    fgg = open('data/broke_fail.txt', 'w+')
    for i in range(0, num_of_sentences):
        c1_name, c2_name = simplifier.check_candidate_name(candidate_list[i], full_tokens[i])
        sent1, sent2, conn_dict = simplifier.break_by_conn(candidate_list[i], full_tokens[i])
        if conn_dict == 'GG':
            fgg.write(sent_list[i]+'\n\n')

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
    fgg.close()
    broken_tokens, broken_depend_list = data_provider.get_json_broken_sent(num_of_sentences*2, broken_sent_string_list)

    print broken_tokens
    print broken_depend_list

    ############################################################
    #  Extract features

    feature = []
    num_of_feature = 1
    answer_list = []
    # run_shell.install_Google_Scraper_shell()

    for i in range(0, num_of_sentences):
        print "\n\nSentence #", i
        print sent_list[i]
        be_sentence = False
        feature.append([])

        ############################################################
        #  Extract subject, verb, obj, pronoun

        # before conn
        _, verb_dep_index = simplifier.query_type(broken_depend_list[2 * i], 'dep', 'nsubj')
        subj_index = broken_depend_list[2 * i][verb_dep_index]['dependent'] - 1
        subj_word = broken_depend_list[2 * i][verb_dep_index]['dependentGloss']
        verb_index = broken_depend_list[2 * i][verb_dep_index]['governor'] - 1
        verb_word = broken_depend_list[2 * i][verb_dep_index]['governorGloss']
        _, verb_dep_index = simplifier.query_type(broken_depend_list[2 * i], 'dep', 'nmod')
        if verb_dep_index == -1:
            _, verb_dep_index = simplifier.query_type(broken_depend_list[2 * i], 'dep', 'dobj')
        obj_index = broken_depend_list[2 * i][verb_dep_index]['dependent'] - 1
        obj_word = broken_depend_list[2 * i][verb_dep_index]['dependentGloss']
        print subj_word, ' ', verb_word, ' ', obj_word

        # after conn
        be_sentence, be_index = simplifier.query_type(broken_tokens[i * 2 + 1], 'lemma', 'be')
        _, pronoun_index = simplifier.query_type(broken_tokens[i*2+1], 'word', pronoun_list[i])
        if pronoun_index == -1: # the pronoun is before the conn
            feature[i].append([0, 0])
            continue
        if be_sentence:
            latter_be, latter_be_dep_index = simplifier.query_type(broken_depend_list[2 * i + 1], 'dep', 'cop')
            latter_be_index = broken_depend_list[2 * i + 1][latter_be_dep_index]['dependent'] - 1
            latter_be_word = broken_depend_list[2 * i + 1][latter_be_dep_index]['dependentGloss']
            latter_predicate_index = broken_depend_list[2 * i + 1][latter_be_dep_index]['governor'] - 1
            latter_predicate_word = broken_depend_list[2 * i + 1][latter_be_dep_index]['governorGloss']
            print pronoun_list[i], ' ', latter_be_word, ' ', latter_predicate_word

        else:
            _, pron_dep_index = simplifier.query_type(broken_depend_list[2 * i + 1], 'dependentGloss', pronoun_list[i])
            _, latter_verb_dep_index = simplifier.query_type(broken_depend_list[2 * i + 1], 'dep', 'nsubj')
            latter_subj_word = broken_depend_list[2 * i + 1][latter_verb_dep_index]['dependentGloss']
            latter_subj_index = broken_depend_list[2 * i + 1][latter_verb_dep_index]['governor'] - 1
            latter_verb_word = broken_depend_list[2 * i + 1][latter_verb_dep_index]['governorGloss']

            if broken_depend_list[2*i+1][pron_dep_index]['dep'] == 'nsubj':
                print 'pronoun is subject!!'
                latter_obj_exist, latter_obj_dep_index = simplifier.query_type(broken_depend_list[2 * i + 1], 'dep', 'dobj')
                if latter_obj_exist:
                    latter_obj_word = broken_depend_list[2*i+1][latter_obj_dep_index]['dependentGloss']
                    latter_obj_index = broken_depend_list[2 * i + 1][latter_obj_dep_index]['dependent'] - 1
                    print latter_subj_word, ' ', latter_verb_word, ' ', latter_obj_word
                else:
                    print pronoun_list[i], ' ', latter_verb_word
            else:
                print 'pronoun is object!!!'
                _, latter_subj_dep_index = simplifier.query_type(broken_depend_list[2 * i + 1], 'dep', 'nsubj')
                print latter_subj_word, ' ', latter_verb_word, ' ', pronoun_list[i]


        ############################################################
        #  Substitute and google it
        # latter_sent = []
        # for j in range(0, len(broken_tokens[i*2+1])-1):
        #     latter_sent.append(str(broken_tokens[i*2+1][j]['word']))

        # latter_sent[pronoun_index] = candidate_list[i][0]
        # C0_BJ = search.google_search(list_to_string(latter_sent))
        # latter_sent[pronoun_index] = candidate_list[i][1]
        # C1_BJ = search.google_search(list_to_string(latter_sent))

        ###
        # C1_BJ = 1000 C2_BJ = 0
        #
        # if C0_BJ > C1_BJ * (1 + 0.2):
        #     feature[i].append([1, 0])
        #     print 'ans: ', origin_candidate_list[i][0], ' vs ', key_list[i]
        # elif C1_BJ > C0_BJ * (1 + 0.2):
        #     feature[i].append([0, 1])
        #     print 'ans: ', origin_candidate_list[i][1], ' vs ', key_list[i]
        # else:
        #     feature[i].append([0, 0])
        #     print "No decision"
        #
        # no_decision_flag = True
        # for j in range(2):
        #     if feature[i][0][j] == 1:
        #         answer_list.append(candidate_list[i][j])
        #         no_decision_flag = False
        # if no_decision_flag:
        #     answer_list.append('NO_DECISION')

    # evaluate.evaluate(sent_list, answer_list, key_list)

    print feature

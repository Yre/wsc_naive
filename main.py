from sets import Set
import data_provider
import simplifier
import search
import evaluate
import narrative_chain
import init
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
    # init.xml_to_txt('WSCExample.xml')

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
        print sent1
        print sent2

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


    ############################################################
    #  Extract features

    feature = []
    num_of_feature = 1
    answer_list = []
    # run_shell.install_Google_Scraper_shell()
    Turn_conn = Set(
        ['but', 'even though', 'even if', 'nonetheless', 'yet', 'although', 'despite', 'in spite of', 'though'])
    chains = narrative_chain.load_chain()

    for i in range(0, num_of_sentences):
        print "\n\nSentence #", i
        print sent_list[i]
        be_sentence = False
        feature.append([-1, -1])
        answer_list.append(["NO_DECISION", "NO_DECISION"])

        pron_found, pronoun_index = simplifier.query_type(broken_tokens[i * 2 + 1], 'word', pronoun_list[i], -1, -1)
        ############################################################
         # Substitute and google it
        if pron_found:
            latter_sent = []
            for j in range(0, len(broken_tokens[i * 2 + 1]) - 1):
                latter_sent.append(str(broken_tokens[i * 2 + 1][j]['word']))

            latter_sent[pronoun_index] = candidate_list[i][0]
            C0_BJ = search.google_search(list_to_string(latter_sent))
            latter_sent[pronoun_index] = candidate_list[i][1]
            C1_BJ = search.google_search(list_to_string(latter_sent))

            ##
            # C1_BJ = 1000 C2_BJ = 0

            if C0_BJ > C1_BJ * (1 + 0.1):
                feature[i][0] = 0
                print 'google ans: ', origin_candidate_list[i][0], ' vs ', key_list[i]
                continue
            elif C1_BJ > C0_BJ * (1 + 0.1):
                feature[i][0] = 1
                print 'google ans: ', origin_candidate_list[i][1], ' vs ', key_list[i]
                continue


        ############################################################
        #  Extract subject, verb, obj, pronoun
        #
        # before conn
        _, root_dep_index = simplifier.query_type(broken_depend_list[2 * i], 'dep', 'ROOT', -1, -1)
        # root_volcab_index = broken_depend_list[2*i][root_dep_index]['dependent']
        # root_volcab = broken_depend_list[2*i][root_dep_index]['dependentGloss']
        #
        # pos_of_root = broken_tokens[2*i][root_volcab_index]['pos']
        # if pos_of_root == 'JJ': # be + adj
        #     adj_word = root_volcab

        # simplifier.extract_sub_verb_obj(broken_depend_list, broken_tokens)

        if pronoun_index != -1:  # the pronoun is after the conn
            verb_index = broken_depend_list[2 * i][root_dep_index]['dependent']
            verb_word = broken_depend_list[2 * i][root_dep_index]['dependentGloss']

            verb_nsubj, verb_dep_index = simplifier.query_type(broken_depend_list[2 * i], 'dep', 'nsubj', 'governorGloss', verb_word)
            if not verb_nsubj:
                verb_nmod, verb_dep_index = simplifier.query_type(broken_depend_list[2 * i], 'dep', 'nmod', 'governorGloss', verb_word)
            subj_index = broken_depend_list[2 * i][verb_dep_index]['dependent']
            subj_word = broken_depend_list[2 * i][verb_dep_index]['dependentGloss']

            verb_lemma = broken_tokens[2 * i][verb_index-1]['lemma']

            _, obj_dep_index = simplifier.query_type(broken_depend_list[2 * i], 'dep', 'nsubjpass', 'governorGloss', verb_word)
            if obj_dep_index == -1:
                _, obj_dep_index = simplifier.query_type(broken_depend_list[2 * i], 'dep', 'dobj', 'governorGloss', verb_word)
            obj_index = broken_depend_list[2 * i][obj_dep_index]['dependent']
            obj_word = broken_depend_list[2 * i][obj_dep_index]['dependentGloss']
            print subj_word, ' ', verb_word, ' ', obj_word


            # after conn

            _, latter_root_dep_index = simplifier.query_type(broken_depend_list[2 * i +1], 'dep', 'ROOT', -1, -1)
            latter_verb_index = broken_depend_list[2 * i + 1][latter_root_dep_index]['dependent']
            latter_verb_word = broken_depend_list[2 * i + 1][root_dep_index]['dependentGloss']

            latter_be_adj, latter_be_dep_index = simplifier.query_type(broken_depend_list[i * 2 + 1], 'dep', 'cop', 'governorGloss', latter_verb_word)

            if latter_be_adj: # be + adj
                print 'be adj sentence!'
                latter_be_index = broken_depend_list[2 * i + 1][latter_be_dep_index]['dependent']
                latter_be_word = broken_depend_list[2 * i + 1][latter_be_dep_index]['dependentGloss']
                latter_predicate_index = broken_depend_list[2 * i + 1][latter_be_dep_index]['governor']
                latter_predicate_word = broken_depend_list[2 * i + 1][latter_be_dep_index]['governorGloss']

                _, latter_subj_dep_index = simplifier.query_type(broken_depend_list[2 * i + 1], 'dep', 'nsubj', 'governorGloss', latter_predicate_word)
                latter_subj_word = broken_depend_list[2*i+1][latter_subj_dep_index]['dependentGloss']
                latter_subj_index = broken_depend_list[2 * i + 1][latter_subj_dep_index]['dependent']

                print latter_subj_word, ' ', latter_be_word, ' ', latter_predicate_word

            else:
                latter_verb_lemma = broken_tokens[2 * i + 1][latter_verb_index-1]['lemma']
                latter_nsubj, latter_verb_subj_dep = simplifier.query_type(broken_depend_list[2 * i + 1], 'governor', latter_verb_index, 'dep', 'nsubj')
                if latter_nsubj:
                    latter_subj_word = broken_depend_list[2*i+1][latter_verb_subj_dep]['dependentGloss']
                    latter_subj_index = broken_depend_list[2 * i + 1][latter_verb_subj_dep]['dependent']
                else:
                    latter_nmod, latter_verb_subj_dep = simplifier.query_type(broken_depend_list[2 * i + 1], 'governor', latter_verb_index, 'dep', 'nmod')
                    latter_subj_word = broken_depend_list[2 * i + 1][latter_verb_subj_dep]['dependentGloss']
                    latter_subj_index = broken_depend_list[2 * i + 1][latter_verb_subj_dep]['dependent']

                latter_obj_exist = True
                latter_dobj, latter_verb_obj_dep = simplifier.query_type(broken_depend_list[2 * i + 1], 'governor', latter_verb_index, 'dep', 'dobj')
                if latter_dobj:
                    latter_obj_word = broken_depend_list[2 * i + 1][latter_verb_obj_dep]['dependentGloss']
                    latter_obj_index = broken_depend_list[2 * i + 1][latter_verb_obj_dep]['dependent']
                else:
                    latter_nmod, latter_verb_obj_dep = simplifier.query_type(broken_depend_list[2 * i + 1], 'governor', latter_verb_index, 'dep', 'nsubjpass')
                    if latter_nmod:
                        latter_obj_word = broken_depend_list[2 * i + 1][latter_verb_obj_dep]['dependentGloss']
                        latter_obj_index = broken_depend_list[2 * i + 1][latter_verb_obj_dep]['dependent']
                    else:
                        latter_obj_exist = False

                if latter_obj_exist:
                    print latter_subj_word, ' ', latter_verb_word, ' ', latter_obj_word
                else:
                    print latter_subj_word, ' ', latter_verb_word

                pron_role = 'n'
                if latter_subj_word == pronoun_list[i]:
                    print 'pronoun is subject!!'
                    pron_role = 's'
                elif latter_obj_exist and latter_obj_word == pronoun_list[i]:
                    print 'pronoun is object!!!'
                    pron_role = 'o'

            if (not latter_be_adj) and (pron_role != 'n'):
                print verb_lemma, ' and ', latter_verb_lemma
                can_role = narrative_chain.check(chains, pron_role, verb_lemma, latter_verb_lemma)
                print 'can role = ', can_role
                # return 1 means pron should be the object one
                if can_role != "NO_DECISION":
                    if candidate_list[i][0] == obj_word or candidate_list[i][1] == subj_word:
                        if can_role:
                            feature[i][0] = 0
                        else:
                            feature[i][0] = 1
                    else:
                        # cand[0] is subject
                        if can_role:
                            feature[i][0] = 1
                        else:
                            feature[i][0] = 0

        ############################################################
        # To answer list
    for i in range(0, num_of_sentences):
        no_decision_flag = True
        num_of_feature = 2
        for j in range(num_of_feature):
            if feature[i][j] != -1:
                answer_list[i][j] = candidate_list[i][feature[i][j]]
            else:
                answer_list[i][j] = "NO_DECISION"

        ############################################################
        # Check Conn
        # Reversed = False
        # for conn in Turn_conn:
        #     if sent_list[i].find(conn):
        #         Reversed = True
        # for j in range(2):
        #     if feature[i][0][j] == 1:
        #         answer_list.append(candidate_list[i][j])
        #         no_decision_flag = False
        #
        #
        #


    evaluate.evaluate(sent_list, answer_list, key_list)

    print feature

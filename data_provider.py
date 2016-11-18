# read train.txt (wsc data-small)
# (later change it to train_.txt (wsc data-large)
# for each test case, based on the two noun candidates,
# find the Conn after them.
# Or use openIE
# http://stackoverflow.com/questions/163542/python-how-do-i-pass-a-string-into-subprocess-popen-using-the-stdin-argument)
# Then split into two sent, and output into FILE: input.txt
# run format:text and output in FILE: input.txt.out
# Then get nsubj, and dobj.

import run_shell
import json


# import data from train.txt
def read_data():
    input_data = [input_data.rstrip('\n') for input_data in open('data/train.txt')]

    sent_list = [input_data[i] for i in xrange(0, len(input_data), 5)]
    pronoun_list = [input_data[i] for i in xrange(1, len(input_data), 5)]
    candidate_list = [input_data[i].strip().split(",") for i in xrange(2, len(input_data), 5)]
    answer_list = [input_data[i] for i in xrange(3, len(input_data), 5)]

    num_of_sentences = len(sent_list)

    return num_of_sentences, sent_list, pronoun_list, candidate_list, answer_list


def simplify_sent(num_of_sentences, sent_list):
    raw_sent_file = open('stanford-corenlp-full-2015-12-09/input.txt', 'w')
    for item in sent_list:
        raw_sent_file.write("%s\n" % item)

    # get parsed and get json
    run_shell.stanfordnlp_shell()
    f = open('data/input.txt.json')
    data_json = json.load(f)

    depend_list=[]
    for i in range(0,num_of_sentences):
        depend_list.append(data_json['sentences'][i]['basic-dependencies'])

    return depend_list



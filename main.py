import data_provider

if __name__ == '__main__':

    num_of_sentences, sent_list, pronoun_list, candidate_list, answer_list = data_provider.read_data()
    simplified_sent_list = data_provider.simplify_sent(num_of_sentences, sent_list)

    print simplified_sent_list

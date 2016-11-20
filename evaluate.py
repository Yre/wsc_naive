import simplifier


def evaluate(sent_list, answer_list, key_list):
    wrong_list = []
    if len(answer_list) != len(key_list):
        print "The number of answers are inconsistent!"
        return -1
    sent_number = len(answer_list)
    right_answer = 0
    no_answer = 0
    fw = open('data/eval_wrongs.txt', 'w+')
    fr = open('data/eval_rights.txt', 'w+')
    fn = open('data/eval_no_decision.txt', 'w+')
    for i in range(0, sent_number):
        simp_key = simplifier.simplify_word(key_list[i])
        if answer_list == 'NO_DECISION':
            no_answer += 1
            fn.write(sent_list[i] + '\n')
            fn.write(key_list[i] + '\n\n')
        elif simp_key == answer_list[i]:
            right_answer += 1
            fr.write(sent_list[i] + '\n')
            fr.write(simp_key+'\n')
            fr.write(key_list[i]+'\n\n')
        else:
            wrong_list.append(i)
            fw.write(sent_list[i]+'\n')
            fw.write('Right:' + key_list[i]+'\n')
            fw.write('Your ans:' + simp_key+'\n\n')
    fw.close()
    fr.close()
    fn.close()
    print 'Accuracy: ', right_answer, ' + ', no_answer + ' / ', sent_number




import simplifier


def evaluate(sent_list, answer_list, key_list):
    wrong_list = []
    if len(answer_list) != len(key_list):
        print "The number of answers are inconsistent!"
        # return -1
    print "\n\n\n\n\n\n ============================================="
    sent_number = len(answer_list)
    right_answer = 0
    no_answer = 0
    fw = open('data/eval_wrongs.txt', 'w+')
    fr = open('data/eval_rights.txt', 'w+')
    fn = open('data/eval_no_decision.txt', 'w+')
    # f = open('data/result.txt','w+')
    for i in range(0, sent_number):
        # if answer_list[i][0] == "NO_DECISION":
        #     continue
        # print "\nSentence # ",i
        simp_key = simplifier.simplify_word(key_list[i])
        # print sent_list[i]
        # print "answer: ", key_list[i]
        # print "Chain: ", answer_list[i][0]
        # print "Search: ", answer_list[i][1]

        ## answer list 2@!
        # for j in range(0, 2):
        if answer_list[i][1] == 'NO_DECISION':
            no_answer += 1
            fn.write(sent_list[i] + '\n')
            fn.write(key_list[i] + '\n\n')
        elif simp_key == answer_list[i][1]:
            right_answer += 1
            fr.write(sent_list[i] + '\n')
            fr.write(simp_key+'  ')
            fr.write(key_list[i]+'\n\n')
        else:
            wrong_list.append(i)
            fw.write(sent_list[i]+'\n')
            fw.write('Right:' + key_list[i]+'  ')
            fw.write('Your ans:' + simp_key+'\n\n')
    fw.close()
    fr.close()
    fn.close()
    print 'Accuracy: ', right_answer, ' + (', no_answer, ') / ', sent_number




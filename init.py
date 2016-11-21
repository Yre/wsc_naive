
def xml_to_txt(file_name):
    f = open(file_name, 'r')
    data = f.read().replace('\n', '')
    f.close()

    f = open('data/train.txt', 'w+')
    number_of_sent = data.count('<schema>')

    for i in range(0,number_of_sent):
        sch1 = data.find('<text>')
        sch1 += 6
        data = data[sch1:]

        tmp = data.find('>')
        data = data[tmp+1:]
        tmp = data.find('<')
        sent = data[:tmp]
        while not('a' <= sent[0] <= 'z') and not('A' <= sent[0] <= 'Z'):
            sent = sent[1:]
        data = data[tmp+1:]
        while not('a' <= data[0] <= 'z') and not('A' <=data[0] <= 'Z'):
            data = data[1:]
        tmp = data.find('>')
        data = data[tmp+1:]
        tmp = data.find('<')
        data = data[tmp + 1:]
        tmp = data.find('>')
        data = data[tmp + 1:]
        tmp = data.find('<')
        sent += data[:tmp]
        data = data[tmp+1:]
        while not('a' <= sent[len(sent)-1] <= 'z') and not('A' <= sent[len(sent)-1] <= 'Z'):
            sent = sent[:-1]
        print sent
        sent += ' '

        tmp = data.find('>')
        data = data[tmp + 1:]
        tmp = data.find('<')
        data = data[tmp + 1:]
        tmp = data.find('>')
        data = data[tmp + 1:]
        tmp = data.find('<')
        while not('a' <= data[0] <= 'z') and not('A' <=data[0] <= 'Z'):
            data = data[1:]
        sent += data[:tmp]
        while not('a' <= sent[len(sent)-1] <= 'z') and not('A' <= sent[len(sent)-1] <= 'Z'):
            sent = sent[:-1]
        print sent

        data = data[tmp:]

        pron1 = data.find('<pron>')
        pron1 += 6
        data = data[pron1:]
        pron2 = data.find('</pron>')
        pron = data[:pron2]
        while not('a' <= pron[0] <= 'z') and not('A' <= pron[0] <= 'Z'):
            pron = pron[1:]
        while not('a' <= pron[len(pron)-1] <= 'z') and not('A' <= pron[len(pron)-1] <= 'Z'):
            pron = pron[:-1]



        ans1 = data.find('<answer>')
        ans1 += 8
        data = data[ans1:]
        ans2 = data.find('</answer>')
        answer1 = data[:ans2]
        while not('a' <= answer1[0] <= 'z') and not('A' <= answer1[0] <= 'Z'):
            answer1 = answer1[1:]
        while not('a' <= answer1[len(answer1)-1] <= 'z') and not('A' <= answer1[len(answer1)-1] <= 'Z'):
            answer1 = answer1[:-1]

        ans1 = data.find('<answer>')
        ans1 += 8
        data = data[ans1:]
        ans2 = data.find('</answer>')
        answer2 = data[:ans2]
        while not('a' <= answer2[0] <= 'z') and not('A' <= answer2[0] <= 'Z'):
            answer2 = answer2[1:]
        while not('a' <= answer2[len(answer2)-1] <= 'z') and not('A' <= answer2[len(answer2)-1] <= 'Z'):
            answer2 = answer2[:-1]

        ans = data.find('<correctAnswer>')
        ans += 15
        data = data[ans:]
        ans = data.find('</correctAnswer>')
        correctAnswer = data[:ans]
        while not('a' <= correctAnswer[0] <= 'z') and not('A' <= correctAnswer[0] <= 'Z'):
            correctAnswer = correctAnswer[1:]
        while not('a' <= correctAnswer[len(correctAnswer)-1] <= 'z') and not('A' <= correctAnswer[len(correctAnswer)-1] <= 'Z'):
            correctAnswer = correctAnswer[:-1]

        if correctAnswer == 'A':
            correctAnswer = answer1
        else:
            correctAnswer = answer2

        sch2 = data.find('</schema>')
        data = data[sch2+8:]

        f.write(sent+'.\n')
        f.write(pron+'\n')
        f.write(answer1+','+answer2+'\n')
        f.write(correctAnswer+'\n\n')
    f.close()







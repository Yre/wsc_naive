def load_chain():
    with open('data/chain.txt') as f:
        lines = f.readlines()
    chains = []
    for i in range(0,len(lines)):
        if '[' in lines[i]:
            chains.append(lines[i])

    for i in range(0, len(chains)):
        pos = chains[i].find(']')
        chains[i] = chains[i][:pos]
    return chains


def check(chains, pron_role, verb1, verb2):
    cnt_s = 0
    cnt_o = 0

    if pron_role == 'o':
        verb2 = verb2 + '-o'
    else:
        verb2 = verb2 + '-s'
    print 'check chain: [', verb1, '] [', verb2, ']'
    for line in chains:
        if verb1 in line and verb2 in line:
            # print line
            pos11 = line.find(verb1)
            pos11 += len(verb1)
            if line[pos11+1] == 'o':
                cnt_o += 1
            else:
                cnt_s += 1
    print cnt_s, cnt_o
    if cnt_s + cnt_o == 0:
        return "NO_DECISION"
    else:
        return cnt_s <= cnt_o


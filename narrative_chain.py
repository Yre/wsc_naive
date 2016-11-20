
def check(pron_role, verb1, verb2):
    with open('data/chain.txt') as f:
        lines = f.readlines()
    chains = [lines[i] for i in range(5, len(lines), 6)]

    cnt_s = 0
    cnt_o = 0
    for line in chains:
        if verb1 in line and verb2 in line:
            pos1 = line.find(verb1)
            pos2 = line.find(verb2)
            if line[pos2+2] != pron_role:
                continue
            if line[pos1+2] == 'o':
                cnt_o += 1
            else:
                cnt_s += 1
    if cnt_s + cnt_o == 0:
        return "NO_DECISION"
    else:
        return cnt_s <= cnt_o




threshold = 50


def form_trace(history_buffer, tgt, old):



def interpreted_branch_taken(countMap, hb_hash, code_cache, history_buffer, src, tgt, exitCodeCacheSet):
    if tgt in code_cache:
        return
    if tgt in hb_hash:
        old = hb_hash[tgt]
        hb_hash[tgt] = len(history_buffer)-1
        if int(tgt, 16) <= int(src, 16) or old in exitCodeCacheSet:
            countMap[tgt] += 1
            if countMap[tgt] == threshold:
                form_trace(history_buffer, tgt, old)
                del history_buffer[old:]
                del countMap[tgt]
    else:
        hb_hash[tgt] = len(history_buffer)-1

def read_output(fileName):
    f = open(fileName, 'r')
    bbls = []
    bbl = []
    bbls.append(bbl)
    history_buffer = []
    hb_hash = {}
    code_cache = {}
    nextBBLMap = {}
    countMap = {}
    for line in f:
        if line.startswith('@'):
            bbl = []
        elif line.startswith('%'):
            bbl.append(line.split('?')[1])
        elif line.startswith('*'):
            tgt = line.split(' ')[2][2:]
            bbl.append(tgt)
            bbls.append(bbl)
        elif line.isdigit():
            if len(history_buffer)>1:
                nextBBLMap[history_buffer[-1]].append(int(line))
                bNumber = history_buffer[-1]
                history_buffer.append(int(line))
                if bbls[bNumber][-1] != bbl[0]:
                    interpreted_branch_taken(countMap, hb_hash, code_cache, history_buffer, bbls[bNumber][-2], bbls[bNumber][-1])
            else:
                history_buffer.append(int(line))
    f.close()



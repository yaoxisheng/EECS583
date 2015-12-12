from sets import Set

threshold = 1


def form_trace(history_buffer, start, old, code_cache, exitCodeCacheSet, nextBBLMap, bbls):
    newTrace = []
    traceBBLTgt = Set([])
    prev = start
    for branchId in range(old, len(history_buffer)):
        if prev not in code_cache:
            #TODO: think about that why pre is not in nextBBLMap
            if prev in nextBBLMap:
                exitCodeCacheSet |= Set(nextBBLMap[prev])
            newTrace.append(branchId)
            traceBBLTgt.add(prev)
        if bbls[history_buffer[branchId]][-1] in traceBBLTgt:
            break
        prev = bbls[history_buffer[branchId]][-1]
    code_cache[start] = newTrace
    #print start



def interpreted_branch_taken(countMap, hb_hash, code_cache, history_buffer, src, tgt, exitCodeCacheSet, nextBBLMap, bbls, bblInCache):
    if tgt in code_cache:
        bblInCache[0] += 1
        return code_cache[tgt][1:]
    print tgt
    if tgt in hb_hash:
        old = hb_hash[tgt]
        hb_hash[tgt] = len(history_buffer)-1
        if int(tgt, 16) <= int(src, 16) or old in exitCodeCacheSet:
            if tgt not in countMap:
                countMap[tgt] = 0
            countMap[tgt] += 1
            if countMap[tgt] == threshold:
                form_trace(history_buffer, tgt, old, code_cache, exitCodeCacheSet, nextBBLMap, bbls)
                del history_buffer[old:]
                del countMap[tgt]
    else:
        hb_hash[tgt] = len(history_buffer)-1
    return []

def read_output(fileName):
    f = open(fileName, 'r')
    bbls = []
    bbl = []
    bbls.append(bbl)
    #list of indexes of bbl
    history_buffer = []
    #tgt address -> index of bbl
    hb_hash = {}
    #tgt address -> list of indexes of bbl
    code_cache = {}
    #index of bbl -> list of indexes
    nextBBLMap = {}
    #tgt address -> count
    countMap = {}
    #index of bbl
    exitCodeCacheSet = Set([])
    currentTrace = []
    bblInCache = [0]
    totalBbl = 0
    for line in f:
        line = line.rstrip('\n')
        if line.startswith('@'):
            bbl = []
        elif line.startswith('%'):
            bbl.append(line.split('?')[1])
        elif line.startswith('*'):
            tgt = line.split(' ')[2][2:]
            bbl.append(tgt)
            bbls.append(bbl)
        elif line.isdigit():
            totalBbl += 1
            if len(currentTrace)>0 and currentTrace[0]==int(line):
                bblInCache[0] += 1
                del currentTrace[0]
                continue;
            if len(history_buffer)>1:
                if history_buffer[-1] not in nextBBLMap:
                    nextBBLMap[history_buffer[-1]] = []
                nextBBLMap[history_buffer[-1]].append(int(line))
                bNumber = history_buffer[-1]
                history_buffer.append(int(line))
                if bbls[bNumber][-1] == bbl[0] and bbls[bNumber][-1] and len(bbls[bNumber][-1])==12:
                    currentTrace = interpreted_branch_taken(countMap, hb_hash, code_cache, history_buffer, bbls[bNumber][-2], bbls[bNumber][-1], exitCodeCacheSet, nextBBLMap, bbls, bblInCache)
            else:
                history_buffer.append(int(line))
    f.close()
    #print len(code_cache)
    #print bblInCache[0]*1.0/totalBbl


read_output('trace.out')




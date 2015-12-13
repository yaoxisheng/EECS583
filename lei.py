from sets import Set

threshold = 50


def form_trace(history_buffer, start, old, code_cache, exitCodeCacheSet, nextBBLMap, bbls):
    newTrace = []
    traceBBLTgt = Set([])
    prev = start
    #print old, '??', len(history_buffer)
    for branchId in range(old, len(history_buffer)):
        if prev in code_cache:
            break;
        if history_buffer[branchId] in nextBBLMap:
            exitCodeCacheSet |= Set(nextBBLMap[history_buffer[branchId]])
        newTrace.append(history_buffer[branchId])
        traceBBLTgt.add(prev)
        if bbls[history_buffer[branchId]][-1] in traceBBLTgt:
            break
        prev = bbls[history_buffer[branchId]][-1]
    code_cache[start] = newTrace
    exitCodeCacheSet.discard(history_buffer[old])
    #print start
    #print newTrace
    #print "-------------------"



def interpreted_branch_taken(countMap, hb_hash, code_cache, history_buffer, src, tgt, exitCodeCacheSet, nextBBLMap, bbls, bblInCache, numberOfCounters, hitNumber):
    if tgt in code_cache:
        bblInCache[0] += 1
        hitNumber[0] += 1
        return code_cache[tgt][1:]
    #print tgt
    if tgt in hb_hash:
        old = hb_hash[tgt]
        hb_hash[tgt] = len(history_buffer)-1
        if old > hb_hash[tgt]:
            return []
        if int(tgt, 16) <= int(src, 16) or old in exitCodeCacheSet:
            if tgt not in countMap:
                numberOfCounters[0] += 1
                countMap[tgt] = 0
            countMap[tgt] += 1
            if countMap[tgt] == threshold:
                form_trace(history_buffer, tgt, old, code_cache, exitCodeCacheSet, nextBBLMap, bbls)
                del history_buffer[old:]
                del countMap[tgt]
                del hb_hash[tgt]
                bblInCache[0] += 1
                hitNumber[0] += 1      
                return code_cache[tgt][1:]
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
    #number of counters of tgt address
    numberOfCounters = [0]
    #index of bbl
    exitCodeCacheSet = Set([])
    currentTrace = []
    bblInCache = [0]
    totalBbl = 0
    idealTraceNumber = 0
    hitNumber = [0]
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
                if len(currentTrace) == 0:
                    idealTraceNumber += 1
                continue;
            else:
                currentTrace = []
            if len(history_buffer)>1:
                if history_buffer[-1] not in nextBBLMap:
                    nextBBLMap[history_buffer[-1]] = []
                nextBBLMap[history_buffer[-1]].append(int(line))
                bNumber = history_buffer[-1]
                currentIndex = int(line)
                history_buffer.append(int(line))
                if bbls[bNumber][-1] == bbls[currentIndex][0] and bbls[bNumber][-1] and len(bbls[bNumber][-1])==12:
                    currentTrace = interpreted_branch_taken(countMap, hb_hash, code_cache, history_buffer, bbls[bNumber][-2], bbls[bNumber][-1], exitCodeCacheSet, nextBBLMap, bbls, bblInCache, numberOfCounters, hitNumber)
            else:
                history_buffer.append(int(line))
    f.close()
    print len(code_cache)
    print bblInCache[0]*1.0/totalBbl
    print numberOfCounters[0]
    print idealTraceNumber*1.0/hitNumber[0]
    totalTraceLength = 0
    for key, value in code_cache.iteritems():
        totalTraceLength += len(value)
    print totalTraceLength*1.0/len(code_cache)



read_output('trace.out')




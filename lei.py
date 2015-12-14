from sets import Set
import time



def form_trace(history_buffer, start, old, code_cache, exitCodeCacheSet, nextBBLMap, bbls):
    newTrace = []
    traceBBLTgt = Set([])
    for branchId in range(old, len(history_buffer)):
        bblIndex = history_buffer[branchId]
        prev = bbls[bblIndex][0]
        if prev in code_cache or prev in traceBBLTgt:
        #if prev in traceBBLTgt:
            break
        exitCodeCacheSet |= nextBBLMap[bbls[bblIndex][0]]
        newTrace.append(bblIndex)
        traceBBLTgt.add(prev)
    code_cache[start] = newTrace
    exitCodeCacheSet.discard(history_buffer[old])
    return


'''
def interpreted_branch_taken(countMap, hb_hash, code_cache, history_buffer, src, tgt, exitCodeCacheSet, nextBBLMap, bbls, bblInCache, hitNumber):
    if tgt in code_cache:
        bblInCache[0] += 1
        hitNumber[0] += 1
        return code_cache[tgt][1:]
    if tgt in hb_hash:
        old = hb_hash[tgt]
        hb_hash[tgt] = len(history_buffer)-1
        if old > hb_hash[tgt]:
            return []
        if int(tgt, 16) <= int(src, 16) or old in exitCodeCacheSet:
            if tgt not in countMap:
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
'''

def read_output(fileName):
    f = open(fileName, 'r')
    bbl = []
    bbls = [bbl]
    threshold = 50
    hitNumber = 0
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
    bblInCache = 0
    totalBbl = 0
    idealTraceNumber = 0
    timeInIsdigits = 0
    for line in f:
        line = line.rstrip('\n')
        if line.startswith('@'):
            bbl = []
            elements = line.split(' ')
            bbl.append(elements[1])
            bbl.append(elements[2])
            bbl.append(elements[4][2:])
            if elements[3]=='jmp' or elements[3]=='ret' or elements[3]=='call':
                bbl[2] = '0'
            bbls.append(bbl)
        elif line.isdigit():
            #start_time = time.time()
            totalBbl += 1
            currentIndex = int(line)
            if len(currentTrace)>0 and currentTrace[0]==currentIndex:
                bblInCache += 1
                del currentTrace[0]
                if len(currentTrace) == 0:
                    idealTraceNumber += 1
                continue;
            else:
                currentTrace = []
            #timeInIsdigits += time.time() - start_time
            if len(history_buffer)>1:
                prevIndex = history_buffer[-1]
                prevStartAddr = bbls[prevIndex][0]
                if prevStartAddr not in nextBBLMap:
                    nextBBLMap[prevStartAddr] = Set([])
                nextBBLMap[prevStartAddr].add(currentIndex)
                history_buffer.append(currentIndex)
                if bbls[prevIndex][-1]=='0' or bbls[prevIndex][-1] == bbls[currentIndex][0]:
                    #currentTrace = interpreted_branch_taken(countMap, hb_hash, code_cache, history_buffer, bbls[prevIndex][-2], bbls[currentIndex][0], exitCodeCacheSet, nextBBLMap, bbls, bblInCache, hitNumber)
                    src = bbls[prevIndex][1]
                    tgt = bbls[currentIndex][0]

                    if tgt in code_cache:
                        bblInCache += 1
                        hitNumber += 1
                        currentTrace = code_cache[tgt][1:]
                        continue
                    if tgt in hb_hash:
                        old = hb_hash[tgt]
                        hb_hash[tgt] = len(history_buffer)-1
                        if old > hb_hash[tgt]:
                            continue
                        if int(tgt, 16) <= int(src, 16) or old in exitCodeCacheSet:
                            if tgt not in countMap:
                                countMap[tgt] = 0
                            countMap[tgt] += 1
                            if countMap[tgt] == threshold:
                                form_trace(history_buffer, tgt, old, code_cache, exitCodeCacheSet, nextBBLMap, bbls)
                                del history_buffer[old:]
                                del countMap[tgt]
                                del hb_hash[tgt]
                                bblInCache += 1
                                hitNumber += 1
                                currentTrace = code_cache[tgt][1:]
                                continue
                    else:
                        hb_hash[tgt] = len(history_buffer)-1
            else:
                history_buffer.append(currentIndex)
    f.close()
    print "trace number: " + str(len(code_cache))
    print "bbl cover ratio: " + str(bblInCache*1.0/totalBbl)
    print "ideal trace ratio: "+str(idealTraceNumber*1.0/hitNumber)
    totalTraceLength = 0
    for key, value in code_cache.iteritems():
        totalTraceLength += len(value)
    print "average trace length(count in block): " + str(totalTraceLength*1.0/len(code_cache))
    #print("--- %s seconds in digits---" % timeInIsdigits)


start_time1 = time.time()
read_output('trace.out')
print("--- %s seconds ---" % (time.time() - start_time1))




from csv import reader
from collections import defaultdict
from itertools import chain, combinations
from optparse import OptionParser
from utils import *

def apriori(itemSetList, minSup, minConf):
    C1ItemSet = getItemSetFromList(itemSetList)
    # Final result global frequent itemset
    globalFreqItemSet = dict()
    # Storing global itemset with support count
    globalItemSetWithSup = defaultdict(int)

    L1ItemSet = getAboveMinSup(
        C1ItemSet, itemSetList, minSup, globalItemSetWithSup)
    currentLSet = L1ItemSet
    k = 2

    # Calculating frequent item set
    while(currentLSet):
        # Storing frequent itemset
        globalFreqItemSet[k-1] = currentLSet
        # Self-joining Lk
        candidateSet = getUnion(currentLSet, k)
        # Perform subset testing and remove pruned supersets
        candidateSet = pruning(candidateSet, currentLSet, k-1)
        # Scanning itemSet for counting support
        currentLSet = getAboveMinSup(
            candidateSet, itemSetList, minSup, globalItemSetWithSup)
        k += 1

    rules = associationRule(globalFreqItemSet, globalItemSetWithSup, minConf)
    rules.sort(key=lambda x: x[2])

    return globalFreqItemSet, rules

def aprioriFromFile(fname, minSup, minConf):
    # print(f"Function: aprioriFromFile!")
    C1ItemSet, itemSetList = getFromFile(fname)
    total_items = len(itemSetList)
    # print(f"Total Transations = {total_items}")
    # print(f"itemSetList = {itemSetList}")
    # Final result global frequent itemset
    globalFreqItemSet = dict()
    # Storing global itemset with support count
    globalItemSetWithSup = defaultdict(int)

    L1ItemSet = getAboveMinSup(
        C1ItemSet, itemSetList, minSup, globalItemSetWithSup)
    currentLSet = L1ItemSet
    k = 2

    # Calculating frequent item set
    while(currentLSet):
        # Storing frequent itemset
        globalFreqItemSet[k-1] = currentLSet
        # Self-joining Lk
        candidateSet = getUnion(currentLSet, k)
        # Perform subset testing and remove pruned supersets
        candidateSet = pruning(candidateSet, currentLSet, k-1)
        # Scanning itemSet for counting support
        currentLSet = getAboveMinSup(
            candidateSet, itemSetList, minSup, globalItemSetWithSup)
        k += 1

    rules = associationRule(globalFreqItemSet, globalItemSetWithSup, minConf)
    rules.sort(key=lambda x: x[2])

    globalFreqItemSetWithSup = getGlobalFrequent(globalItemSetWithSup, minSup, total_items)

    return globalFreqItemSet, globalFreqItemSetWithSup, rules

if __name__ == "__main__":
    # print(f"Function: Main!")
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='inputFile',
                         help='CSV filename',
                         default=None)
    optparser.add_option('-s', '--minSupport',
                         dest='minSup',
                         help='Min support (float)',
                         default=0.5,
                         type='float')
    optparser.add_option('-c', '--minConfidence',
                         dest='minConf',
                         help='Min confidence (float)',
                         default=0.5,
                         type='float')

    (options, args) = optparser.parse_args()
    # print(f"Options = {options} & Arguments = {args}")

    freqItemSet, freqItemSetWithSup, rules = aprioriFromFile(options.inputFile, options.minSup, options.minConf)

    if args:
        out_file_name = args[0]
        # print(f"File Name = {out_file_name}")
        with open(out_file_name, "w") as patterns_file:
            for freqItems, itemSup in freqItemSetWithSup.items():
                formatted_text = ";".join(map(str, freqItems))
                patterns_file.write(str(itemSup) + ':' + str(formatted_text) + '\n')
        print(f"Output file with name {out_file_name} generated!")
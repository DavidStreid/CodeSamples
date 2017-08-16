#PART 1
def createDocumentVectors(documentSet):
    N = len(documentSet)        # Obtain number of documents in corpus
    wordFreqList = []           # List of hashMaps. Each map has word->freq entries
    docFreq = {}                # HashMap of words to their document frequency
    documentVectors = []        # Return list of document vectors

    stopWords = set(["the", "and", "to", "but", "because", "an", "a", "are", "in", "our", "that", "on", "this"])

    # STEP 1: Iterate through each doc and create wordFreq dic for each and document frequency for each word
    for doc in documentSet:
        wordFreqDic = {}        # WordFreq dic for this document
        seenWords = set([])     # Track words seen in this document
        for word in doc.split(' '):
            if word not in stopWords:               # Skip word if it is a stop word

                if word.lower() not in seenWords:   # Check if first time word is observed in doc
                    seenWords.add(word)             # Record word has been seen in doc
                    if word not in docFreq:         # Increment word's document frequency
                        docFreq[word] = 1
                    else:
                        docFreq[word] += 1

                if word in wordFreqDic:             # Increment word frequency 
                    wordFreqDic[word] += 1
                else:
                    wordFreqDic[word] = 1

        wordFreqList.append(wordFreqDic)            # Add count of doc's word frequenceis to list

    # STEP 2: Create document vectors from word frequency maps weighted using document frequencies of each word
    for wfDic in wordFreqList:
        dv = [] # Document Vector

        # Iterate through each word observed in corpus
        for w in docFreq:
            weight = 0                                  # weight is 0 if word wasn't in doc
            if w in wfDic:
                weight = wfDic[w] #+ log(N/docFreq[w])       # w = wf_i + log(N/df_i)

            dv.append(weight)                           # Add weight to document vector

        documentVectors.append(dv)

    return documentVectors
# PART 2
def documentSimilarity(documentVectorA, documentVectorB):
    if len(documentVectorA) != len(documentVectorB):
        print "Incompatible Vectors"
        return
    n = len(documentVectorA)
    aSq = 0     # weight^2 for each word of documentVectorA
    bSq = 0     # weight^2 for each word of documentVectorB
    prod = 0    # product of weights for each word in both vectors
    for i in range(n):
        prod += documentVectorA[i]*documentVectorB[i]
        aSq += documentVectorA[i]**2
        bSq += documentVectorB[i]**2

    return float(prod/float(aSq*bSq))

# HELPER FUNCTIONS
def printDocs(docA, docB):
    print "DOCUMENT A - \n\t%s" % docA
    print "DOCUMENT B - \n\t%s" % docB

def findSimilarity(docA,docB):
    printDocs(docA, docB)
    dv = createDocumentVectors([docA, docB])
    print "DOCUMENT SIMILARITY: %s" % documentSimilarity(dv[0], dv[1])

if __name__ == '__main__':
    doc1 = "The Simons Foundation Autism Research Initiative (SFARI) today announced the launch of SPARK, an online research initiative designed to become the largest autism study ever undertaken in the United States. SPARK, which stands for Simons Foundation Powering Autism Research for Knowledge, will collect information and DNA for genetic analysis from 50,000 individuals with autism - and their families - to advance our understanding of the condition's causes and accelerate the development of new treatments and supports."
    doc2 = "The complexity of biological networks and the volume of genes present increase the challenges of comprehending and interpretation of the resulting mass of data, which consists of millions of measurements; these data also inhibit vagueness, imprecision, and noise. Therefore, the use of clustering techniques is a first step toward addressing these challenges, which is essential in the data mining process to reveal natural structures and identify interesting patterns in the underlying data."
    findSimilarity(doc1,doc2)




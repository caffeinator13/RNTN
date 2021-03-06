import sys
import math
from operator import itemgetter
import numpy


def visualize(wordEmbeddings):
    """
    Visualize a set of examples using t-SNE.
    """
    PERPLEXITY=30

    titles = wordEmbeddings.keys()
    titlesStr = ["_".join(y.strip().split()) for y in titles]
    x = numpy.vstack(wordEmbeddings.values())    

    filename = "./embeddings.png"
    try:
        #from textSNE.calc_tsne import tsne
        from tsne import tsne
        out = tsne(x, no_dims = 2,perplexity=PERPLEXITY)
        import render
        render.render([(title, point[0], point[1]) for title, point in zip(titles, out)], filename)
    except IOError:
        print "ERROR visualizing", filename

    data = numpy.column_stack((titlesStr,out))
    numpy.savetxt("/home/bhanu/workspace/RNTN/scripts/embeddings2d_phrase_vis.txt", data, "%s")
    
    #command to plot
    #gnuplot -e plot "./embeddings2d.txt" using 2:3:1 with labels


def euclDistance(vec1, vec2):
    dist = 0
    
    if len(vec1) != len(vec2):
        raise ValueError('len(Vec1)!=len(Vec2) '+str(len(vec1))+"!="+str(len(vec2)))
    for i in range(len(vec1)):
        dist += (vec1[i] - vec2[i]) ** 2
        
    return math.sqrt(dist)

def distance(vec1, vec2):
    return euclDistance(vec1, vec2)

def nNearestNeighbours(word, n, wordEmbeddings):
    distances = []
    
    for key in wordEmbeddings.keys():
        dist = distance(wordEmbeddings[word],wordEmbeddings[key])
        word_dist_pair = (key,dist)
        distances.append(word_dist_pair)
  
    return sorted(distances,key=itemgetter(1))[:n]    

def readEmbeddingsfromFile(file,nRows=-1):
    """
    nRows: no of rows to read
    """
    embeddingsDict = {}
    f = open(file)
    iRow = 0
    for row in f:
        values = row.split('\t')
        phrase = values[0]
        embStr = [x.strip() for x in values[1].split()]
        embeddings = map(float, embStr)
#        sumE = sum(embeddings)
        #if not (sumE > 0.999 and sumE<1.001):
        #    print "Not Normalised Embeddings. sum=" + str(sumE) + " for " + phrase
        embeddingsDict[phrase] = embeddings
        iRow += 1
        if (nRows != -1) and (iRow > nRows):
            break
    f.close()
    print "loaded embeddings of size: " + str(iRow)
    return embeddingsDict    

def printNNs(file, phrase, n):    
    phraseEmbDict = readEmbeddingsfromFile(file, nRows=-1)
    
#    all_phrases = phraseEmbDict.keys()
#    rnd = numpy.random.RandomState(17)
#    rnd.shuffle(all_phrases)
#    all_nearPhrases = []
#    for phrase in all_phrases[:1000]:
    nearPhrases =  nNearestNeighbours(phrase, n, phraseEmbDict)   
    for ph in nearPhrases:
#        all_nearPhrases.append(ph)
        print ph[0]


def vis(file, phrase, n):
    phraseEmbDict = readEmbeddingsfromFile(file, nRows=-1)
#    all_phrases = phraseEmbDict.keys()
#    rnd = numpy.random.RandomState(17)
#    rnd.shuffle(all_phrases)
    all_nearPhrases = [] #    for phrase in all_phrases[:1000]:
    phrases = ["over the weekend ", "earlier this month ",  "the government ", "the past week ", "a 2.2 % increase "] #"the chancellor 's "
    for phrase in phrases[:]:
        nearPhrases = nNearestNeighbours(phrase, n, phraseEmbDict)
        for ph in nearPhrases:
            all_nearPhrases.append(ph) #        print ph[0]
    
#    print "dimensions of embeddigns", len(phraseEmbDict["."])
    vis_dict = {}
    for phrase in all_nearPhrases:
        vis_dict[phrase[0]] = phrase[1] #        print phrase[0]
    
    visualize(vis_dict)

def main():
    file = sys.argv[1]
#    file = '/home/bhanu/workspace/RNTN/data/results/phrases_n_vectors_len3_rae.txt'
#    nuse = sys.argv[2]
    #nwords = sys.argv[2]
    phrase = sys.argv[2]
    n =   int(sys.argv[3])
    if(sys.argv[4] == "print"):
        printNNs(file, phrase, n)
    elif(sys.argv[4] == "vis"):    
        vis(file, phrase, n)
    else: 
        print "Invalid option"

if __name__ == "__main__":
    main()

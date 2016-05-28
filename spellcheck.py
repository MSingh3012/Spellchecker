# spellCheck.py
#
# Created by Manpreet Singh

from bitmap  import Bitmap
from hashlib import md5

def makeHashes(word) :
    # convert 32 hexdigits to list of 6 hash keys
    hex32 = md5(word).hexdigest()
    hashes = []
    for i in range(0,30,5) :
        hashes.append(int(hex32[i:i+5],16))
    return hashes

def loadBitmap(file) :
    # generate bitmap from lexicon file (one word per line)
    words = open(file).readlines()
    words = map(lambda x: x.strip(), words) # no newlines please
    bmap  = Bitmap(2**20)
    for word in words :
        hashes = makeHashes(word)
        for hash in hashes :
            bmap.setBit(hash)
    return bmap

def checkWord(bmap, word) :
    # return True if word in lexicon
    hashes = makeHashes(word)
    for hash in hashes :
        if not bmap.getBit(hash): return False
    return True

def main() :
    # lexicon file is argument on command line
    import sys, re
    bmap  = loadBitmap(sys.argv[1])  # dict file is 1st arg
    text  = sys.stdin.read()         # read text as a blob
    # strip puncuation, set all to lower case, set words to array
    #  note. dash and single quote are valid characters
    words = re.sub("[^a-zA-Z'-]"," ",text).lower().split()
    for word in words :
        print " %-6s %s" % (checkWord(bmap,word),word)

if __name__ == "__main__" : main()
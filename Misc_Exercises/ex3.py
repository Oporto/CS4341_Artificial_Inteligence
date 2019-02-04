import re

def wordset(fname):
    """Returns the set of words corresponding to the given file"""
    # Create regexp for character filtering
    regex = re.compile('[^a-zA-Z ]')
    wset = set()
    
    with open(fname) as file:
        for line in file: #Loops through file lines
            cleanline = regex.sub(' ', line) #Substitutes any non-alphabetic character to an empty space
            cleanline = cleanline.lower() #lowers characters
            splitline = cleanline.split() #Splits it into list
            for w in splitline: #Adds every word in that line to set (Which only adds elements not already present in it)
                wset.add(w)
    return wset;
        

def jaccard(fname1, fname2):
    """Calculate Jaccard index"""
    wset1 = wordset(fname1)
    wset2 = wordset(fname2)
    union = wset1 | wset2
    inter = wset1 & wset2
    return len(inter)/len(union);

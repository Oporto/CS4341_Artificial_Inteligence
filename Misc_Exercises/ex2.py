def isreverse(s1, s2):
    
    #Edge cases
    if len(s1) != len(s2): #If strings have different lengths, return false
        return False;
    elif len(s1) == 0: #Else if they have length being 0, return true (Also when recursion reaches the end)
        return True;
    elif s1[0] != s2[-1]: #Else If the first element of the first string is not the last element of the second, return false
        return False;
    #Recursion
    else:
        return isreverse(s1[1:], s2[:-1]); #Calls itself on substrings
    

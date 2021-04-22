import hanzidentifier as ha
import re

def hasTraditional(s):
    return(True if checktype(s) in [1,2,3,4,7,8] else False)

def hasSimplified(s):
    return( True if checktype(s) in [1,2,5,6,7,8] else False) 

def hasBoth(s):
    return( True if checktype(s) in [1,2] else False)

def hasEnglish(s):
    return( True if checktype(s) in [1,3,5,7,9] else False)


def checktype(s):

    def isEng(s):
        return(1 if str(type(re.match('[0-9A-z]',s))).find('re.Match') != -1 else 0)

    if ha.identify(s) is ha.MIXED:
        return( 1 if isEng(s)==1 else 2)

    elif ha.identify(s) is ha.TRADITIONAL:
        return( 3 if isEng(s)==1 else 4)

    elif ha.identify(s) is ha.SIMPLIFIED:
        return( 5 if isEng(s)==1 else 6)

    elif ha.identify(s) is ha.BOTH:
        return( 7 if isEng(s)==1 else 8)
        
    else:
        return( 9 if isEng(s)==1 else 10)
        

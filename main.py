import requests

def cook(URL):
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    return page

def ii_finder(phrase, iindex):
    keys = iindex.keys()
    if type(phrase) == list:
        words = phrase
    else:
        words = [word.lower() for word in phrase.lower().split(' ') if len(word) > 1]
    cands = []
    non = []
    for word in words:
        if word in keys:
            #print(word)
            cands.append(set(iindex[word]))
        else:
            non.append(word)
    if len(cands) == 0:
        return (None, non)
    elif len(cands) == 1:
        return (list(cands[0]), non)
    else:
        for c in cands[1:]:
            cands[0] = cands[0] & c
        return (list(cands[0]), non)
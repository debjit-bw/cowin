import requests, json

with open('./states_ii.json') as f:
    s_ii = json.load(f)

with open('./districts_ii.json') as f:
    d_ii = json.load(f)

with open('./district_state.json') as f:
    d_s = json.load(f)

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

def get_dis_code(phrase, s_ii = s_ii, d_ii = d_ii):
    (states, non) = ii_finder(phrase, s_ii)
    (districts, _) = ii_finder(phrase, d_ii)
    if len(districts) == 0:
        return None
    elif len(districts) == 1:
        return districts[0]
    else: # len(districts) > 1
        if len(states) == 1:
            return districts[0]
        else:
            for district in districts:
                if s_d[str(district)]["state_id"] in states:
                    return district
    return None

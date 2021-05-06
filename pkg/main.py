import requests, json

class parser:

    def __init__(self):

        with open('./states_ii.json') as f:
            self.s_ii = json.load(f)

        with open('./districts_ii.json') as f:
            self.d_ii = json.load(f)

        with open('./district_state.json') as f:
            self.d_s = json.load(f)

    def cook(self, URL):
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        page = requests.get(URL, headers=headers)
        return page
    
    def no_punct(self, phrase):
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        no_punct = ""
        for char in phrase:
            if char not in punctuations:
                no_punct = no_punct + char
        return(no_punct)


    def ii_finder(self, phrase, iindex):
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

    def get_dis_code(self, phrase):
        phrase = self.no_punct(phrase)

        (states, non) = self.ii_finder(phrase, self.s_ii)
        (districts, _) = self.ii_finder(phrase, self.d_ii)
        
        if districts == None or states == None:
            return None
        elif len(districts) == 0:
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

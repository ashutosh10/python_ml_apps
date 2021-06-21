from collections import Counter
from districtfinderapp.dictionary import model_dis_to_state
from googlesearch import search
import nltk
import re

cmnwords = ['co', 'org', 'net', 'of', 'html', 'com', 'in', 'www', 'http:', 'https:', 'pincode']  # Words to ignore from each search result url

class DistrictFinder:
    def simillarity(self, address, match):
        for i, a in enumerate(address):
            for m in match:
                if nltk.edit_distance(a, m) <= 2:
                    address[i] = m
        return address

    def get_result_json(self, address):
        dislist = model_dis_to_state.keys()
        wordlist = []

        if address:
            searchstr = address.split()
            searchstr = list(map((lambda x: x.lower()), searchstr))  # convert argument to lowercase
            wordlist = []
            for j in search(" ".join(searchstr), num_results=50):
                tmp = re.split("[/,_,\.,-]+", j)
                tmp = list(map(lambda x: x.lower(), tmp))
                tmp = list(filter((lambda x: x not in cmnwords + searchstr), tmp))

                wordlist = wordlist + tmp

            wordc = Counter(wordlist).most_common(10)  # get word frequencies of top 10 words
            wordc = [w[0] for w in wordc]

            correct_add = self.simillarity(searchstr, wordc)

            problist = []
            problist2 = None
            state = None
            data_2 = None
            # for i in sorted(wordc,key=wordc.get, reverse=True):
            for w in wordc:
                if w in dislist:
                    print("Probable distt is:", w.capitalize())
                    problist.append(w)

            if len(problist) == 1:  # if only one dist found in top 10, it is certain
                print("Final distt is:", problist[0].capitalize())
                state = model_dis_to_state[problist[0]].lower()
                print("Final state is:", state.capitalize())
            elif len(problist) > 1:
                print("Found more than 1 distt")
                print(problist)
                problist2 = problist[1]

            output = {}
            if len(problist) > 0:
                output['district'] = problist[0].capitalize()
                output['state'] = state.capitalize()
                correct_add = [x.capitalize() for x in correct_add]
                output['correct_add'] = ' '.join(correct_add) + ' ' + problist[0].capitalize() + ' ' + state.capitalize()

            return output


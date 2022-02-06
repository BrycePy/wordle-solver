from matplotlib.style import available
import words

words.answers.sort()

words_string = "".join(words.answers)

az = "abcdefghijklmnopqrstuvwxyz"
frequency = {c:words_string.count(c) for c in az}

sorted_freq = sorted(frequency.items(), key=lambda x: x[1])

for c, count in sorted_freq:
    print(c, count)

freq_string = "".join([x[0] for x in sorted_freq][::-1])

print(freq_string[:20])

available_0 = set(freq_string[:20])
for i1, word1 in enumerate(words.answers):
    available_1 = available_0.difference(set(word1))
    #print(available_1)
    if len(available_1)!=15: continue
    for i2, word2 in enumerate(words.answers[i1:]):
        available_2 = available_1.difference(set(word2))
        if len(available_2)!=10: continue
        for i3, word3 in enumerate(words.answers[i1+i2:]):
            available_3 = available_2.difference(set(word3))
            if len(available_3)!=5: continue
            for i4, word4 in enumerate(words.answers[i1+i2+i3:]):
                available_4 = available_3.difference(set(word4))
                if len(available_4)!=0: continue
                print(word1, word2, word3, word4)
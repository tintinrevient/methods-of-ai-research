import random, pandas

def distribution_baseline(sentences):

    sentence_act = []
    distribution = []

    for sentence in sentences:
        sentence = sentence.split(" ", )
        sentence_act.append(sentence[0])

    # Frequencies for each dialog act
    f1 = sentence_act.count('(ack)') / len(sentence_act)
    f2 = sentence_act.count('(affirm)') / len(sentence_act)
    f3 = sentence_act.count('(bye)') / len(sentence_act)
    f4 = sentence_act.count('(confirm)') / len(sentence_act)
    f5 = sentence_act.count('(deny)') / len(sentence_act)
    f6 = sentence_act.count('(hello)') / len(sentence_act)
    f7 = sentence_act.count('(inform)') / len(sentence_act)
    f8 = sentence_act.count('(negate)') / len(sentence_act)
    f9 = sentence_act.count('(null)') / len(sentence_act)
    f10 = sentence_act.count('(repeat)') / len(sentence_act)
    f11 = sentence_act.count('(reqalts)') / len(sentence_act)
    f12 = sentence_act.count('(reqmore)') / len(sentence_act)
    f13 = sentence_act.count('(request)') / len(sentence_act)
    f14 = sentence_act.count('(restart)') / len(sentence_act)
    f15 = sentence_act.count('(thankyou)') / len(sentence_act)

    # Data frame with the frequencies and dialog acts
    frequency = [['ack', f1], ['affirm', f2], ['bye', f3], ['confirm', f4], ['deny', f5], ['hello', f6],
                 ['inform', f7], ['negate', f8], ['null', f9], ['repeat', f10], ['reqalts', f11],
                 ['reqmore', f12], ['request', f13], ['restart', f14], [' thankyou', f15]]

    frequency = pandas.DataFrame(frequency, columns=['Act', 'Frequency'])

    frequency = frequency.sort_values('Frequency')

    # Cumulative frequency
    ascending_frequency = list(frequency['Frequency'])
    distribution.append(ascending_frequency[0])
    for i in range(1, len(ascending_frequency)):
        distribution.append(ascending_frequency[i] + distribution[i - 1])

    frequency.Frequency = distribution

    # Random number to select the dialog act
    r = random.random()

    for i in range(len(distribution)):
        if r <= distribution[i]:
            label = distribution[i]
            break

    # Find label of the selected dialog act and get the dialog act
    index_label = list(frequency['Frequency']).index(label)
    act = list(frequency['Act'])[index_label]

    return act

sentences = ["(bye) goodbye", "(inform) i want food", "(inform) i am looking for chinese"]

a = distribution_baseline(sentences)
print(a)

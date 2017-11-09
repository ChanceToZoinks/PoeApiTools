import matplotlib.pyplot as plt
import numpy as np
import PoeApiTools as pat
import json


def ClassRepComparison(useOldData=False, league='Harbinger'):
    ladderStats = None
    if useOldData:
        with open('previous_ladder_class_stats.json') as infile:
            ladderStats = json.load(infile)
    else:
        ladderStats = pat.GGGGetLadderClassCount(league=league)
    sortedLadderStats = dict(zip(sorted(ladderStats, key=ladderStats.get), sorted(ladderStats.values())))
    classes = list(sortedLadderStats.keys())
    truncatedClasses = []
    for i in classes:
        t = i[0:5]
        t += '\n{0}'.format("{:4.3f}".format(sortedLadderStats[i] / 15000))
        truncatedClasses.append(t)
    height = list(sortedLadderStats.values())
    yPos = np.arange(len(classes))

    plt.bar(yPos, height, align='center', alpha=.5)
    plt.xticks(yPos, truncatedClasses)
    plt.grid(b=True, which='major', color='black', linestyle='-', alpha=.1)
    plt.ylabel('Count')
    plt.title('{0} Ladder Ascendancy Representation'.format(league))

    plt.show()

    with open('previous_ladder_class_stats.json', 'w+') as outfile:
        json.dump(ladderStats, outfile, ensure_ascii=False, indent=4)


ClassRepComparison(useOldData=True)

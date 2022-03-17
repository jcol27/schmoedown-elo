from parsing import *
import json
from difflib import SequenceMatcher
from matplotlib import pyplot as plt
import datetime

def calc_elo():
    # Read input
    matches = {
        "singles":[],
        "teams":[],
        "innergeekdom":[],
        "starwars":[],
        "exhibition":[]
    }

    for k,v in parse_s1('./Data/season1.txt').items():
        matches[k] += v

    for k,v in parse_s2('./Data/season2.txt').items():
        matches[k] += v

    for x in range(3,9):
        for k,v in parse_s3_to_8(f'./Data/season{x}.txt').items():
            matches[k] += v

    print(matches)

    with open('matches.json', 'w+') as f:
        json.dump(matches, f, indent='    ')

    # Process elos
    elos = {
        "singles":{},
        "teams":{},
        "innergeekdom":{},
        "starwars":{}        
    }

    for k1,v1 in matches.items():
        if k1 is not 'exhibition':
            for count, match in enumerate(v1):
                date = match[0].strip()
                p1 = match[1].strip()
                p2 = match[2].strip()
                score = match[3].strip()
                winner = match[4].strip()

                winner = p1 if SequenceMatcher(None, p1, winner).ratio() > SequenceMatcher(None, p2, winner).ratio() else p2

                if p1 == '' or p2 == '':
                    pass
                else:
                    if p1 not in elos[k1].keys():
                        elos[k1][p1] = [(date, count, 1200, 350)]

                    if p2 not in elos[k1].keys():
                        elos[k1][p2] = [(date, count, 1200, 350)]

                    # update rating p1
                    si = 1 if winner == p1 else 0
                    r0 = elos[k1][p1][-1][2]
                    ri = elos[k1][p2][-1][2]
                    RD = elos[k1][p1][-1][3]
                    RDi = elos[k1][p2][-1][3]
                    gRDi = 1/((1+(3*(0.00575646273**2)*(RDi**2))/((3.14159**2))**0.5))
                    E = 1/(1+10**(gRDi*(r0-ri)*(1/-400)))
                    d2 = 1/((0.00575646273**2)*(gRDi**2)*E*(1-E))
                    elos[k1][p1].append([date, count, elos[k1][p1][-1][2] + (0.00575646283/(1/RD**2 + 1/d2)) * gRDi * (si - E), ((1/(RD**2) + 1/(d2))**-1)**0.5])

                    # update rating
                    si = 1 if winner == p2 else 0
                    r0 = elos[k1][p2][-1][2]
                    ri = elos[k1][p1][-1][2]
                    RD = elos[k1][p2][-1][3]
                    RDi = elos[k1][p1][-1][3]
                    gRDi = 1/((1+(3*(0.00575646273**2)*(RDi**2))/((3.14159**2))**0.5))
                    E = 1/(1+10**(gRDi*(r0-ri)*(1/-400)))
                    d2 = 1/((0.00575646273**2)*(gRDi**2)*E*(1-E))
                    elos[k1][p2].append((date, count, elos[k1][p2][-1][2] + (0.00575646283/(1/RD**2 + 1/d2)) * gRDi * (si - E), ((1/(RD**2) + 1/(d2))**-1)**0.5))

    print(elos)

    with open('elos.json', 'w+') as f:
        json.dump(elos, f, indent='    ')

    return elos

def plot_elos_dates(elos, N):
    fig, axs = plt.subplots(4,1)

    # singles
    nthsinglesrating = sorted([max([x[2] for x in playerdata]) for playerdata in elos['singles'].values()], reverse=True)[N]
    for playername, playerdata in elos['singles'].items():
        if len(playerdata) > 3 and max([x[2] for x in playerdata]) >= nthsinglesrating:
            axs[0].plot([datetime.datetime.strptime(data[0], r'%m/%d/%y') for data in playerdata], [data[2] for data in playerdata], label=playername, linewidth=2)

    # teams
    nthteamsrating = sorted([max([x[2] for x in playerdata]) for playerdata in elos['teams'].values()], reverse=True)[N]
    for playername, playerdata in elos['teams'].items():
        if len(playerdata) > 3 and max([x[2] for x in playerdata]) >= nthteamsrating:
            axs[1].plot([datetime.datetime.strptime(data[0], r'%m/%d/%y') for data in playerdata], [data[2] for data in playerdata], label=playername, linewidth=2)

    # innergeekdom
    nthinnergeekdomrating = sorted([max([x[2] for x in playerdata]) for playerdata in elos['innergeekdom'].values()], reverse=True)[N]
    for playername, playerdata in elos['innergeekdom'].items():
        if len(playerdata) > 3 and max([x[2] for x in playerdata]) >= nthinnergeekdomrating:
            axs[2].plot([datetime.datetime.strptime(data[0], r'%m/%d/%y') for data in playerdata], [data[2] for data in playerdata], label=playername, linewidth=2)

    # star wars
    nthstarwarsrating = sorted([max([x[2] for x in playerdata]) for playerdata in elos['starwars'].values()], reverse=True)[N]
    for playername, playerdata in elos['starwars'].items():
        if len(playerdata) > 3 and max([x[2] for x in playerdata]) >= nthstarwarsrating:
            axs[3].plot([datetime.datetime.strptime(data[0], r'%m/%d/%y') for data in playerdata], [data[2] for data in playerdata], label=playername, linewidth=2)

    # legends
    leg0 = axs[0].legend(bbox_to_anchor = (1.1, 1.0))
    leg1 = axs[1].legend(bbox_to_anchor = (1.1, 1.0))
    leg2 = axs[2].legend(bbox_to_anchor = (1.12, 1.0))
    leg3 = axs[3].legend(bbox_to_anchor = (1.11, 1.0))

    for leg in [leg0, leg1, leg2, leg3]:
        for line in leg.get_lines():
            line.set_linewidth(3.0)

    # axis labels
    for ax in axs:
        ax.set_xlabel('Date')
        ax.set_ylabel('Glicko Rating')
    
    # titles
    axs[0].set_title('Singles Division')
    axs[1].set_title('Teams Division')
    axs[2].set_title('Innergeekdom Division')
    axs[3].set_title('Star Wars Division')

    plt.subplots_adjust(hspace=0.4)

    #plt.show()
    fig.set_size_inches(30,20)
    plt.tight_layout()
    plt.savefig('glicko plot date.png', dpi=400)

def plot_elos_matches(elos, N):
    fig, axs = plt.subplots(4,1)

    # singles
    nthsinglesrating = sorted([max([x[2] for x in playerdata]) for playerdata in elos['singles'].values()], reverse=True)[N]
    for playername, playerdata in elos['singles'].items():
        if len(playerdata) > 3 and max([x[2] for x in playerdata]) >= nthsinglesrating:
            axs[0].plot([data[1] for data in playerdata], [data[2] for data in playerdata], label=playername, linewidth=2)

    # teams
    nthteamsrating = sorted([max([x[2] for x in playerdata]) for playerdata in elos['teams'].values()], reverse=True)[N]
    for playername, playerdata in elos['teams'].items():
        if len(playerdata) > 3 and max([x[2] for x in playerdata]) >= nthteamsrating:
            axs[1].plot([data[1] for data in playerdata], [data[2] for data in playerdata], label=playername, linewidth=2)

    # innergeekdom
    nthinnergeekdomrating = sorted([max([x[2] for x in playerdata]) for playerdata in elos['innergeekdom'].values()], reverse=True)[N]
    for playername, playerdata in elos['innergeekdom'].items():
        if len(playerdata) > 3 and max([x[2] for x in playerdata]) >= nthinnergeekdomrating:
            axs[2].plot([data[1] for data in playerdata], [data[2] for data in playerdata], label=playername, linewidth=2)

    # star wars
    nthstarwarsrating = sorted([max([x[2] for x in playerdata]) for playerdata in elos['starwars'].values()], reverse=True)[N]
    for playername, playerdata in elos['starwars'].items():
        if len(playerdata) > 3 and max([x[2] for x in playerdata]) >= nthstarwarsrating:
            axs[3].plot([data[1] for data in playerdata], [data[2] for data in playerdata], label=playername, linewidth=2)

    # legends
    leg0 = axs[0].legend(bbox_to_anchor = (1.1, 1.0))
    leg1 = axs[1].legend(bbox_to_anchor = (1.1, 1.0))
    leg2 = axs[2].legend(bbox_to_anchor = (1.12, 1.0))
    leg3 = axs[3].legend(bbox_to_anchor = (1.11, 1.0))

    for leg in [leg0, leg1, leg2, leg3]:
        for line in leg.get_lines():
            line.set_linewidth(3.0)

    # axis labels
    for ax in axs:
        ax.set_xlabel('Date')
        ax.set_ylabel('Glicko Rating')
    
    # titles
    axs[0].set_title('Singles Division')
    axs[1].set_title('Teams Division')
    axs[2].set_title('Innergeekdom Division')
    axs[3].set_title('Star Wars Division')

    plt.subplots_adjust(hspace=0.4)

    #plt.show()
    fig.set_size_inches(30,20)
    plt.tight_layout()
    plt.savefig('glicko plot match count.png', dpi=400)

if __name__ == '__main__':
    elos = calc_elo()
    plot_elos_dates(elos, 10)
    plot_elos_matches(elos, 10)
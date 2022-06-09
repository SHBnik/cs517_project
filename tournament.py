import numpy as np
import re
import random
from solver import vertex_cover

def getNodes(graph):
    nodes = []
    for n in graph.keys():
        nodes.append(n)
    for n2 in graph.values():
        if type(n2) == "string":
            nodes.append(n2)
        else:
            nodes += n2
    return np.unique(nodes).tolist()


def getEdges(graph, isDirected):
    edges = []
    for item in graph.items():
        for destination in item[1]:
            if (not isDirected):
                string1 = item[0] if item[0] < destination else destination
                string2 = destination if item[0] < destination else item[0]
            else:
                string1 = item[0]
                string2 = destination
            edges.append(string1 + string2)
    return np.unique(edges).tolist()

def getEdgesPair(graph, isDirected):
    edges = []
    for item in graph.items():
        for destination in item[1]:
            if (not isDirected):
                string1 = item[0] if item[0] < destination else destination
                string2 = destination if item[0] < destination else item[0]
            else:
                string1 = item[0]
                string2 = destination
            edges.append((string1,string2))
    return edges

class Player:
    def __init__(self, types, shorthand, roundNum, isCover=False):
        self.types = types
        self.shorthand = shorthand
        self.roundNum = roundNum
        self.isCover = isCover
    def self_introduce(self):
        return f'Player {self.shorthand} for round {self.roundNum}'

def buildPlayers(nodes, edges, covers):
    # objectives
    objectivelayer = [Player('objective', 'o', 1)]
    # nodes
    n = len(nodes)
    vertexplayers = [Player('vertex', 'v-0', 1)]
    for i in nodes:
        vertexplayers.append(Player('vertex', f'v-{i}', 1, i in covers))
    # edges
    m = len(edges)
    edgeplayers = []
    for j in edges:
        edgeplayers.append(Player('edge', f'e-{j}', 1))
    # filler
    k = len(covers)
    roundLimit1 = int(np.ceil(np.log(n-k)))
    fillerplayers = []
    for r in range(1, roundLimit1+1):
        for i in range(1,k+1):
            #for j in vertexplayers:
            fillerplayers.append(Player('filler', f'f^{r}_v#{i}', r))
    roundLimit2 = int(np.ceil(np.log(n-k)) + np.ceil(np.log(m)))
    for r in range(roundLimit1+1, roundLimit2+1):
        for i in range(1,k+1):
            #for j in edgeplayers:
            fillerplayers.append(Player('filler', f'f^{r}_e#{i}', r))
    # holder
    holderplayers = []
    for ei in edgeplayers:
        for l in range(0, 2**roundLimit1 - 1):
            holderplayers.append(Player('holder', f'h^{l}_{ei.shorthand}', 1))

    for fi in fillerplayers:
        fillerplayerR = fi.roundNum
        for l in range(0, 2**(fillerplayerR -1) -1):
            holderplayers.append(Player('holder', f'h^{l}_{fi.shorthand}', r))
    kfiller = 2**(roundLimit2 + int(np.ceil(np.log(k+1)))+1) - 1
    for l in range(0, kfiller):
        holderplayers.append(Player('holder', f'h^{l}_o', 1))
    return {
        'objectivePlayer': objectivelayer,
        'vertexPlayers': vertexplayers,
        'edgePlayers': edgeplayers,
        'fillerPlayers': fillerplayers,
        'holderPlayers': holderplayers
    }

def pair(p1, p2, r1, r2, matches):
    matches.append((p1, p2))
    if p1 in r1:
        r1.remove(p1)
    if p2 in r2:
        r2.remove(p2)

def matchingPhase1(playerList, r):
    seeds = []
    objective = playerList['objectivePlayer'][0]
    holderString = playerList['holderPlayers']
    remainingHolders = holderString.copy()

    vertexString = playerList['vertexPlayers']
    remainingVertices = vertexString.copy()

    edgeString = playerList['edgePlayers']
    remainingEdges = edgeString.copy()

    fillerString = playerList['fillerPlayers']
    remainingFillers = fillerString.copy()

    matchedPlayers = []
    for holderPlayer in holderString:
        if 'o' in holderPlayer.shorthand:
            seeds.append((objective, holderPlayer))
            remainingHolders.remove(holderPlayer)
            break
    holderString = remainingHolders.copy()
    for vertexPlayer in vertexString:
        if vertexPlayer.isCover:
            for fillerPlayer in fillerString:
                if (
                        "v" in fillerPlayer.shorthand and
                        fillerPlayer.roundNum == r and
                        fillerPlayer not in matchedPlayers and
                        vertexPlayer not in matchedPlayers
                    ):
                    pair(fillerPlayer, vertexPlayer, remainingFillers, remainingVertices, seeds)
                    matchedPlayers.append(fillerPlayer)
                    matchedPlayers.append(vertexPlayer)
        else:
            for vertexPlayer2 in remainingVertices:
                matchCountvertexPlayer2 = 0
                if (
                        vertexPlayer.shorthand != vertexPlayer2.shorthand and
                        not vertexPlayer2.isCover and
                        vertexPlayer2 not in matchedPlayers and
                        vertexPlayer not in matchedPlayers
                    ):
                    pair(vertexPlayer, vertexPlayer2, remainingVertices, remainingVertices, seeds)
                    matchedPlayers.append(vertexPlayer)
                    matchedPlayers.append(vertexPlayer2)
    fillerString = remainingFillers.copy()
    vertexString = remainingVertices.copy()

    for edgePlayer in edgeString:
        for holdPlayer in holderString:
            if (
                    edgePlayer.shorthand in holdPlayer.shorthand and
                    edgePlayer not in matchedPlayers and
                    holdPlayer not in matchedPlayers
                ):
                pair(edgePlayer, holdPlayer, remainingEdges, remainingHolders, seeds)
                matchedPlayers.append(edgePlayer)
                matchedPlayers.append(holdPlayer)
    holderString = remainingHolders.copy()
    edgeString = remainingEdges.copy()

    for fillerPlayer in fillerString:
        for holdPlayer in holderString:
            if (
                    fillerPlayer.shorthand in holdPlayer.shorthand and
                    fillerPlayer not in matchedPlayers and
                    holdPlayer not in matchedPlayers
                ):
                pair(fillerPlayer, holdPlayer, remainingFillers, remainingHolders, seeds)
                matchedPlayers.append(fillerPlayer)
                matchedPlayers.append(holdPlayer)
    holderString = remainingHolders.copy()
    fillerString = remainingFillers.copy()

    for holderPlayer in holderString:
        for holderPlayer2 in remainingHolders:
            holderPlayerName = holderPlayer.shorthand
            holderPlayer2Name = holderPlayer2.shorthand
            if (
                    'f' in holderPlayerName and
                    'f' in holderPlayer2Name and
                    holderPlayerName != holderPlayer2Name and
                    list(holderPlayerName)[3:] == list(holderPlayer2Name)[3:] and
                    holderPlayer not in matchedPlayers and
                    holderPlayer2 not in matchedPlayers
                ):
                pair(holderPlayer, holderPlayer2, remainingHolders, remainingHolders, seeds)
                matchedPlayers.append(holderPlayer)
                matchedPlayers.append(holderPlayer2)

            if (
                    'e' in holderPlayerName and
                    'e' in holderPlayer2Name and
                    holderPlayerName != holderPlayer2Name and
                    list(holderPlayerName)[3:] == list(holderPlayer2Name)[3:] and
                    holderPlayer not in matchedPlayers and
                    holderPlayer2 not in matchedPlayers
                ):
                pair(holderPlayer, holderPlayer2, remainingHolders, remainingHolders, seeds)
                matchedPlayers.append(holderPlayer)
                matchedPlayers.append(holderPlayer2)
    holderString = remainingHolders.copy()
    #straggers:
    remainings = remainingFillers + remainingHolders + remainingEdges + remainingVertices;
    while len(remainings) >= 2:
        selectPairs = random.sample(remainings, 2)
        pair(selectPairs[0], selectPairs[1], remainings, remainings, seeds)
#     print('seeds:', len(seeds))
#     print('remainings:',len(remainings))
    return seeds

def decider(player1, player2):
    #print(f'{player1.self_introduce()} vs. {player2.self_introduce()}')
    type1 = player1.types
    type2 = player2.types
    if type1 == 'objective':
        if type2 == 'vertex':
            return player1
        elif type2 == 'edge':
            return player2
        elif type2 == 'filler':
            return player2
        elif type2 == 'holder':
            if 'o' in player2.shorthand:
                return player1
            else:
                return player2

    elif type1 == 'vertex':
        if type2 == 'vertex':
            if player1.shorthand < player2.shorthand:
                return player1
            else:
                return player2
        elif type2 == 'edge':
            vertice = re.search(r"v-(\w+)", player1.shorthand).group(1)
            edge = re.search(r"e-(\w+)", player2.shorthand).group(1)
            if vertice in edge:
                return player1
            else:
                return player2
        elif type2 == 'filler':
            return player1
        elif type2 == 'holder':
            return player2
        elif type2 == 'objective':
            return player2

    elif type1 == 'edge':
        if type2 == 'vertex':
            vertice = re.search(r"v-(\w+)", player1.shorthand).group(1)
            edge = re.search(r"e-(\w+)", player2.shorthand).group(1)
            if vertice in edge:
                return player2
            else:
                return player1
        elif type2 == 'edge':
            return random.choice([player1, player2])
        elif type2 == 'filler':
            return random.choice([player1, player2])
        elif type2 == 'holder':
            if 'e-' in player2.shorthand:
                if player1.shorthand in player2.shorthand:
                    return player1
                else:
                    return random.choice([player1, player2])
            else:
                return player2
        elif type2 == 'objective':
            return player1

    elif type1 == 'filler':
        if type2 == 'vertex':
            return player2
        elif type2 == 'edge':
            return random.choice([player1, player2])
        elif type2 == 'filler':
            return random.choice([player1, player2])
        elif type2 == 'holder':
            if 'e-' in player2.shorthand:
                return random.choice([player1, player2])
            elif  'o' in player2.shorthand or  player1.shorthand in player2.shorthand:
                return player1
            else:
                return random.choice([player1, player2])
        elif type2 == 'objective':
            return player1

    elif type1 == 'holder':
        if 'e-' in player1.shorthand:
            if type2 == 'vertex':
                return player1
            elif type2 == 'edge':
                if player2.shorthand in player1.shorthand:
                    return player2
                else:
                    return random.choice([player1, player2])
            elif type2 == 'filler':
                return random.choice([player1, player2])
            elif type2 == 'holder':
                if 'o' in player2.shorthand:
                    return player1
                else:
                    return random.choice([player1, player2])
            elif type2 == 'objective':
                return player1
        elif 'f^' in player1.shorthand:
            if type2 == 'vertex':
                return player1
            elif type2 == 'edge':
                return player2
            elif type2 == 'filler':
                if player2.shorthand in player1.shorthand:
                    return player2
                else:
                    return random.choice([player1, player2])
            elif type2 == 'holder':
                if 'o' in player2.shorthand:
                    return player1
                else:
                    return random.choice([player1, player2])
            elif type2 == 'objective':
                return player1
        elif 'o' in player1.shorthand:
            if type2 == 'vertex':
                return player1
            elif type2 == 'edge':
                return player2
            elif type2 == 'filler':
                return player2
            elif type2 == 'holder':
                if 'o' in player2.shorthand:
                    return random.choice([player1, player2])
                else:
                    return player2
            elif type2 == 'objective':
                return player2

def getRoundResult(r):
    result = {
        'objectivePlayer': [],
        'vertexPlayers': [],
        'edgePlayers': [],
        'fillerPlayers': [],
        'holderPlayers': []
    }
    for match in r:
        matchResult = decider(match[0], match[1])
        if matchResult.types == 'vertex':
            result['vertexPlayers'].append(matchResult)
        elif matchResult.types == 'edge':
            result['edgePlayers'].append(matchResult)
        elif matchResult.types == 'filler':
            result['fillerPlayers'].append(matchResult)
        elif matchResult.types == 'objective':
            result['objectivePlayer'].append(matchResult)
        elif matchResult.types == 'holder':
            result['holderPlayers'].append(matchResult)
    return result

def matchingPhase2(playerList, r, nodes, edges, covers):
    seeds = []
    objective = playerList['objectivePlayer'][0]
    holderString = playerList['holderPlayers']
    remainingHolders = holderString.copy()

    vertexString = playerList['vertexPlayers']
    remainingVertices = vertexString.copy()

    edgeString = playerList['edgePlayers']
    remainingEdges = edgeString.copy()

    fillerString = playerList['fillerPlayers']
    remainingFillers = fillerString.copy()

    matchedPlayers = []
    for vertexPlayer in vertexString:
        for edgePlayer in edgeString:
            vertice = re.search(r"v-(\w+)", vertexPlayer.shorthand).group(1)
            edge = re.search(r"e-(\w+)", edgePlayer.shorthand).group(1)
            if vertice in edge and not vertexPlayer in matchedPlayers and not edgePlayer in matchedPlayers:
                pair(vertexPlayer, edgePlayer, remainingVertices, remainingEdges, seeds)
                matchedPlayers.append(vertexPlayer)
                matchedPlayers.append(edgePlayer)
    vertexString = remainingVertices.copy()
    edgeString = remainingEdges.copy()
    #pair remaining vertex with a filler
    for vertexPlayer in vertexString:
        for fillerPlayer in fillerString:
            if not vertexPlayer in matchedPlayers and not fillerPlayer in matchedPlayers:
                pair(vertexPlayer, fillerPlayer, remainingVertices, remainingFillers, seeds)
                matchedPlayers.append(vertexPlayer)
                matchedPlayers.append(fillerPlayer)
    vertexString = remainingVertices.copy()
    fillerString = remainingFillers.copy()

    for edgePlayer in edgeString:
        for edgePlayer2 in remainingEdges:
            if checkStringShare(edgePlayer.shorthand, edgePlayer2.shorthand) and edgePlayer.shorthand != edgePlayer2.shorthand:
                pair(edgePlayer, edgePlayer2, remainingEdges, remainingEdges, seeds)
                matchedPlayers.append(edgePlayer)
                matchedPlayers.append(edgePlayer2)
    edgeString = remainingEdges.copy()

    for fillerPlayer in fillerString:
        for holderPlayer in holderString:
            if (
                    fillerPlayer.shorthand in holderPlayer.shorthand and
                    fillerPlayer not in matchedPlayers and
                    holderPlayer not in matchedPlayers
                ):
                pair(fillerPlayer, holderPlayer, remainingFillers, remainingHolders, seeds)
                matchedPlayers.append(fillerPlayer)
                matchedPlayers.append(holderPlayer)
    fillerString = remainingFillers.copy()
    holderString = remainingHolders.copy()

    #pair remaining edges
    for edgePlayer in edgeString:
        for fillerPlayer in fillerString:
            if (
                    'e' in fillerPlayer.shorthand and
                    edgePlayer not in matchedPlayers and
                    fillerPlayer not in matchedPlayers
                ):
                pair(edgePlayer, fillerPlayer, remainingEdges, remainingFillers, seeds)
                matchedPlayers.append(edgePlayer)
                matchedPlayers.append(fillerPlayer)
    edgeString = remainingEdges.copy()
    fillerString = remainingFillers.copy()

    for holderPlayer in holderString:
        if 'o' in holderPlayer.shorthand:
            seeds.append((objective, holderPlayer))
            remainingHolders.remove(holderPlayer)
            break
    holderString = remainingHolders.copy()
    #straggers:
    remainings = remainingFillers + remainingHolders + remainingEdges + remainingVertices;
    for p1 in remainings:
        for p2 in remainings:
            if (p1.types == "edge"):
                if (
                        p2.types == 'filler' and 'e' in p2.shorthand and
                        p1 not in matchedPlayers and
                        p2 not in matchedPlayers
                    ):
                    pair(p1,p2, remainings, remainings, seeds)
                    matchedPlayers.append(p1)
                    matchedPlayers.append(p2)
    while len(remainings) >= 2:
        selectPairs = random.sample(remainings, 2)
        pair(selectPairs[0], selectPairs[1], remainings, remainings, seeds)
    return seeds

def matchingFinal(playerList):
    objective = playerList['objectivePlayer']
    vertexString = playerList['vertexPlayers']
    holderString = playerList['holderPlayers']
    seeds = []
    remainings = objective + vertexString + holderString
    while len(remainings) >= 2:
        selectPairs = random.sample(remainings, 2)
        pair(selectPairs[0], selectPairs[1], remainings, remainings, seeds)
    return seeds

def bracketMaker(p, nodes, edges, covers):
    #phase1
    n = len(nodes)
    m = len(edges)
    k = len(covers)
    pri = p
    playerNums = int(np.sum([
        len(p['objectivePlayer']),
        len(p['vertexPlayers']),
        len(p['edgePlayers']),
        len(p['fillerPlayers']),
        len(p['holderPlayers'])
    ]))
    bracket = {}
    for i in range(1, int(np.ceil(np.log(n-k)))+1):
        ri = matchingPhase1(pri, i)
        pri = getRoundResult(ri)
        bracket[f'round{i}'] = ri
    #phase2
    for j in range(int(np.ceil(np.log(n-k)))+1,int(np.ceil(np.log(m)) + np.ceil(np.log(k+1)) + 1 +1)):
        rj = matchingPhase2(pri, j, nodes, edges, covers)
        pri = getRoundResult(rj)
        bracket[f'round{j}'] = rj
    #final
    for f in range(int(np.ceil(np.log(m)) + np.ceil(np.log(k+1)) + 1 +1), int(np.log2(playerNums) + 1)):
        rf = matchingFinal(pri)
        pri = getRoundResult(rf)
        bracket[f'round{f}'] = rf
    return bracket

def checkStringShare(str1, str2):
    joinString = str1 + str2
    charArray = list(joinString)
    newArray = np.unique(charArray)
    if len(newArray) < len(charArray):
        return True
    return False

def bracketGenerator(graph):
    chosenGraph = graph
    nodes = getNodes(chosenGraph)
    edges = getEdges(chosenGraph, False)
    edgesPair = getEdgesPair(chosenGraph, False)
    covers = vertex_cover(nodes, edgesPair) #put solver
    players = buildPlayers(nodes, edges, covers)
    #rounds of number of players
    def getFullPlayers(playerNums):
        n = 0
        stopFlag = False
        while (not stopFlag):
            if playerNums > 2**n:
                n += 1
            else:
                stopFlag = True
        return 2**n
    def fillPlayers(playersList):
        playerNums = np.sum([
            len(playersList['objectivePlayer']),
            len(playersList['vertexPlayers']),
            len(playersList['edgePlayers']),
            len(playersList['fillerPlayers']),
            len(playersList['holderPlayers'])
        ])
        if getFullPlayers(playerNums) > playerNums:
            for i in range(0, getFullPlayers(playerNums) - playerNums):
                players['holderPlayers'].append(Player('holder', f'h^{i}_o_ammend', 1))
        return playersList
    players = fillPlayers(players)
    tour = bracketMaker(players, nodes, edges, covers)
    return tour


def bracketGenerator2(nodes, edgesPair):
    covers = vertex_cover(nodes, edgesPair) #put solver
    players = buildPlayers(nodes, edges, covers)
    #rounds of number of players
    def getFullPlayers(playerNums):
        n = 0
        stopFlag = False
        while (not stopFlag):
            if playerNums > 2**n:
                n += 1
            else:
                stopFlag = True
        return 2**n
    def fillPlayers(playersList):
        playerNums = np.sum([
            len(playersList['objectivePlayer']),
            len(playersList['vertexPlayers']),
            len(playersList['edgePlayers']),
            len(playersList['fillerPlayers']),
            len(playersList['holderPlayers'])
        ])
        if getFullPlayers(playerNums) > playerNums:
            for i in range(0, getFullPlayers(playerNums) - playerNums):
                players['holderPlayers'].append(Player('holder', f'h^{i}_o_ammend', 1))
        return playersList
    players = fillPlayers(players)
    tour = bracketMaker(players, nodes, edges, covers)
    return tour

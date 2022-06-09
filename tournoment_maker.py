

teams_out = []
tournament = []



def countwin(team,matrix):
    win = 0
    P_index = matrix[0].index(team) + 1
    for j in range(1,len(matrix[P_index])):
        if matrix[0][j-1] == team: continue
        if matrix[P_index][j] == 1: 
            win+=1              
    return win

def pass_winner_teams(team,matrix):
    winners = []
    P_index = matrix[0].index(team) + 1
    for j in range(1,len(matrix[P_index])):
        if matrix[0][j-1] == team: continue
        if matrix[P_index][j] == 1: 
            winners.append([matrix[0][j-1],countwin(matrix[0][j-1],matrix) * 100])
            
        if matrix[P_index][j] == 0.5:
            winners.append([matrix[0][j-1],countwin(matrix[0][j-1],matrix)])
    winners.sort(key = lambda x: x[1],reverse=True)
    return winners


def make_strongest_losser(winner_team,p,round):
    global teams_out,bracket
    #is this the first seed ? 
    if(not round):return
    
    #find team
    teams = pass_winner_teams(winner_team,p)
    oppenent = None
    #did he played before ? 
    for team,score in teams:
        try:
            teams_out.index(team)
        except Exception as e:
            oppenent = team
            teams_out.append(team)
            # print(winner_team,team)
            break

    tournament[round-1].append((winner_team,oppenent))
    # if round == 1: 
    #     print('seed',winner_team,team)
    make_strongest_losser(winner_team,p,round-1)
    make_strongest_losser(oppenent,p,round-1)
    



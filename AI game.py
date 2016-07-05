import sys
import copy

player = ''
cutting_depth = 0
current_positions_list = []
points_list = []
value_i = 0
value_j = 0
stable_player = ''
level = 0
alphabeta_i = 0
alphabeta_j = 0
minimax_i = 0
minimax_j = 0
greedy_i = 0
greedy_j = 0
minimax_case = True
alphabeta_case = True
opponent=''
opponent_algorithm = 0
opponent_depth = 0
current_positions_list_1 = []
current_positions_list_change =[]


def check_end_state(current_positions_list):
    for i in range(5):  # changed form 5
        for j in range(5):
            if current_positions_list[i][j] == '*':
                return False
    return True

def check(i, j, current_positions_list, player):
    if i < 0 or j < 0 or j > 4 or i > 4:  # changed from 4
        return 0
    elif current_positions_list[i][j] == player:
        return 1
    else:
        return 0

def change_state(i, j, current_positions_list, player):
    if i < 0 or j < 0 or j > 4 or i > 4:  # changed from 4
        return 3
    if current_positions_list[i][j] == player:
        return 0
    if current_positions_list[i][j] == '*':
        return 2
    current_positions_list[i][j] = player
    return 1

def calculate_previous_state(current_positions_list, track_list, i, j, player):
    if track_list[0] == 1:
        if current_positions_list[i][j + 1] == 'X':
            current_positions_list[i][j + 1] = 'O'
        else:
            current_positions_list[i][j + 1] = 'X'
    if track_list[1] == 1:
        if current_positions_list[i + 1][j] == 'X':
            current_positions_list[i + 1][j] = 'O'
        else:
            current_positions_list[i + 1][j] = 'X'
    if track_list[2] == 1:
        if current_positions_list[i - 1][j] == 'X':
            current_positions_list[i - 1][j] = 'O'
        else:
            current_positions_list[i - 1][j] = 'X'
    if track_list[3] == 1:
        if current_positions_list[i][j - 1] == 'X':
            current_positions_list[i][j - 1] = 'O'
        else:
            current_positions_list[i][j - 1] = 'X'

def convert_To_Infinity(alpha,beta):
    if alpha == -float('inf'):
        alpha = '-Infinity'
    if beta == float('inf'):
        beta = 'Infinity'
    if alpha == float('inf'):
        alpha = 'Infinity'
    if beta == -float('inf'):
        beta = '-Infinity'
    return str(alpha)+','+str(beta)

def calculate_final_state(current_positions_list, i, j, check_raid, player):
    current_positions_list[i][j] = player
    if check_raid == 1:
        change_state(i, j + 1, current_positions_list, player)
        change_state(i + 1, j, current_positions_list, player)
        change_state(i - 1, j, current_positions_list, player)
        change_state(i, j - 1, current_positions_list, player)

class Game:
    def __init__(self, player, cutting_depth, current_positions_list, parent,i,j,alpha,beta):
        self.i = i
        self.j = j
        self.alpha = alpha
        self.beta = beta
        self.parent = parent
        self.player = player
        self.cutting_depth = cutting_depth
        self.current_positions_list = copy.deepcopy(current_positions_list)
        self.eval_value = self.calculate_eval_value(self.current_positions_list, points_list, stable_player)

    def GreedyBestFirstSearch(self):
        global greedy_i
        global greedy_j
        max_eval_value = -9999999
        max_i = 0
        max_j = 0
        for i in range(5):
            for j in range(5):
                if self.current_positions_list[i][j] == "*":

                    temp_object = copy.deepcopy(self)

                    is_raid = temp_object.isRaid(temp_object.current_positions_list, i, j, temp_object.player)

                    if is_raid == 1:

                        raided_state = temp_object.calculate_next_raid_state(temp_object.current_positions_list, i, j, temp_object.player)
                        eval_value = temp_object.calculate_eval_value(raided_state.current_positions_list, points_list, temp_object.player)

                        if eval_value > max_eval_value:
                            max_eval_value = eval_value
                            max_i = i
                            max_j = j

                    else:

                        sneaked_state = temp_object.calculate_next_sneak_state(temp_object.current_positions_list, i, j, temp_object.player)
                        eval_value = temp_object.calculate_eval_value(sneaked_state.current_positions_list, points_list, temp_object.player)

                        if eval_value > max_eval_value:
                            max_eval_value = eval_value
                            max_i = i
                            max_j = j

        greedy_i = max_i
        greedy_j = max_j


    def MinMax(self, depth, fo):
        global level
        global minimax_i
        global minimax_j
        global minimax_case
        tempi = 0
        tempj = 0

        if depth%2 == 0:
            eval_value = -float('inf')
        elif depth%2 != 0:
            eval_value = float('inf')

        if level == 0:
            minimax_case = False
        elif depth == level:
            if not fo is None:
                fo.write(chr(self.j + ord('A')) + str(self.i + 1) + ',' + str(depth) + ','+ str(self.eval_value)+'\n')
            return self.eval_value
        elif self.check_Game(self.current_positions_list):
            if not fo is None:
                fo.write(chr(self.j + ord('A')) + str(self.i + 1) + ',' + str(depth) + ','+ str(self.eval_value)+'\n')
            if self.i == 100 and self.j == 100:
                minimax_case = False
            return self.eval_value
        else:

            if self.i == 100 and self.j == 100:
                if not fo is None:
                    if eval_value == float('inf'):
                        fo.write('root,0,Infinity\n')
                    elif eval_value == -float('inf'):
                        fo.write('root,0,-Infinity\n')
                    else:
                        fo.write('root,0,'+str(eval_value)+'\n')

            else:
                if not fo is None:
                    if eval_value == float('inf'):
                        fo.write(chr(self.j + ord('A')) + str(self.i + 1) + ',' + str(depth) + ','+ 'Infinity\n')
                    elif eval_value == -float('inf'):
                        fo.write(chr(self.j + ord('A')) + str(self.i + 1) + ',' + str(depth) + ','+ '-Infinity\n')
                    else:
                        fo.write(chr(self.j + ord('A')) + str(self.i + 1) + ',' + str(depth) + ','+ str(eval_value)+'\n')

            for i in range(5):
                for j in range(5):
                    if self.current_positions_list[i][j] == "*":

                        temp_object = copy.deepcopy(self)
                        temp_object.i = i
                        temp_object.j = j
                        is_raid = temp_object.isRaid(temp_object.current_positions_list, i, j, temp_object.player)
                        if is_raid == 1:

                            raided_state = temp_object.calculate_next_raid_state(temp_object.current_positions_list, i,j, temp_object.player)
                            temp_object = raided_state

                        else:

                            sneaked_state = temp_object.calculate_next_sneak_state(temp_object.current_positions_list,i, j, temp_object.player)
                            temp_object = sneaked_state


                        if temp_object.player == stable_player:

                            if temp_object.player == 'X':
                                temp_object.player = 'O'
                            else:
                                temp_object.player = 'X'

                            abcd = temp_object.MinMax(depth + 1,fo)

                            if depth%2 == 0:
                                if abcd>eval_value:
                                    eval_value = abcd
                                    tempi = i
                                    tempj = j

                            elif depth%2 !=0:
                                if abcd<eval_value:
                                    tempi = i
                                    tempj = j
                                    eval_value = abcd
                            if not fo is None:
                                if self.i == 100 and self.j == 100:
                                    fo.write('root,' + str(depth) + ','+ str(eval_value)+'\n')
                                else:
                                    fo.write(chr(self.j + ord('A')) + str(self.i + 1) + ',' + str(depth) + ','+ str(eval_value)+'\n')

                        else:
                            if temp_object.player == 'X':
                                temp_object.player = 'O'
                            else:
                                temp_object.player = 'X'

                            abcd = temp_object.MinMax(depth + 1,fo)

                            if depth%2 == 0:
                                if abcd>eval_value:
                                    tempi = i
                                    tempj = j
                                    eval_value = abcd
                            elif depth%2 !=0:
                                if abcd<eval_value:

                                    tempi = i
                                    tempj = j

                                    eval_value = abcd
                            if not fo is None:
                                if self.i == 100 and self.j == 100:
                                    fo.write('root,' + str(depth) + ','+ str(eval_value)+'\n')
                                else:
                                    fo.write(chr(self.j + ord('A')) + str(self.i + 1) + ',' + str(depth) + ','+ str(eval_value)+'\n')

            minimax_i = tempi
            minimax_j = tempj
            return eval_value

    def AlphaBetaPruning(self, depth,fo):
        global level
        global alphabeta_i
        global alphabeta_j
        global alphabeta_case
        alphabetaflag = True
        tempi = 0
        tempj = 0

        if depth%2 == 0:
            eval_value = -float('inf')
        elif depth%2 != 0:
            eval_value = float('inf')

        if level == 0:
            alphabeta_case = False
        elif int(depth) == int(level):
            if not fo is None:
                fo.write(chr(self.j + ord('A')) + str(self.i + 1) + ',' + str(depth) + ','+ str(self.eval_value)+','+convert_To_Infinity(self.alpha,self.beta)+'\n')
            return self.eval_value
        elif self.check_Game(self.current_positions_list):
            if not fo is None:
                fo.write(chr(self.j + ord('A')) + str(self.i + 1) + ',' + str(depth) + ','+ str(self.eval_value)+','+convert_To_Infinity(self.alpha,self.beta)+'\n')
            if self.i == 100 and self.j == 100:
                alphabeta_case = False
            return self.eval_value
        else:

            if self.i == 100 and self.j == 100:
                if not fo is None:
                    if eval_value == float('inf'):
                        fo.write('root,0,Infinity,-Infinity,Infinity\n')
                    elif eval_value == -float('inf'):
                        fo.write('root,0,-Infinity,-Infinity,Infinity\n')
                    else:
                        fo.write('root,0,'+str(eval_value)+'\n')

            else:
                if not fo is None:
                    if eval_value == float('inf'):
                        fo.write(chr(self.j + ord('A')) + str(self.i + 1) + ',' + str(depth) + ','+ 'Infinity,'+convert_To_Infinity(self.alpha,self.beta)+'\n')
                    elif eval_value == -float('inf'):
                        fo.write(chr(self.j + ord('A')) + str(self.i + 1) + ',' + str(depth) + ','+ '-Infinity,'+convert_To_Infinity(self.alpha,self.beta)+'\n')
                    else:
                        #print 'depth check', depth
                        fo.write(chr(self.j + ord('A')) + str(self.i + 1) + ',' + str(depth) + ','+ str(eval_value)+','+convert_To_Infinity(self.alpha,self.beta)+'\n')

            for i in range(5):
                if alphabetaflag:
                    for j in range(5):
                        if self.current_positions_list[i][j] == "*":

                            temp_object = copy.deepcopy(self)

                            is_raid = temp_object.isRaid(temp_object.current_positions_list, i, j, temp_object.player)
                            if is_raid == 1:

                                raided_state = temp_object.calculate_next_raid_state(temp_object.current_positions_list, i,j, temp_object.player)
                                temp_object = raided_state

                            else:

                                sneaked_state = temp_object.calculate_next_sneak_state(temp_object.current_positions_list,i, j, temp_object.player)
                                temp_object = sneaked_state


                            if temp_object.player == stable_player:

                                if temp_object.player == 'X':
                                    temp_object.player = 'O'
                                else:
                                    temp_object.player = 'X'

                                abcd = temp_object.AlphaBetaPruning(depth+1,fo)

                                if depth%2 == 0:
                                    if abcd>eval_value:
                                        eval_value = abcd
                                        tempi = i
                                        tempj = j

                                    if abcd>=self.beta:
                                        alphabetaflag = False
                                        break

                                    if abcd > self.alpha:
                                        self.alpha = abcd

                                elif depth%2 !=0:
                                    if abcd<eval_value:
                                        tempi = i
                                        tempj = j
                                        eval_value = abcd

                                    if self.alpha>=abcd:
                                        alphabetaflag = False
                                        break


                                    if abcd < self.beta:
                                        self.beta = abcd

                                if not fo is None:
                                    if self.i == 100 and self.j == 100:
                                        fo.write('root,' + str(depth) + ','+ str(eval_value)+','+convert_To_Infinity(self.alpha,self.beta)+'\n')
                                    else:
                                        print 'depth check', depth
                                        fo.write(chr(self.j + ord('A')) + str(self.i + 1) + ',' + str(depth) + ','+ str(eval_value)+','+convert_To_Infinity(self.alpha,self.beta)+'\n')

                            else:
                                if temp_object.player == 'X':
                                    temp_object.player = 'O'
                                else:
                                    temp_object.player = 'X'

                                abcd = temp_object.AlphaBetaPruning(depth+1,fo)

                                if depth%2 == 0:
                                    if abcd>eval_value:
                                        tempi = i
                                        tempj = j
                                        eval_value = abcd

                                    if abcd>=self.beta:
                                        alphabetaflag = False
                                        break

                                    if abcd > self.alpha:
                                        self.alpha = abcd

                                elif depth%2 !=0:
                                    if abcd<eval_value:
                                        tempi = i
                                        tempj = j
                                        eval_value = abcd

                                    if self.alpha>=abcd:
                                        alphabetaflag = False
                                        break

                                    if abcd < self.beta:
                                        self.beta = abcd
                                if not fo is None:
                                    if self.i == 100 and self.j == 100:
                                       fo.write('root,' + str(depth) + ','+ str(eval_value)+','+convert_To_Infinity(self.alpha,self.beta)+'\n')
                                    else:
                                        print 'depth check', depth
                                        fo.write(chr(self.j + ord('A')) + str(self.i + 1) + ',' + str(depth) + ','+ str(eval_value)+','+convert_To_Infinity(self.alpha,self.beta)+'\n')
                else:
                    break
            if not alphabetaflag:
                if self.i!=100 and self.j!=100:
                    if not fo is None:
                        fo.write(chr(self.j + ord('A')) + str(self.i + 1) + ',' + str(depth) + ','+ str(eval_value)+','+convert_To_Infinity(self.alpha,self.beta)+'\n')
                    else:
                        fo.write('root,0,'+str(eval_value)+'\n')

            alphabeta_i = tempi
            alphabeta_j = tempj
            return eval_value


    def isRaid(self, current_positions_list, i, j, player):
        a = check(i, j + 1, current_positions_list, player)
        b = check(i + 1, j, current_positions_list, player)
        c = check(i - 1, j, current_positions_list, player)
        d = check(i, j - 1, current_positions_list, player)
        if a == 1 or b == 1 or c == 1 or d == 1:
            return 1
        else:
            return 0

    def calculate_next_raid_state(self, current_positions_list, i, j, player):
        current_positions_list[i][j] = player
        change_state(i, j + 1, current_positions_list, player)
        change_state(i + 1, j, current_positions_list, player)
        change_state(i - 1, j, current_positions_list, player)
        change_state(i, j - 1, current_positions_list, player)
        raided_state = Game(self.player, self.cutting_depth, current_positions_list,self.parent,i,j,self.alpha,self.beta)

        return raided_state

    def calculate_next_sneak_state(self, current_positions_list, i, j, player):
        current_positions_list[i][j] = player
        sneaked_state = Game(self.player, self.cutting_depth, current_positions_list,self.parent,i,j,self.alpha,self.beta)

        return sneaked_state

    def check_Game(self, current_positions_list):
        for i in range(5):  # changed form 5
            for j in range(5):
                if current_positions_list[i][j] == '*':
                    return False
        return True

    def calculate_eval_value(self, current_positions_list, points_list, stable_player):
        X_score = 0
        O_score = 0
        for i in range(5):  # changed from 5
            for j in range(5):
                if current_positions_list[i][j] == 'X':
                    X_score += points_list[i][j]
                if current_positions_list[i][j] == 'O':
                    O_score += points_list[i][j]

        if stable_player == 'X':
            return X_score - O_score
        else:
            return O_score - X_score


def main():
    global stable_player
    global points_list
    global alphabeta_i
    global alphabeta_j
    global minimax_j
    global minimax_i
    global minimax_case
    global greedy_i
    global greedy_j
    global level
    global current_positions_list_1
    algorithm = 0
    current_positions_list = []

    fh = open(sys.argv[2], 'r')
    #fh = open('input.txt', 'r')

    i = 1
    for line in fh:
        words = line.rstrip().split()
        if i == 1:
            algorithm = int(words[0])
            if algorithm == 4:
                break
        elif i == 2:
            player = words[0]
            stable_player = player
        elif i == 3:
            cutting_depth = int(words[0])
            level = cutting_depth

        elif 3 < i <= 8:
            temp_points_list = []
            for word in words:
                temp_points_list.append(int(word))
            points_list.append(temp_points_list)
        else:
            word = list(line.strip('\n'))
            current_positions_list.append(word)
        i += 1

    if algorithm == 1:

        greedy_best_first = Game(player, cutting_depth, current_positions_list,0,0,0,0,0)

        fo = open('next_state.txt', 'w')

        if level!= 0:
            greedy_best_first.GreedyBestFirstSearch()

            is_raid = greedy_best_first.isRaid(current_positions_list, greedy_i, greedy_j, stable_player)

            if is_raid == 1:
                calculate_final_state(current_positions_list, greedy_i, greedy_j, 1, stable_player)
            else:
                calculate_final_state(current_positions_list, greedy_i, greedy_j, 0, stable_player)

        for position in current_positions_list:
            fo.write('%s' % ''.join(map(str, position))+'\n')

        fo.close()

    elif algorithm == 2:

        minimax = Game(player, cutting_depth, current_positions_list,'root',100,100,0,0)

        fo = open('traverse_log.txt', 'w')
        fo1 = open('next_state.txt','w')

        fo.write('Node,Depth,Value\n')

        minimax.MinMax(0,fo)

        is_raid = minimax.isRaid(current_positions_list, minimax_i, minimax_j, stable_player)
        if minimax_case:
            if is_raid == 1:
                calculate_final_state(current_positions_list, minimax_i, minimax_j, 1, stable_player)
            else:
                calculate_final_state(current_positions_list, minimax_i, minimax_j, 0, stable_player)

        for position in current_positions_list:
            fo1.write('%s' % ''.join(map(str, position))+'\n')
        fo.close()
        fo1.close()

    elif algorithm == 3:

        alphabetapruning = Game(player, cutting_depth, current_positions_list,'root',100,100,float('-inf'),float('inf'))


        fo1 = open('next_state.txt','w')
        fo = open('traverse_log.txt', 'w')

        fo.write('Node,Depth,Value,Alpha,Beta\n')

        alphabetapruning.AlphaBetaPruning(0,fo)

        is_raid = alphabetapruning.isRaid(current_positions_list, alphabeta_i, alphabeta_j, stable_player)
        if alphabeta_case:
            if is_raid == 1:
                calculate_final_state(current_positions_list, alphabeta_i, alphabeta_j, 1, stable_player)
            else:
                calculate_final_state(current_positions_list, alphabeta_i, alphabeta_j, 0, stable_player)

        for position in current_positions_list:
            fo1.write('%s' % ''.join(map(str, position))+'\n')

        fo.close()
        fo1.close()

    elif algorithm == 4:
        i = 1
        for line in fh:
            words = line.rstrip().split()
            if i == 1:
                player = words[0]
            elif i == 2:
                player_algorithm = int(words[0])
            elif i == 3:
                player_depth = int(words[0])
            elif i == 4:
                opponent = words[0]
            elif i == 5:
                opponent_algorithm = int(words[0])
            elif i == 6:
                opponent_depth = int(words[0])
            elif 6 < i <= 11:
                temp_points_list = []
                for word in words:
                    temp_points_list.append(int(word))
                points_list.append(temp_points_list)
            else:
                word = list(line.strip('\r\n'))
                current_positions_list_1.append(word)
            i += 1

        fo = open('trace_state.txt','w')
        playerflag = True

        while not check_end_state(current_positions_list_1):
            if playerflag:
                if player_algorithm == 1:

                    greedy_best_first = Game(player, player_depth,current_positions_list_1,0,0,0,0,0)

                    if player_depth!= 0:

                        greedy_best_first.GreedyBestFirstSearch()

                        is_raid = greedy_best_first.isRaid(current_positions_list_1, greedy_i, greedy_j, player)

                        if is_raid == 1:
                            calculate_final_state(current_positions_list_1, greedy_i, greedy_j, 1, player)
                        else:
                            calculate_final_state(current_positions_list_1, greedy_i, greedy_j, 0, player)

                    for position in current_positions_list_1:
                        fo.write('%s' % ''.join(map(str, position))+'\n')
                    playerflag = False

                elif player_algorithm == 2:
                    level = player_depth
                    stable_player = player

                    minimax = Game(player, player_depth, current_positions_list_1,'root',100,100,0,0)

                    minimax.MinMax(0,None)

                    is_raid = minimax.isRaid(current_positions_list_1, minimax_i, minimax_j, stable_player)
                    if minimax_case:
                        if is_raid == 1:
                            calculate_final_state(current_positions_list_1, minimax_i, minimax_j, 1, stable_player)
                        else:
                            calculate_final_state(current_positions_list_1, minimax_i, minimax_j, 0, stable_player)

                    for position in current_positions_list_1:
                        fo.write('%s' % ''.join(map(str, position))+'\n')
                    playerflag = False


                elif player_algorithm == 3:
                    level = player_depth
                    stable_player = player

                    alphabetapruning = Game(player, player_depth, current_positions_list_1,'root',100,100,float('-inf'),float('inf'))

                    alphabetapruning.AlphaBetaPruning(0,None)

                    is_raid = alphabetapruning.isRaid(current_positions_list_1, alphabeta_i, alphabeta_j, stable_player)
                    if alphabeta_case:
                        if is_raid == 1:
                            calculate_final_state(current_positions_list_1, alphabeta_i, alphabeta_j, 1, stable_player)
                        else:
                            calculate_final_state(current_positions_list_1, alphabeta_i, alphabeta_j, 0, stable_player)

                    for position in current_positions_list_1:
                        fo.write('%s' % ''.join(map(str, position))+'\n')
                    playerflag = False


            else:

                if opponent_algorithm == 1:

                    greedy_best_first = Game(opponent, opponent_depth,current_positions_list_1,0,0,0,0,0)
                    if opponent_depth!= 0:
                        greedy_best_first.GreedyBestFirstSearch()

                        is_raid = greedy_best_first.isRaid(current_positions_list_1, greedy_i, greedy_j, opponent)

                        if is_raid == 1:
                            calculate_final_state(current_positions_list_1, greedy_i, greedy_j, 1, opponent)
                        else:
                            calculate_final_state(current_positions_list_1, greedy_i, greedy_j, 0, opponent)

                    for position in current_positions_list_1:
                        fo.write('%s' % ''.join(map(str, position))+'\n')

                    playerflag = True

                elif opponent_algorithm == 2:

                    level = opponent_depth
                    stable_player = opponent

                    minimax = Game(opponent, opponent_depth, current_positions_list_1,'root',100,100,0,0)

                    minimax.MinMax(0,None)

                    is_raid = minimax.isRaid(current_positions_list_1, minimax_i, minimax_j, stable_player)

                    if minimax_case:
                        if is_raid == 1:
                            calculate_final_state(current_positions_list_1, minimax_i, minimax_j, 1, stable_player)
                        else:
                            calculate_final_state(current_positions_list_1, minimax_i, minimax_j, 0, stable_player)

                    for position in current_positions_list_1:
                        fo.write('%s' % ''.join(map(str, position))+'\n')
                    playerflag = True


                elif opponent_algorithm == 3:

                    level = opponent_depth
                    stable_player = opponent

                    alphabetapruning = Game(opponent, opponent_depth, current_positions_list_1,'root',100,100,float('-inf'),float('inf'))

                    alphabetapruning.AlphaBetaPruning(0,None)

                    is_raid = alphabetapruning.isRaid(current_positions_list_1, alphabeta_i, alphabeta_j, stable_player)
                    if alphabeta_case:
                        if is_raid == 1:
                            calculate_final_state(current_positions_list_1, alphabeta_i, alphabeta_j, 1, stable_player)
                        else:
                            calculate_final_state(current_positions_list_1, alphabeta_i, alphabeta_j, 0, stable_player)

                    for position in current_positions_list_1:
                        fo.write('%s' % ''.join(map(str, position))+'\n')
                    playerflag = True

if __name__ == "__main__":
    main()

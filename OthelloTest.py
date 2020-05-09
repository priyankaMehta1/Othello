import sys
   
def partitionMoves(game,player):
   moves = rows(game,player)
   moves1 = cols(game,player)
   moves2 = diags(game,player)
   moves3 = moves.union(moves1)
   finalmoves = moves3.union(moves2)
   return finalmoves

def cols(game,player):
   if player == "X":
      sets = ["XO.","XOO.","XOOO.","XOOOO.","XOOOOO.","XOOOOOO."]
      sets2 = [".OX",".OOX",".OOOOX",".OOOOOX",".OOOOOOX",".OOOX"]
   else:
      sets = ["OX.","OXX.","OXXX.","OXXXX.","OXXXXX.","OXXXXXX."]
      sets2 = [".XO",".XXO",".XXXO",".XXXXO",".XXXXXO",".XXXXXXO"]
   moves = set()
   for i in col:
      sequence = [game[x] for x in i]
      seqstring = ''.join(sequence) 
      for a in sets:
         if a in seqstring:
            moves.add(i[seqstring.index(a)+len(a)-1])
      for b in sets2:
         if b in seqstring:
            moves.add(i[seqstring.index(b)])
   return moves

def diags(game,player):
   if player == "X":
      sets = ["XO.","XOO.","XOOO.","XOOOO.","XOOOOO.","XOOOOOO."]
      sets2 = [".OX",".OOX",".OOOOX",".OOOOOX",".OOOOOOX",".OOOX"]
   else:
      sets = ["OX.","OXX.","OXXX.","OXXXX.","OXXXXX.","OXXXXXX."]
      sets2 = [".XO",".XXO",".XXXO",".XXXXO",".XXXXXO",".XXXXXXO"]
   moves = set()
   for i in diag:
      sequence = [game[x] for x in i]
      seqstring = ''.join(sequence)   
      for a in sets:
         if a in seqstring:
            moves.add(i[seqstring.index(a)+len(a)-1])
      for b in sets2:
         if b in seqstring:
            moves.add(i[seqstring.index(b)])
   return moves

def rows(game,player):
   if player == "X":
      sets = ["XO.","XOO.","XOOO.","XOOOO.","XOOOOO.","XOOOOOO."]
      sets2 = [".OX",".OOX",".OOOOX",".OOOOOX",".OOOOOOX",".OOOX"]
   else:
      sets = ["OX.","OXX.","OXXX.","OXXXX.","OXXXXX.","OXXXXXX."]
      sets2 = [".XO",".XXO",".XXXO",".XXXXO",".XXXXXO",".XXXXXXO"]
   moves = set()
   for i in row:
      sequence = [game[x] for x in i]
      seqstring = ''.join(sequence)   
      for a in sets:
         if a in seqstring:
            moves.add(i[seqstring.index(a)+len(a)-1])
      for b in sets2:
         if b in seqstring:
            moves.add(i[seqstring.index(b)])
   return moves  
   
def negamax6(game,player,level):
   #need to change this to terminate when there are no moves left      
   moves = partitionMoves(game[:],player)
   opp = "O" if player == "X" else "X"
   oppmoves = partitionMoves(game[:],opp)
   if len(moves) == 0 and len(oppmoves) == 0:
      return [evalGame(game[:],player)]
   negMax = [negamax(makeMove(game[:],player,move),opp,level-1) + [move] for move in moves]
   if len(negMax) > 0:
      best = negMax[0]
      return [-best[0]] + best[1:]
   else:
      return [evalGame(game[:],player)]
      
def negamax2(game,player,level):
   if level == 0:
      return [evalGame(game[:],player)]
   moves = partitionMoves(game[:],player)
   opp = "O" if player == "X" else "X"
   if len(moves) == 0:
      negMax = negamax(game[:],opp,level-1)
      return [-negMax[0]] + negMax[1:]
   negMax = sorted([negamax(makeMove(game[:],player,move),opp,level-1) + [move] for move in moves])
   best = negMax[0]
   return [-best[0]] + best[1:]

def negamax1(game, player, levels):
   lm = partitionMoves(game, player)
   print("In negamax, legal moves are: " + str(lm))
   if not lm:
      print("In negamax, eval game gives: " + str(evalGame(game,player))) 
      return [evalGame(game, player)]
   opp = "O" if player == "X" else "X"
   ln = partitionMoves(game, opp)
   if not ln: 
      best = negamax(game, opp, levels-1)
   else: 
      best = sorted([negamax(makeMove(game, player, mv), opp, levels-1) + [mv] for mv in lm])[-1]
   return [-best[0]] + best[1:]

def negamax(board, token, levels):
   for i in range(8): print(''.join(board[:][i*8:i*8 + 8]))
   print("Levels: " + str(levels))
   print("Token is: " + str(token))
   print()
   if levels == 0:
      print("Number of levels is 0")
      print("Eval game returns: " + str(evalGame(board[:],token)))
      print()
      return [evalGame(board[:], token)]
   opp = "O" if token == "X" else "X"
   lm = partitionMoves(board[:], token)
   if len(lm) == 0:
      ln = partitionMoves(board[:], opp) 
      if len(ln) == 0:
         print("No moves possible for either player")
         print("Eval game returns: " + str(evalGame(board[:],token)))
         print()
         return [evalGame(board[:], token)]
      else:
         best = negamax(board[:], opp, levels)
   else: 
      print("Legal moves are: " + str(lm))
      print()
      print(board)
      print()
      for mv in lm:
         print("Make move with levels at " + str(levels))
         print(makeMove(board[:], token, mv))
         print("Number of open spaces was " + str(board[:].count(".")))
         print("Number of possible moves for " + str(token) + " was " + str(len(lm)))
         print("Moved to position " + str(mv))
         print("")
      print("Board")
      for i in range(8): print(''.join(board[:][i*8:i*8 + 8]))
      print()
      print("Levels: " + str(levels))
      print()
      best = sorted([negamax(makeMove(board[:], token, mv),opp,levels-1) + [mv] for mv in lm])
      print(best)
      best = best[0]
   return [-best[0]] + best[1:]

def negamax4(board, token, levels):
   opp = "O" if token == "X" else "X"
   lm = partitionMoves(board[:], token)
   if len(lm) == 0:
      ln = partitionMoves(board[:], opp) 
      if len(ln) == 0:
         return [evalGame(board[:], token)]
      else:
         best = negamax(board[:], opp, levels)
   else: 
      best = sorted([negamax(makeMove(board[:], token, mv),opp,levels-1) + [mv] for mv in lm])
      print(best)
      best = best[0]
   return [-best[0]] + best[1:]

def negamax5(board, token, levels):
   enemy = "O" if token == "X" else "X"
   if not levels: 
      return [evalGame(board[:], token)]
   lm = partitionMoves(board[:], token)
   if not lm: best = negamax(board[:], enemy, levels-1) + [-1]
   else: best = sorted([negamax(makeMove(board[:], token, mv),enemy, levels-1) + [mv] for mv in lm])[0]
   return [-best[0]] + best[1:]

def makeMove(game4,player,pos):
   game4[int(pos)] = player
   opp = "O" if player == "X" else "X" 
   game4 = flipTokens2(game4,pos,row,player,opp)
   game4 = flipTokens2(game4,pos,col,player,opp)
   game4 = flipTokens2(game4,pos,diag,player,opp)
   return game4

def evalGame(game,player):
   opp = "X" if player == "O" else "O"
   return(game.count(player) - game.count(opp))

def flipTokens2(game2,pos,table,player,opp):
   for i in table:
      if pos in i:
         positions = i[:]
         characters = [game2[x] for x in i]
         if player in characters and opp in characters:
            fragment = ''.join(characters)
            setsX = ["XOX","XOOX","XOOOX","XOOOOX","XOOOOOX","XOOOOOOX"]
            setsO = ["OXO","OXXO","OXXXO","OXXXXO","OXXXXXO","OXXXXXXO"]
            if player == "X":
               for x in setsX:
                  if x in fragment:
                     length = len(x)
                     index = positions.index(pos)
                     frag1 = fragment[index:index + length]
                     frag2 = fragment[index-length+1:index+1]
                     if frag1 == x:
                        for y in range(index, index+length):
                           game2[positions[y]] = player
                     if frag2 == x:
                        for y in range(index-length+1,index):
                           game2[positions[y]] = player
            else:
               for x in setsO:
                  if x in fragment:
                     length = len(x)
                     index = positions.index(pos)
                     frag1 = fragment[index:index + length]
                     frag2 = fragment[index-length+1:index+1]
                     if frag1 == x:
                        for y in range(index, index+length):
                           game2[positions[y]] = player
                     if frag2 == x:
                        for y in range(index-length+1,index):
                           game2[positions[y]] = player
   return game2
      
col = [[0,8,16,24,32,40,48,56],[1,9,17,25,33,41,49,57],
      [2,10,18,26,34,42,50,58],[3,11,19,27,35,43,51,59],
      [4,12,20,28,36,44,52,60],[5,13,21,29,37,45,53,61],
      [6,14,22,30,38,46,54,62],[7,15,23,31,39,47,55,63]]
row = [
      [0,1,2,3,4,5,6,7],[8,9,10,11,12,13,14,15],
      [16,17,18,19,20,21,22,23],[24,25,26,27,28,29,30,31],
      [32,33,34,35,36,37,38,39],[40,41,42,43,44,45,46,47],
      [48,49,50,51,52,53,54,55],[56,57,58,59,60,61,62,63]]
diag = [
      [0],[8,1],[16,9,2],[24,17,10,3],[32,25,18,11,4],
      [40,33,26,19,12,5],[48,41,34,27,20,13,6],
      [56,49,42,35,28,21,14,7],[57,50,43,36,29,22,15],
      [58,51,44,37,30,23],[59,52,45,38,31],[60,53,46,39],
      [61,54,47],[62,58],[63],[7],[6,15],[5,14,23],
      [4,13,22,31],[3,12,21,30,39],[2,11,20,29,38,47],
      [1,10,19,28,37,46,55],[0,9,18,27,36,45,54,63],
      [8,17,26,35,44,53,62],[16,25,34,43,52,61],[56],
      [24,33,42,51,60],[32,41,50,59],[40,49,58],[48,57]]

game = list(sys.argv[1])
game1 = game[:]
for i in range(len(game)):
   if game[i] == "x" or game[i] == "o":
      game[i] = game[i].upper()
player = sys.argv[2].upper()
opp = "O" if player == "X" else "X"
#print 2D board
#show possible moves on the board (lab1)
#print my heuristic choice is + the choice
for i in range(8): print(''.join(game[i*8:i*8 + 8]))
print("Legal moves are")
moves = partitionMoves(game,player)
print(moves)
print()
if game1.count(".") <= 8:
   nm = negamax(game, player,-1)
   if nm[-1] in moves:
      print("Negamax score is " + str(nm[0]) + " and my move is " + str(nm[-1]))
      print(nm)
   elif nm[0] in moves:
      nm = nm[::-1]
      print("Negamax score is " + str(nm[0]) + " and my move is " + str(nm[-1]))
      print(nm)
   else:
      print()
      print(moves.pop())
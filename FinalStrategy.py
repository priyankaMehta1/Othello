#
#Priyanka Mehta
import sys

class Strategy:
   def best_strategy(self, board, player, best_move, still_running):
      game = list(''.join(board).replace("?","").replace("@","X").replace("o","O"))
      player = "X" if player == "@" else "O"
      moves = partitionMoves(game[:],player)
      opp = "X" if player == "O" else "O"
      moveDict = {}
      for i in moves:
         moveDict[i] = 0
      moveDict = greedyCorners(moveDict,game[:],player,opp)
      moveDict = oppositionCorners(moveDict,game[:],player,opp)
      moveDict = cxChecks(moveDict,game[:],player,opp)
      moveDict = playEdge(moveDict,game[:],player,opp)
      moveDict = chooseBest(moveDict,game[:],player,opp)
      inverse = [(value, key) for key, value in moveDict.items()]
      choice = max(inverse)[1]
      choice = ((choice//8) * 10) + (choice%8) + 11
      best_move.value = choice
      if game[:].count(".") <= 8:
         nm = negamax(game[:], player,-1)
         move = nm[-1]
         bestt = 11 + (move//8)*10 + (move%8)
         best_move.value = bestt
         
def partitionMoves(game,player):
   moves = table(row,game,player)
   moves1 = table(col,game,player)
   moves2 = table(diag,game,player)
   moves3 = moves.union(moves1)
   finalmoves = moves3.union(moves2)
   return finalmoves

def table(tabl,game,player):
   if player == "X":
      sets = ["XO.","XOO.","XOOO.","XOOOO.","XOOOOO.","XOOOOOO."]
      sets2 = [".OX",".OOX",".OOOOX",".OOOOOX",".OOOOOOX",".OOOX"]
   else:
      sets = ["OX.","OXX.","OXXX.","OXXXX.","OXXXXX.","OXXXXXX."]
      sets2 = [".XO",".XXO",".XXXO",".XXXXO",".XXXXXO",".XXXXXXO"]
   moves = set()
   for i in tabl:
      sequence = [game[x] for x in i]
      seqstring = ''.join(sequence) 
      for a in sets:
         if a in seqstring:
            moves.add(i[seqstring.index(a)+len(a)-1])
      for b in sets2:
         if b in seqstring:
            moves.add(i[seqstring.index(b)])
   return moves
      
def greedyCorners(dictionary,game,player,opp): 
   for i in dictionary:
      if i in [0,7,56,63]:
         dictionary[i] += 1000
   return dictionary
         
def oppositionCorners(dictionary,game,player,opp):
   opp = "X" if player == "O" else "O"
   for x in dictionary:
      game2 = game[:]
      oppMoves = partitionMoves(makeMove(game2,player,x),opp)
      for y in oppMoves:
         if y in [0,7,56,63]:
            dictionary[x] -= 1000
   return dictionary
   
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


def makeMove(game,player,pos):
   game[int(pos)] = player
   opp = "O" if player == "X" else "X" 
   game = flipTokens2(game,pos,row,player,opp)
   game = flipTokens2(game,pos,col,player,opp)
   game = flipTokens2(game,pos,diag,player,opp)
   return game

def evalGame(game,player):
   opp = "X" if player == "O" else "O"
   return(game.count(player) - game.count(opp))
   
def cxChecks(dictionary,game,player,opp):
   CX = {1:0,8:0,9:0,6:7,15:7,14:7,57:56,48:56,49:56,62:63,55:63,54:63}
   for i in dictionary:
      if i in CX:
         if game[CX.get(i)] != player:
            dictionary[i] -= 100
   return dictionary

def playEdge(dictionary,game,player,opp):
   edges = [0,1,2,3,4,5,6,7,8,16,24,32,40,48,56,57,58,59,60,61,62,63,55,47,39,31,23,15]
   for i in dictionary:
      if i in edges:
         dictionary[i] += 10
   return dictionary
         
def chooseBest(dictionary,game,player,opp):
   for i in dictionary:
      countt = 0
      game1 = game[:]
      game1[i] = player
      countt += flipTokens(game1,i,row,player,opp)
      countt += flipTokens(game1,i,col,player,opp)
      countt += flipTokens(game1,i,diag,player,opp)
      dictionary[i] += countt
   return dictionary
         
def flipTokens(game,pos,table,player,opp):
   count = 0
   for i in table:
      if pos in i:
         positions = i[:]
         characters = [game[x] for x in i]
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
                           count+=1
                     if frag2 == x:
                        for y in range(index-length+1,index):
                           count+=1
            else:
               for x in setsO:
                  if x in fragment:
                     length = len(x)
                     index = positions.index(pos)
                     frag1 = fragment[index:index + length]
                     frag2 = fragment[index-length+1:index+1]
                     if frag1 == x:
                        for y in range(index, index+length):
                           count+=1
                     if frag2 == x:
                        for y in range(index-length+1,index):
                           count+=1
   return count
   
def negamax(board, token, levels):
   if levels == 0:
      return [evalGame(board[:], token)]
   opp = "O" if token == "X" else "X"
   lm = partitionMoves(board[:], token)
   if len(lm) == 0:
      ln = partitionMoves(board[:], opp) 
      if len(ln) == 0:
         return [evalGame(board[:], token)]
      else:
         best = negamax(board[:], opp, levels-1) + [-1]
   else: 
      best = sorted([negamax(makeMove(board[:], token, mv),opp,levels-1) + [mv] for mv in lm])
      best = best[0]
   return [-best[0]] + best[1:]
         
def main():
   game = list(''.join(sys.argv[1]))
   player = sys.argv[2].upper()
   opp = "X" if player == "O" else "O"
   moves = partitionMoves(game[:],player)
   moveDict = {}
   for i in moves:
      moveDict[i] = 0
   moveDict = greedyCorners(moveDict)
   moveDict = oppositionCorners(moveDict,game[:])
   moveDict = cxChecks(moveDict,game[:])
   moveDict = playEdge(moveDict)
   moveDict = chooseBest(moveDict,game[:])
   inverse = [(value, key) for key, value in moveDict.items()]
   choice = max(inverse)[1]
   print(choice)
   if game1.count(".") <= 8:
      nm = negamax(game[:], player,-1)
      move = str(nm[-1])
      print(move)

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

if __name__ == "__main__":
   main()
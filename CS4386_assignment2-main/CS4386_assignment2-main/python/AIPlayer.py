##################################     
    # CS4386 Semester B, 2021-2022
    # Assignment 2
    # Name: Xian Jia Le
    # Student ID: 56214537
##################################


from ast import Index
from asyncio.windows_events import NULL
from unicodedata import name
import Game


class GamePiece:
    def __init__(self, name, pong, chow, pair,seq,seq2,importance):
        self.name = name
        self.Pong = pong
        self.Chow = chow
        self.Pair = pair
        self.Seq = seq
        self.Seq2=seq2
        self.Importance = importance


def PrintClasses(obj):
    for o in obj:
        print(" ",o.name, " Pong: ", o.Pong, " Chow: ", o.Chow," Pair: ",o.Pair," Seq1: ",o.Seq," Seq2: ",o.Seq2," Importance ",o.Importance, "\n")


class AIPlayer():

    def __init__(self):
        self.name = 'AIPlayer'
        self.pieces = []

    def update_state(self, gametable_receive_tiles, gametable_receive_cnt, player_cnt, player_cnt_p, player_cnt_c, oppo_cnt_p, oppo_cnt_c):
        self.gametable_receive_tiles = gametable_receive_tiles
        self.gametable_receive_cnt = gametable_receive_cnt
        self.player_cnt = player_cnt
        self.player_cnt_p = player_cnt_p
        self.player_cnt_c = player_cnt_c
        self.oppo_cnt_p = oppo_cnt_p
        self.oppo_cnt_c = oppo_cnt_c

    def think_pong(self):  # get 4 234 456 -> 444 2356
        print("think_pong")
        action=False
        maxChowValue=-1000
        #get the drop piece
        dropPiece=self.gametable_receive_tiles[len(self.gametable_receive_tiles)-1][1]
        print("drop",dropPiece+1)
        index=self.Analysis(dropPiece)
        print("think_pong")
        PrintClasses(self.pieces)
        if(self.pieces[index].Pong!=0):
            action=True
        # for piece in self.pieces:
        #     if((dropPiece+1)==piece.name):
        #         if(piece.Chow!=0):
        #             chowSum=0
        #             for chow in self.pieces:
        #                 if(piece.Chow==chow.Chow):
        #                     chowSum=chowSum+chow.name
        #             if(chowSum>maxChowValue):
        #                 maxChowValue=chowSum

        # if(maxChowValue<(dropPiece+1)*3):
        #     action=True
        return action

    def think_chow(self):  # 56777 get(6 or 4) 11123
        #get the drop piece
        dropPiece=self.gametable_receive_tiles[len(self.gametable_receive_tiles)-1][1]
        print("drop",dropPiece+1)
        index=self.Analysis(dropPiece)
        print("think_chow")
        PrintClasses(self.pieces)
        #find the largest possible action
        action=0
        if(self.pieces[index].Chow!=0):
            action=1
            i=0
            while(action<3 and i<len(self.pieces)):
                if(self.pieces[i].Chow==self.pieces[index].Chow):
                    if(self.pieces[i].name==self.pieces[index].name):
                        break
                    action=action+1
                i=i+1
        return action

    def think(self):
        self.Analysis()
        print("think")
        PrintClasses(self.pieces)
        # reform status
        # prority ->single(not in chow group or pong group) and piece in oppoent pong> single(not in chow group or pong group) > pair
        i=0
        minVal=100
        piece=-1
        while(i<len(self.pieces)):
            if(self.pieces[i].Importance<minVal):
                minVal=self.pieces[i].Importance
                piece=self.pieces[i].name-1
            i=i+1
        print(piece+1)#map to the name from index
        return piece
       # for i in range(0, 9):
       #     if self.player_cnt[i] > 0:
       #         return i

    def Analysis(self,extraPieces=None):
        self.pieces.clear()
        extraIndex=-1
        # insert data
        for i, cnt in enumerate(self.player_cnt):
            k = cnt
            if (extraPieces!=None and i==extraPieces):
                self.pieces.append(GamePiece(extraPieces+1,0,0,0,0,0,0))
                extraIndex=len(self.pieces)-1
            while(k > 0):
                self.pieces.append(GamePiece(i+1, 0, 0, 0,0,0,0))
                k = k-1

        # PrintClasses(self.pieces)
        # mark existingChow
        i = len(self.pieces)-1
        group = 1
        while(i >= 0):
            if(self.pieces[i].Chow == 0):
                k = i-1
                target = self.pieces[i].name-1
                counter = 0
                candidates = []
                while(k >= 0 and counter < 2):                
                    if(target == self.pieces[k].name):
                        if(self.pieces[k].Chow == 0):
                            target = target-1
                            counter = counter+1
                            candidates.append(k)
                    k = k-1

                if(counter >= 2):
                    self.pieces[i].Chow = group
                    self.pieces[i].Importance+=2 #add importance 2
                    for candidate in candidates:
                        self.pieces[candidate].Chow = group
                        self.pieces[candidate].Importance+=2 #add importance 2
                    group = group+1
            i=i-1

        # mark existingPong
        i = len(self.pieces)-1
        group=1
        while(i>1):
            if(self.pieces[i].Pong==0):
                if(self.pieces[i].name==self.pieces[i-1].name and self.pieces[i-1].name==self.pieces[i-2].name):
                    #find chowSum
                    k=i
                    bestChowSum=0
                    ChowGroup=0
                    while(self.pieces[k].Chow!=0 and k>=i-2):
                        ChowGroup =self.pieces[k].Chow
                        chowSum=0
                        for piece in self.pieces:
                            if(piece.Chow==ChowGroup):
                                chowSum=chowSum+piece.name
                        if(bestChowSum<chowSum):
                            bestChowSum=chowSum
                        k=k-1
                    if(self.pieces[i].name*3 > bestChowSum):
                        self.pieces[i].Pong=group
                        self.pieces[i-1].Pong=group
                        self.pieces[i-2].Pong=group
                        #add importance 
                        self.pieces[i].Importance+=2
                        self.pieces[i-1].Importance+=2
                        self.pieces[i-2].Importance+=2
                        #clean up chow
                        for piece in self.pieces:
                            if(piece.Chow==ChowGroup):
                                piece.Chow=0

                    group=group+1
            i=i-1

        #mark pair
        i = len(self.pieces)-1
        group=1
        while(i>0):
            if((self.pieces[i].Chow==0 and self.pieces[i].Pong==0) and self.pieces[i].Pair==0):
                if(self.pieces[i].name==self.pieces[i-1].name):
                    self.pieces[i].Pair=group
                    self.pieces[i-1].Pair=group

                    #add importance 1
                    self.pieces[i].Importance+=1
                    self.pieces[i-1].Importance+=1

                    group=group+1
            i=i-1

        #mark consecutive seq 21
        i = len(self.pieces)-1
        group = 1
        while(i >= 0):
            if((self.pieces[i].Chow==0 and self.pieces[i].Pong==0) and self.pieces[i].Seq == 0):
                k = i-1
                target = self.pieces[i].name-1
                while(k >= 0):                
                    if(target == self.pieces[k].name and (self.pieces[k].Chow==0 and self.pieces[k].Pong==0)):
                        if(self.pieces[k].Seq == 0):
                            self.pieces[k].Seq = group
                            self.pieces[k].Importance+=0.5
                            self.pieces[i].Seq = group
                            self.pieces[i].Importance+=0.5 #add importance 2
                            group = group+1
                            break
                    k=k-1
            i=i-1

             #mark consecutive seq 2 
        i = len(self.pieces)-1
        group = 1
        while(i >= 0):
            if((self.pieces[i].Chow==0 and self.pieces[i].Pong==0) and self.pieces[i].Seq2 == 0):
                k = i-1
                target = self.pieces[i].name-2
                while(k >= 0):                
                    if(target == self.pieces[k].name and (self.pieces[k].Chow==0 and self.pieces[k].Pong==0)):
                        if(self.pieces[k].Seq2 == 0):
                            self.pieces[k].Seq2 = group
                            self.pieces[k].Importance+=0.5
                            self.pieces[i].Seq2 = group
                            self.pieces[i].Importance+=0.5 #add importance 2
                            group = group+1
                            break
                    k=k-1
            i=i-1

        return extraIndex



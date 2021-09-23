# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 15:31:30 2020

@author: jeton
"""

import http.client
import time
import numpy as np

CRED = '\33[31m'
CEND = '\033[0m'
CBLUE = '\33[34m'


#meilleur coup pour IA
def maxi(g, profondeur, alpha, beta):
    beta=200000
    if (profondeur==0 or terminal_test(g)==1 or terminal_test(g)==2):
        return utility(g)
    for a in actions_possibles(g):
        for i in range(5,-1,-1):
            if(g[i][a]==0):
                lig=i
                g[i][a]=ia
                break 

        alpha=max(alpha, mini(g, profondeur-1, alpha, beta))
        if(beta<=alpha):
            return alpha
        for i in range(lig, -1,-1):
            g[i][a]=0
    return alpha

#meilleur coup pour joueur
def mini(g, profondeur, alpha, beta):
    alpha=-200000
    if (profondeur==0 or terminal_test(g)==1 or terminal_test(g)==2):
        return utility(g)

    for a in actions_possibles(g):
        for i in range(5,-1,-1):
            if(g[i][a]==0):
                lig=i
                g[i][a]=joueur
                break   
        beta=min(beta, maxi(g,profondeur-1, alpha, beta))
        if (alpha>=beta):
            return beta
        for i in range(lig, -1,-1):
            g[i][a]=0
    return beta


def minmax(g, profondeur, alpha, beta):
    a_max=0
    g_copie=[[0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0]]
    for i in range(6):
        for j in range(12):
            g_copie[i][j]=g[i][j]
    alpha=-200000
    for a in actions_possibles(g_copie):
        for i in range(5,-1,-1):
            if(g_copie[i][a]==0):
                lig=i
                g_copie[i][a]=ia
                break  
        tmp=mini(g_copie, profondeur-1, alpha, beta)
        if(tmp>alpha):
            alpha=tmp
            a_max=a
        for i in range(lig, -1,-1):
            g_copie[i][a]=0
    remplirGrille(g, ia, a_max)
    

def terminal_test(g):
    for i in range (6):
        for j in range (12):
            if (g[i][j]!=0):
                if (j<=8):
                    if(g[i][j]==g[i][j+1] and g[i][j]==g[i][j+2] and g[i][j]==g[i][j+3]):
                        return g[i][j]
                if (i<=2):
                    if (g[i][j]==g[i+1][j] and g[i][j]==g[i+2][j] and g[i][j]==g[i+3][j]):
                        return g[i][j]
                if (j<=8 and i<=2):
                    if (g[i][j]==g[i+1][j+1] and g[i][j]==g[i+2][j+2] and g[i][j]==g[i+3][j+3]):
                        return g[i][j]
                if(j>=3 and i<=2):
                    if(g[i][j]==g[i+1][j-1] and g[i][j]==g[i+2][j-2] and g[i][j]==g[i+3][j-3]):
                        return g[i][j]
    return 0

def action_possible(g):
    actions=[]
    for i in range(12):
        if (g[0][i]==0):
            actions.append(i)
    return actions
 
    
def actions_possibles(g):
    actions=[]
    for i in range(12):
        if(g[5][i]!=0 and g[0][i]==0):
            actions.append(i)
    for i in range(12):
        if(g[5][i]==0 and g[0][i]==0):
            actions.append(i)
    return actions
    
def remplirGrille(g, player, jeu):
    for i in range(5,-1,-1):
        if(g[i][jeu]==0):
            g[i][jeu]=player
            break           

def utility(g):
    
    if(terminal_test(g)==2):
        return 5000
    if(terminal_test(g)==1):
        return -5000

    
    s_player = somme_pion(2,g)
    s_opponent = somme_pion(1, g)
    return s_player - s_opponent



def somme_pion(player, g):
    somme_cpt=0
    for i in range(6):
        for j in range(12):
            if(g[i][j]==player):
                somme_cpt=somme_cpt+pion_alignes(j,i, player, g)

    return somme_cpt
        
def pion_alignes(x, y, player, g):
    if(player==1):
        opponent=2
    else:
        opponent=1
    cpt=0
    p_ali = 0
    cpt_temp=cpt
    for j in range(1,4):
        #test vers le haut
        if(y-j<0):
            cpt=cpt_temp
            p_ali=-10
            break
        if (g[y-j][x]==opponent):
            cpt=cpt_temp
            p_ali = -10
            break
        if(g[y-j][x]==g[y][x]):
            cpt=cpt+(4-j)**2
            p_ali += 1
        if(g[y-j][x]==0):
            cpt=cpt+1
        
    if p_ali == 1:
        cpt+=5
    elif p_ali == 2:
        cpt += 50
    elif p_ali == 3:
        cpt += 500
    
    p_ali = 0    
    cpt_temp=cpt
    for j in range(1,4):
        #test vers le bas
        if(y+j>5):
            cpt=cpt_temp
            p_ali=-10
            break
        if (g[y+j][x]==opponent):
            cpt=cpt_temp
            p_ali = -1
            break
        if(g[y+j][x]==g[y][x]):
            cpt=cpt+(4-j)**2
            p_ali += 1
        if(g[y+j][x]==0):
            cpt=cpt+1
    if p_ali == 1:
        cpt+=5
    elif p_ali == 2:
        cpt += 50
    elif p_ali == 3:
        cpt += 500
    
    p_ali = 0        
    cpt_temp=cpt
    for j in range(1,4):
        #test vers la droite
        if(x+j>11):
            cpt=cpt_temp
            p_ali=-10
            break
        if (g[y][x+j]==opponent):
            p_ali = -10
            cpt=cpt_temp
            break
        if(g[y][x+j]==g[y][x]):
            cpt=cpt+(4-j)**2
            p_ali += 1
        if(g[y][x+j]==0):
            cpt=cpt+1
    if p_ali == 1:
        cpt+=5
    elif p_ali == 2:
        cpt += 50
    elif p_ali == 3:
        cpt += 500
    
    p_ali = 0        
    cpt_temp=cpt
    for j in range(1,4):
        
        #test vers la gauche
        if(x-j<0):
            cpt=cpt_temp
            break
        if (g[y][x-j]==opponent):
            cpt=cpt_temp
            p_ali = -10
            break
        if(g[y][x-j]==g[y][x]):
            cpt=cpt+(4-j)**2
            p_ali += 1
        if(g[y][x-j]==0):
            cpt=cpt+1
    if p_ali == 1:
        cpt+=5
    elif p_ali == 2:
        cpt += 50
    elif p_ali == 3:
        cpt += 500
    
    p_ali = 0
    cpt_temp=cpt        
    for j in range(1,4):
        #test vers la diagonale haut droite
        if(x+j>11 or y-j<0):
            cpt=cpt_temp
            p_ali=-10
            break
        if (g[y-j][x+j]==opponent):
            cpt=cpt_temp
            p_ali = -10
            break
        if(g[y-j][x+j]==g[y][x]):
            cpt=cpt+(4-j)**2
            p_ali += 1
        if(g[y-j][x+j]==0):
            cpt=cpt+1
    if p_ali == 1:
        cpt+=5
    elif p_ali == 2:
        cpt += 50
    elif p_ali == 3:
        cpt += 500
    
    p_ali = 0        
    cpt_temp=cpt
    for j in range(1,4):
        #test vers la diagonale haut gauche
        if(x-j<0 or y-j<0):
            cpt=cpt_temp
            p_ali=-10
            break
        if (g[y-j][x-j]==opponent):
            cpt=cpt_temp
            p_ali = -10
            break
        if(g[y-j][x-j]==g[y][x]):
            cpt=cpt+(4-j)**2
            p_ali += 1
        if(g[y-j][x-j]==0):
            cpt=cpt+1
    if p_ali == 1:
        cpt+=5
    elif p_ali == 2:
        cpt += 50
    elif p_ali == 3:
        cpt += 500
    
    p_ali = 0
    cpt_temp=cpt
    for j in range(1,4):
        #test vers la diagonale bas gauche
        if(x-j<0 or y+j>5):
            cpt=cpt_temp
            p_ali=-10
            break
        if (g[y+j][x-j]==opponent):
            cpt=cpt_temp
            p_ali = -10
            break
        if(g[y+j][x-j]==g[y][x]):
            cpt=cpt+(4-j)**2
            p_ali += 1
        if(g[y+j][x-j]==0):
            cpt=cpt+1
    if p_ali == 1:
        cpt+=5
    elif p_ali == 2:
        cpt += 50
    elif p_ali == 3:
        cpt += 500

    p_ali = 0
    cpt_temp=cpt
    for j in range(1,4):
        #test vers la diagonale bas droite
        if(x+j>11 or y+j>5):
            cpt=cpt_temp
            p_ali=-10
            break
        if (g[y+j][x+j]==opponent):
            cpt=cpt_temp
            p_ali = -10
            break
        if(g[y+j][x+j]==g[y][x]):
            cpt=cpt+(4-j)**2
            p_ali += 1
        if(g[y+j][x+j]==0):
            cpt=cpt+1
    if p_ali == 1:
        cpt+=5
    elif p_ali == 2:
        cpt += 50
    elif p_ali == 3:
        cpt += 500
    return cpt
            
def printGrille(g):
    for i in range(6):
        print("|",end=' ')
        for j in range(12):
            if(g[i][j]==1):
                print(CBLUE+'0'+CEND,end=' ')
            elif g[i][j]==2:
                print(CRED+'0'+CEND,end=' ')
            else:
                print(" ",end=' ')
            print("|",end=' ')
        print()
    print("|",end=' ')
    for i in range(12):
        print("_",end=" ")
        print("|",end=' ')
    print()
    print("|",end=' ')
    for i in range(12):
        print(i%10,end=" ")
        print("|",end=' ')
    print()
    
grille=[[0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0]]

grilleDim=12
ia=2
joueur=1
printGrille(grille)
depth=4
while(terminal_test(grille)!=2 and terminal_test(grille)!=1):
    
        print("Quelle colonne?")
        
        col=int(input())
        while(col not in action_possible(grille)):
            col=int(input())
        remplirGrille(grille, joueur, col)
        printGrille(grille)
        print("Ordinateur")
        minmax(grille, depth, -200000,200000)
        printGrille(grille)


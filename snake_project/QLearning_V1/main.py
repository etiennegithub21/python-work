import sys, time, pygame
from pygame.locals import *
from modules import *
import pickle
import math

agent = Agent((2,2)) 
moteur = Moteur(20, "configs/conf_1.cf", agent)

def train(n):

    for k in range(n):

        if k%10000 == 0:
            print(k)
        
        # reset
        agent.reset()
        moteur.reset(agent)  

        # état initial
        st = moteur.get_state(agent.position_X, agent.position_Y)

        while moteur.in_game: 

            # ON RECUPERE L'ACTION QUE LE (JOUEUR/AGENT) VEUT REALISER
            at = agent.get_action(st, moteur.Q, 0.6) 
            #print(at)

            # EVALUATION
            stp1, r = moteur.evaluer(agent, at)
            #print(stp1, r)

            # MEILLEURE ACTION
            atp1 = agent.get_action(stp1, moteur.Q, 0.0)
            #print(atp1)

            # ACTUALISATION DE LA QTABLE
            moteur.bellmann_equation(at, atp1, st, stp1, r)

            # ON ACTUALISE LA POSITION DU JOUEUR
            moteur.update_position(agent) 

            st = stp1

            #time.sleep(2)

    # enregistrement de la qtable
    moteur.save_q('q_tables/qtable_1')

def jeu_visuel(human=False): 

    if human:
        agent = Human((2,2))
    else: 
        agent = Agent((2,2)) 

    agent.reset()
    moteur.reset(agent)

    Q = moteur.load_q('q_tables/qtable_1')

    affichage = Affichage(500, 20) 

    # état initial
    st = moteur.get_state(agent.position_X, agent.position_Y)

    while moteur.in_game:

        # ON RECUPERE L'ACTION QUE LE (JOUEUR/AGENT) VEUT REALISER
        if not human:
            st = moteur.get_state(agent.position_X, agent.position_Y)
            at = agent.get_action(st, Q, 0.0) 
        else: 
            at = agent.get_action()

        # AFFICHAGE
        affichage.afficher(moteur.plateau, agent)

        # ON ACTUALISE LA POSITION DU JOUEUR
        moteur.update_position(agent) 

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        affichage.FPS.tick(10)



#####


#train(100) 
jeu_visuel(human=False)
"""
  AO PREENCHER ESSE CABECALHO COM O MEU NOME E O MEU NUMERO USP,
  DECLARO QUE SOU A UNICA PESSOA AUTORA E RESPONSAVEL POR ESSE PROGRAMA.
  TODAS AS PARTES ORIGINAIS DESSE EXERCICIO PROGRAMA (EP) FORAM
  DESENVOLVIDAS E IMPLEMENTADAS POR MIM SEGUINDO AS INSTRUCOES
  DESSE EP E, PORTANTO, NAO CONSTITUEM ATO DE DESONESTIDADE ACADEMICA,
  FALTA DE ETICA OU PLAGIO.
  DECLARO TAMBEM QUE SOU A PESSOA RESPONSAVEL POR TODAS AS COPIAS
  DESSE PROGRAMA E QUE NAO DISTRIBUI OU FACILITEI A
  SUA DISTRIBUICAO. ESTOU CIENTE QUE OS CASOS DE PLAGIO E
  DESONESTIDADE ACADEMICA SERAO TRATADOS SEGUNDO OS CRITERIOS
  DIVULGADOS NA PAGINA DA DISCIPLINA.
  ENTENDO QUE EPS SEM ASSINATURA NAO SERAO CORRIGIDOS E,
  AINDA ASSIM, PODERAO SER PUNIDOS POR DESONESTIDADE ACADEMICA.

  Nome : Lucas Roberto da Costa de Santana
  NUSP : 11891371

  Referencias: Com excecao das rotinas fornecidas no enunciado
  e em sala de aula, caso voce tenha utilizado alguma referencia,
  liste-as abaixo para que o seu programa nao seja considerado
  plagio ou irregular.

  Exemplo:
  - O algoritmo Quicksort foi baseado em:
  https://pt.wikipedia.org/wiki/Quicksort
  http://www.ime.usp.br/~pf/algoritmos/aulas/quick.html
"""

import math
import random
from collections import defaultdict
import util


# **********************************************************
# **            PART 01 Modeling BlackJack                **
# **********************************************************


class BlackjackMDP(util.MDP):
    """
    The BlackjackMDP class is a subclass of MDP that models the BlackJack game as a MDP
    """
    def __init__(self, valores_cartas, multiplicidade, limiar, custo_espiada):
        """
        valores_cartas: list of integers (face values for each card included in the deck)
        multiplicidade: single integer representing the number of cards with each face value
        limiar: maximum number of points (i.e. sum of card values in hand) before going bust
        custo_espiada: how much it costs to peek at the next card
        """
        self.valores_cartas = valores_cartas
        self.multiplicidade = multiplicidade
        self.limiar = limiar
        self.custo_espiada = custo_espiada

    def startState(self):
        """
         Return the start state.
         Each state is a tuple with 3 elements:
           -- The first element of the tuple is the sum of the cards in the player's hand.
           -- If the player's last action was to peek, the second element is the index
              (not the face value) of the next card that will be drawn; otherwise, the
              second element is None.
           -- The third element is a tuple giving counts for each of the cards remaining
              in the deck, or None if the deck is empty or the game is over (e.g. when
              the user quits or goes bust).
        """
        return (0, None, (self.multiplicidade,) * len(self.valores_cartas))

    def actions(self, state):
        """
        Return set of actions possible from |state|.
        You do not must to modify this function.
        """
        return ['Pegar', 'Espiar', 'Sair']

    def peeked(self, state):
        """
        Given a |state| it returns if the player already peeked.
        """
        # print('PEEKED') if state[1] is not None else 0
        return state[1] is not None
    
    def bankrupted(self, points):
        # print('BANKRUPTED') if points > self.limiar else False
        return True if points > self.limiar else False

    def get_next_points(self, state, card_index):
        """
        Return the points in the next hand
        """
        next_points = state[0] + self.valores_cartas[card_index]
        return next_points

    def get_next_deck(self, state, card_index):
        """
        Return the deck in the next hand
        """
        list_deck = list(state[2])
        list_deck[card_index] -= 1
        next_deck = tuple(list_deck) 
        
        if (self.bankrupted(self.get_next_points(state, card_index)))  or (sum(next_deck) == 0):
            next_deck = None

        return next_deck
    
    def get_card(self, state, card_index):
        """
        Get a card in top of card
        """
        new_state = (self.get_next_points(state, card_index), None, self.get_next_deck(state, card_index))
        return new_state

    def peek_card(self, state, card_index):
        """
        Peek a card in top of deck
        """
        new_state = (state[0], card_index, state[2])
        return new_state
   
    def leave_game(self, state):
        """
        Leave the game
        """
        new_state = (state[0], state[1], None)
        return new_state

    def succAndProbReward(self, state, action):
        """
        Given a |state| and |action|, return a list of (newState, prob, reward) tuples
        corresponding to the states reachable from |state| when taking |action|.
        A few reminders:
         * Indicate a terminal state (after quitting, busting, or running out of cards)
           by setting the deck to None.
         * If |state| is an end state, you should return an empty list [].
         * When the probability is 0 for a transition to a particular new state,
           don't include that state in the list returned by succAndProbReward.
        """
        # BEGIN_YOUR_CODE
        state = state
        action = action
        possible_states = []

        if state[2] is None:
            return possible_states

        else:
            if action == 'Pegar':
                if self.peeked(state):
                    card_index = state[1]
                    new_state = self.get_card(state, card_index)
                    prob = 1
                    reward = 0
                    possible_states.append((new_state, prob, reward))
                else:
                    for card_index in range(0, len(state[2])):
                        new_state = self.get_card(state, card_index)
                        prob = state[2][card_index] / sum(state[2])
                        reward = 0

                        if (new_state[2] is None) and (not self.bankrupted(new_state[0])):
                            reward = new_state[0]

                        possible_states.append((new_state, prob, reward)) if prob > 0 else 0

            if action == 'Espiar':
                if self.peeked(state):
                    possible_states = []
                else:
                    for card_index in range(0, len(state[2])):
                        new_state = self.peek_card(state, card_index)
                        prob = state[2][card_index] / sum(state[2])
                        reward = -self.custo_espiada
                        possible_states.append((new_state, prob, reward)) if prob > 0 else 0

            if action == 'Sair':
                new_state = self.leave_game(state)
                prob = 1
                reward = new_state[0]
                if self.bankrupted(new_state[0]):
                    reward = 0

                possible_states.append((new_state, prob, reward))
            
        # print(possible_states)
        # print('END ACTION\n')
        return possible_states    
            
        # END_YOUR_CODE

    def discount(self):
        """
        Return the descount  that is 1
        """
        return 1

# **********************************************************
# **                    PART 02 Value Iteration           **
# **********************************************************

class ValueIteration(util.MDPAlgorithm):
    """ Asynchronous Value iteration algorithm """
    def __init__(self):
        self.pi = {}
        self.V = {}

    def compute_possible_utilities(self, transition):
        possible_utilities = 0

        for state in transition:
            prob = state[1]
            reward = state[2]

            possible_utilities = prob * reward
            
        return possible_utilities

    def solve(self, mdp, epsilon=0.001):
        """
        Solve the MDP using value iteration.  Your solve() method must set
        - self.V to the dictionary mapping states to optimal values
        - self.pi to the dictionary mapping states to an optimal action
        Note: epsilon is the error tolerance: you should stop value iteration when
        all of the values change by less than epsilon.
        The ValueIteration class is a subclass of util.MDPAlgorithm (see util.py).
        """
        # print('START SOLVE')
        mdp.computeStates()
        def computeQ(mdp, V, state, action):
            # Return Q(state, action) based on V(state).
            return sum(prob * (reward + mdp.discount() * V[newState]) \
                            for newState, prob, reward in mdp.succAndProbReward(state, action))

        def computeOptimalPolicy(mdp, V):
            # Return the optimal policy given the values V.
            pi = {}
            for state in mdp.states:
                pi[state] = max((computeQ(mdp, V, state, action), action) for action in mdp.actions(state))[1]
            return pi


        # V = defaultdict(float)  # state -> value of state 
        V = {}
        # Implement the main loop of Asynchronous Value Iteration Here:
        # BEGIN_YOUR_CODE
        #raise Exception("Not implemented yet")
        gamma = mdp.discount()
        delta = 10000000

        for state in mdp.states:
            V[state] = 0

        while True:
            V_1 = {}
            for state in mdp.states:
                if state[2] is None:
                    V_1[state] = 0
                else:
                    V_1[state] = max(computeQ(mdp, V, state, action) for action in mdp.actions(state))
                     
            if max(abs(V[state] - V_1[state])  for state in mdp.states ) < epsilon:
                break

            V = V_1
        
        # END_YOUR_CODE

        # Extract the optimal policy now
        pi = computeOptimalPolicy(mdp, V)
        # print("ValueIteration: %d iterations" % numIters)
        self.pi = pi
        self.V = V

# First MDP
MDP1 = BlackjackMDP(valores_cartas=[1, 5], multiplicidade=2, limiar=10, custo_espiada=1)

# Second MDP
MDP2 = BlackjackMDP(valores_cartas=[1, 5], multiplicidade=2, limiar=15, custo_espiada=1)

def geraMDPxereta():
    """
    Return an instance of BlackjackMDP where peeking is the
    optimal action for at least 10% of the states.
    """
    # BEGIN_YOUR_CODE
    # raise Exception("Not implemented yet")
    MDPxereta = BlackjackMDP(valores_cartas=[1, 5, 11], multiplicidade=4, limiar=20, custo_espiada=1)
    return MDPxereta
    # END_YOUR_CODE


# **********************************************************
# **                    PART 03 Q-Learning                **
# **********************************************************

class QLearningAlgorithm(util.RLAlgorithm):
    """
    Performs Q-learning.  Read util.RLAlgorithm for more information.
    actions: a function that takes a state and returns a list of actions.
    discount: a number between 0 and 1, which determines the discount factor
    featureExtractor: a function that takes a state and action and returns a
    list of (feature name, feature value) pairs.
    explorationProb: the epsilon value indicating how frequently the policy
    returns a random action
    """
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    def getQ(self, state, action):
        """
         Return the Q function associated with the weights and features
        """
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    def getAction(self, state):
        """
        Produce an action given a state, using the epsilon-greedy algorithm: with probability
        |explorationProb|, take a random action.
        """
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    def getStepSize(self):
        """
        Return the step size to update the weights.
        """
        return 1.0 / math.sqrt(self.numIters)

    def incorporateFeedback(self, state, action, reward, newState):
        """
         We will call this function with (s, a, r, s'), which you should use to update |weights|.
         You should update the weights using self.getStepSize(); use
         self.getQ() to compute the current estimate of the parameters.

         HINT: Remember to check if s is a terminal state and s' None.
        """
        # BEGIN_YOUR_CODE
        for feature in blackjackFeatureExtractor(state, action):
            self.weights[feature[0]] = feature[1]

        return self.weights
        #raise Exception("Not implemented yet")
        # END_YOUR_CODE

def identityFeatureExtractor(state, action):
    """
    Return a single-element list containing a binary (indicator) feature
    for the existence of the (state, action) pair.  Provides no generalization.
    """
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

# Large test case
largeMDP = BlackjackMDP(valores_cartas=[1, 3, 5, 8, 10], multiplicidade=3, limiar=40, custo_espiada=1)

# **********************************************************
# **        PART 03-01 Features for Q-Learning             **
# **********************************************************

def blackjackFeatureExtractor(state, action):
    """
    You should return a list of (feature key, feature value) pairs.
    (See identityFeatureExtractor() above for a simple example.)
    """
    # BEGIN_YOUR_CODE
    # raise Exception("Not implemented yet")
    # Features
    # 1 - (pontos_na_mao, int)
    # 2 - (n_cartas_restantes, int)
    features = []
    features.append(('points', state[0]))
    features.append(('cards_left', sum(state[2])))

    return features
    # END_YOUR_CODE

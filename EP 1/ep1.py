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

  Nome : LUCAS ROBERTO DA COSTA DE SANTANA
  NUSP : 11891371

  Referencias: Com excecao das rotinas fornecidas no enunciado
  e em sala de aula, caso voce tenha utilizado alguma referencia,
  liste-as abaixo para que o seu programa nao seja considerado
  plagio ou irregular.

  Exemplo:
  - O algoritmo Quicksort foi baseado em:
  https://pt.wikipedia.org/wiki/Quicksort
  http://www.ime.usp.br/~pf/algoritmos/aulas/quick.html
  https://journals.sagepub.com/doi/full/10.1155/2014/532759
"""

from typing import Tuple, List
import util

############################################################
# Part 1: Segmentation problem under a unigram model


class SegmentationProblem(util.Problem):
    def __init__(self, query: str, unigramCost: object):
        self.query = query
        self.unigramCost = unigramCost

    def isState(self, state: Tuple[str, str]) -> bool:
        """ Metodo que implementa verificacao de estado """
        if type(state) == tuple and type(state[0]) == str and type(state[1]) == str:
            return True
        else:
            return False

    def initialState(self, query: str) -> Tuple[str, str]:
        """ Metodo que implementa retorno da posicao inicial

        Args:
            query: str
                Query inicial do problema

        Returns
            initial_state: tuple 
        """
        initial_state = (query, str())

        return initial_state


    def actions(self, state: Tuple[str, str]) -> List[Tuple[str, str]]:
        """ Metodo que implementa retorno da lista de acoes validas
        para um determinado estado

        A acao possível é separar a palavra do estado em duas, fazendo
        todas as possibilidades de separação.

        Args:
            state: tuple
                Estado atual. ex: ('beliebeinyourself', '')
        
        Returns:
            possible_states: list
                Possíveis estados da palavra separada
                Ex: [
                        ('elieveinyourselfhavefaithinyourabilities', 'b'), 
                        ('lieveinyourselfhavefaithinyourabilities', 'be')
                    ]
        """

        word = state[0]
        possible_states = []

        for index in range(0, len(word)):
            right_word = word[-index-1: ]
            left_word = word[:-index-1]

            if state[1] == '':
                _word = [right_word]
            else:
                _word = [state[1]] + [right_word]
            _word = ' '.join(_word)
            possible_states.append((left_word, _word))

        return possible_states

    def nextState(self, state: Tuple[str, str], action: Tuple[str, str]) -> Tuple[str, str]:
        """ Metodo que implementa funcao de transicao """
        next_state = (action[0], action[1])

        return next_state

    def isGoalState(self, state: Tuple[str, str]) -> bool:
        """ Metodo que implementa teste de meta """
        if state[0] == '':
            return True
        else:
            return False

    def stepCost(self, state: Tuple[str, str], action: object) -> List[float]:
        """ Metodo que implementa funcao custo """
        residual_state_cost = action(state[0])
        state_cost = sum([action(x) for x in state[1].split()])
        step_cost = state_cost

        return step_cost

def segmentWords(query, unigramCost):

    if len(query) == 0:
        return ''
        
    # BEGIN_YOUR_CODE 

    else:
        sp = SegmentationProblem(
                                query=query, 
                                unigramCost=unigramCost
                                )
        
        state = sp.initialState(query=query)
        print(f'INITIAL STATE {state}')

        while not sp.isGoalState(state=state):
            if sp.isState(state=state):
                possible_states = sp.actions(state=state)
                costs = [sp.stepCost(state=x, action=unigramCost) for x in possible_states]
                index_min_cost = costs.index(min(costs))
                state = sp.nextState(state=state, action=possible_states[index_min_cost])
            else:
                return 'Não é estado'
        result_segment = ' '.join(reversed(state[1].split()))
        print('##### RESULT SEGMENT #####')
        print(result_segment)
        print('\n')
        return result_segment

    # Voce pode usar a função getSolution para recuperar a sua solução a partir do no meta
        # valid, solution  = util.getSolution(
        #                                     problem = 'believeinyourselfhavefaithinyourabilities'
        #                                     )

    #raise NotImplementedError

    # END_YOUR_CODE

############################################################
# Part 2: Vowel insertion problem under a bigram cost


class VowelInsertionProblem(util.Problem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def isState(self, state):
        """ Metodo  que implementa verificacao de estado """
        raise NotImplementedError

    def initialState(self):
        """ Metodo  que implementa retorno da posicao inicial """
        raise NotImplementedError

    def actions(self, state):
        """ Metodo  que implementa retorno da lista de acoes validas
        para um determinado estado
        """
        raise NotImplementedError

    def nextState(self, state, action):
        """ Metodo que implementa funcao de transicao """
        raise NotImplementedError

    def isGoalState(self, state):
        """ Metodo que implementa teste de meta """
        raise NotImplementedError

    def stepCost(self, state, action):
        """ Metodo que implementa funcao custo """
        raise NotImplementedError



def insertVowels(queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_CODE 
    # Voce pode usar a função getSolution para recuperar a sua solução a partir do no meta
    # valid,solution  = util.getSolution(goalNode,problem)
    raise NotImplementedError
    # END_YOUR_CODE

############################################################


def getRealCosts(corpus='corpus.txt'):

    """ Retorna as funcoes de custo unigrama, bigrama e possiveis fills obtidas a partir do corpus."""
    
    _realUnigramCost, _realBigramCost, _possibleFills = None, None, None
    if _realUnigramCost is None:
        print('Training language cost functions [corpus: ' + corpus + ']... ')
        
        _realUnigramCost, _realBigramCost = util.makeLanguageModels(corpus)
        _possibleFills = util.makeInverseRemovalDictionary(corpus, 'aeiou')

        print('Done!')

    return _realUnigramCost, _realBigramCost, _possibleFills

def main():
    """ Voce pode/deve editar o main() para testar melhor sua implementacao.

    A titulo de exemplo, incluimos apenas algumas chamadas simples para
    lhe dar uma ideia de como instanciar e chamar suas funcoes.
    Descomente as linhas que julgar conveniente ou crie seus proprios testes.
    """
    unigramCost, bigramCost, possibleFills  =  getRealCosts()
    
    resulSegment = segmentWords('believeinyourselfhavefaithinyourabilities', unigramCost)
    print(resulSegment)
    
    # resultInsert = insertVowels('smtms ltr bcms nvr'.split(), bigramCost, possibleFills)
    # print(resultInsert)

if __name__ == '__main__':
    main()

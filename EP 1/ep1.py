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
import unidecode

############################################################
# Part 1: Segmentation problem under a unigram model


class SegmentationProblem(util.Problem):
    def __init__(self, query: str, unigramCost: object):
        self.query = query
        self.unigramCost = unigramCost

    def isState(self, state: Tuple[str, str]) -> bool:
        """ Metodo que implementa verificacao de estado """
        if type(state) == str:
            return True
        else:
            print('Não é um estado válido')
            return False
        
        # return True

    def initialState(self) -> Tuple[str, str]:
        """ Metodo que implementa retorno da posicao inicial

        Args:
            query: str
                Query inicial do problema

        Returns
            initial_state: tuple 
        """
        query = unidecode.unidecode(self.query.lower())

        return query


    def actions(self, state: Tuple[str, str]) -> List[Tuple[str, str]]:
        """ Metodo que implementa retorno da lista de acoes validas
        para um determinado estado

        A acao possível é separar a palavra do estado em duas, fazendo
        todas as possibilidades de separação.

        Args:
            state: tuple
                Estado atual. ex: ('beliebeinyourself', '')
        
        Returns:
            actions: list(tuple)
                Possíveis estados da palavra separada
                Ex: [
                        ('elieveinyourselfhavefaithinyourabilities', 'b'), 
                        ('lieveinyourselfhavefaithinyourabilities', 'be')
                    ]
        """
        state = state.split()
        word = state[0]
        actions = []
        
        for index in range(0, len(word)):
            action = state.copy()
            right_word = word[-index-1: ]
            left_word = word[:-index-1]
            
            action[0] = left_word
            action.append(right_word)
            actions.append(' '.join(action))
        
        return actions

    def nextState(self, state: Tuple[str, str], action: Tuple[str, str]) -> Tuple[str, str]:
        """ Metodo que implementa funcao de transicao """
        next_state = action
        # next_state = action

        return next_state

    def isGoalState(self, state: Tuple[str, str]) -> bool:
        """ Metodo que implementa teste de meta """
        if state[0] == '':
            return True
        else:
            return False

        # if ''.join(reversed(state.split())) == self.query:
        #     return True
        # else:
        #     False

    def stepCost(self, state: Tuple[str, str], action: Tuple[str, str]) -> float:
        """ Metodo que implementa funcao custo """
        # state_cost = sum([self.unigramCost(x) for x in state])
        # action_cost = sum([self.unigramCost(x) for x in action])

        state_cost = sum([self.unigramCost(x) for x in state.split()])
        action_cost = sum([self.unigramCost(x) for x in action.split()])
        step_cost = action_cost
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

        goal_sp_node = util.uniformCostSearch(sp)
        result_segment = ' '.join(reversed(goal_sp_node.state.split()))
        
        # valid, solution  = util.getSolution(goal_sp_node, sp)
        # print(valid, solution)
        
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

    def isState(self, state: Tuple[str, str]) -> bool:
        """ Metodo  que implementa verificacao de estado """
        if type(state) == tuple and type(state[0]) == str and type(state[1]) == str:
            return True
        else:
            print('Estado não é válido')
            return False

    def initialState(self) -> Tuple[str, str]:
        """ Metodo  que implementa retorno da posicao inicial """
        queryWords = unidecode.unidecode(' '.join(self.queryWords).lower())

        initial_state = (queryWords, str())

        return initial_state

    def actions(self, state: Tuple[str, str]) -> List[Tuple[str, str]]:
        """ Metodo  que implementa retorno da lista de acoes validas
        para um determinado estado
        """
        old_phrase = state[0]
        words = old_phrase.split()
        actions = []

        if len(words) > 1:
            first_element = self.possibleFills(words[0])
            second_element = self.possibleFills(words[1])

            for _f in first_element:
                for _s in second_element:
                    actions.append((_f, _s))
        else:
            first_element = self.possibleFills(words[0])
            if first_element:
                actions.append((list(first_element)[0], list(first_element)[0]))
            else:
                actions.append((str(), str()))
        
        return actions

    def nextState(self, state: Tuple[str, str], action: Tuple[str, str]) -> List[Tuple[str, str]]:
        """ Metodo que implementa funcao de transicao """
        
        broken_phrase = state[0].split()
        fixed_phrase = state[1]
        
        if action[0] or action[1]:
            if len(broken_phrase) == 2:
                fixed_phrase = state[1] + ' ' + action[0] + ' ' + action[1]
                broken_phrase.pop(0)
                broken_phrase.pop(0)
            
            else:
                fixed_phrase = fixed_phrase + ' ' + action[0]        
                broken_phrase.pop(0)

            broken_phrase = ' '.join(broken_phrase)
            next_state = (broken_phrase, fixed_phrase)
        
        else:
            next_state = (str(), state[0])

        return next_state
        

    def isGoalState(self, state: Tuple[str, str]):
        """ Metodo que implementa teste de meta """
        if state[0] == '':
            return True
        else:
            return False

    def stepCost(self, state: Tuple[str, str], action: Tuple[str, str]) -> float:
        """ Metodo que implementa funcao custo """
        # state_cost = self.bigramCost(state[0], state[1])
        action_cost = self.bigramCost(action[0], action[1])

        step_cost = action_cost
        
        return step_cost



def insertVowels(queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_CODE 

    vip = VowelInsertionProblem(
                                queryWords=queryWords, 
                                bigramCost=bigramCost, 
                                possibleFills=possibleFills
                                )

    goal_vowel_node = util.uniformCostSearch(vip)

    result_insert = goal_vowel_node.state[1].split()
    result_insert = ' '.join(result_insert)
    
    # valid, solution  = util.getSolution(goal_vowel_node, vip)
    # print(valid, solution)

    return result_insert

    # Voce pode usar a função getSolution para recuperar a sua solução a partir do no meta
    # valid, solution  = util.getSolution(goal_vowel_node, vip)
    # print(valid, solution)
    #raise NotImplementedError
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
    
    print('### TESTING MAIN FUNCTIONS ###')
    resulSegment = segmentWords('believeinyourselfhavefaithinyourabilities', unigramCost)
    print(resulSegment)
    
    resultInsert = insertVowels('smtms ltr bcms nvr'.split(), bigramCost, possibleFills)
    print(resultInsert)

if __name__ == '__main__':
    main()

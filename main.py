import numpy as np
from random import random, choice
import curses

class Ambiente:
    def __init__(self, largura, altura, tropeco):
        self.largura = largura
        self.altura = altura
        self.tropeco = tropeco
        self.suprimentos_iniciais = [[1, 1], [3, 3]]
        self.pedra = [4, 4]
        self.suprimentos = self.suprimentos_iniciais.copy()
        self.zumbi = [[3, 1], [1, 3]]
        self.zona_segura = [5, 5]
        self.reseta()

    def reseta(self):
        self.posicao = [0, 0]
        self.suprimentos = self.suprimentos_iniciais.copy()  # Resetar suprimentos
        return self.posicao.copy()

    def imprime_tabela_ambiente(self, stdscr):
        tabela = np.full((self.altura, self.largura), ' ', dtype=str)
        tabela[self.posicao[0]][self.posicao[1]] = 'A'

        for suprimento in self.suprimentos:
            tabela[suprimento[0]][suprimento[1]] = 'S'

        for zumbi in self.zumbi:
            tabela[zumbi[0]][zumbi[1]] = 'Z'
        tabela[self.pedra[0]][self.pedra[1]] = 'P'
        tabela[self.zona_segura[0]][self.zona_segura[1]] = 'E'

        linha_superior_inferior = '+' + '---+' * self.largura
        stdscr.clear()
        stdscr.addstr(linha_superior_inferior + '\n')
        for linha in tabela:
            linha_meio = '|'
            for elemento in linha:
                linha_meio += f' {elemento} |'
            stdscr.addstr(linha_meio + '\n')
            stdscr.addstr(linha_superior_inferior + '\n')
        stdscr.refresh()

    def acoes(self, acao_agente):
        if acao_agente == 0:
            self.posicao[0] -= 1
        elif acao_agente == 1:
            self.posicao[1] += 1
        elif acao_agente == 2:
            self.posicao[0] += 1
        elif acao_agente == 3:
            self.posicao[1] -= 1
        else:
            print('Ação inválida: {}'.format(str(acao_agente)))

        if random() < self.tropeco:
            self.posicao[0] += choice([-1, 0, 1])
            self.posicao[1] += choice([-1, 0, 1])

        self.posicao[0] = min(self.altura - 1, max(0, self.posicao[0]))
        self.posicao[1] = min(self.largura - 1, max(0, self.posicao[1]))

        recompensa = 0
        final = False
        if self.posicao in self.suprimentos:
            self.suprimentos.remove(self.posicao)
            recompensa = 10
        elif self.posicao in self.zumbi:
            recompensa = -10
        elif self.posicao == self.pedra:
            recompensa = -10
        elif self.posicao == self.zona_segura:
            recompensa = 50
            final = True

        return self.posicao.copy(), recompensa, final

class QLearning:
    def __init__(self, altura, largura, alpha=0.1, epsilon=0.1, gamma=0.7, acoes=4):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.acoes = acoes
        self.altura = altura
        self.largura = largura
        self.qtable = np.zeros((altura, largura, acoes))

    def saveQTable(self, filename):
            with open(filename, 'w') as f:
                f.write("Pos\t|\tUp\t|\tRight\t|\tDown\t|\tLeft\t|\n")
                for i in range(self.altura):
                    for j in range(self.largura):
                        f.write("%d,%d\t|\t%.2f\t|\t%.2f\t|\t%.2f\t|\t%.2f\t|\n" % 
                                (i, j, self.qtable[i][j][0], self.qtable[i][j][1], self.qtable[i][j][2], self.qtable[i][j][3]))

    def pega_maior_q(self, posicao):
        return max(self.qtable[posicao[0]][posicao[1]])

    def pega_melhor_acao(self, posicao):
        valores_q = self.qtable[posicao[0]][posicao[1]]
        valor_maximo = max(valores_q)
        melhores = [i for i, j in enumerate(valores_q) if j == valor_maximo]
        return choice(melhores)

    def pega_acao_aleatoria(self):
        return int(random() * self.acoes)

    def pega_acao(self, posicao):
        if random() < self.epsilon:
            return self.pega_acao_aleatoria()
        else:
            return self.pega_melhor_acao(posicao)

    def update(self, posicao_antiga, acao, nova_posicao, recompensa, final):
        if final:
            self.qtable[posicao_antiga[0]][posicao_antiga[1]][acao] += self.alpha * (recompensa - self.qtable[posicao_antiga[0]][posicao_antiga[1]][acao])
        else:
            self.qtable[posicao_antiga[0]][posicao_antiga[1]][acao] += self.alpha * (recompensa + self.gamma * self.pega_maior_q(nova_posicao) - self.qtable[posicao_antiga[0]][posicao_antiga[1]][acao])


def main(stdscr):
    largura = 6
    altura = 6
    tropeco = 0.1
    episodios = 120000

    alpha = 0.1
    epsilon = 0.1

    mapa = Ambiente(largura, altura, tropeco)
    ql = QLearning(altura, largura, alpha, epsilon)

    # Treinamento do agente
    for i in range(episodios):
        posicao_atual = mapa.reseta()
        for etapa in range(altura * largura):
            acao = ql.pega_acao(posicao_atual)
            nova_posicao, recompensa, final = mapa.acoes(acao)
            ql.update(posicao_atual, acao, nova_posicao, recompensa, final)
            posicao_atual = nova_posicao
            if final:
                break

    ql.saveQTable('qtable.txt')

    # Simulação do agente usando a melhor política aprendida
    posicao_atual = mapa.reseta()
    recompensa_total = 0
    stdscr.nodelay(True)
    while True:
        mapa.imprime_tabela_ambiente(stdscr)
        acao = ql.pega_melhor_acao(posicao_atual)
        nova_posicao, recompensa, final = mapa.acoes(acao)
        posicao_atual = nova_posicao
        recompensa_total += recompensa
        curses.napms(500)
        if final:
            break

    mapa.imprime_tabela_ambiente(stdscr)
    stdscr.addstr("Agente chegou ao destino final!\n")
    stdscr.addstr("Recompensa: {}".format(recompensa_total))
    stdscr.refresh()
    curses.napms(2000)

if __name__ == "__main__":
    curses.wrapper(main)

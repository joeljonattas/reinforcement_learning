# Inteligência Artificial

## Implementação - Reinforcement Learning

Vamos criar um algoritmo de reinforcement learning (aprendizado por reforço) inspirado no jogo "The Last of Us”. Neste cenário, nosso agente será um sobrevivente em um ambiente pós-apocalíptico infestado por zumbis. 

O objetivo do agente é maximizar sua recompensa acumulada ao longo do tempo, coletando suprimentos (comida, água, medicamentos) e evitando zumbis.


## Ambiente

* O ambiente é um grid 2D que representa a área pós-apocalíptica;

* Cada célula do grid pode conter um dos seguintes elementos: agente, zumbi, parede, pedras, suprimento (comida, água, medicamentos..), porta (área segura) ou espaço vazio.

## Ações do Agente

* O agente pode executar quatro ações: mover para cima, mover para baixo, mover para a esquerda e mover para a direita;

* O agente pode realizar uma ação por vez e se mover para uma célula adjacente no grid.


## Recompensas

* O agente recebe recompensas com base em suas ações no ambiente;
* +10 pontos para cada suprimento coletado;
* -10 pontos para cada encontro com um zumbi;
* O episódio termina após um número fixo de passos, quando o agente é capturado por um zumbi ou quando alcança uma área segura.

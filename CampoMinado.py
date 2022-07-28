#Criar um quadro como objeto para representar o Campo Minado
#Isto quer dizer que podemos dizer: "Criar uma novo quadro", ou "Cave aqui", ou "Renderize este jogo a partir deste objeto
import random
import re


class Board:
    def __init__(self, dim_size, num_bombs):
        #Deixarei traos deste parâmetro, vai ser de grande ajuda posteriormente
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        #Criação do quadro
        #Função Salvadora
        self.board = self.make_new_board() #Plantar as bombas
        self.assign_value_to_board()

        #iniciar um conjunto para manter traços das localizações escolhidas que cobrimos
        #Salvarei (row, col) tuplas dentro deste conjunto
        self.dug = set() #se escolher 0, 0, então self.dug = {(0,0)}

    def make_new_board(self):
        #Contrói um novo quadro baseado na dim_size e do num_bombs
        #Devemos contruir a listas das listas
        #Enquanto tivermos um quadro 2-D, a lista das Listas


        # Gerar um novo quadro
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        # Vai criar um array assim:
        # [[None, None,....,None],
        #  [None, None,..., None]
        #  [...                 ]
        #  [None, None,... , None]]
        # Conseguiremos ver como será representado no quadro

        # Plantar as bombas
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size ** 2 - 1)  # Retorna para um número inteiro N desde que a <= N <= b
            row = loc // self.dim_size  # Quero o número de vezes que o dim_sizes vai para a variável loc e nos contar
            col = loc % self.dim_size  # Queremos o restante para falar qual index do row está no loc

            if board[row][col] == '*':
                # Isto significa que atualmente plantaram as bombas, então continua.
                continue

            board[row][col] = '*'  # Plantar a bomba
            bombs_planted += 1

        return board

    def assign_value_to_board(self):
        # Agora que temos as bombas plantadas, vamos atribuir um número 0-8 para todos os espaços vazios,
        # o que representa quantas bombas vizinhas existem. Podemos pré-computá-los e isso vai nos salvar
        # algum esforço verificando o que está em torno do conselho mais tarde.
        for r in range (self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    #Se isto for a bomba, não preciso calcular nada
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)


    def get_num_neighboring_bombs(self, row, col):
        # Vamos iterar através de cada uma das posições vizinhas e somar números de bombas
        # top left: (row-1, col-1)
        # #top middle: (row-1, col)
        # top right: (row-1, col+1)
        # left: (row, col-1)
        # right: (row, col+1)
        # bottom left: (row+1, col-1)
        # bottom middle: (row+1, col)
        # bottom right: (row+1, col+1)

        #Ter certeza que não saia do quadro

        num_neighboring_bombs = 0
        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if r == row and c == col:
                    # our original location, don't check
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):
        # Cavar a localização
        # retornar VERDADEIRO se for um sucesso o cavar, FALSO se achar uma bomba

        #Cenários
        # acertar a bomba -> Game Over
        # cavar onde há bombas por perto -> acaba o "cavar"
        # cavar numa localização onde não há bombas próximas -> Recursivamente cava os blocos vizinhos

        self.dug.add((row, col)) #Deixa marcado que cavamos aqui

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        # self.board[row][col] == 0
        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if(r, c) in self.dug:
                    continue #Não cave onde você já cavou
                self.dig(r, c)

        #Se onde iniciou a cavação não acertar a bomba, não acertará aqui
        return True

    def __str__(self):
        # Função mágica para caso você chame a fução PRINT sobre este objeto
        # irá mostrar na tela o que essa função retorna
        #Retornar um string para mostrar o quadro para o player

        # Primeiro: criar um array para representar o que o usuário verá
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '


        #Colocar isso junto dentro de uma string
        string_rep = ''
        #Pegar o máximo de coluna e mostrar na tela
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )
        #Printar o cvs strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '    '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '   '.join(cells)
        indices_row += '   \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


#Função para iniciar o game:
def play(dim_size=10, num_bombs=10):

    # 1 - criar o quadro e plantar as bombas
    board = Board(dim_size, num_bombs)

    # 2 - Mostrar ao usuário o quadro e perguntar onde ele quer cavar ou "clicar"
    # 3a - Se a localização for a bomba, mostrar a mensagem "Game Over"
    # 3b - Se a localização não for a bomba, continua cavando até chegar a próxima bomba
    # 4 - Repetir o passo 2 e 3a/b até não ter mais local para cavar ---> Vitória!!
    safe = True


    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input('Onde você gostaria de cavar? Escreva a linha e a coluna: ')) #'0, 3'
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print('Localização inválida, por favor tente novamente!')
            continue


        #Se o usuário cavar num local válido
        safe = board.dig(row, col)
        if not safe:
            #cavou um bomba
            break #Game Over


    #2 maneiras de encerrar o loop
    if safe:
        print("Parabéns. Você ganhou!!")
    else:
        print("Vish....Acabou o jogo!")
        #Revelar o quadro
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)



if __name__ == '__main__':
        play()


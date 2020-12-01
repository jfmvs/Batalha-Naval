import pygame as pg


class WorldManager:
    """
    Descrição
    ---------
    WorldManager divide o mundo em chunks e distribui objetos do jogo
    entre os chunks para reduzir o número de objetos a serem renderizados
    e testados para colisão.

    Atributos
    ---------
    _columns : int
        número de colunas da matriz que representa o mundo
    _rows : int
        número de linhas da matriz que representa o mundo
    _chunk_width : int
        largura de um chunk
    _chunk_height : int
        altura de um chunk
    _chunks : dict
        dicionário tuple-list que armazena uma lista de objetos do jogo
        usando sua posição na matriz como chave

    Métodos
    -------
    add_obj(obj):
        verifica a posição do objeto `obj` para adicioná-lo à lista do
        chunk adequado
    get_objs(chunk):
        retorna a lista de objetos do chunk na posição `chunk`
    get_active_chunks(pos):
        retorna com os chunks mais próximos da posição `pos`
    clamp_coords(coords):
        garante que `coords` seja uma posição válida na matriz dos
        chunks
    """
    def __init__(self, world_size, chunk_size):
        """
        Descrição
        ---------
        Inicializa uma instância de WorldManager

        Parâmetros
        ----------
        world_size : list, tuple
            largura e altura totais do mundo em pixels
        chunk_size: list, tuple
            largura e altura de um chunk
        """
        self._columns, self._rows = world_size
        self._chunk_width, self._chunk_height = chunk_size
        self._chunks = {}

        for j in range(self._rows):
            for i in range(self._columns):
                self._chunks[(j, i)] = []

    def add_obj(self, obj):
        """
        Descrição
        ---------
        Posiciona um objeto do jogo `obj` à lista de um chunk
        dependente de sua posição

        Parâmetros
        ----------
        obj : any
            objeto a ser adicionado à lista de um chunk

        Retorno
        -------
        None
        """
        grid_pos = (obj.position.x // self._chunk_width, obj.position.y // self._chunk_height)
        try:
            self._chunks[grid_pos].append(obj)
        except KeyError:
            self._chunks[grid_pos] = [obj]

    def get_objs(self, chunk):
        """
        Descrição
        ---------
        Retorna a lista de objetos do chunk na posição `chunk`

        Parâmetros
        ----------
        chunk : list, tuple
            a posição do chunk na matriz do mundo

        Retorno
        -------
        lis

        Exceções
        --------
        KeyError
            se `chunk` não for a posição de um chunk válido
        """
        return self._chunks[chunk]

    def get_active_chunks(self, pos):
        """
        Descrição
        ---------
        Retorna a lista de posições dos chunks mais próximos da posição
        `pos`

        Parâmetros
        ----------
        pos : pygame.Vector2
            posição de um objeto do jogo

        Retorno
        -------
        list
        """
        main = pg.Vector2((pos.x // self._chunk_width, pos.y // self._chunk_height))
        main_center = pg.Vector2((
            main[0] * self._chunk_width  + self._chunk_width  // 2,
            main[1] * self._chunk_height + self._chunk_height // 2
        ))

        dist = pos - main_center
        dist.x = max([min([dist.x, 1]), -1])
        dist.y = max([min([dist.y, 1]), -1])

        active = [
            self.clamp_coords((          main.x,          main.y )),
            self.clamp_coords(( dist.x + main.x,          main.y )),
            self.clamp_coords((          main.x, dist.y + main.y )),
            self.clamp_coords(( dist.x + main.x, dist.y + main.y ))
        ]
        active = list(dict.fromkeys(active))
        return active

    def clamp_coords(self, coords):
        """
        Descrição
        ---------
        Caso um dos valores de `coords` esteja fora de seu intervalo
        válido, retorna uma tupla que substitui o valor inválido pelo
        limite. Se os dois forem válidos, retorna coords

        Parâmetros
        ----------
        coords : list, tuple
            posição de um chunk na matriz

        Retorno
        -------
        tuple
        """
        pos = [int(coords[0]), int(coords[1])]

        pos[0] = min([pos[0], self._columns])
        pos[1] = min([pos[1], self._rows])

        pos[0] = max([pos[0], 0])
        pos[1] = max([pos[1], 0])

        return tuple(pos)
# Quake Log Parser / Game API


API desenvolvida com o intuito de prover informações das partidas do jogo 'Quake 3 Arena', extraídas do arquivo `games.log` através de um `script` capaz de parsear e agrupar os dados de cada jogo, coletando as seguintes informações por cada partida:

- `game_<id>` - Identificação de cada partida;
- `players` - Lista dos jogadores da partida;
- `kills` - Contagem de kills por cada jogador (exceto suícidios), e subtraindo 1 ponto por cada kill pelo `<world>`.
- `total_kills` - Contagem total de kills, incluindo mortes do `<world>` e suicídios.
#

Antes de começar é necessário a criação e ativação de uma VirtualEnv com Python 3.6, recomendo a utilização do pyenv.
Após isso, vá para a pasta raiz desse projeto (QuakeLogParser) e siga as instruções abaixo.

1) Instale os requisitos do projeto:

    ```
    $ make requirements_dev
    ```

2) Suba o container do `mongo` no docker:

    ```
    $ make up
    ```

3) Para executar o `script` que parseia os dados de `games.log` execute:

    ```
    $ make run
    ```

4) Para subir a API utilize:
    ```
    $ make runserver
    ```
 

## Testando com curl:

- Retorna todas os jogos:

    - request:

    ```
    $ curl http://127.0.0.1:8000/games/
    ```

    ou
    ```
    $ curl http://127.0.0.1:8000/games/ | python -m json.tool  # pretty view
    ```
    - response:
    
    ```
    {
        "game_1": {
            "total_kills": 0,
            "players": [
                "Isgalamido"
            ],
            "kills": {
                "Isgalamido": 0
            }
        },

        ...

    }
    ```

- Retorna um jogo em específico utilizando `id`:

    - request:

    ```
    $ curl http://127.0.0.1:8000/game/1/
    ```
    ou

    ```
    $ curl http://127.0.0.1:8000/game/1/ | python -m json.tool  # pretty view
    ```
    - response
    ```
    {
        "game_id": "1",
        "game_info": {
            "game_1": {
                "total_kills": 0,
                "players": [
                    "Isgalamido"
                ],
                "kills": {
                    "Isgalamido": 0
                }
            }
        }
    }
    ```
#    

Para executar os testes unitários utilize:

    ```
    $ make unit
    ```
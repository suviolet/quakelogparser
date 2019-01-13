import logging
import re

from core.settings import FORMAT
from db.mongo import MongoClient

logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)


class ParseGamesLog():

    def __init__(self):
        self.games = {}

        self.client = MongoClient()
        logger.info('Connecting to MongoDB')

        self.initgame_pattern = re.compile(r'.*InitGame.*')
        self.user_pattern = re.compile(r'.*n\\(.*)\\t\\')
        self.kill_pattern = re.compile(r'.*Kill:.*:\s(.*)\skilled\s(.*)by.*')

    def parse_log(self):
        logger.info('Start to parse games.log file')

        try:
            with open('./games.log', 'r', encoding='utf-8') as f:
                logging.info('Reading file: games.log')
                quakelog = f.read()
        except FileNotFoundError:
            logger.error('File games.log not found')
            return

        game_count = 1

        for line in quakelog.split('\n'):

            if self.initgame_pattern.match(line):
                key_game = 'game_{count}'.format(count=game_count)
                self.games[key_game] = {
                    'total_kills': 0,
                    'players': [],
                    'kills': {}
                }
                game_count += 1
                logger.info(
                    'Found new game: {game}, starting parse info about '
                    'players and kills'.format(game=key_game)
                )

            elif self.user_pattern.match(line):
                player = self.user_pattern.match(line)
                player = player.group(1).strip()
                if player not in self.games[key_game]['players']:
                    self.games[key_game]['players'].append(player)
                    self.games[key_game]['kills'][player] = 0
                    logger.info('Found player: {player}'.format(player=player))

            elif self.kill_pattern.match(line):
                self.parse_kills(line, key_game)

        list_games = [
            {
                'game_id': k.split('_')[1],
                'game_info': {k: v}
            } for k, v in self.games.items()
        ]

        if list_games:
            self.client.collection.insert_many(list_games)
            logger.info(
                'Recording parsed games in MongoDB: {games}'.format(
                    games=self.games
                )
            )
        else:
            logger.warning('There are no games to record')

    def parse_kills(self, line, key_game):
        players = self.kill_pattern.match(line)
        player_alive = players.group(1).strip()
        player_dead = players.group(2).strip()

        self.games[key_game]['total_kills'] += 1

        if player_alive != '<world>':
            if player_alive != player_dead:
                self.games[key_game]['kills'][player_alive] += 1
        else:
            self.games[key_game]['kills'][player_dead] -= 1

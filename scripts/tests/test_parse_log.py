from unittest.mock import mock_open, patch

from scripts.parse_log import ParseGamesLog


class TestParseGamesLog:

    def test_execute_parse_log(self, collection, file_response_json):
        ParseGamesLog().parse_log()

        games = collection.find()

        games_dict = {}
        for g in games:
            game_key = [list(g['game_info'].keys())[0]][0]
            games_dict[game_key] = g['game_info'][game_key]

        assert games_dict == file_response_json
        assert collection.estimated_document_count() == 21

    def test_execute_parse_log_with_empty_games_log(self, caplog, collection):
        with patch('builtins.open', mock_open(read_data='')):
            ParseGamesLog().parse_log()

        game = collection.find_one()
        assert game is None
        assert 'There are no games to record' in caplog.records[3].getMessage()

    def test_execute_parse_log_without_games_log(self, caplog, collection):
        with patch('builtins.open', side_effect=FileNotFoundError):
            ParseGamesLog().parse_log()

        game = collection.find_one()
        assert game is None
        assert 'File games.log not found' in caplog.records[2].getMessage()

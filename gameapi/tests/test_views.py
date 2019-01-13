import pytest


class TestViewGameapi:

    def test_retrieve_games_with_success(
        self,
        client,
        populate_db,
        collection
    ):
        response = client.get('/games/')

        games = collection.find()
        games_dict = {}
        for g in games:
            game_key = [list(g['game_info'].keys())[0]][0]
            games_dict[game_key] = g['game_info'][game_key]

        assert response.status_code == 200
        assert response.json() == games_dict
        assert len(response.json()) == 21


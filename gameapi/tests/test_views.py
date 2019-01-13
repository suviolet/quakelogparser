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

    def test_retrieve_game(self, client, populate_db, collection):
        response = client.get('/game/1/')

        game_one = collection.find_one({'game_id': '1'})
        del game_one['_id']

        assert response.status_code == 200
        assert response.json() == game_one

    def test_retrieve_game_not_found_with_pre_populated_db(
        self,
        client,
        populate_db,
        collection
    ):
        response = client.get('/game/22/')

        assert response.status_code == 404
        assert response.json() == {'error': 'game not found'}

    @pytest.mark.parametrize('game_id', ['1', '22'])
    def test_retrieve_game_not_found_with_empty_db(
        self,
        client,
        collection,
        game_id
    ):
        response = client.get('/game/{game_id}/'.format(game_id=game_id))

        assert response.status_code == 404
        assert response.json() == {'error': 'game not found'}

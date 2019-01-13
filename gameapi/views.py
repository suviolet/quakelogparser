
from django.http import JsonResponse

from db.mongo import MongoClient

collection = MongoClient().collection


def games(request):
    games = collection.find()
    games_dict = {}

    for g in games:
        games_key = [list(g['game_info'].keys())][0][0]
        games_dict[games_key] = g['game_info'][games_key]

    return JsonResponse(games_dict)


def game(request, game_id):
    game_one = collection.find_one({'game_id': game_id})

    if game_one:
        del game_one['_id']
        return JsonResponse(game_one)
    return JsonResponse({'error': 'game not found'}, status=404)

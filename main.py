from flask import Flask, request, jsonify

from entity.Game import Game
from enums.GameStatus import GameStatus

app = Flask(__name__)
games = []


# 新增遊戲
@app.route('/game', methods=["POST"])
def create_game():
    data = request.get_json()
    name = data["name"]
    game = Game(len(games) + 1, name)
    game_dict = game.to_json_object()
    games.append(game)
    return jsonify(game_dict), 200


# 下注
@app.route('/game/<int:game_id>/bet', methods=["POST"])
def game_bet(game_id):
    data = request.get_json()
    game:Game = next((b for b in games if b.id == game_id), None)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    if game.status != GameStatus.NEW:
        return "operation error", 400
    #清空手牌
    game.player.hand.clear()
    game.dealer.hand.clear()
    #下注
    bet=data.get("bet")
    if game.player.chips>bet:
        print("chips<bet")
        return "operation error", 400


    game.player.bet = data.get("bet")
    game.status = GameStatus.BET


    #發牌
    game.deal_cards()
    #要提示
    game.player_next_move()

    game_dict = game.to_json_object()
    return jsonify(game_dict), 200

# 玩家操作
@app.route('/game/<int:game_id>/player_operation',methods=['POST'])
def player_operation(game_id):
    game:Game = next((b for b in games if b.id == game_id), None)
    print(game.to_json_object())
    if not game:
        return jsonify({"error": "Game not found"}), 404
    if not GameStatus.operation_allow(game.status):
        return "operation error", 400
    data = request.get_json()
    opt=data.get("operation")
    success=game.player_operation(opt)
    if not success:
        return "operation error", 400
    else:
        match GameStatus.get(game.status):
            case GameStatus.PLAYER_OPERATION | GameStatus.STATEMENT | GameStatus.NEW|GameStatus.GAME_OVER:
                game_dict = game.to_json_object()
                return jsonify(game_dict), 200
            case _:
                return "system error", 500

# 取得遊戲
@app.route('/game/<int:game_id>', methods=['GET'])
def get_game(game_id):
    game = next((b for b in games if b.id == game_id), None)
    return jsonify(game.to_json_object()), 200


if __name__ == '__main__':
    app.run(debug=True)

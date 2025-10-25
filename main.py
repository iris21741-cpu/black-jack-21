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
    return jsonify(game_dict), 201


# 下注
@app.route('/game/<int:game_id>/bet', methods=["POST"])
def game_bet(game_id):
    data = request.get_json()
    game:Game = next((b for b in games if b.id == game_id), None)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    if game.status != GameStatus.NEW:
        return "operation error", 400
    # TODO 清空手牌
    @app.route('/game/<int:game_id>/hand', methods=["POST"])
    def hand():
        data = request.get_json()
        game: Game = next((b for b in games if b.id == game_id), None)
    def play_round(self):
        # 清空手牌
        self.player.hand=Hand()
        self.dealer.hand=Hand()
    game.player.bet = data.get("bet")
    game.status = GameStatus.BET

    #發牌
    game.deal_cards()
    #要提示
    game.player_next_move()

    game_dict = game.to_json_object()
    return jsonify(game_dict), 201

# 玩家操作
@app.route('/game/<int:game_id>/player_operation',methods=['POST'])
def player_operation(game_id):
    game:Game = next((b for b in games if b.id == game_id), None)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    if game.status != GameStatus.BET and game.status != GameStatus.PLAYER_OPERATION:
        return "operation error", 400
    data = request.get_json()
    opt=data.get("operation")
    success=game.player_operation(opt)
    if not success:
        return "operation error", 400
    else:
        if game.status == GameStatus.PLAYER_OPERATION:
            game_dict = game.to_json_object()
            return jsonify(game_dict), 201
        elif game.status == GameStatus.STATEMENT:
            return "you loss!", 200
        return "system error", 500


# 取得遊戲
@app.route('/game/<int:game_id>', methods=['Get'])
def get_game(game_id):
    game = next((b for b in games if b.id == game_id), None)
    return jsonify(game.to_json_object()), 201


if __name__ == '__main__':
    app.run(debug=True)

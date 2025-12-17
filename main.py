from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from auth.JWTUtil import verify_token
from dao.UserDao import get_by_id, get_by_email
from email2fa.CodeBuilder import verify
from entity.Game import Game
from enums.GameStatus import GameStatus
from login.Login import login, gen_token
from register.Register import register, checkRegister

app = Flask(__name__)
games = []
# --------------------------
# 方式一：全域配置 (推薦，適用於整個 API)
# --------------------------
# 配置只允許您的前端域名訪問所有路由
CORS(app, resources={r"/api/*": {"origins": "*"}})


# --- 統一 Token 驗證裝飾器 ---
def token_required(f):
    """
    這是自定義的 @ 裝飾器
    用來檢查 token 是否正確
    token 正確會用 email 查詢用戶資訊 User
    再將 User 放入 current_user_data 變數
    api 就可以使用 current_user_data 變數取得 User 資訊
    """

    def decorated(*args, **kwargs):
        token = None
        # 從 HTTP Header 的 Authorization: Bearer <token> 中提取 Token
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({
                'message': 'Token is missing!',
                'code': 40101
            }), 401  # 401 Unauthorized

        data = verify_token(token)
        user = get_by_email(data["email"])
        kwargs['current_user_data'] = user

        if "code" in data and data["code"] >= 401 :
            return jsonify({
                'message': data["message"],
                'code': data["code"]
            }), 401

        return f(*args, **kwargs)

    decorated.__name__ = f.__name__  # 確保裝飾器不會隱藏原始函式的名稱
    return decorated


# 註冊
@app.route('/register', methods=["POST"])
@cross_origin()
def api_register():
    data = request.get_json()
    full_name = data["full_name"]
    email = data["email"]
    gender = int(data["gender"])
    password = data["password"]
    try:
        is_valid = checkRegister(email)
        if not is_valid:
            return "email is duplicate", 400
        new_user = register(full_name, email, gender, password)
    except Exception as e:
        return str(e), 400
    return jsonify({
        "user": new_user.to_json_object()
    }), 200
# 登入
@app.route('/login', methods=["POST"])
@cross_origin()
def api_login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    if len(email) < 1:
        return "email is empty", 400
    if len(password) < 8:
        return "password length <8", 400
    return login(email, password), 200


@app.route('/email2fa', methods=["POST"])
@cross_origin()
def api_email_2fa():
    data = request.get_json()
    uid = request.headers.get("X-User-Id")
    if uid is None:
        return "params error [uid]", 400
    code = data.get("code")
    if code is None:
        return "params error [code]", 400

    user = get_by_id(int(uid))
    ok = verify(user.otp_secret, code)
    if not ok:
        return "驗證碼錯誤", 400
    else:
        return gen_token(user), 200

# 新增遊戲
@app.route('/game', methods=["POST"])
@cross_origin()
@token_required
def create_game(current_user_data):
    uid = current_user_data.id
    game = Game(len(games) + 1, uid, current_user_data.full_name)
    games.append(game)
    game_dict = game.to_json_object()
    return jsonify(game_dict), 200


# 下注
@app.route('/game/<int:game_id>/bet', methods=["POST"])
@cross_origin()
@token_required
def game_bet(game_id, current_user_data):
    data = request.get_json()
    game: Game = next((b for b in games if b.id == game_id), None)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    if game.status != GameStatus.NEW:
        return "operation error", 400
    # 清空手牌
    game.player.hand.clear()
    # 回復成第一次下注
    game.player.is_first_turn = True
    game.dealer.hand.clear()
    # 下注
    bet = data.get("bet")
    if game.player.chips < bet:
        print("chips<bet")
        return "operation error", 400

    game.status = GameStatus.BET
    game.player.bet = bet

    # 發牌
    game.deal_cards()
    # 要提示
    game.player_next_move()

    game_dict = game.to_json_object()
    return jsonify(game_dict), 200


# 玩家操作
@app.route('/game/<int:game_id>/player_operation', methods=["POST"])
@cross_origin()
@token_required
def player_operation(game_id, current_user_data):
    game: Game = next((b for b in games if b.id == game_id), None)
    if not game:
        return jsonify({{"error": "Game not found"}}), 404
    if not GameStatus.operation_allow(game.status):
        return "operation error", 400
    data = request.get_json()
    opt = data.get("operation")
    print(f"operation={opt}")
    success = game.player_operation(opt)
    if not success:
        return "operation error", 400
    else:
        match GameStatus.get(game.status):
            case GameStatus.PLAYER_OPERATION | GameStatus.STATEMENT | GameStatus.NEW | GameStatus.GAME_OVER:
                game_dict = game.to_json_object()
                return jsonify(game_dict), 200
            case _:
                return "system error", 500


# 取得遊戲
@app.route('/game/<int:game_id>', methods=["GET"])
@cross_origin()
@token_required
def get_game(game_id, current_user_data):
    game = next((b for b in games if b.id == game_id), None)
    if game is None:
        return "The game cannot be found.You need to start a new game!", 200
    return jsonify(game.to_json_object()), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)

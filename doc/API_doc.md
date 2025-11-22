### POST `/game`
**功能說明**：建立一個新的遊戲實例，並回傳初始狀態。

**Request Body**
```json
{
  "name": "Player1"
}
```

| 參數   | 型別     | 必填 | 說明   |
|------|--------|----|------|
| name | string | ✅  | 玩家名稱 |


**Response (200 OK)**
```json
{
  "id": 1,
  "name": "Player1",
  "status": "NEW",
  "player": {
    "chips": 1000,
    "hand": []
  },
  "dealer": {
    "hand": []
  }
}
```
### POST `/game/{game_id}/bet`
**功能說明**：玩家下注後系統自動發牌。  
**限制條件**：僅能在遊戲狀態為 `NEW` 時執行。

**Path Parameter**

| 參數      | 型別  | 必填 | 說明   |
|---------|-----|----|------|
| game_id | int | ✅  | 遊戲編號 |

**Request Body**
```json
{
  "bet": 100
}
```

| 參數  | 型別  | 必填 | 說明             |
|-----|-----|----|----------------|
| bet | int | ✅  | 下注金額（不可超過玩家籌碼） |

**Response (200 OK)**
```json
{
  "id": 1,
  "status": "BET",
  "player": {
    "chips": 900,
    "bet": 100,
    "hand": ["10♠", "7♥"]
  },
  "dealer": {
    "hand": ["A♦", "hidden"]
  }
}
```

**Error Responses**

| 狀態碼 | 原因                   |
|-----|----------------------|
| 400 | 非法操作（如籌碼不足或非 NEW 狀態） |
| 404 | 遊戲不存在                |

### POST `/game/{game_id}/player_operation`
**功能說明**：執行玩家動作（如要牌、停牌等）。  

**Path Parameter**

| 參數      | 型別  | 必填 | 說明   |
|---------|-----|----|------|
| game_id | int | ✅  | 遊戲編號 |

**Request Body**
```json
{
  "operation": "h"
}
```

| 參數        | 型別     | 必填 | 說明                                                   |
|-----------|--------|----|------------------------------------------------------|
| operation | string | ✅  | 玩家動作，可為 `"要牌"`, `"停牌"`, `"double"`  等（依 `Game` 類別實作） |

**Response (200 OK)**
```json
{
  "id": 1,
  "status": "PLAYER_OPERATION",
  "player": {
    "hand": ["10♠", "5♥", "3♦"],
    "chips": 800
  },
  "dealer": {
    "hand": ["A♦", "h"]
  }
}
```

**Error Responses**

| 狀態碼 | 原因                  |
|-----|---------------------|
| 400 | 當前狀態無法執行此操作         |
| 404 | 遊戲不存在               |
| 500 | 系統錯誤（未知 GameStatus） |

### GET `/game/{game_id}`
**功能說明**：取得目前遊戲狀態。

**Path Parameter**

| 參數      | 型別  | 必填 | 說明   |
|---------|-----|----|------|
| game_id | int | ✅  | 遊戲編號 |

**Response (200 OK)**
```json
{
  "id": 1,
  "name": "Player1",
  "status": "BET",
  "player": {
    "chips": 900,
    "bet": 100,
    "hand": ["10♠", "5♥"]
  },
  "dealer": {
    "hand": ["A♦", "hidden"]
  }
}
```

**Error Responses**

| 狀態碼 | 原因    |
|-----|-------|
| 404 | 遊戲不存在 |


| 狀態碼 | 說明        |
|-----|-----------|
| 200 | 請求成功      |
| 400 | 操作錯誤或無效狀態 |
| 404 | 找不到指定的遊戲  |
| 500 | 系統錯誤      |

## POST /register
註冊新使用者。

### Request Body
```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "gender": 1,
  "password": "password123"
}
```

### Response 200
```json
{
  "id": 10,
  "full_name": "John Doe",
  "email": "john@example.com",
  "gender": 1
}
```

### Error Responses

| 狀態碼 | 訊息           |
|-----|--------------|
| 400 | 帳號重複、資料格式錯誤等 |

## POST /login
登入並取得 Token。

### Request Body
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

### Response 200
```json
{
  "success": true,
  "token": "JWT_TOKEN_HERE",
  "user": {
    "id": 10,
    "email": "john@example.com",
    "full_name": "John Doe"
  }
}
```

### Error Responses

| 狀態碼 | 訊息 |
|--------|------|
| 400 | email is empty / password length < 8 |
| 400 | 帳號或密碼錯誤 |

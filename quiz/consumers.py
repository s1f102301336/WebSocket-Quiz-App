import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 認証ユーザーまたはゲストの設定
        self.user = self.scope.get("user")  # Django認証ミドルウェアによりスコープに設定される
        if self.user and self.user.is_authenticated:
            # 認証済みユーザー
            self.username = self.user.username
            self.user_id = self.user.id
        else:
            # ゲストユーザー（channel_nameをIDとして使用）
            self.username = f"guest_{self.channel_name[:8]}"  # 一意なIDを生成
            self.user_id = self.channel_name  # ゲスト用の一意な識別子としてchannel_nameを使用

        # 部屋情報
        self.room_name = f"category_{self.scope['url_route']['kwargs']['category']}"
        self.room_group_name = f"group_{self.room_name}"

        # グループに参加
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        print(f"{self.username}が接続しました")

        # 自分にメッセージを送信
        await self.send(text_data=json.dumps({
            "type": "my_preparation",
            "user_name": self.username,  # ユーザー名
            "user_id": self.user_id,    # ユーザーID（ゲストの場合はchannel_name）
        }))

        # 他プレイヤーにメッセージを送信
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "opp_preparation",
                "user_name": self.username,
                "user_id": self.user_id,
            }
        )

    async def disconnect(self, close_code):
        print("Close")
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            print(f"{self.username}が切断しました")

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data["type"] == "answer":
            answer = data["answer"]
            is_correct = data["is_correct"]

            # 自分にメッセージを送信
            await self.send(text_data=json.dumps({
                "type": "my_result",
                "user_id": self.user_id,
                "answer": answer,
                "is_correct": is_correct
            }))

            # 他プレイヤーにメッセージを送信
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "opp_answer",
                    "user_id": self.user_id,
                    "answer": answer,
                    "is_correct": is_correct,
                }
            )

    async def opp_answer(self, event):
        if event["user_id"] != self.user_id:
            await self.send(text_data=json.dumps({
                "type": "opp_answer",
                "answer": event["answer"],
                "is_correct": event["is_correct"]
            }))

    async def opp_preparation(self, event):
        if event["user_id"] != self.user_id:
            print("相手は準備完了")
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "start_game",
                    "player1_id": self.user_id,
                    "player1_name": self.username,
                    "player2_id": event["user_id"],
                    "player2_name": event["user_name"],
                }
            )

    async def start_game(self, event):
        n, m = (2, 1) if event["player1_id"] != self.user_id else (1, 2)
        await self.send(text_data=json.dumps({
            "type": "start_game",
            "my_name": event[f"player{n}_name"],
            "opp_name": event[f"player{m}_name"],
        }))

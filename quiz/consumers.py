import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User 

class QuizConsumer(AsyncWebsocketConsumer):
    for user in User.objects.all():
        print(user.username, user.email)
    async def connect(self):
        # 認証ユーザーの取得
        self.user = self.scope.get("user")  # Django認証ミドルウェアによりスコープに設定される
        if self.user and self.user.is_authenticated:
            # ユーザーが認証済みの場合、接続を許可
            self.room_name = f"quiz_{self.scope['url_route']['kwargs']['quiz_id']}"
            self.room_group_name = f"group_{self.room_name}"

            # グループに参加
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            # 認証されていない場合は拒否
            print(f"Unauthorized connection attempt: {self.scope}")
            await self.close()

    async def disconnect(self, close_code):
        print("Close")
        # room_group_nameが定義されている場合のみグループから離脱
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data["type"] == "answer":
            answer = data["answer"]
            correct_answer = data["correct_answer"]

            # 自分の正解判定
            is_correct = (answer == correct_answer)

            # 自分へのメッセージ
            await self.send(text_data=json.dumps({
                "type": "my_result",
                "user_id": self.user.id,  # 認証済みユーザーのIDを使用
                "is_correct": is_correct
            }))

            # 他プレイヤーへのメッセージ
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "opponent_answer",
                    "user_id": self.user.id,
                    "answer": answer,
                    "is_correct": is_correct,
                }
            )

    async def opponent_answer(self, event):

        # 他プレイヤーからのメッセージを送信
        if event["user_id"] != self.user.id:
            await self.send(text_data=json.dumps({
                "type": "opponent_answer",
                "answer": event["answer"],
                "is_correct": event["is_correct"]
            }))

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User 

class QuizConsumer(AsyncWebsocketConsumer):
    # for user in User.objects.all():
    #     print("UserID",user.username)
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
            print("I'm", self.user)

            # 部屋に入ると同時に準備完了
            print("自分は準備完了")
            await self.send(text_data=json.dumps({
                "type": "my_preparation",
                "user_id": self.user.id,  # 認証済みユーザーのIDを使用
            }))

            # 他プレイヤーにもメッセージを送信する
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "opponent_preparation",
                    "user_id": self.user.id,
                }
            )
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

            # 自分の正解判定を取得
            is_correct = data["is_correct"]

            # 自分へのメッセージ
            await self.send(text_data=json.dumps({
                "type": "my_result",
                "user_id": self.user.id,  # 認証済みユーザーのIDを使用
                "answer":answer,
                "is_correct": is_correct
            }))

            # 他プレイヤーにもメッセージを送信する
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

        # 他プレイヤーからのメッセージを受信する
        if event["user_id"] != self.user.id:

            if event["type"] == "opponent_answer":
                await self.send(text_data=json.dumps({
                    "type": "opponent_answer",
                    "answer": event["answer"],
                    "is_correct": event["is_correct"]
                }))


    async def opponent_preparation(self, event):

        if event["user_id"] != self.user.id:
            print("相手は準備完了")
            if event["type"] == "opponent_preparation":
                # 相手の準備完了メッセージを処理
                await self.send(text_data=json.dumps({
                    "type": "opponent_preparation",
                    "opponent_user_id": event["user_id"]
                }))

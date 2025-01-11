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
            self.room_name = f"category_{self.scope['url_route']['kwargs']['category']}"
            self.room_group_name = f"group_{self.room_name}"

            # グループに参加
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            print(f"{self.user.username}が接続しました")
            # print("room_info", self.scope)

            # 部屋に入ると同時に準備完了
            # 自分にメッセージを送信する
            print("自分は準備完了")
            
            await self.send(text_data=json.dumps({
                "type": "my_preparation",
                "user_name": self.user.username,  # 認証済みユーザーのIDを使用
                "user_id": self.user.id,  # 認証済みユーザーを使用
            }))

            # 他プレイヤーへのメッセージをグループに送信する
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "opp_preparation",
                    "user_name": self.user.username,
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
            print(f"{self.user}が切断しました")


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

            # 他プレイヤーにも向けてメッセージをグループに送信する
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "opp_answer",
                    "user_id": self.user.id,
                    "answer": answer,
                    "is_correct": is_correct,
                }
            )

    async def opp_answer(self, event):

        # グループにきた他プレイヤーからのメッセージを受信し、自分に送信
        if event["user_id"] != self.user.id:
            await self.send(text_data=json.dumps({
                "type": "opp_answer",
                "answer": event["answer"],
                "is_correct": event["is_correct"]
            }))


    async def opp_preparation(self, event):

        if event["user_id"] != self.user.id:
            print("相手は準備完了")
            # 相手の準備完了メッセージを処理
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type":"start_game",
                    "player1_id":self.user.id,
                    "player1_name":self.user.username,
                    "player2_id":event['user_id'],
                    "player2_name":event['user_name'],
                }
            )

    async def start_game(self, event):
        # グループにゲームスタートのメッセージを送信
        n, m =  (2, 1) if event["player1_id"] != self.user.id else (1, 2)
        await self.send(text_data=json.dumps({
            "type": "start_game",
            "my_name": event[f"player{n}_name"],
            "opp_name": event[f"player{m}_name"],
        }))

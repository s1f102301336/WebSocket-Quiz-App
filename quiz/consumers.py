import json
from channels.generic.websocket import AsyncWebsocketConsumer

class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # プレイヤー識別子を接続時に設定
        self.player_id = self.scope["session"].get("player_id", None)
        self.room_name = f"quiz_{self.scope['url_route']['kwargs']['quiz_id']}"
        self.room_group_name = f"group_{self.room_name}"

        # グループに参加
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # グループから離脱
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
                "player_id": self.player_id,
                "is_correct": is_correct
            }))

            # 他プレイヤーへのメッセージ
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "opponent_answer",
                    "player_id": self.player_id,
                    "answer": answer,
                    "is_correct": is_correct,
                }
            )

    async def opponent_answer(self, event):
        # 自分以外のプレイヤーに送信
        
        if event["player_id"] != self.player_id:
            await self.send(text_data=json.dumps({
                "type": "opponent_answer",
                "answer": event["answer"],
                "is_correct": event["is_correct"]
            }))

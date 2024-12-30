from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/quiz/(?P<quiz_id>\w+)/$", consumers.QuizConsumer.as_asgi()),
    # re_path:正規表現を用いてURLパターンを定義するよ
    # ws専用
    # ?P<room_name> : 名前付きキャプチャグループ
    # \w+ : 任意の1文字
    # /　: 普通にスラッシュ
    # $ : 終端文字列。文字列の終わり
]
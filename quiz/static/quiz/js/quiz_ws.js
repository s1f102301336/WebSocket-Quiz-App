// const quizNum = JSON.parse(
//   //jsonから値を読み込むだけ
//   document.getElementById("quiz_id").textContent
// );
// console.log("quizNum", quizNum);

// // WebSocketの設定
// const chatSocket = new WebSocket(
//   "ws://" + window.location.host + "/ws/quiz/" + quizNum + "/"
// );

// // 初期スコア
// let myScore = 0;
// let opponentScore = 0;

// // WebSocketメッセージの処理
// chatSocket.onmessage = function (e) {
//   const data = JSON.parse(e.data);

//   if (data.type === "my_result") {
//     // 自分の結果を更新
//     if (data.is_correct) {
//       myScore += 1;
//     }
//     document.getElementById("my_score").textContent = myScore;
//     document.getElementById("my_answer").textContent = data.is_correct
//       ? "正解!"
//       : "不正解!";
//   }

//   if (data.type === "opponent_answer") {
//     // 相手の結果を更新
//     opponentScore += data.is_correct ? 1 : 0;
//     document.getElementById("opponent_score").textContent = opponentScore;
//     document.getElementById("opponent_answer").textContent = data.is_correct
//       ? "正解!"
//       : "不正解!";
//   }
// };

// // ボタンのクリックイベントで回答を送信
// document.querySelectorAll(".selection").forEach((button) => {
//   button.addEventListener("click", (e) => {
//     const answer = e.target.value;
//     const correctAnswer = document.getElementById("correct_answer").value;
//     console.log("You clicked ", answer);

//     chatSocket.send(
//       JSON.stringify({
//         type: "answer",
//         answer: answer,
//         correct_answer: correctAnswer,
//       })
//     );
//   });
// });

document.addEventListener("DOMContentLoaded", async () => {
  // クイズデータを取得
  try {
    const response = await fetch(DATA_URL);
    const quizzes = await response.json();
    console.log("Fetched quizzes:", quizzes);

    let currentQuizIndex = 0;
    let myScore = 0;
    let opponentScore = 0;

    //準備OKをリセット
    let myName = null;
    let oppName = null;

    // WebSocket 設定
    const chatSocket = new WebSocket(
      "ws://" +
        window.location.host +
        "/ws/match/" +
        quizzes[currentQuizIndex].category +
        "/"
    );

    console.log("Websocketに接続");

    // 現在の回答状況
    let myAnswer = null;
    let opponentAnswer = null;

    // クイズを表示
    function displayQuiz(quiz) {
      document.getElementById("quiz-title").textContent = quiz.title;
      document.getElementById("quiz-description").textContent =
        quiz.description;
      document.getElementById("quiz-content").textContent = quiz.content;

      const answers = [
        { text: quiz.correct_answer, is_correct: true },
        { text: quiz.incorrect1, is_correct: false },
        { text: quiz.incorrect2, is_correct: false },
        { text: quiz.incorrect3, is_correct: false },
      ];

      // 選択肢をランダムにシャッフル
      const shuffledAnswers = answers.sort(() => Math.random() - 0.5);

      const buttons = document.querySelectorAll(".selection");
      buttons.forEach((button, index) => {
        button.textContent = shuffledAnswers[index].text;
        button.value = shuffledAnswers[index].text;
        button.dataset.is_correct = shuffledAnswers[index].is_correct;
      });

      // 解説を非表示
      document.getElementById("explanation").classList.add("hidden");

      // 状況リセット
      myAnswer = null;
      opponentAnswer = null;
      document.getElementById("my_answer").textContent = "";
      document.getElementById("opponent_answer").textContent = "";
    }

    //クイズを開始
    const startQuiz = (myName, oppName) => {
      document.getElementById("wait_container").setAttribute("class", "hidden");
      document
        .getElementById("quiz_container")
        .removeAttribute("class", "hidden");
      document.getElementById("myName").textContent = myName;
      document.getElementById("oppName").textContent = oppName;
    };

    // 次のクイズに移行
    function nextQuiz() {
      currentQuizIndex++;

      if (currentQuizIndex < quizzes.length) {
        displayQuiz(quizzes[currentQuizIndex]);
      } else {
        endGame();
      }
    }

    // クイズ終了
    function endGame() {
      alert(
        "クイズ終了！最終スコア: 自分 - " +
          myScore +
          ", 相手 - " +
          opponentScore
      );
      chatSocket.close();
    }

    // WebSocket メッセージ受信
    chatSocket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      console.log("Received data:", data);

      if (data.type === "my_result") {
        document.getElementById("my_answer").textContent = data.answer;
        document.getElementById("my_judge").textContent = data.is_correct
          ? "正解"
          : "不正解";
        myScore += data.is_correct ? 1 : 0;
        document.getElementById("my_score").textContent = myScore;
        myAnswer = data.is_correct;
      }

      if (data.type === "opponent_answer") {
        document.getElementById("opponent_answer").textContent = data.answer;
        document.getElementById("opponent_judge").textContent = data.is_correct
          ? "正解"
          : "不正解";
        opponentScore += data.is_correct ? 1 : 0;
        document.getElementById("opponent_score").textContent = opponentScore;
        opponentAnswer = data.is_correct;
      }

      if (data.type === "start_game") {
        myName = data.my_name;
        oppName = data.opp_name;
        startQuiz(myName, oppName);
      }

      // 両者の回答が揃ったら次の問題に進む
      if (myAnswer !== null && opponentAnswer !== null) {
        setTimeout(() => {
          nextQuiz();
        }, 8000); // 8秒待機
      }
    };

    // 回答ボタンのイベントリスナー設定
    document.querySelectorAll(".selection").forEach((button) => {
      button.addEventListener("click", (e) => {
        const answer = e.target.value;
        const is_correct = e.target.dataset.is_correct === "true";
        console.log("You clicked ", answer);

        // 自分の回答を送信
        chatSocket.send(
          JSON.stringify({
            type: "answer",
            answer: answer,
            is_correct: is_correct,
          })
        );
      });
    });

    // 最初のクイズを表示
    displayQuiz(quizzes[currentQuizIndex]);
  } catch (error) {
    console.error("クイズデータの取得に失敗しました:", error);
  }
});

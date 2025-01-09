document.addEventListener("DOMContentLoaded", async () => {
  // <script>タグに記載
  try {
    const response = await fetch(DATA_URL);
    const quizzes = await response.json();
    console.log(response);
    console.log(quizzes);

    // 最初のクイズを表示
    let currentQuizIndex = 0;
    displayQuiz(quizzes[currentQuizIndex]);

    function displayQuiz(quiz) {
      document.getElementById("quiz-title").textContent = quiz.title;
      document.getElementById("quiz-description").textContent =
        quiz.description;
      document.getElementById("quiz-content").textContent = quiz.content;

      document.getElementById("correct_answer").textContent =
        quiz.correct_answer;
      document.getElementById("correct_answer").value = quiz.correct_answer;
      document.getElementById("incorrect1").textContent = quiz.incorrect1;
      document.getElementById("incorrect1").value = quiz.incorrect1;
      document.getElementById("incorrect2").textContent = quiz.incorrect2;
      document.getElementById("incorrect2").value = quiz.incorrect2;
      document.getElementById("incorrect3").textContent = quiz.incorrect3;
      document.getElementById("incorrect3").value = quiz.incorrect3;
      document.getElementById("quiz-explanation").textContent =
        quiz.explanation;

      // 選択肢の表示を更新
    }

    // 次の問題へ移行する処理
    function nextQuestion() {
      currentQuizIndex++;
      if (currentQuizIndex < quizzes.length) {
        displayQuiz(quizzes[currentQuizIndex]);
      } else {
        endGame();
      }
    }

    // クイズ終了処理
    function endGame() {
      document.getElementById("quiz-container").style.display = "none";
      document.getElementById("end-screen").style.display = "block";
    }
  } catch (error) {
    console.error("クイズデータの取得に失敗しました:", error);
  }
});

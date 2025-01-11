//主なWebsocket通信処理-----------------------------------------

document.addEventListener("DOMContentLoaded", async () => {
  // クイズデータを取得
  try {
    let currentQuizIndex = 0;

    //準備OKをリセット
    let myName = null;
    let oppName = null;
    let isChangingQuiz = false;

    // 現在の回答状況
    let score_p = { myScore: 0, oppScore: 0 };
    let ans_p = { myAnswer: null, oppAnswer: null };
    const isFinished = () =>
      ans_p["myAnswer"] !== null && ans_p["oppAnswer"] !== null;

    //Websocket関係
    const response = await fetch(DATA_URL);
    const quizzes = await response.json();
    console.log("Fetched quizzes:", quizzes);

    // WebSocket 設定
    const chatSocket = new WebSocket(
      "ws://" +
        window.location.host +
        "/ws/match/" +
        quizzes[currentQuizIndex].category +
        "/"
    );

    console.log("Websocketに接続");

    // クイズを表示
    const displayQuiz = async (quiz) => {
      console.log("問題はこれ", quiz);

      document.getElementById("quiz-category").textContent = quiz.category;
      document.getElementById("quiz-title").textContent = quiz.title;
      document.getElementById("quiz-description").textContent =
        quiz.description;
      document.getElementById("quiz-content").textContent = quiz.content;
      document.getElementById("quiz-explanation").textContent =
        quiz.explanation;
      console.log("ここ1");

      const answers = [
        { text: quiz.correct_answer, is_correct: true },
        { text: quiz.incorrect1, is_correct: false },
        { text: quiz.incorrect2, is_correct: false },
        { text: quiz.incorrect3, is_correct: false },
      ];

      // 選択肢をランダムにシャッフル
      const shuffledAnswers = answers.sort(() => Math.random() - 0.5);

      console.log("ここ2");
      const buttons = document.querySelectorAll(".selection");
      buttons.forEach((button, index) => {
        button.textContent = shuffledAnswers[index].text;
        button.value = shuffledAnswers[index].text;
        button.dataset.is_correct = shuffledAnswers[index].is_correct;
        button.removeAttribute("disabled");
      });

      console.log("ここ3");
      // 解説を非表示
      document
        .getElementById("quiz-explanation")
        .setAttribute("class", "hidden");
      //回答を非表示
      document.getElementById("now_result").setAttribute("class", "hidden");
      //タイマー表示リセット
      document.getElementById("next_count_p").setAttribute("class", "hidden");
      document
        .getElementById("answer_count_p")
        .removeAttribute("class", "hidden");

      console.log("ここ4");
      // 状況リセット
      ans_p["myAnswer"] = null;
      ans_p["oppAnswer"] = null;
      document.getElementById("my_answer").textContent = "";
      document.getElementById("opp_answer").textContent = "";
      document.getElementById("my_judge").textContent = "";
      document.getElementById("opp_judge").textContent = "";

      console.log("ここ5");

      //時間切れを確認する
      TimeUp();
    };

    //カウントダウン用関数
    //setInterval:ミリ秒おきに繰り返す setTimeout:ミリ秒待つ
    const countDown = async (purpose, n) => {
      let id;
      if (purpose === "pre") {
        id = document.getElementById("start_count");
      } else if (purpose === "ans") {
        id = document.getElementById("answer_count");
      } else if (purpose === "next") {
        id = document.getElementById("next_count");
      }

      console.log("id", id);
      await timer(id, n);
    };

    const timer = (id, n) => {
      return new Promise((resolve) => {
        const intervalId = setInterval(() => {
          console.log("秒数", n);
          if (n < 0 || (id === "ans" && isFinished())) {
            clearInterval(intervalId);
            resolve();
          } else {
            id.textContent = n;
            n--;
          }
        }, 1000);
      });
    };

    //ボタン非表示
    const disable = (push) => {
      const all = true ? push === "ALL" : false;
      const buttons = document.getElementsByClassName("selection");
      console.log(push.id);
      for (let i = 0; i < buttons.length; i++) {
        console.log(buttons[i].id);
        if (buttons[i].id != push.id || all) {
          buttons[i].disabled = "disabled";
        }
      }
    };

    //時間切れ用関数
    const TimeUp = async () => {
      await countDown("ans", 5); //本来2-30
      if (!isFinished()) {
        console.log("TimeUp");
        disable("ALL");
        if (ans_p["myAnswer"] === null) {
          document.getElementById("my_answer").textContent = "時間切れ";
          document.getElementById("my_judge").textContent = "不正解";
        }
        if (ans_p["oppAnswer"] === null) {
          document.getElementById("opp_answer").textContent = "時間切れ";
          document.getElementById("opp_judge").textContent = "不正解";
        }
        changeQuiz();
      } else {
        console.log("notTimeUp");

        return;
      }
    };

    //スコア調整
    const setScore = (data, p) => {
      document.getElementById(`${p}_answer`).textContent = data.answer;
      document.getElementById(`${p}_judge`).textContent = data.is_correct
        ? "正解"
        : "不正解";
      score_p[`${p}Score`] += data.is_correct ? 1 : 0;
      document.getElementById(`${p}_score`).textContent = score_p[`${p}Score`];
      ans_p[`${p}Answer`] = data.is_correct; //Finかどうか調べるため
      console.log("score", score_p);
      console.log("answer", ans_p);
    };

    //タグ作成
    function createElementWithAttributes(tag, attributes) {
      const element = document.createElement(tag);
      for (const [key, value] of Object.entries(attributes)) {
        element.setAttribute(key, value);
      }
      return element;
    }

    //table作成
    const createTable = () => {
      //スコアを表示
      const result = document.getElementById("quiz_result");
      const tr = document.createElement("tr");

      const th = createElementWithAttributes("th", { id: "quiz_num" });
      const td_m = createElementWithAttributes("td", { id: "myJudge" });
      const td_o = createElementWithAttributes("td", { id: "oppJudge" });

      th.textContent = currentQuizIndex + 1;
      td_m.textContent = ans_p["myAnswer"] ? "正解" : "不正解";
      td_o.textContent = ans_p["oppAnswer"] ? "正解" : "不正解";
      tr.appendChild(th);
      tr.appendChild(td_m);
      tr.appendChild(td_o);
      result.appendChild(tr);
    };

    //クイズを開始
    const startQuiz = async (myName, oppName) => {
      //相手待ち画面を隠す
      document.getElementById("wait_container").setAttribute("class", "hidden");
      //準備画面
      document
        .getElementById("pre_container")
        .removeAttribute("class", "hidden");
      const ms = document.getElementsByClassName("myName");
      const os = document.getElementsByClassName("oppName");
      for (let i = 0; i < ms.length; i++) {
        ms[i].innerText = myName;
        os[i].innerText = oppName;
      }
      await countDown("pre", 5);
      document.getElementById("pre_container").setAttribute("class", "hidden");
      //クイズ画面
      document
        .getElementById("quiz_container")
        .removeAttribute("class", "hidden");
      displayQuiz(quizzes[currentQuizIndex]);
    };

    //クイズの回答と移行準備
    const changeQuiz = async () => {
      if (isChangingQuiz) return;
      isChangingQuiz = true;
      console.log("score1", score_p);
      console.log("answer1", ans_p);

      document
        .getElementById("quiz-explanation")
        .removeAttribute("class", "hidden");
      document.getElementById("now_result").removeAttribute("class", "hidden");

      document.getElementById("answer_count_p").setAttribute("class", "hidden");
      document
        .getElementById("next_count_p")
        .removeAttribute("class", "hidden");
      await countDown("next", 5);
      isChangingQuiz = false;

      createTable();
      nextQuiz();
    };

    // 次のクイズに移行
    function nextQuiz() {
      currentQuizIndex++;
      console.log(currentQuizIndex, quizzes.length);

      if (currentQuizIndex < quizzes.length) {
        console.log("クイズNo.", currentQuizIndex);

        displayQuiz(quizzes[currentQuizIndex]);
      } else {
        endGame();
      }
    }

    // クイズ終了
    function endGame() {
      createTable();

      //最終スコア表示
      const result = document.getElementById("quiz_result");
      const tr = document.createElement("tr");

      const th = createElementWithAttributes("th", { id: "quiz_score" });
      const td_m = createElementWithAttributes("td", { id: "myScore" });
      const td_o = createElementWithAttributes("td", { id: "oppScore" });

      th.textContent = "最終スコア";
      td_m.textContent = score_p["myScore"];
      td_o.textContent = score_p["oppScore"];
      tr.appendChild(th);
      tr.appendChild(td_m);
      tr.appendChild(td_o);
      result.appendChild(tr);

      //html表示
      document
        .getElementById("match_container")
        .setAttribute("class", "hidden");
      document
        .getElementById("result_container")
        .removeAttribute("class", "hidden");

      const result_judge = getElementById("winner");
      result_judge.textContent = [
        `${myName}の勝ち！`,
        `${oppName}の勝ち！`,
        "引き分け！",
      ][
        +(score_p["myScore"] >= score_p["oppScore"]) +
          +(score_p["myScore"] === score_p["oppScore"])
      ];

      // alert(
      //   "クイズ終了！最終スコア: 自分 - " +
      //     score_p["myScore"] +
      //     ", 相手 - " +
      //     score_p["oppScore"]
      // );
      chatSocket.close();
    }

    // WebSocket メッセージ受信
    chatSocket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      console.log("Received data:", data);

      if (data.type === "my_result") {
        setScore(data, "my");
      }

      if (data.type === "opp_answer") {
        setScore(data, "opp");
      }

      if (data.type === "start_game") {
        console.log(data);

        myName = data.my_name;
        oppName = data.opp_name;
        console.log(myName, oppName);

        startQuiz(myName, oppName);
      }

      // 両者の回答が揃ったら次の問題に進む
      if (isFinished()) {
        changeQuiz();
      }
    };

    // 回答ボタンのイベントリスナー設定
    document.querySelectorAll(".selection").forEach((button) => {
      button.addEventListener("click", (e) => {
        disable(button);
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
  } catch (error) {
    console.error("クイズデータの取得に失敗しました:", error);
  }
});

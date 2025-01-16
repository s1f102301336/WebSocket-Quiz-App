// ボタンの要素を取得
const correct = document.getElementById("correct_answer");
const incorrect1 = document.getElementById("incorrect1");
const incorrect2 = document.getElementById("incorrect2");
const incorrect3 = document.getElementById("incorrect3");

const exp = document.getElementById("explanation");
const btns = [correct, incorrect1, incorrect2, incorrect3];
const result = document.getElementById("result");

// 正解ボタンのイベントリスナー
correct.addEventListener("click", () => {
  judge(correct.id);
  disable(correct);
});

// 不正解ボタンのイベントリスナー
incorrect1.addEventListener("click", () => {
  judge(incorrect1.id);
  disable(incorrect1);
});
incorrect2.addEventListener("click", () => {
  judge(incorrect2.id);
  disable(incorrect2);
});
incorrect3.addEventListener("click", () => {
  judge(incorrect3.id);
  disable(incorrect3);
});

// 正誤判定関数
const judge = (id) => {
  if (id === "correct_answer") {
    result.textContent = "正解";
    result.style.color = "green";
  } else {
    result.textContent = "不正解";
    result.style.color = "red";
  }
  exp.classList.remove("hidden"); // 解説を表示
};

// ボタン無効化関数
const disable = (push) => {
  btns.forEach((b) => {
    if (b.id !== push.id) {
      b.disabled = true; // ボタンを無効化
      b.style.opacity = "0.5"; // 無効化されたボタンを半透明に
    }
  });
};
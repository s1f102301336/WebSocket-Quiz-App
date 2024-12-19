const correct = document.getElementById("correct_answer");
correct.addEventListener("click", () => {
  judge(correct.id);
  disable(correct);
});
console.log(correct);

const incorrect1 = document.getElementById("incorrect1");
incorrect1.addEventListener("click", () => {
  judge(incorrect1.id);
  disable(incorrect1);
});

const incorrect2 = document.getElementById("incorrect2");
incorrect2.addEventListener("click", () => {
  judge(incorrect2.id);
  disable(incorrect2);
});

const incorrect3 = document.getElementById("incorrect3");
incorrect3.addEventListener("click", () => {
  judge(incorrect3.id);
  disable(incorrect3);
});

const exp = document.getElementById("explanation");
const btns = [correct, incorrect1, incorrect2, incorrect3];
const result = document.getElementById("result");

const judge = (id) => {
  if (id === "correct_answer") {
    result.textContent = "正解";
  } else {
    result.textContent = "不正解";
  }
  exp.className = null;
};

const disable = (push) => {
  btns.map((b) => {
    if (b.id != push.id) {
      b.disabled = "disabled";
    }
  });
};

document.getElementById('submit-button').addEventListener('click', async () => {
    const form = document.getElementById('quiz-form');
    const formData = new FormData(form);

    const quizData = {
        question: formData.get('question'),
        correct_option: formData.get('correct_option'),
        wrong_options: [
            formData.get('wrong_option1'),
            formData.get('wrong_option2'),
            formData.get('wrong_option3'),
        ],
        explanation: formData.get('explanation'),
        genres: Array.from(formData.getAll('genres')),
    };

    if (!quizData.question || !quizData.correct_option || quizData.wrong_options.some(opt => !opt)) {
        document.getElementById('result-message').textContent = '全ての必須項目を入力してください。';
        return;
    }

    try {
        const response = await fetch('/submit-quiz', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(quizData),
        });

        if (response.ok) {
            document.getElementById('result-message').textContent = 'クイズが正常に投稿されました！';
            document.getElementById('result-message').style.color = 'green';
            form.reset(); // フォームをリセット
        } else {
            throw new Error('サーバーエラーが発生しました。');
        }
    } catch (error) {
        document.getElementById('result-message').textContent = error.message;
    }
});
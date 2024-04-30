function nextQuestion(next) {
    hideAllQuestions();
    document.getElementById('question-' + next).style.display = 'block';
}

function previousQuestion(prev) {
    hideAllQuestions();
    document.getElementById('question-' + prev).style.display = 'block';
}

function hideAllQuestions() {
    var screens = document.querySelectorAll('.question-screen');
    screens.forEach(function(screen) {
        screen.style.display = 'none';
    });
}

function finishQuiz() {
    var correctAnswers = 0;
    if (document.querySelector('input[name="q1"][value="b"]:checked') || 
        document.querySelector('input[name="q1"][value="c"]:checked')) correctAnswers++;
    if (document.querySelector('input[name="q2"][value="d"]:checked')) correctAnswers++;
    if (document.querySelector('input[name="q3"][value="b"]:checked') || 
        document.querySelector('input[name="q3"][value="d"]:checked')) correctAnswers++;

    hideAllQuestions();
    document.getElementById('results-screen').style.display = 'block';
    document.getElementById('score').textContent = `${correctAnswers} out of 3 correct`;
}

function tryAgain() {
    document.querySelectorAll('input[type="radio"]').forEach(radio => {
        radio.checked = false;
    });
    hideAllQuestions();
    nextQuestion(1);
}

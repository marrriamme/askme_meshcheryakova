function likeQuestion(questionId, event) {
    event.preventDefault();
    const url = document.querySelector(`#question-like-${questionId}`).closest('a').getAttribute('data-url');
    const csrfToken = getCSRFToken();

    console.log("URL:", url); 
    console.log("CSRF Token:", csrfToken); 

    fetch(url, {
        method: "POST",
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        console.log("Response Status:", response.status); 
        if (response.status === 403) {
            console.error("CSRF token error.");
            return;
        }
        return response.json();
    })
    .then(data => {
        console.log("Response Data:", data); 
        if (data) {
            document.getElementById('question-like-counter-' + questionId).textContent = data.rating;
            toggleQuestionActive('like', questionId); 
        }
    })
    .catch(error => {
        console.error("Error:", error); 
    });
}


function dislikeQuestion(questionId, event) {
    event.preventDefault(); 
    const url = document.querySelector(`#question-dislike-${questionId}`).closest('a').getAttribute('data-url');
    
    fetch(url, {
        method: "POST",
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => {
        if (response.status === 403) {
            console.error("CSRF token error.");
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data) {
            document.getElementById('question-like-counter-' + questionId).textContent = data.rating;
            toggleQuestionActive('dislike', questionId); 
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

function toggleQuestionActive(type, questionId) {
    const likeIcon = document.getElementById(`question-like-${questionId}`);
    const dislikeIcon = document.getElementById(`question-dislike-${questionId}`);
    
    if (type === 'like') {
        if (likeIcon.classList.contains('active')) {
            likeIcon.classList.remove('active');
        } else {
            likeIcon.classList.add('active');
            dislikeIcon.classList.remove('active'); 
        }
    } else if (type === 'dislike') {
        if (dislikeIcon.classList.contains('active')) {
            dislikeIcon.classList.remove('active');
        } else {
            dislikeIcon.classList.add('active');
            likeIcon.classList.remove('active'); 
        }
    }
}


function likeAnswer(answerId, event) {
    event.preventDefault();
    const url = document.querySelector(`#answer-like-${answerId}`).closest('a').getAttribute('data-url');
    const csrfToken = getCSRFToken();

    console.log("URL:", url); 
    console.log("CSRF Token:", csrfToken); 

    fetch(url, {
        method: "POST",
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        console.log("Response Status:", response.status); 
        if (response.status === 403) {
            console.error("CSRF token error.");
            return;
        }
        return response.json();
    })
    .then(data => {
        console.log("Response Data:", data); 
        if (data) {
            document.getElementById('answer-like-counter-' + answerId).textContent = data.rating;
            toggleAnswerActive('like', answerId); 
        }
    })
    .catch(error => {
        console.error("Error:", error); 
    });
}

function dislikeAnswer(answerId, event) {
    event.preventDefault(); 
    const url = document.querySelector(`#answer-dislike-${answerId}`).closest('a').getAttribute('data-url');
    const csrfToken = getCSRFToken();

    console.log("URL:", url); 
    console.log("CSRF Token:", csrfToken); 

    fetch(url, {
        method: "POST",
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        console.log("Response Status:", response.status); 
        if (response.status === 403) {
            console.error("CSRF token error.");
            return;
        }
        return response.json();
    })
    .then(data => {
        console.log("Response Data:", data); 
        if (data) {
            document.getElementById('answer-like-counter-' + answerId).textContent = data.rating;
            toggleAnswerActive('dislike', answerId); 
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

function toggleAnswerActive(type, answerId) {
    const likeIcon = document.getElementById(`answer-like-${answerId}`);
    const dislikeIcon = document.getElementById(`answer-dislike-${answerId}`);
    
    if (type === 'like') {
        if (likeIcon.classList.contains('active')) {
            likeIcon.classList.remove('active');
        } else {
            likeIcon.classList.add('active');
            dislikeIcon.classList.remove('active'); 
        }
    } else if (type === 'dislike') {
        if (dislikeIcon.classList.contains('active')) {
            dislikeIcon.classList.remove('active');
        } else {
            dislikeIcon.classList.add('active');
            likeIcon.classList.remove('active'); 
        }
    }
}

function setCorrectAnswer(questionId, answerId, event) {
    event.preventDefault(); 

    const url = document.querySelector(`#correct-${answerId}`).closest('a').getAttribute('data-url');
    const csrfToken = getCSRFToken();

    console.log("URL:", url); 
    console.log("CSRF Token:", csrfToken); 

    fetch(url, {
        method: "POST",
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        console.log("Response Status:", response.status); 
        if (response.status === 403) {
            console.error("CSRF token error.");
            return;
        }
        return response.json();
    })
    .then(data => {
        console.log("Response Data:", data); 
        if (data) {
            toggleCorrectAnswer(questionId, answerId); 
        }
    })
    .catch(error => {
        console.error("Error:", error); 
    });
}

function toggleCorrectAnswer(questionId, answerId) {
    const previousCorrect = document.querySelector('.form-check-input:checked');
    const newCorrect = document.getElementById(`correct-${answerId}`);

    if (previousCorrect) {
        previousCorrect.checked = false;
    }

    if (newCorrect) {
        newCorrect.checked = true;
    }
}

function getCSRFToken() {
    const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfTokenElement ? csrfTokenElement.value : '';
}


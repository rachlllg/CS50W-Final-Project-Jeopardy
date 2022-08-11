// get csrf token for put requests
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie != '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// load functions when page fully loaded
document.addEventListener('DOMContentLoaded', function(){
    show_clue();
    answer_clue();
    close_clue();
})

// close button to remove the pop-up clue and enable all buttons and reset all choice style to default
function close_clue(){
    document.querySelector('.btn-close').addEventListener('click', function (){
        document.querySelector('.popup').style.display = "none";
        document.querySelector('.choiceone').style.backgroundColor = "#edc7b7";
        document.querySelector('.choicetwo').style.backgroundColor = "#edc7b7";
        document.querySelector('.choicethree').style.backgroundColor = "#edc7b7";
        document.querySelectorAll('.clue').forEach(elem => {
            elem.disabled = false;
        })
    })
}

// show the popup question/clue card when a category/cluevalue is pressed
function show_clue(clicked_id){
    document.querySelector('.popup').style.display = "none";
    // hide the close button until the question is answered
    document.querySelector('.btn-close').style.display = "none";
    document.querySelector(`#${clicked_id}`).addEventListener('click', function(){
        document.querySelector('.popup').style.display = "flex";
        // disable all clue buttons once the popup has opened
        document.querySelectorAll('.clue').forEach(elem => {
            elem.disabled = true;
        })
        id = parseInt(document.querySelector(`#${clicked_id}`).getAttribute('id').substring(5))
        fetch(`/clue`,{
            method: 'GET',
        })
        .then(result => {
            load_clue(id);
        })
    })
}

// load the clue and the three choices for that specific question/clue_id
function load_clue(question_id){
    fetch(`/clue/${question_id}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(clue => {
        // if the clue has already been answered, display a message for the user to select a different clue
        if (clue[0].answered == true){
            document.querySelector(`#clue-${question_id}`).style.backgroundColor = "#bab2b5";
            document.querySelector('#popup-clue').innerHTML = "This clue has been answered, please select a different clue";
            document.querySelectorAll('.choice').forEach(elem =>{
                elem.style.display = "none";
            })
            document.querySelector('.btn-close').style.display = "block";
            close_clue();
        }
        // if the clue has not been answered, provide the user with 3 choices to answer
        else {
            document.querySelectorAll('.choice').forEach(elem =>{
                elem.style.display = "block";
            })
            document.querySelector('#popup-clue').innerHTML = clue[0].clue;
            document.querySelector('.choiceone').innerHTML = clue[0].choiceone;
            document.querySelector('.choiceone').id = clue[0].id;
            document.querySelector('.choicetwo').innerHTML = clue[0].choicetwo;
            document.querySelector('.choicetwo').id = clue[0].id;
            document.querySelector('.choicethree').innerHTML = clue[0].choicethree;
            document.querySelector('.choicethree').id = clue[0].id;
        }
    })
}

// Use put request to update the answered attribute for the specific question/clue as answered
function answer_clue(question_id, choice){
    fetch(`/clue/${question_id}/${choice.textContent}`, {
        method: 'PUT',
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            id: question_id,
            choice: choice.textContent,
        })
    })
    .then(response => response.json())
    .then(result => {
        answer(question_id, choice);
    })
}

// Once a question/clue has been answered, present the user with the correct answer with different colors on the choices and let user close the clue-card
function answer(question_id, choice){
    document.querySelector('.btn-close').style.display = "block";
    close_clue();
    fetch(`/clue/${question_id}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(clue => {
        document.querySelector(`#clue-${question_id}`).style.backgroundColor = "#bab2b5";
        if (clue[0].answer == choice.textContent){
            score(clue)
        }
        if (clue[0].choiceone == clue[0].answer) {
            document.querySelector('.choiceone').style.backgroundColor = "green";
            document.querySelector('.choicetwo').style.backgroundColor = "red";
            document.querySelector('.choicethree').style.backgroundColor = "red";
        }
        else if (clue[0].choicetwo == clue[0].answer) {
            document.querySelector('.choiceone').style.backgroundColor = "red";
            document.querySelector('.choicetwo').style.backgroundColor = "green";
            document.querySelector('.choicethree').style.backgroundColor = "red";
        }
        else if (clue[0].choicethree == clue[0].answer) {
            document.querySelector('.choiceone').style.backgroundColor = "red";
            document.querySelector('.choicetwo').style.backgroundColor = "red";
            document.querySelector('.choicethree').style.backgroundColor = "green";
        }
    })
}

// keep track of the score
let value = 0;
function score(clue){
    value += clue[0].cluevalue;
    document.querySelector('#value').innerHTML = value;
}


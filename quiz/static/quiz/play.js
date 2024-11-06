var curr_qn_index;
var quiz_info;
var num_qns;
var next_btn;
var quiz_id;
var leaderboard;

document.addEventListener('DOMContentLoaded', function() {

    // Get the DOM elements and initialise variables
    quiz_info = document.querySelector('#quiz_info');
    quiz_id = parseInt(quiz_info.dataset.quiz_id);
    curr_qn_index = parseInt(quiz_info.dataset.curr_qn);
    num_qns = parseInt(quiz_info.dataset.num_qns);
    next_btn = document.querySelector('#next');
    leaderboard = document.querySelector('#leaderboard');

    if (curr_qn_index < num_qns) {
        initialise_options();
        options = document.querySelectorAll('.option:not(.attempted)');
        options.forEach(option => {
            option.onclick = select_option;
        });
        next_btn.onclick = next;
        if (!localStorage.getItem('start')) {
            start_timer();
        } 
        show_timer();
        document.querySelector(`#qn_${curr_qn_index}`).style.display = 'block';
    } else {
        display_score();
    }
})


/**
 * Initialises the options for the page.
 */
function initialise_options() {
    const options = document.querySelectorAll('.option');
    options.forEach(option => {
        switch (parseInt(option.dataset.option_no)) {
            case 0:
                option.classList.add('btn-danger');
                option.prepend('▲ ');
                break;
            case 1:
                option.classList.add('btn-primary');
                option.prepend('◆ ');
                break;
            case 2:
                option.classList.add('btn-warning');
                option.prepend('⬤ ');
                break;
            case 3:
                option.classList.add('btn-success');
                option.prepend('■ ');
                break;
        }    
    })
}


/**
 * Selects an option and submits the answer for a given question.
 *
 * @param {Event} e - The event object that triggered the function.
 */
function select_option(e) {
    stop_timer();
    var option = e.target;
    var option_chosen = option.dataset.option_no;
    submit_answer(option_chosen).then((response) => {
        mark_qn(response);
    });
}


/**
 * Submits the chosen option and time left for the quiz.
 *
 * @param {type} option_chosen - The chosen option for the quiz.
 * @return {type} A promise that resolves to the response data in JSON format.
 */
function submit_answer(option_chosen) {
    return fetch(`${quiz_id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': quiz_info.dataset.csrf_token
        },
        body: JSON.stringify({
            'option_chosen': option_chosen, 
            'time_left': time_left()
        })
    })
    .then((response) => response.json())
}


/**
 * Marks the question based on the given response.
 *
 * @param {object} response - The response object containing information about the question.
 */
function mark_qn(response) {
    console.log(response)
    // Reset the timer
    localStorage.removeItem('start');

    var correct_option = response['correct_option'];
    var score = response['score'];
    var qn = document.querySelector(`#qn_${curr_qn_index}`);
    var symbol = qn.querySelector('.symbol');
    var result = qn.querySelector('.result');
    var score_div = qn.querySelector('.score');
    
    if (score > 0) {
        result.append('Correct!');
        result.classList.add('text-success');
        symbol.append('✓');
        symbol.classList.add('bg-success');
        score_div.append(`+${score}`);
    }
    else {
        result.append('Incorrect!');
        result.classList.add('text-danger');
        symbol.append('✗');
        symbol.classList.add('bg-danger');
    }

    qn.querySelectorAll('.option').forEach((option) => {
        if (option.dataset.option_no == correct_option) {
            option.append('✓ ');
            option.onclick = null;
        }
        else {
            option.disabled = true;
            option.append('✗ ');
        }
    })
    qn.querySelector('.results').style.removeProperty('display');
    next_btn.style.display = 'block';
}

/**
 * A function that advances to the next question in the quiz.
 */
function next() {
    document.querySelector(`#qn_${curr_qn_index++}`).remove();
    next_btn.style.display = 'none';
    if (curr_qn_index < num_qns) {
        curr_qn.innerHTML = `${curr_qn_index + 1}/${num_qns}`;
        document.querySelector(`#qn_${curr_qn_index}`).style.display = 'block';
        start_timer();
        show_timer();
    } else {
        display_score();
    }
}


/**
 * Displays the score on the leaderboard.
 */
function display_score() {
    document.querySelector('#curr_qn').style.display = 'none';
    fetch(`score/${quiz_id}`)
    .then(response => response.json())
    .then(data => {
        for (var i = 0; i < data['leaderboard'].length; i++) {
            add_leaderboard_entry(i + 1, data['leaderboard'][i]['username'], data['leaderboard'][i]['score']);
        }
        if (data['in_leaderboard'] !== true) {
            add_leaderboard_entry('', data['username'], data['score']);
        } 
        leaderboard.querySelector(`#${data['username']}`).classList.add('list-group-item-success');
        leaderboard.style.display = 'block';
        document.querySelector('#finish').style.display = 'block';
    })
}


/**
 * Add a leaderboard entry to the list.
 *
 * @param {number} rank - The rank of the user.
 * @param {string} user - The username of the user.
 * @param {number} score - The score of the user.
 */
function add_leaderboard_entry(rank, user, score) {
    leaderboard.insertAdjacentHTML('beforeend', `
    <li id="${user}" class="list-group-item">
        <div class="row">
            <div class="col-1">${rank}</div>
            <div class="col-9 username">${user}</div>
            <div class="col-2 score">${score}</div>
        </div>
    </li>
    `)
}



/**
 * Shows a timer on the page that counts down the time left for the current question.
 */
function show_timer() {
    var qn = document.querySelector(`#qn_${curr_qn_index}`);
    var progress_bar = qn.querySelector('.progress-bar');
    var class_list = progress_bar.classList;

    timer = setInterval(function () {
        // update timer every 500ms
        var percent_time_left = (time_left() / qn.dataset.time_limit) * 100;
        qn.querySelector('.time_left').innerHTML = time_left();
        progress_bar.style.width = `${percent_time_left}%`;

        if (percent_time_left <= 25 && class_list.contains('bg-warning')) {
            class_list.remove('bg-warning');
            class_list.add('bg-danger');
        } else if (percent_time_left <= 50 && class_list.contains('bg-success')) {
            class_list.remove('bg-success');
            class_list.add('bg-warning');
        }

        // mark qn as incorrect if time runs out
        if (time_left() <= 0) {
            stop_timer();
            submit_answer(-1).then((response) => {
                mark_qn(response);
            });
        }
    }, 500)
}

/**
 * Starts a timer and saves the start time in local storage.
 */
function start_timer() {
    var start = new Date().getTime();
    localStorage.setItem('start', start);
}


/**
 * Stops the timer and hides the timer display for the current question.
 */
function stop_timer() {
    var qn = document.querySelector(`#qn_${curr_qn_index}`);
    clearInterval(timer);
    qn.querySelector('.timer').style.display = 'none';
}


/**
 * Calculates the time left until the time limit is reached.
 *
 * @return {number} The remaining time in seconds.
 */
function time_left() {
    var now = new Date().getTime();
    var delta = now - localStorage.getItem('start');
    var seconds = Math.floor(delta / 1000);
    var time_limit = document.querySelector(`#qn_${curr_qn_index}`).dataset.time_limit;
    return Math.max(0, time_limit - seconds);
}



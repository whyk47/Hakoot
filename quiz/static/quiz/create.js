var qn_ids = [];
var option_ids = [];
var new_qns = [];


document.addEventListener('DOMContentLoaded', () => {
    localStorage.clear();
    document.querySelector('#add_question').onclick = add_question;
    document.querySelectorAll('.remove_qn').forEach(button => {
        button.onclick = remove_question;
    });
    document.querySelector('#submit').onclick = submit;
    try {
        document.querySelector('#del').onclick = del_quiz;
    } catch (e) {
        console.log(e);
    }
});


/**
 * Adds a new question to the DOM and updates the display.
 *
 * @return {boolean} Returns false to prevent form submission.
 */
function add_question() {
    const questions = document.querySelector('#questions');
    const new_qn = document.querySelector('#new_qn').cloneNode(true);
    var num_qns = questions.querySelectorAll('.qn').length; 

    // Edit form for new qn and options
    new_qn.querySelector('.qn_no').innerHTML = `Question ${num_qns + 1}`;
    new_qn.querySelector('.remove_qn').onclick = remove_question;
    new_qn.removeAttribute('id');
    new_qn.style.display = 'block';
    new_qns.push(new_qn);
    questions.append(new_qn);
    return false;
}

/**
 * Removes a question from the DOM and updates the remaining questions.
 *
 * @param {Event} e - The event object.
 * @return {boolean} False to prevent default behavior.
 */
function remove_question(e) {
    // save ids of removed questions and options
    var qn = e.target.parentNode;
    replace_prefix(qn, '00')
    var qn_id = qn.querySelector('#id_question-00-id').value;
    if (qn_id) {
        qn_ids.push(qn_id);
    }
    qn.querySelectorAll('#id_option-00-id').forEach(id => {
        var option_id = id.value;
        if (option_id) {
            option_ids.push(option_id);
        }
    });
    if (qn in new_qns) {
        new_qns.splice(new_qns.indexOf(qn), 1);
    }
    qn.remove();

    // update existing questions
    const questions = document.querySelector('#questions');
    questions.querySelectorAll('.qn').forEach((qn, index) => {
        qn.querySelector('.qn_no').innerHTML = `Question ${index + 1}`;
    });
    return false;
}


/**
 * Submits the form with all the questions and options.
 *
 * @return {boolean} Returns true if the form is successfully submitted.
 */
function submit() {

    const questions = document.querySelector('#questions');
    const total_qn_forms = document.querySelector('#id_question-TOTAL_FORMS');
    const total_option_forms = document.querySelector('#id_option-TOTAL_FORMS');

    new_qns.forEach(new_qn => {
        // fill in id of removed qns and options (if any)
        if (qn_ids.length > 0) {
            new_qn.querySelector('#id_question-__prefix__-id').value = qn_ids.pop();
        }
        if (option_ids.length > 0) {
            new_qn.querySelectorAll('#id_option-__prefix__-id').forEach(id => id.value = option_ids.pop());
        }
    })

    questions.querySelectorAll('.qn').forEach((qn, index) => {

        // Set form prefixes (need to backup and refill input values)
        const qn_form = qn.querySelector('.qn_form');
        var data = backup(qn_form);
        replace_prefix(qn_form, index);
        restore(qn_form, data);
        qn_form.querySelector(`#id_question-${index}-qn_no`).value = index;

        qn.querySelectorAll('.option').forEach((option, i) => {
            var option_no = i + index * 4;
            data = backup(option);
            replace_prefix(option, option_no);
            restore(option, data);
            option.querySelector(`#id_option-${option_no}-qn_no`).value = index;
        });
    });

    // Update management form
    total_qn_forms.value = questions.querySelectorAll('.qn').length;
    total_option_forms.value = questions.querySelectorAll('.option').length;
    document.querySelector('#form').submit();
    return true;
}

/**
 * Replaces the prefix in the given node's inner HTML with the specified index.
 *
 * @param {Node} node - The node whose inner HTML will be modified.
 * @param {number} index - The index to replace the prefix with.
 * @return {boolean} Returns false.
 */
function replace_prefix(node, index) {
    const regex = new RegExp('__prefix__', 'g');
    const qn_regex = new RegExp('question-\\d+-', 'g');
    const option_regex = new RegExp('option-\\d+-', 'g');

    node.innerHTML = node.innerHTML.replace(qn_regex, `question-${index}-`);
    node.innerHTML = node.innerHTML.replace(option_regex, `option-${index}-`);
    node.innerHTML = node.innerHTML.replace(regex, index);

    return false;
}

/**
 * Generates a backup of the input values of a given HTML node.
 *
 * @param {Node} node - The HTML node to generate a backup for.
 * @return {Array} An array containing the backup of the input values.
 */
function backup(node) {
    var data = [];
    node.querySelectorAll('input, select').forEach((input, i) => {
        data[i] = input.value;
    });
    return data;
}

/**
 * Restores the values of input and select elements within a given node
 * based on the data provided.
 *
 * @param {Node} node - The HTML node to restore the values for.
 * @param {Array} data - An array containing the values to be restored.
 * @return {boolean} Returns false to prevent the default form submission behavior.
 */
function restore(node, data) {
    node.querySelectorAll('input, select').forEach((input, i) => {
        input.value = data[i];
    });
    return false;
}


/**
 * Deletes a quiz based on user confirmation.
 *
 * @param {Event} e - The event object triggered by the delete action.
 * @return {boolean} Returns true if the quiz is deleted, false otherwise.
 */
function del_quiz(e) {
    if (confirm('Are you sure you want to delete this quiz?')) {
        document.querySelector('#del_quiz').submit();
        return true;
    } else {
        e.preventDefault();
        return false;
    }
}

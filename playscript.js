
// Define the initial state
let state = {
    hearts: 3
};

let where = 0;

// Function to start the game
function startGame() {
    state.hearts = 3;
    displayNextPrompt(1);
}

function restartGame() {
    where = 0;
    state.hearts = 3; // Reset hearts to 3

    const textElement = document.querySelector('.messages');
    textElement.innerHTML = '';
    
    startGame(); // Restart the game

}

// Function to display the next prompt and its options
function displayNextPrompt(textNodeIndex) {
    const textNode = textNodes.find(textNode => textNode.id === textNodeIndex);
    const textElement = document.querySelector('.messages');
    const optionButtonsElement = document.querySelector('.options_wrapper');

    // Clear existing options
    optionButtonsElement.innerHTML = '';

    // Create the message element for the prompt
    const message = document.createElement('li');
    message.classList.add('message', 'bot');
    message.innerHTML = `
        <div class="avatar bot"><span>BOT</span></div>
        <div class="text_wrapper">
            <div class="text">${textNode.text}</div>
        </div>
    `;
    textElement.appendChild(message);

    // Create buttons for each option
    textNode.options.forEach(option => {
        if (showOption(option)) {
            const button = document.createElement('button');
            button.innerText = option.text;
            button.classList.add('btn');
            button.addEventListener('click', () => selectOption(option));
            optionButtonsElement.appendChild(button);
        }
    });
    textElement.scrollTop = textElement.scrollHeight;
}

// Function to determine if an option should be shown based on current state
function showOption(option) {
    return option.requiredState == null || option.requiredState(state);
}

function decreaseHearts() {
    state.hearts--;
}

// Function to handle user selection of an option
function selectOption(option) {
    where++;
    // Display the selected option's text in the chat log
    const userMessage = document.createElement('li');
    userMessage.classList.add('message', 'user');
    userMessage.innerHTML = `
        <div class="avatar user"><span>YOU</span></div>
        <div class="text_wrapper">
            <div class="text">${option.text}</div>
        </div>
    `;
    const textElement = document.querySelector('.messages');
    textElement.appendChild(userMessage);

    const id = option.nextText;

    if (option.decreaseHearts) {
        option.decreaseHearts(); // Call the function to decrease hearts
    }

    if (id == -1) {
        if (option.end != null && state.hearts <= 0) {
            showGameOverPopup("Game Over!", "You lost all of your hearts. Please use SafeSurf’s Practice Mode to improve your skills."); // Show game over popup if hearts are zero
        } else if (option.popup && state.hearts > 0) {
            showGameOverPopup("Game Over!", "Although you did not lose all of your hearts, you still ended on an unsafe option. Please use SafeSurf’s Practice Mode to improve your skills."); // Restart the game if nextTextNodeId is negative and hearts are not zero
        } else {
            showGameOverPopup("Congratulations!", "You made it through the scenario! Either restart or continue practicing using Practice Mode!");
        }
        return;
    }

    if (option.popup) {
        showErrorPopup(); // Show the error popup
        return;
    }   

    // Display the next prompt
    displayNextPrompt(where + 1);
    textElement.scrollTop = textElement.scrollHeight;
}

function showErrorPopup() {
    const popup = document.getElementById('popup');
    const popupContent = popup.querySelector('.popup_content');
    popupContent.innerHTML = `
        <h2>Uh oh!</h2>
        <p>You shouldn't share sensitive information on the internet. You have lost a heart.</p>
        <p>You now have ${state.hearts} hearts left.</p> <!-- Display the number of hearts left -->
        <button id="continueButton">Continue</button>
    `;
    popup.classList.remove('hidden');
    
    // Add event listener to the "Continue" button
    const continueButton = document.getElementById('continueButton');
    continueButton.addEventListener('click', () => {
        popup.classList.add('hidden'); // Hide the popup
        displayNextPrompt(where + 1); // Proceed with the game
    });
}

function showGameOverPopup(heading, gameOverMessage) {
    const popup = document.getElementById('popup');
    const popupContent = popup.querySelector('.popup_content');
    popupContent.innerHTML = `
        <h2>${heading}</h2>
        <p>${gameOverMessage}</p>
        <button id="restartButton">Restart</button>
    `;
    popup.classList.remove('hidden');
    
    // Add event listener to the "Restart" button
    const restartButton = document.getElementById('restartButton');
    restartButton.addEventListener('click', () => {
        popup.classList.add('hidden'); // Hide the popup
        restartGame(); // Restart the game
    });
}


// Define textNodes containing prompts and options
const textNodes = [
    {
        id: 1,
        text: 'Hi! I really like your profile. Tell me a bit more about yourself.',
        options: [
            {
                text: 'Hi! Thank you so much. My name is X and I am Y years old.',
                decreaseHearts: decreaseHearts,
                popup: true,
                nextText: 2
            },
            {
                text: 'Thank you so much! I really appreciate it.',
                nextText: 2
            }
        ]
    },
    {
        id: 2,
        text: 'What sort of things do you like to do in your free time?',
        options: [
            {
                text: 'I like to surf and hang out with my friends. How about you?',
                nextText: 3
            },
            {
                text: 'Well, since I am from Florida, I like to go to the beach with my friends. How about you?',
                decreaseHearts: decreaseHearts,
                popup: true,
                nextText: 3
            }
        ]
    },
    {
        id: 3,
        text: 'I love to paint! Maybe if you send over you number, I can send you a few of my art pieces.',
        options: [
            {
                text: 'Sure, my number is XXX-XXX-XXXX!',
                decreaseHearts: decreaseHearts,
                popup: true,
                end: true,
                nextText: -1
            },
            {
                text: 'I’m not very comfortable with sharing this information with you. Please do not contact me again.',
                nextText: -1
            }
        ]
    }
];

// // Disable text entry area
 document.querySelector('.message_input').disabled = true;

// // Call startGame once the DOM content is fully loaded
document.addEventListener('DOMContentLoaded', startGame);

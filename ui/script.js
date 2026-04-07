let mode = 'interview';
let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let waitingForAnswer = false;
let recordingStartTime = 0;

const loginPage = document.getElementById('loginPage');
const dashboardPage = document.getElementById('dashboardPage');
const interviewPage = document.getElementById('interviewPage');
const teachingPage = document.getElementById('teachingPage');
const chatMessagesInterview = document.getElementById('chatMessagesInterview');
const chatEmptyInterview = document.getElementById('chatEmptyInterview');
const chatMessagesTeaching = document.getElementById('chatMessagesTeaching');
const chatEmptyTeaching = document.getElementById('chatEmptyTeaching');
const textInputInterview = document.getElementById('textInput');
const textInputTeaching = document.getElementById('textInputTeaching');
const loginBtn = document.getElementById('loginBtn');
const googleLoginBtn = document.getElementById('googleLoginBtn');
const selectInterviewModeBtn = document.getElementById('selectInterviewMode');
const selectTeachingModeBtn = document.getElementById('selectTeachingMode');
const logoutFromSelectionBtn = document.getElementById('logoutFromSelection');
const logoutFromInterviewBtn = document.getElementById('logoutFromInterview');
const logoutFromTeachingBtn = document.getElementById('logoutFromTeaching');
const switchToInterviewFromInterviewBtn = document.getElementById('switchToInterviewFromInterview');
const switchToTeachingFromInterviewBtn = document.getElementById('switchToTeachingFromInterview');
const switchToInterviewFromTeachingBtn = document.getElementById('switchToInterviewFromTeaching');
const switchToTeachingFromTeachingBtn = document.getElementById('switchToTeachingFromTeaching');
const suggestionsGridInterview = document.getElementById('suggestionsGridInterview');
const suggestionsGridTeaching = document.getElementById('suggestionsGridTeaching');

const suggestionsByMode = {
    interview: [
        'Practice an OOP interview question',
        'Ask me a coding question',
        'Evaluate my answer to a system design prompt'
    ],
    teaching: [
        'Explain recursion with an example',
        'Show me how REST APIs work',
        'Teach me about database normalization'
    ]
};

function showModeSelection() {
    loginPage.classList.remove('active-page');
    dashboardPage.classList.add('active-page');
    interviewPage.classList.remove('active-page');
    teachingPage.classList.remove('active-page');
}

function showInterviewPage() {
    dashboardPage.classList.remove('active-page');
    interviewPage.classList.add('active-page');
    teachingPage.classList.remove('active-page');
    mode = 'interview';
    activateHeaderToggle('interview');
    renderSuggestions();
}

function showTeachingPage() {
    dashboardPage.classList.remove('active-page');
    teachingPage.classList.add('active-page');
    interviewPage.classList.remove('active-page');
    mode = 'teaching';
    activateHeaderToggle('teaching');
    renderSuggestions();
}

function activateHeaderToggle(targetMode) {
    if (targetMode === 'interview') {
        switchToInterviewFromInterviewBtn.classList.add('mode-pill--active');
        switchToTeachingFromInterviewBtn.classList.remove('mode-pill--active');
        switchToInterviewFromInterviewBtn.setAttribute('aria-selected', 'true');
        switchToTeachingFromInterviewBtn.setAttribute('aria-selected', 'false');

        switchToInterviewFromTeachingBtn.classList.add('mode-pill--active');
        switchToTeachingFromTeachingBtn.classList.remove('mode-pill--active');
        switchToInterviewFromTeachingBtn.setAttribute('aria-selected', 'true');
        switchToTeachingFromTeachingBtn.setAttribute('aria-selected', 'false');
    } else {
        switchToInterviewFromInterviewBtn.classList.remove('mode-pill--active');
        switchToTeachingFromInterviewBtn.classList.add('mode-pill--active');
        switchToInterviewFromInterviewBtn.setAttribute('aria-selected', 'false');
        switchToTeachingFromInterviewBtn.setAttribute('aria-selected', 'true');

        switchToInterviewFromTeachingBtn.classList.remove('mode-pill--active');
        switchToTeachingFromTeachingBtn.classList.add('mode-pill--active');
        switchToInterviewFromTeachingBtn.setAttribute('aria-selected', 'false');
        switchToTeachingFromTeachingBtn.setAttribute('aria-selected', 'true');
    }
}

function getActiveChatElements() {
    if (mode === 'interview') {
        return {
            messages: chatMessagesInterview,
            empty: chatEmptyInterview,
            textInput: textInputInterview
        };
    }
    return {
        messages: chatMessagesTeaching,
        empty: chatEmptyTeaching,
        textInput: textInputTeaching
    };
}

function renderSuggestions() {
    if (mode === 'interview') {
        suggestionsGridInterview.innerHTML = '';
        suggestionsByMode.interview.forEach((suggestion) => {
            const button = document.createElement('button');
            button.className = 'suggestion-pill';
            button.textContent = suggestion;
            button.addEventListener('click', () => handleSuggestion(suggestion));
            suggestionsGridInterview.appendChild(button);
        });
    } else {
        suggestionsGridTeaching.innerHTML = '';
        suggestionsByMode.teaching.forEach((suggestion) => {
            const button = document.createElement('button');
            button.className = 'suggestion-pill';
            button.textContent = suggestion;
            button.addEventListener('click', () => handleSuggestion(suggestion));
            suggestionsGridTeaching.appendChild(button);
        });
    }
}

function clearChat() {
    const { messages, empty } = getActiveChatElements();
    messages.innerHTML = '';
    empty.style.display = 'block';
    waitingForAnswer = false;
    isRecording = false;
    document.getElementById(mode === 'interview' ? 'mic' : 'micTeaching').textContent = '🎤';
}

function addMessage(text, sender) {
    const { messages, empty } = getActiveChatElements();
    empty.style.display = 'none';
    const messageEl = document.createElement('div');
    messageEl.classList.add('message', sender);
    messageEl.innerText = text;
    messages.appendChild(messageEl);
    messages.scrollTop = messages.scrollHeight;
}

async function handleSuggestion(suggestion) {
    addMessage(suggestion, 'user');

    if (mode === 'teaching') {
        try {
            const res = await fetch('http://127.0.0.1:5000/teaching/text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: suggestion }),
            });
            const data = await res.json();
            addMessage(data.explanation, 'agent');
            if (data.speech_file) {
                const audio = new Audio(data.speech_file);
                audio.play();
            }
        } catch (error) {
            addMessage('Error: ' + error.message, 'agent');
        }
    } else {
        try {
            const res = await fetch('http://127.0.0.1:5000/interview/text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: suggestion }),
            });
            const data = await res.json();
            addMessage(data.question, 'agent');
            if (data.audio) {
                const audio = new Audio('http://127.0.0.1:5000/' + data.audio);
                audio.play();
            }
            waitingForAnswer = true;
        } catch (error) {
            addMessage('Error: ' + error.message, 'agent');
        }
    }
}

function logout() {
    dashboardPage.classList.remove('active-page');
    interviewPage.classList.remove('active-page');
    teachingPage.classList.remove('active-page');
    loginPage.classList.add('active-page');
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    mode = 'interview';
    clearChat();
}

function backToModes() {
    dashboardPage.classList.add('active-page');
    interviewPage.classList.remove('active-page');
    teachingPage.classList.remove('active-page');
}

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        recordingStartTime = Date.now();

        mediaRecorder.ondataavailable = (event) => {
            if (event.data && event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            if (audioBlob.size === 0) {
                alert('No audio recorded! Try again.');
                return;
            }
            await sendAudio(audioBlob);
        };

        mediaRecorder.start(1000);
        isRecording = true;
        const micBtn = document.getElementById(mode === 'interview' ? 'mic' : 'micTeaching');
        micBtn.textContent = '⏹️';
    } catch (error) {
        alert('Allow microphone access to use voice features.');
    }
}

function stopRecording() {
    if (mediaRecorder && isRecording) {
        const duration = Date.now() - recordingStartTime;
        if (duration < 1000) {
            alert('Recording too short!');
            return;
        }

        mediaRecorder.stop();
        isRecording = false;
        const micBtn = document.getElementById(mode === 'interview' ? 'mic' : 'micTeaching');
        micBtn.textContent = '🎤';
        mediaRecorder.stream.getTracks().forEach((track) => track.stop());
    }
}

async function sendAudio(audioBlob) {
    addMessage('Recording sent...', 'user');
    const formData = new FormData();
    formData.append('file', audioBlob, 'audio.webm');

    try {
        if (mode === 'teaching') {
            const res = await fetch('http://127.0.0.1:5000/teaching/ask', {
                method: 'POST',
                body: formData,
            });
            const data = await res.json();
            addMessage(data.question, 'user');
            addMessage(data.explanation, 'agent');
            if (data.speech_file) {
                const audio = new Audio(data.speech_file);
                audio.play();
            }
        } else {
            const url = waitingForAnswer ? 'http://127.0.0.1:5000/interview/answer' : 'http://127.0.0.1:5000/interview/question';
            const res = await fetch(url, {
                method: 'POST',
                body: formData,
            });
            const data = await res.json();
            addMessage(data.transcript, 'user');
            if (waitingForAnswer) {
                addMessage(data.feedback, 'agent');
                if (data.audio) {
                    const audio = new Audio('http://127.0.0.1:5000/' + data.audio);
                    audio.play();
                }
                waitingForAnswer = false;
            } else {
                addMessage(data.question, 'agent');
                if (data.audio) {
                    const audio = new Audio('http://127.0.0.1:5000/' + data.audio);
                    audio.play();
                }
                waitingForAnswer = true;
            }
        }
    } catch (error) {
        addMessage('Error: ' + error.message, 'agent');
    }
}

async function sendTextMessage() {
    const { textInput } = getActiveChatElements();
    const text = textInput.value.trim();
    if (!text) return;
    addMessage(text, 'user');
    textInput.value = '';

    if (mode === 'teaching') {
        try {
            const res = await fetch('http://127.0.0.1:5000/teaching/text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: text }),
            });
            const data = await res.json();
            addMessage(data.explanation, 'agent');
            if (data.speech_file) {
                const audio = new Audio(data.speech_file);
                audio.play();
            }
        } catch (error) {
            addMessage('Error: ' + error.message, 'agent');
        }
    } else {
        try {
            const res = await fetch('http://127.0.0.1:5000/interview/text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: text }),
            });
            const data = await res.json();
            addMessage(data.question, 'agent');
            if (data.audio) {
                const audio = new Audio('http://127.0.0.1:5000/' + data.audio);
                audio.play();
            }
            waitingForAnswer = true;
        } catch (error) {
            addMessage('Error: ' + error.message, 'agent');
        }
    }
}

function setupEventListeners() {
    loginBtn.addEventListener('click', (event) => {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        if (username === 'user' && password === 'password') {
            showModeSelection();
        } else {
            alert('Invalid username or password. Please try again.');
        }
    });

    googleLoginBtn.addEventListener('click', (event) => {
        event.preventDefault();
        alert('Google sign-in is not configured in this demo.');
    });

    selectInterviewModeBtn.addEventListener('click', () => {
        showInterviewPage();
    });

    selectTeachingModeBtn.addEventListener('click', () => {
        showTeachingPage();
    });

    logoutFromSelectionBtn.addEventListener('click', () => {
        logout();
    });

    logoutFromInterviewBtn.addEventListener('click', () => {
        logout();
    });

    logoutFromTeachingBtn.addEventListener('click', () => {
        logout();
    });

    switchToInterviewFromInterviewBtn.addEventListener('click', () => {
        showInterviewPage();
    });

    switchToTeachingFromInterviewBtn.addEventListener('click', () => {
        showTeachingPage();
    });

    switchToInterviewFromTeachingBtn.addEventListener('click', () => {
        showInterviewPage();
    });

    switchToTeachingFromTeachingBtn.addEventListener('click', () => {
        showTeachingPage();
    });

    document.getElementById('mic').addEventListener('click', async (event) => {
        event.preventDefault();
        if (isRecording) {
            stopRecording();
        } else {
            await startRecording();
        }
    });

    document.getElementById('send').addEventListener('click', async (event) => {
        event.preventDefault();
        await sendTextMessage();
    });

    textInputInterview.addEventListener('keypress', async (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            await sendTextMessage();
        }
    });

    document.getElementById('micTeaching').addEventListener('click', async (event) => {
        event.preventDefault();
        if (isRecording) {
            stopRecording();
        } else {
            await startRecording();
        }
    });

    document.getElementById('sendTeaching').addEventListener('click', async (event) => {
        event.preventDefault();
        await sendTextMessage();
    });

    textInputTeaching.addEventListener('keypress', async (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            await sendTextMessage();
        }
    });
}

setupEventListeners();

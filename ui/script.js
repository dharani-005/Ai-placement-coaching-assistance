let mode = "interview";
let chat;
let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let waitingForAnswer = false;

// Initialize after DOM is loaded
document.addEventListener("DOMContentLoaded", function() {
    chat = document.getElementById("chat");
    setupEventListeners();
});

function addMessage(text, sender){

const div = document.createElement("div");
div.classList.add("message");
div.classList.add(sender);

div.innerText = text;

chat.appendChild(div);

chat.scrollTop = chat.scrollHeight;

}

// Audio Recording Setup
async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
        
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
            await sendAudio(audioBlob);
        };
        
        mediaRecorder.start();
        isRecording = true;
        document.getElementById("mic").textContent = "⏹️";
    } catch (error) {
        console.error("Microphone access denied:", error);
        alert("Please allow microphone access to record audio.");
    }
}

function stopRecording() {
    if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        isRecording = false;
        document.getElementById("mic").textContent = "🎤";
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }
}

async function sendAudio(audioBlob) {
    const formData = new FormData();
    formData.append("file", audioBlob, "audio.webm");
    
    try {
        if (mode === "teaching") {
            let res = await fetch("http://127.0.0.1:5000/teaching/ask", {
                method: "POST",
                body: formData
            });
            
            if (!res.ok) throw new Error(`Server error: ${res.status}`);
            
            let data = await res.json();
            addMessage(data.question, "user");
            addMessage(data.explanation, "agent");
            
            if (data.speech_file) {
                let audio = new Audio(data.speech_file);
                audio.play();
            }
        } else if (mode === "interview") {
            let url;

            if (waitingForAnswer) {
                url = "http://127.0.0.1:5000/interview/answer";
            } else {
                url = "http://127.0.0.1:5000/interview/question";
            }

            let res = await fetch(url, {
                method: "POST",
                body: formData
            });

            if (!res.ok) throw new Error(`Server error: ${res.status}`);

            let data = await res.json();

            // show what user said
            addMessage(data.transcript, "user");

            if (waitingForAnswer) {
                addMessage(data.feedback, "agent");

                if (data.audio) {
                    let audio = new Audio("http://127.0.0.1:5000/" + data.audio);
                    audio.play();
                }

                waitingForAnswer = false;
            } else {
                addMessage(data.question, "agent");

                if (data.audio) {
                    let audio = new Audio("http://127.0.0.1:5000/" + data.audio);
                    audio.play();
                }

                waitingForAnswer = true;
            }
        }
    } catch (error) {
        console.error("Error:", error);
        addMessage("Error: " + error.message, "agent");
    }
}

function setupEventListeners() {
    document.getElementById("interviewMode").onclick = () => {
        mode = "interview";
        document.getElementById("interviewMode").classList.add("active");
        document.getElementById("teachingMode").classList.remove("active");
    };

    document.getElementById("teachingMode").onclick = () => {
        mode = "teaching";
        document.getElementById("teachingMode").classList.add("active");
        document.getElementById("interviewMode").classList.remove("active");
    };

    // Microphone button handler
    document.getElementById("mic").addEventListener("click", function(e) {
        e.preventDefault();
        if (isRecording) {
            stopRecording();
        } else {
            startRecording();
        }
    });

    // Send text message
    document.getElementById("send").addEventListener("click", async function(e) {
        e.preventDefault();
        let textInput = document.getElementById("textInput");
        let text = textInput.value;

        if(!text) return;

        addMessage(text,"user");
        textInput.value="";

        if(mode==="teaching"){
            let res = await fetch("http://127.0.0.1:5000/teaching/text",{
                method:"POST",
                headers:{
                    "Content-Type":"application/json"
                },
                body:JSON.stringify({
                    question:text
                })
            });

            let data = await res.json();
            addMessage(data.explanation,"agent");

            let audio = new Audio("../"+data.speech_file);
            audio.play();
        }
    });

    // Allow Enter key to send text
    document.getElementById("textInput").addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            document.getElementById("send").click();
        }
    });
}
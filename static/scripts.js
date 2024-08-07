// scripts.js

// Variable to store whether seeking is in progress
var isSeeking = false;

function playSong(song) {
    var audioPlayer = document.getElementById("audio-player");
    var songUrl = "/static/songs/" + song + ".mp3"; // Replace "/static/songs/" with the correct path to your songs

    audioPlayer.src = songUrl;
    audioPlayer.play();
}

// Function to update the progress bar and enable seeking
function updateProgressBar() {
    var audioPlayer = document.getElementById("audio-player");
    var progressBar = document.querySelector(".progress");
    var ongoingTime = document.querySelector(".progress-ongoing");
    var totalTime = document.querySelector(".progress-total");

    var progress = (audioPlayer.currentTime / audioPlayer.duration) * 100;
    progressBar.style.width = progress + "%";

    // Update ongoing time duration
    var currentMinutes = Math.floor(audioPlayer.currentTime / 60);
    var currentSeconds = Math.floor(audioPlayer.currentTime % 60);
    ongoingTime.textContent = currentMinutes + ":" + (currentSeconds < 10 ? "0" : "") + currentSeconds;

    // Update total time duration
    var totalMinutes = Math.floor(audioPlayer.duration / 60);
    var totalSeconds = Math.floor(audioPlayer.duration % 60);
    totalTime.textContent = totalMinutes + ":" + (totalSeconds < 10 ? "0" : "") + totalSeconds;

    // If seeking is not in progress, continue updating progress bar
    if (!isSeeking) {
        requestAnimationFrame(updateProgressBar);
    }
}

// Add an event listener to update the progress bar on timeupdate
var audioPlayer = document.getElementById("audio-player");
audioPlayer.addEventListener("timeupdate", function () {
    // Only update progress bar if not seeking
    if (!isSeeking) {
        updateProgressBar();
    }
});

// Function to handle seeking on the progress bar
function seek(event) {
    var audioPlayer = document.getElementById("audio-player");
    var progressBar = document.querySelector(".progress");

    var rect = progressBar.getBoundingClientRect();
    var totalWidth = rect.width;
    var offsetX = event.clientX - rect.left;
    var percentage = offsetX / totalWidth;

    // Calculate the new time position
    var newTime = audioPlayer.duration * percentage;

    // Set the new time position for the audio player
    audioPlayer.currentTime = newTime;
}

// Event listeners for seeking
var progressBar = document.querySelector(".progress-bar");
progressBar.addEventListener("mousedown", function (event) {
    isSeeking = true;
    seek(event);
});

window.addEventListener("mouseup", function () {
    isSeeking = false;
});

// Initial call to start updating progress bar
updateProgressBar();

// Play/Resume button function
function playResume() {
    if (audioPlayer.paused) {
        audioPlayer.play();
    } else {
        audioPlayer.pause();
    }
}

// Forward button function
function forward() {
    audioPlayer.currentTime += 5; // Adjust the value as per your preference for the forward duration
}

// Backward button function
function backward() {
    audioPlayer.currentTime -= 5; // Adjust the value as per your preference for the backward duration
}

// Initial call to start updating progress bar and song durations
updateProgressBar();

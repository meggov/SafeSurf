function submitName() {
    const name = document.getElementById("nameInput").value;
    if (name.trim() === "") {
        alert("Please enter your name.");
        return;
    }
    document.getElementById("welcomeScreen").classList.add("hidden");
    document.getElementById("mainScreen").classList.remove("hidden");
    document.getElementById("welcomeMessage").textContent += name + "!";
}

function practiceSkills() {
    // Implement the logic for practicing skills
    alert("Practice Your Skills clicked.");
}

function playSafeSurf() {
    // Implement the logic for playing SafeSurf
    alert("Play SafeSurf clicked.");
}
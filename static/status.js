function updateStatus() {
    // Get the status element
    let statusElement = document.getElementById("status");

    // Update status to "waiting" when the form is submitted
    statusElement.innerHTML = "Bot is waiting for the scheduled time...";

    // Simulate a delay before starting the bot
    setTimeout(function() {
        statusElement.innerHTML = "Bot is starting...";
    }, 2000);  // 2 seconds delay

    // Simulate bot running and then finishing
    setTimeout(function() {
        statusElement.innerHTML = "Bot has finished running.";
    }, 5000);  // 5 seconds delay after start
}
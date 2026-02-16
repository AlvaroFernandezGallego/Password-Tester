// Get DOM elements for password input, strength bar, status, and toggle button
const input = document.getElementById("password");
const bar = document.getElementById("bar");
const statusText = document.getElementById("status");
const toggle = document.getElementById("togglePassword");

// Toggle password visibility
toggle.addEventListener("click", () => {
  if (input.type === "password") 
    {
      input.type = "text";
      toggle.innerText = "Hide";
    } 
  else 
    {
      input.type = "password";
      toggle.innerText = "Show";
    }
});

// Listen for input changes to evaluate password in real-time
input.addEventListener("input", () => {
  const password = input.value;

  // Send password to the backend for evaluation
  fetch("/check_password", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({password})
  })
  .then(res => res.json())
  .then(data => updateUI(data));
});

// Update the strength bar and status message
function updateUI(data) 
{
  bar.style.width = data.score + "%";

  // Set bar color based on password strength
  if (data.is_common || data.score < 20) 
    {
      bar.style.background = "#ef4444";
    } 
  else if (data.score < 40) 
    {
      bar.style.background = "#f97316";
    } 
  else if (data.score < 60) 
    {
      bar.style.background = "#eab308";
    } 
  else if (data.score < 80) 
    {
      bar.style.background = "#84cc16";
    } 
  else 
    {
      bar.style.background = "#16a34a";
    }

  // Update textual status
  statusText.innerText = data.status;
}

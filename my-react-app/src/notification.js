function showNotification(message) {
  const notification = document.querySelector(".notification");
  const notificationMessage = document.querySelector("#notification-message");
  notificationMessage.textContent = message;
  notification.style.display = "block";

  setTimeout(() => {
    closeNotification();
  }, 5000); // Auto-close the notification after 5 seconds
}

function closeNotification() {
  const notification = document.querySelector(".notification");
  notification.style.display = "none";
}

export default showNotification;

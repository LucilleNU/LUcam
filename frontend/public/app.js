// Register Service Worker
if ("serviceWorker" in navigator) {
  navigator.serviceWorker
    .register("/serviceworker.js")
    .then((registration) => {
      console.log("Service Worker Registered");
      return registration;
    })
    .catch((err) => {
      console.error("Unable to register service worker.", err);
    });
}

window.addEventListener(
  "online",
  (e) => {
    console.log("You are online");
  },
  false
);

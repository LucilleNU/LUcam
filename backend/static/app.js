// Register Service Worker
if ("serviceWorker" in navigator) {
  navigator.serviceWorker
    .register("/service-worker.js")
    .then((registration) => {
      console.log("Service Worker Registered");
      return registration;
    })
    .catch((err) => {
      console.error("Unable to register service worker.", err);
    });
}

// PWA
let deferredPrompt;
const addBtn = document.querySelector(".add-button");
addBtn.style.display = "inline-block";

window.addEventListener("beforeinstallprompt", (e) => {
  e.preventDefault();
  console.log("1");
  deferredPrompt = e;
  // addBtn.style.display = "inline-block";
  addBtn.addEventListener("click", (_e) => {
    // addBtn.style.display = "inline-block";
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === "accepted") {
        console.log("User accepted the A2HS prompt");
      } else {
        console.log("User dismissed the A2HS prompt");
      }
      deferredPrompt = null;
    });
  });
});

window.addEventListener(
  "online",
  (e) => {
    console.log("You are online");
  },
  false
);

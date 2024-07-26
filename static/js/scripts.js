document.querySelectorAll(".delete-button321").forEach((deleteButton) => {
  deleteButton.addEventListener("click", () => {
    const targetPopupId = deleteButton.getAttribute("data-target");
    const deletePopup = document.getElementById(targetPopupId);
    deletePopup.style.display = "block";
  });
});

// document.querySelectorAll(".yes-button321").forEach((yesButton) => {
//   yesButton.addEventListener("click", () => {
//     const targetPopupId = yesButton.closest(".popup321").id;
//     const deletePopup = document.getElementById(targetPopupId);
//     deletePopup.style.display = "none";
//   });
// });

document.querySelectorAll(".yes-button321").forEach((noButton) => {
  noButton.addEventListener("click", () => {
    noButton.parentElement.parentElement.parentElement.style.display = "flex";
    console.log(
      noButton.parentElement.parentElement.parentElement.style.display
    );
    document.querySelectorAll(".popup321").forEach((currentItem) => {
      currentItem.style.display = "flex";
    });
  });
});

document.querySelectorAll(".no-button321").forEach((noButton) => {
  noButton.addEventListener("click", () => {
    noButton.parentElement.parentElement.parentElement.style.display = "none";
    console.log(
      noButton.parentElement.parentElement.parentElement.style.display
    );
    document.querySelectorAll(".popup321").forEach((currentItem) => {
      currentItem.style.display = "none";
    });
  });
});

document.querySelectorAll(".delete-button321").forEach((currentItem) => {
  currentItem.addEventListener("click", () => {
    console.log(currentItem.nextElementSibling);
    currentItem.nextElementSibling.style.display = "block";
  });
});

//below code is for inputting of otp
const otpInputs1 = document.querySelectorAll(".otp-input");

otpInputs1.forEach((input) => {
  input.addEventListener("input", (e) => {
    const text = e.target.value;
    if (text.length === 1) {
      const nextInput = input.nextElementSibling;
      if (nextInput) {
        nextInput.focus(); // Move focus to the next input box
      }
    } else if (text.length === 0) {
      const prevInput = input.previousElementSibling;
      if (prevInput) {
        prevInput.focus(); // Move focus to the previous input box
      }
    }
  });
});

// toggleing icon on the nav bar
//  nav bar toggle
let check = 1;
const navbar = document.querySelector("#navbarDropdown");
const navbar_list = document.querySelector("#nav_bar123");
console.log(navbar_list);
navbar.addEventListener("click", () => {
  navbar_list.style.display == check++ % 2 ? "none" : "block";
  console.log(navbar_list.classList);
  console.log(check);
});

document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("edit-profile-btn_234")
    .addEventListener("click", function () {
      var modal = document.getElementById("edit-profile-modal_789");
      modal.style.display = "flex";
    });

  document
    .getElementsByClassName("close_321")[0]
    .addEventListener("click", function () {
      var modal = document.getElementById("edit-profile-modal_789");
      modal.style.display = "none";
    });
});

//color123
const navbar_links = document.querySelectorAll(".navbar_links123");
window.addEventListener("scroll", () => {
  navbar_links.forEach((currentItem) => {
    currentItem.style.color = window.pageYOffset < 350 ? "white" : "black";
  });
});

const toggle = document.querySelector(".navbar-toggler-icon");
const links_container = document.querySelector(".above_link_container");
const btm_container = document.querySelector(".all_links_container");

toggle.addEventListener("click", function () {
  const btm_height = btm_container.getBoundingClientRect().height; // new
  const links_container_height = links_container.getBoundingClientRect().height;
  if (links_container_height != btm_height) {
    links_container.style.height = `${btm_height}px`;
  } else {
    links_container.style.height = `0px`;
  }
});

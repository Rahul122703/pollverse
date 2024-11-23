// Handling delete button
const delete_button = document.querySelector(".delete-button321");
if (delete_button) {
  delete_button
    .querySelectorAll(".delete-button321")
    .forEach((deleteButton) => {
      deleteButton.addEventListener("click", () => {
        const targetPopupId = deleteButton.getAttribute("data-target");
        const deletePopup = document.getElementById(targetPopupId);
        deletePopup.style.display = "block";
      });
    });
}

// Handling "Yes" buttons
// const yes_buttons = document.querySelectorAll(".yes-button321");
// if (yes_buttons) {
//   yes_buttons.forEach((yesButton) => {
//     yesButton.addEventListener("click", () => {
//       yesButton.parentElement.parentElement.parentElement.style.display =
//         "flex";
//       document.querySelectorAll(".popup321").forEach((currentItem) => {
//         currentItem.style.display = "flex";
//       });
//     });
//   });
// }

// Handling "No" buttons
const no_buttons = document.querySelectorAll(".no-button321");
if (no_buttons) {
  no_buttons.forEach((noButton) => {
    noButton.addEventListener("click", () => {
      noButton.parentElement.parentElement.parentElement.style.display = "none";
      document.querySelectorAll(".popup321").forEach((currentItem) => {
        currentItem.style.display = "none";
      });
    });
  });
}

// Handling delete-popup visibility
const delete_buttons = document.querySelectorAll(".delete-button321");
if (delete_buttons) {
  delete_buttons.forEach((currentItem) => {
    currentItem.addEventListener("click", () => {
      currentItem.nextElementSibling.style.display = "block";
    });
  });
}

// Handling OTP inputs
const otpInputs1 = document.querySelectorAll(".otp-input");
if (otpInputs1) {
  otpInputs1.forEach((input) => {
    input.addEventListener("input", (e) => {
      const text = e.target.value;
      if (text.length === 1) {
        const nextInput = input.nextElementSibling;
        if (nextInput) nextInput.focus();
      } else if (text.length === 0) {
        const prevInput = input.previousElementSibling;
        if (prevInput) prevInput.focus();
      }
    });
  });
}

// Handling Navbar toggle
const navbar = document.querySelector("#navbarDropdown");
if (navbar) {
  const navbar_list = document.querySelector("#nav_bar123");
  let check = 1;
  navbar.addEventListener("click", () => {
    navbar_list.style.display = check++ % 2 ? "none" : "block";
  });
}

// Handling Edit Profile Modal
document.addEventListener("DOMContentLoaded", function () {
  const editProfileButton = document.getElementById("edit-profile-btn_234");
  const closeModalButton = document.getElementsByClassName("close_321")[0];
  const modal = document.getElementById("edit-profile-modal_789");

  if (editProfileButton && closeModalButton && modal) {
    editProfileButton.addEventListener("click", () => {
      modal.style.display = "flex";
    });

    closeModalButton.addEventListener("click", () => {
      modal.style.display = "none";
    });
  }
});

// Navbar links color toggle based on scroll
const navbar_links = document.querySelectorAll(".navbar_links123");
if (navbar_links) {
  window.addEventListener("scroll", () => {
    navbar_links.forEach((currentItem) => {
      currentItem.style.color = window.pageYOffset < 350 ? "white" : "black";
    });
  });
}

// Navbar toggler for mobile view
const toggle = document.querySelector(".navbar-toggler-icon");
if (toggle) {
  const links_container = document.querySelector(".above_link_container");
  const btm_container = document.querySelector(".all_links_container");

  if (links_container && btm_container) {
    toggle.addEventListener("click", function () {
      const btm_height = btm_container.getBoundingClientRect().height;
      const links_container_height =
        links_container.getBoundingClientRect().height;

      links_container.style.height =
        links_container_height !== btm_height ? `${btm_height}px` : `0px`;
    });
  }
}

// Handling Login Popup
const index_login = document.querySelector("#indexLogin");
const index_modal = document.querySelector("#loginPopup");
const cross_button = document.querySelector("#cross_png");

if (index_login && index_modal && cross_button) {
  index_login.addEventListener("click", () => {
    index_modal.classList.remove("dont_show");
    index_modal.classList.add("overlay");
  });

  cross_button.addEventListener("click", () => {
    index_modal.classList.remove("overlay");
    index_modal.classList.add("dont_show");
  });
}


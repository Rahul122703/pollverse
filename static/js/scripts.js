document.querySelectorAll(".delete-button321").forEach((deleteButton) => {
  deleteButton.addEventListener("click", () => {
    const targetPopupId = deleteButton.getAttribute("data-target");
    const deletePopup = document.getElementById(targetPopupId);
    deletePopup.style.display = "block";
  });
});

document.querySelectorAll(".yes-button321").forEach((yesButton) => {
  yesButton.addEventListener("click", () => {
    const targetPopupId = yesButton.closest(".popup321").id;
    const deletePopup = document.getElementById(targetPopupId);
    deletePopup.style.display = "none";
  });
});

document.querySelectorAll(".no-button321").forEach((noButton) => {
  noButton.addEventListener("click", () => {
    const targetPopupId = noButton.closest(".popup321").id;
    const deletePopup = document.getElementById(targetPopupId);
    deletePopup.style.display = "none";
  });
});

document.querySelectorAll(".cross321").forEach((crossButton) => {
  crossButton.addEventListener("click", () => {
    const targetPopupId = crossButton.closest(".popup321").id;
    const deletePopup = document.getElementById(targetPopupId);
    deletePopup.style.display = "none";
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

  window.addEventListener("click", function (event) {
    var modal = document.getElementById("edit-profile-modal_789");

    if (event.target == modal) {
      modal.style.display = "none";
    }
  });
});

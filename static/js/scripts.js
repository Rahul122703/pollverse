
//This part of the code is for toggling delete button and the pop up 
document.querySelectorAll('.delete-button321').forEach(deleteButton => {
    deleteButton.addEventListener('click', () => {
        const targetPopupId = deleteButton.getAttribute('data-target');
        const deletePopup = document.getElementById(targetPopupId);
        deletePopup.style.display = 'block';
    });
});

document.querySelectorAll('.yes-button321').forEach(yesButton => {
    yesButton.addEventListener('click', () => {
        const targetPopupId = yesButton.closest('.popup321').id;
        const deletePopup = document.getElementById(targetPopupId);
        deletePopup.style.display = 'none';
    });
});

document.querySelectorAll('.no-button321').forEach(noButton => {
    noButton.addEventListener('click', () => {
        const targetPopupId = noButton.closest('.popup321').id;
        const deletePopup = document.getElementById(targetPopupId);
        deletePopup.style.display = 'none';
    });
});

document.querySelectorAll('.cross321').forEach(crossButton => {
    crossButton.addEventListener('click', () => {
        const targetPopupId = crossButton.closest('.popup321').id;
        const deletePopup = document.getElementById(targetPopupId);
        deletePopup.style.display = 'none';
    });
});




const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const registercontainer = document.getElementById('registercontainer');

signUpButton.addEventListener('click', () => {
    registercontainer.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
    registercontainer.classList.remove("right-panel-active");
});

function signUp() {
    // Add your sign up logic here
    console.log('Sign Up button clicked');
}

function signIn() {
    // Add your sign in logic here
    console.log('Sign In button clicked');
}

//below code is for inputting of otp
const otpInputs = document.querySelectorAll('.otp-input');

otpInputs.forEach(input => {
  input.addEventListener('input', (e) => {
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



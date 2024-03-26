
//this below code is for toggling side bar
function w3_open() {
    document.getElementById("mySidebar").style.display = "block";
}
function w3_close() {
    document.getElementById("mySidebar").style.display = "none";
}


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


function toggleReply(button) {
var replyInput = button.nextElementSibling;
replyInput.style.display = (replyInput.style.display === 'none') ? 'block' : 'none';
}

function saveReply(button) {
var replyInput = button.previousElementSibling;
var replyText = replyInput.value.trim();
if (replyText !== '') {
    var parentComment = button.closest('.comment-container');
    var repliesContainer = parentComment.querySelector('.replies-container');

    var replyContainerId = 'reply-' + Date.now(); // Generate unique ID for reply container
    var replyContainer = `
    <div class="comment-container" id="${replyContainerId}">
        <div class="user-info">
            <div class="user-icon"><img src = "{{ user_obj.icon }}" class="user-icon" /></div>
            <div class="username">{{ user_obj.username}}</div>
        </div>

        <div class="comment-content">${replyText}</div>
        <button class="toggle-replies-button" onclick="toggleReplies(this, '${replyContainerId}')">+</button>
        <span class="reply-symbol" onclick="toggleReply(this)">↵</span>
        <div class="reply-input" style="display:none;">
            <textarea placeholder="Your reply" class="minimal-input"></textarea>
            <button onclick="saveReply(this)">Save</button>
        </div>
        <div class="replies-container">
            <!-- Nested replies will go here -->
        </div>
    </div>
    `;

    repliesContainer.innerHTML += replyContainer;
    replyInput.value = ''; // Clear input field after saving reply
}
}

function toggleReplies(button, commentId) {
var repliesContainer = document.getElementById(commentId).querySelector('.replies-container');
var replies = repliesContainer.querySelectorAll('.comment-container');

for (var i = 0; i < replies.length; i++) {
    replies[i].style.display = (replies[i].style.display === 'none') ? 'block' : 'none';
}

// Change button text based on replies visibility
button.textContent = (replies[0].style.display === 'none') ? '+' : '-';
}

// Function to toggle comments visibility
document.getElementById('toggle-comments').addEventListener('click', function() {
var comments = document.querySelectorAll('.comment-container');
for (var i = 0; i < comments.length; i++) {
    comments[i].style.display = (comments[i].style.display === 'none') ? 'block' : 'none';
}
});

function vote(voteButton) {
var voteCountSpan = voteButton.parentElement.querySelector('.vote-count');
var voteCount = parseInt(voteCountSpan.textContent);

if (voteButton.classList.contains('upvote')) {
    voteCount++;
} else if (voteButton.classList.contains('downvote')) {
    voteCount--;
}

voteCountSpan.textContent = voteCount;
}


function vote(voteButton) {
var voteCountSpan = voteButton.parentElement.querySelector('.vote-count');
var voteCount = parseInt(voteCountSpan.textContent);

var upvoteButton = voteButton.parentElement.querySelector('.upvote');
var downvoteButton = voteButton.parentElement.querySelector('.downvote');

if (voteButton.classList.contains('upvote')) {
    if (!upvoteButton.classList.contains('active')) {
    voteCount++;
    voteCountSpan.textContent = voteCount;
    upvoteButton.classList.add('active');
    downvoteButton.classList.remove('active');
    }
} else if (voteButton.classList.contains('downvote')) {
    if (!downvoteButton.classList.contains('active')) {
    voteCount--;
    voteCountSpan.textContent = voteCount;
    downvoteButton.classList.add('active');
    upvoteButton.classList.remove('active');
    }
}
}

window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    const headerHeight = mainNav.clientHeight;
    window.addEventListener('scroll', function() {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        if ( currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                console.log(123);
                mainNav.classList.remove('is-visible', 'is-fixed');
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove(['is-visible']);
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }
        scrollPos = currentTop;
    });
})

//This is for the side nav bar opening and closing button
document.addEventListener("DOMContentLoaded", function () {
    const leftNav = document.querySelector('.sidenav.left');
    const rightNav = document.querySelector('.sidenav.right');

    // Toggle left navigation panel
    document.querySelector('#openLeftNav').addEventListener('click', function () {
      leftNav.classList.toggle('open');
    });

    // Toggle right navigation panel
    document.querySelector('#openRightNav').addEventListener('click', function () {
      rightNav.classList.toggle('open');
    });
  });


//USER PROFILE LOGIC



  
function showForm() {
    document.getElementById('discussion-form').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
}

function closeForm() {
    document.getElementById('discussion-form').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
}

function submitDiscussion() {
    const title = document.getElementById('newTitle').value;
    const content = document.getElementById('newContent').value;

    if (title.trim() === "" || content.trim() === "") {
        alert("Please fill in both fields!");
        return;
    }

    const discussionsDiv = document.getElementById('discussions');
    const discussion = document.createElement('div');
    discussion.className = 'discussion-card';
    discussion.innerHTML = `
        <div class="user-info">User${Math.floor(Math.random() * 90000) + 10000}</div>
        <h2 class="post-title">${title}</h2>
        <p class="post-content">${content}</p>
        <div class="upvote">
            <button class="upvote-btn" onclick="upvote(this)">⬆️</button>
            <span>0</span>
        </div>
    `;
    discussionsDiv.prepend(discussion);

    document.getElementById('newTitle').value = '';
    document.getElementById('newContent').value = '';
    closeForm();
}

function upvote(button) {
    const span = button.nextElementSibling;
    span.innerText = parseInt(span.innerText) + 1;
}

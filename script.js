let discussionsData = [];

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

    const newDiscussion = {
        id: discussionsData.length + 1,
        username: "User" + (Math.floor(Math.random() * 90000) + 10000),
        title: title,
        content: content,
        createdAt: new Date(),
        upvotes: 0
    };

    discussionsData.unshift(newDiscussion);
    renderDiscussions();
    document.getElementById('newTitle').value = '';
    document.getElementById('newContent').value = '';
    closeForm();
}

function renderDiscussions() {
    const discussionsDiv = document.getElementById('discussions');
    discussionsDiv.innerHTML = '';

    discussionsData.forEach(discussion => {
        const discussionEl = document.createElement('div');
        discussionEl.className = 'discussion-card';
        discussionEl.innerHTML = `
            <div class="user-info">${discussion.username}</div>
            <h2 class="post-title">${discussion.title}</h2>
            <p class="post-content">${discussion.content}</p>
            <div class="vote-buttons">
                <button onclick="upvote(${discussion.id})">⬆️</button>
                <span>${discussion.upvotes}</span>
                <button onclick="downvote(${discussion.id})">⬇️</button>
                <button class="delete-btn" onclick="deleteDiscussion(${discussion.id})">🗑️</button>
            </div>
        `;
        discussionsDiv.appendChild(discussionEl);
    });
}

function upvote(id) {
    const post = discussionsData.find(d => d.id === id);
    if (post) {
        post.upvotes++;
        renderDiscussions();
    }
}

function downvote(id) {
    const post = discussionsData.find(d => d.id === id);
    if (post && post.upvotes > 0) {
        post.upvotes--;
        renderDiscussions();
    }
}

function deleteDiscussion(id) {
    discussionsData = discussionsData.filter(d => d.id !== id);
    renderDiscussions();
}

function sortDiscussions() {
    const sortBy = document.getElementById('sortOptions').value;

    if (sortBy === "time") {
        discussionsData.sort((a, b) => b.createdAt - a.createdAt);
    } else if (sortBy === "upvotes") {
        discussionsData.sort((a, b) => b.upvotes - a.upvotes);
    }
    renderDiscussions();
}

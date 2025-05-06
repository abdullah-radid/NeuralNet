from flask import Flask, render_template, request, redirect

app = Flask(__name__)

posts = []

@app.route('/')
def home():
    sort = request.args.get('sort', 'newest')

    if sort == 'upvotes':
        sorted_posts = sorted(posts, key=lambda x: x['votes'], reverse=True)
    else:
        sorted_posts = posts

    return render_template('index.html', posts=sorted_posts, sort=sort)

@app.route('/add', methods=['POST'])
def add_post():
    title = request.form['title']
    content = request.form['content']
    posts.insert(0, {"title": title, "content": content, "votes": 0})
    return redirect('/')

@app.route('/vote/<int:post_index>/<action>', methods=['POST'])
def vote(post_index, action):
    if 0 <= post_index < len(posts):
        if action == 'up':
            posts[post_index]['votes'] += 1
        elif action == 'down':
            posts[post_index]['votes'] -= 1
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)


popular_df = pickle.load(open("assets/popular.pkl", "rb"))
pt = pickle.load(open("assets/pt.pkl", "rb"))
books = pickle.load(open("assets/books.pkl", "rb"))
similarity_scores = pickle.load(open("assets/similarity_scores.pkl", "rb"))

@app.route("/")
def index():
    return render_template("index.html",
                            book_names=list(popular_df['Book-Title'].values),
                            authors=list(popular_df['Book-Author'].values),
                            images=list(popular_df['Image-URL-M'].values),
                            votes=list(popular_df['num_ratings'].values),
                            ratings=list(popular_df['avg_ratings'].values),
    )

@app.route("/recommend")
def recommend_ui():
    return render_template("recommend.html")

@app.route("/recommend_books", methods =['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index_of_book = np.where(pt.index==user_input)[0][0]
    suggestions = sorted(list(enumerate(similarity_scores[index_of_book])), key=lambda x: x[1], reverse=True)[1:6]
    
    data = []

    for suggestion in suggestions:
        item=[]
        temp_df = books[books['Book-Title'] == pt.index[suggestion[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')  ['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')  ['Image-URL-M'].values))
        data.append(item)

    return render_template("recommend.html", data=data)

if __name__=="__main__":
    app.run(debug=True)
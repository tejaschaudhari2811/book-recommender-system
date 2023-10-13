from flask import Flask, render_template
import pickle

app = Flask(__name__)


popular_df = pickle.load(open("popular.pkl", "rb"))

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

if __name__=="__main__":
    app.run(debug=True)
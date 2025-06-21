import pickle, difflib, requests

# Load model.pkl
with open("model.pkl", "rb") as f:
    tfidf, similarity_score, df = pickle.load(f)

def recommend_movies(movie_list, top_n=10):
    if not movie_list:
        return []

    matched_titles, matched_indices = [], []
    for movie in movie_list:
        exact = [t for t in df['Movie_Title'] if movie.lower() in t.lower()]
        titles = exact if exact else difflib.get_close_matches(movie, df['Movie_Title'], n=3, cutoff=0.5)
        for t in titles:
            idx = df[df['Movie_Title'] == t].index[0]
            if t not in matched_titles:
                matched_titles.append(t)
                matched_indices.append(idx)

    sim_scores = {}
    for idx in matched_indices:
        for j, s in enumerate(similarity_score[idx]):
            sim_scores[j] = sim_scores.get(j, 0) + s

    sim_ordered = sorted(sim_scores.items(), key=lambda x: x[1], reverse=True)
    recs = list(matched_titles)
    for idx, _ in sim_ordered:
        t = df.iloc[idx]['Movie_Title']
        if t not in recs and t not in movie_list:
            recs.append(t)
        if len(recs) >= top_n:
            break

    return recs

def get_all_movies():
    return df['Movie_Title'].tolist()

def get_poster(title):
    try:
        # Search TMDb to get correct movie
        resp = requests.get(
            f"https://api.themoviedb.org/3/search/movie?api_key=8265bd1679663a7ea12ac168da84d2e8&query={requests.utils.quote(title)}"
        ).json()
        results = resp.get('results', [])
        if results:
            pid = results[0]['id']
            poster_path = results[0].get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except:
        pass
    return "https://via.placeholder.com/160x240?text=No+Image"






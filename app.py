import streamlit as st
import streamlit.components.v1 as components
from utility import get_all_movies, recommend_movies, get_poster

st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System")

# Sidebar selections
st.sidebar.header("Select movies to base recommendations on")
all_movies = get_all_movies()
recent = st.sidebar.multiselect("Recently Watched", all_movies)
watchlist = st.sidebar.multiselect("Watchlist", all_movies)
selected = list(dict.fromkeys(recent + watchlist))

# Function to render a horizontal scrollable movie row
def render_scroll(title, titles_list, recommend_from_model=True):
    st.subheader(title)
    if not titles_list:
        st.warning("No movies to show.")
        return
    
    # If needed, run recommendation engine
    if recommend_from_model:
        titles_list = recommend_movies(titles_list)

    html = '<div style="display:flex; overflow-x:auto; padding:10px;">'
    for t in titles_list:
        img = get_poster(t)
        html += f'''
            <div style="flex:0 0 auto; width:160px; margin-right:16px; text-align:center;">
                <img src="{img}" style="width:100%; border-radius:12px;"/>
                <div style="margin-top:8px; color:#fff;">{t}</div>
            </div>
        '''
    html += '</div>'
    components.html(html, height=300, scrolling=True)

# Show automatic recommendations based on sidebar
render_scroll("🎯 Recommended for You", selected)

# Search and Recommend section (independent)
st.markdown("---")
st.subheader("🔍 Search & Recommend")
query = st.text_input("Enter a movie name to search")
if st.button("Recommend"):
    if query:
        search_recs = recommend_movies([query])
        render_scroll(f"🔍 Results for: {query}", search_recs, recommend_from_model=False)
    else:
        st.warning("Please enter a movie name.")





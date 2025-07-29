import streamlit as st
import json
import os

# Sample data
def get_index(options, value):
    """Safely get index of value or return 0"""
    
    return options.index(value) if value in options else 0

samples = [
    {
        "query": "What are the health benefits of turmeric?",
        "texts": [
            "Turmeric is known for its anti-inflammatory properties.",
            "It is used widely in Indian cooking.",
            "Some studies suggest turmeric helps with brain function.",
            "Turmeric is a yellow spice that gives curry its color.",
            "The Eiffel Tower is in Paris."
        ]
    },
    {
        "query": "How does photosynthesis work?",
        "texts": [
            "Photosynthesis converts sunlight into chemical energy.",
            "Chlorophyll absorbs light energy in plants.",
            "It is used in food production.",
            "The moon reflects sunlight but doesn’t produce its own.",
            "Photosynthesis takes place in chloroplasts."
        ]
    }
]
videos = [

    "https://www.youtube.com/watch?v=yvFQwD8AAbk",
    "https://www.youtube.com/watch?v=yvFQwD8AAbk",
    "https://www.youtube.com/watch?v=yvFQwD8AAbk",
    "https://www.youtube.com/watch?v=yvFQwD8AAbk",
    "https://www.youtube.com/watch?v=yvFQwD8AAbk"


]
def save_all_rankings():
        os.makedirs("saved_data", exist_ok=True)

        all_data = []
        for i, sample in enumerate(samples):
            ranking = st.session_state.rankings.get(i, ["", "", ""])
            entry = {
                "query": sample["query"],
                "ranked_texts": ranking
            }
            all_data.append(entry)

        with open("saved_data/all_rankings.json", "w") as f:
            json.dump(all_data, f, indent=2)

        return json.dumps(all_data)

def login_page():
    st.title("Login")
    username = st.text_input("Enter your username")

    if st.button("Submit"):
        if username:
            st.session_state.username = username  # Store username in session state
            st.success(f"Welcome, {username}!")
            # You can then redirect to another page or display further content
        else:
            st.error("Please enter a username.")

def main(username):
    # Initialize session state
    if 'index' not in st.session_state:
        
        try:
            file_path = f"saved_data/all_rankings.json"
            with open(file_path, "r") as f:
                data = json.load(f)
            st.session_state.index = len(data)-1
            
            st.session_state.rankings = {}
            for i, elem in enumerate(data):
                st.session_state.rankings[i] = data[i]["ranked_texts"]
            
        except:
            st.session_state.rankings = {}
            st.session_state.index = 0
            
    #if 'rankings' not in st.session_state:
    #    st.session_state.rankings = {}

    current_index = st.session_state.index
    current_sample = samples[current_index]
    query = current_sample["query"]
    texts = current_sample["texts"]

    st.title("Therapy Video Ranking")

    st.subheader(f"Sample {current_index + 1} of {len(samples)}")
    st.markdown(f"### Therapy: {query}")

    # Load saved ranking if any
    existing_ranking = st.session_state.rankings.get(current_index, ["", "", ""])

    # Create two columns: left for full list, right for ranking
    col1, col_spacer, col2 = st.columns([1.5, 0.1, 1])

    # Setup session state to track clicked item
    if "clicked_indexes" not in st.session_state:
        st.session_state.clicked_indexes = set()

    with col1:
        st.markdown("### YT videos")

        for i, (text, video) in enumerate(zip(texts, videos)):
            if st.button(f"{i+1}. {text}", key=f"toggle_{i}"):
                # Toggle logic: add if not present, remove if already present
                if i in st.session_state.clicked_indexes:
                    st.session_state.clicked_indexes.remove(i)
                else:
                    st.session_state.clicked_indexes.add(i)

            # Show video if this text is toggled on
            if i in st.session_state.clicked_indexes:
                st.video(video)
                st.markdown("---")


    with col2:
        st.markdown("#### Select Top 3 Relevant Videos")
        
        rank_1_val, rank_2_val, rank_3_val = existing_ranking[0], existing_ranking[1], existing_ranking[2]
        rank1_options = [""] + texts
        rank2_options = [""] + texts
        rank3_options = [""] + texts


        rank_1 = st.selectbox("🥇 Rank 1", rank1_options, index=get_index(rank1_options, rank_1_val), key="rank1")
        rank_2 = st.selectbox("🥈 Rank 2", rank2_options, index=get_index(rank2_options, rank_2_val), key="rank2")
        rank_3 = st.selectbox("🥉 Rank 3", rank3_options, index=get_index(rank3_options, rank_3_val), key="rank3")


        if st.button("⬅️ Previous", disabled=current_index == 0):
            _ = save_all_rankings()
            st.session_state.index -= 1
            st.rerun()
        
        if st.button("Clear Rankings"):
            st.session_state.rankings[current_index] = ["", "", ""]
            st.rerun()

        if st.button("Clear Videos"):
            st.session_state.clicked_indexes = set()
            st.rerun()

        if st.button("Next ➡️"):

            if "" in [rank_1, rank_2, rank_3]:
                st.write("Please fill in the rankings!")
            elif rank_1 in [rank_2, rank_3] or rank_2 == rank_3:
                st.write("Duplicate rankings!! Please correct.")
            else:
                _ = save_all_rankings()
                if st.session_state.index == len(samples)-1:
                    st.success('All samples done!', icon="✅")
                else:
                    st.session_state.index += 1
                    st.session_state.clicked_indexes = set()
                    st.rerun()
        
        st.download_button("Download Data", data=save_all_rankings(), file_name="rankings.json")



    # Save to session (optional)
    st.session_state.rankings[current_index] = [rank_1, rank_2, rank_3]

    # Save current ranking to session state
    st.session_state.rankings[current_index] = [rank_1, rank_2, rank_3]

    # Save function
    

    def save_current_ranking(index):
        os.makedirs("saved_data", exist_ok=True)
        data = {
            "query": samples[index]["query"],
            "ranked_texts": st.session_state.rankings.get(index, ["", "", ""])
        }
        file_path = f"saved_data/query_data.json"
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

    # Navigation
    #col_prev, col_next = st.columns(2)

    # Manual save
    #if st.button("✅ Save Ranking"):
    #    save_current_ranking(current_index)
    #    st.success("Ranking saved.")

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main("")    
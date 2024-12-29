import streamlit as st
import requests
import random
from datetime import datetime
from dotenv import load_dotenv
import os


# GitHub API setup
GITHUB_API_URL = "https://api.github.com"
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
TOKEN = st.secrets["general"]["api_key"]
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


st.set_page_config(page_title="GitHub Wrapped", layout="wide", page_icon="🎁")
st.subheader("📸 GitHub Wrapped 2024",anchor=None,divider= True)
st.markdown("""#### Let's see your GitHub journey!
👀 Ready to cringe at your "epic" GitHub stats? 😏 """)


username = st.text_input("Enter your GitHub username", placeholder="e.g., octocat")

st.divider()

# Styling for Polaroid cards with dynamic animations
def polaroid_card(title, value, roast=None):
    """
    Generate a Polaroid-style card layout.
    :param title: Title of the stat (e.g., 'Followers')
    :param value: Stat value (e.g., '120')
    :param roast: Optional funny roast to display
    """
    card_style = f"""
    <div class="card">
        <h3>{title}</h3>
        <p class="value">{value}</p>
        <p class="roast">{roast or ''}</p>
    </div>
    """
    return card_style


animations_css = """
<style>
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        width: 220px; 
        height: 325px; 
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        font-family: Arial, sans-serif;
        display: flex; 
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        transition: all 0.3s ease-in-out;
    }
    .card:hover {
        transform: scale(1.05);
        box-shadow: 0px 8px 12px rgba(0, 0, 0, 0.2);
    }
    .card h3 {
        margin: 5px;
        color: #444;
    }
    .card .value {
        font-size: 2em;
        font-weight: bold;
        margin: 5px;
        color: black; 
    }
    .card .roast {
        color: #888;
        font-size: 0.9em;
        margin: 5px;
        text-align: center; 
        word-wrap: break-word;
    }
</style>

"""
st.markdown(animations_css, unsafe_allow_html=True)


def create_dynamic_layout(card_data, cols_per_row=4):
    rows = [card_data[i:i + cols_per_row] for i in range(0, len(card_data), cols_per_row)]
    for row in rows:
        cols = st.columns(len(row))
        for i, (title, value, roast) in enumerate(row):
            with cols[i]:
                st.markdown(polaroid_card(title, value, roast), unsafe_allow_html=True)


if username:
    
    user_response = requests.get(f"{GITHUB_API_URL}/users/{username}", headers=HEADERS)
    repos_response = requests.get(f"{GITHUB_API_URL}/users/{username}/repos", headers=HEADERS)
    events_response = requests.get(f"{GITHUB_API_URL}/users/{username}/events", headers=HEADERS)

    if user_response.status_code == 200 and repos_response.status_code == 200 and events_response.status_code == 200:
        user_data = user_response.json()
        repos_data = repos_response.json()
        events_data = events_response.json()

        
        followers = user_data["followers"]
        following = user_data["following"]
        public_repos = user_data["public_repos"]

        
        current_year = 2024
        contributions_2024 = 0
        total_stars = 0
        repo_languages = {}
        total_commits = 0
        total_issues = 0
        total_prs = 0
        repo_contributions = {}

        
        contribution_types = [
            "PushEvent", "PullRequestEvent", "IssuesEvent", 
            "ForkEvent", "CreateEvent", "StarEvent", "WatchEvent"
        ]

        for event in events_data:
            event_date = datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            if event_date.year == current_year and event["type"] in contribution_types:
                contributions_2024 += 1

        for repo in repos_data:
            repo_name = repo["name"]
            repo_languages[repo["language"]] = repo_languages.get(repo["language"], 0) + 1
            total_stars += repo["stargazers_count"]

            
            commits_response = requests.get(f"{repo['url']}/commits?author={username}", headers=HEADERS)
            if commits_response.status_code == 200:
                for commit in commits_response.json():
                    commit_date = datetime.strptime(commit["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ")
                    if commit_date.year == current_year:
                        total_commits += 1

            
            issues_response = requests.get(f"{repo['url']}/issues", headers=HEADERS)
            if issues_response.status_code == 200:
                for issue in issues_response.json():
                    issue_date = datetime.strptime(issue["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                    if issue_date.year == current_year:
                        total_issues += 1

            
            prs_response = requests.get(f"{repo['url']}/pulls", headers=HEADERS)
            if prs_response.status_code == 200:
                for pr in prs_response.json():
                    pr_date = datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                    if pr_date.year == current_year:
                        total_prs += 1

            
            repo_contributions[repo_name] = total_commits + total_issues + total_prs

        
        most_active_repo = max(repo_contributions, key=repo_contributions.get)
        repo_activity = repo_contributions[most_active_repo]
        most_used_language = max(repo_languages, key=repo_languages.get)
        language_usage = repo_languages[most_used_language]

        
        active_month = datetime.now().strftime("%B")


        # Fun roasts based on stats
        roast_followers = random.choice([
            "You're a GitHub celebrity! 🌟",
            "Not many stalkers yet. 👀",
            "Looks like you're loved! ❤️"
        ]) if followers > 10 else "Time to gain some followers! 😅"

        roast_repos = random.choice([
            "Do you even sleep? 😴",
            "GitHub should start charging you rent for all those repos. 🏠",
            "Your repos are multiplying faster than rabbits! 🐇",
            "GitHub just called—they want a part of your repo empire. 👑"
        ]) if public_repos > 10 else random.choice([
            "How about creating a repo? 😅",
            "GitHub is lonely without your repositories. 🏚️",
            "Maybe it's time to actually create something? 💻",
            "You’ve got zero repos, but that’s okay. Maybe next year? 😜"
        ])

        roast_stars = random.choice([
            "Looks like you're a GitHub celebrity! 🌟",
            "Is your repo a new trend? 🔥",
            "GitHub just called—they want to make you an influencer. 🏆"
        ]) if total_stars > 50 else random.choice([
            "Hey, it's the thought that counts, right? 🤷‍♂️",
            "Maybe it's time to make your repos a little shinier? ✨",
            "Don't worry, not everyone is a GitHub rockstar. 😎"
        ])
        
        roast_contributions = random.choice([
            "Wow, someone's busy! 🏃‍♂️",
            "GitHub is lucky to have you this year! 🌟",
            "Are you secretly a bot? 🤖",
            "GitHub might give you a medal for the most contributions. 🏆"
        ]) if contributions_2024 > 150 else random.choice([
            "Are you sure you're using GitHub, or just stalking others? 🤔",
            "Your contribution graph is looking like a desert. 🏜️",
            "Looks like you went on a vacation for 2024. 😅",
            "Are you a ghost on GitHub?"
        ])
        
        roast_commits = random.choice([
            "Commitment issues? Not you! 🔥",
            "You're committing like a pro! 🚀",
            "Commit king/queen! Your keyboard must be tired. ⌨️",
            "Your commit history is hotter than my CPU right now. 🖥️💨"
        ]) if total_commits > 500 else random.choice([
            "What's this? A commit a month? 😴",
            "Are you writing code or just admiring your GitHub profile? 🤔",
            "Your commit history looks like a Wi-Fi signal. 📶",
            "Commits so sparse, even GitHub thinks you're on a break. 🏖️"
        ])
            
        roast_active_repo = random.choice([
            "Your repo is busier than Times Square on New Year's Eve! 🎉",
            "This repo should have its own fan club. 🌟",
            "You're treating this repo like it's your magnum opus. 🎨",
            "Repo on fire! 🔥 You might need a fire extinguisher. 🧯",
            "Your repo activity could rival a bustling startup. 🚀"
        ]) if repo_activity > 100 else random.choice([
            "Is this repo a museum? Because it's full of cobwebs. 🕸️",
            "Looks like this repo got lost in the void. 🕳️",
            "This repo is quieter than my notifications. 📵",
            "Are you planning to visit this repo anytime soon? 🗓️",
            "Repo so inactive, even GitHub forgot it exists. 😬"
        ])
            
        roast_language = random.choice([
            f"You and {most_used_language}? A match made in heaven. 💕",
            f"{most_used_language} is lucky to have you! 🥰",
            f"Living the dream with {most_used_language}, aren't you? 🌈",
            f"You've unlocked the true power of {most_used_language}. ⚡",
            f"{most_used_language} must be proud of all the code you're writing! 🎉"
        ]) if language_usage > 50 else random.choice([
            f"{most_used_language}? Are you sure that's your favorite? 🤔",
            f"{most_used_language} is probably wondering where you went. 🧐",
            f"{most_used_language} deserves better than this. 😢",
            f"Your {most_used_language} code is rare, like a unicorn. 🦄",
            f"{most_used_language} has seen better days with you. 💔"
        ])


        
        st.markdown(f"""
<h3 style='text-align: center;'>✨ GitHub Stats for {username} in 2024 ✨</h3>

<div style='text-align: center; margin-top: 20px;'>
<p>👀 So, you think you're a coding wizard, huh? Let's see how your stats stack up:</p>
</div>
""", unsafe_allow_html=True)

        
        card_data = [
            ("Followers", followers, roast_followers),
            ("Repositories", public_repos, roast_repos),
            ("Stars", total_stars, roast_stars),
            ("Contributions", contributions_2024, roast_contributions),
            ("Commits", total_commits, roast_commits),
            ("Most Used Language", most_used_language, roast_language),
            ("Most Active Repo", most_active_repo, roast_active_repo),
        ]

        
        create_dynamic_layout(card_data, cols_per_row=4)

    else:
        st.error("Could not fetch GitHub data. Please check your username.")
else:
    st.info("Enter a GitHub username to see your wrapped!")

# Google Analytics tracking script (replace 'UA-XXXXXXXX-X' with your tracking ID)
google_analytics_script = """
<script async src="https://www.googletagmanager.com/gtag/js?id=G-8BB4J1Z2TW"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-8BB4J1Z2TW');
</script>
"""

# Insert Google Analytics script into the app
st.components.v1.html(google_analytics_script, height=0)

st.divider()
st.markdown("Made with ❤️ by [Arvindh](https://github.com/Arvindh99)")

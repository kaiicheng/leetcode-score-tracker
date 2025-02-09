import requests
import re

GITHUB_README_PATH = "README.md"
LEETCODE_USERNAME = "kaiicheng"  # Your LeetCode username
BADGE_TEMPLATE = r"!\[LeetCode\]\(https:\/\/img\.shields\.io\/badge\/LeetCode-\d+-orange\?style=flat&logo=leetcode&logoColor=white\)"

def get_leetcode_score(username):
    url = f"https://leetcode.com/{username}/"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to fetch LeetCode profile page")
        return None
    
    match = re.search(r'"totalSolved":(\d+),', response.text)
    if match:
        return match.group(1)
    return None

def update_readme(score):
    with open(GITHUB_README_PATH, "r", encoding="utf-8") as file:
        content = file.read()

    new_badge = f"![LeetCode](https://img.shields.io/badge/LeetCode-{score}-orange?style=flat&logo=leetcode&logoColor=white)"

    if re.search(BADGE_TEMPLATE, content):
        content = re.sub(BADGE_TEMPLATE, new_badge, content)
    else:
        content += f"\n\n{new_badge}"

    with open(GITHUB_README_PATH, "w", encoding="utf-8") as file:
        file.write(content)

def main():
    score = get_leetcode_score(LEETCODE_USERNAME)
    if score:
        update_readme(score)
        print(f"Updated LeetCode score to {score}")
    else:
        print("Failed to fetch LeetCode score")

if __name__ == "__main__":
    main()
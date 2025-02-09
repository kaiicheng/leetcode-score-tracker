import re
import requests

GITHUB_README_PATH = "README.md"
LEETCODE_USERNAME = "kaiicheng"
BADGE_TEMPLATE = r"!\[LeetCode\]\(https:\/\/img\.shields\.io\/badge\/LeetCode-\d+(,\d+)?-orange\?style=flat&logo=leetcode&logoColor=white\)"

def get_leetcode_contest_rating(username):
    """
    Fetches the LeetCode contest rating using GraphQL API.

    Args:
        username (str): The LeetCode username.

    Returns:
        str or None: The contest rating as a string, or None if the request fails.
    """
    print("[INFO] Fetching LeetCode contest rating via GraphQL API...")

    # LeetCode GraphQL endpoint
    url = "https://leetcode.com/graphql"
    
    # GraphQL query payload to fetch contest rating
    query = {
        "query": """
        query getContestRanking($username: String!) {
            userContestRanking(username: $username) {
                rating
            }
        }
        """,
        "variables": {"username": username},
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }

    try:
        # Send POST request to the GraphQL API
        response = requests.post(url, json=query, headers=headers)
        print(f"[INFO] HTTP Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print("[ERROR] Failed to fetch data from LeetCode GraphQL API.")
            return None

        # Parse the JSON response to extract the contest rating
        data = response.json()
        rating = data.get("data", {}).get("userContestRanking", {}).get("rating")
        
        if rating is not None:
            print(f"[INFO] Contest rating found: {rating}")
            return str(round(rating))  # Round the rating to remove decimal places
        else:
            print("[ERROR] Contest rating not found in the API response.")
            return None
    except Exception as e:
        print(f"[ERROR] An exception occurred: {e}")
        return None

def update_readme(rating):
    """
    Updates the README file with the latest LeetCode contest rating badge.

    Args:
        rating (str): The latest LeetCode contest rating.
    """
    print("[INFO] Updating README.md file...")

    try:
        # Open and read the existing README.md file
        with open(GITHUB_README_PATH, "r", encoding="utf-8") as file:
            content = file.read()
            print("[INFO] Successfully read README.md.")

        # Create a new badge with the updated contest rating
        new_badge = f"![LeetCode](https://img.shields.io/badge/LeetCode-{rating}-orange?style=flat&logo=leetcode&logoColor=white)"

        # If the badge already exists, replace it with the updated badge
        if re.search(BADGE_TEMPLATE, content):
            content = re.sub(BADGE_TEMPLATE, new_badge, content)
            print("[INFO] Badge updated in README.md.")
        else:
            # If no badge exists, append the new badge to the README
            content += f"\n\n{new_badge}"
            print("[INFO] Badge added to README.md.")

        # Write the updated content back to the README.md file
        with open(GITHUB_README_PATH, "w", encoding="utf-8") as file:
            file.write(content)
            print("[INFO] Successfully updated README.md.")
    except Exception as e:
        print(f"[ERROR] An exception occurred while updating README.md: {e}")

def main():
    """
    Main function to fetch the LeetCode contest rating and update the README file.
    """
    print("[INFO] Starting script...")

    # Get the latest LeetCode contest rating
    rating = get_leetcode_contest_rating(LEETCODE_USERNAME)
    if rating:
        print(f"[INFO] Successfully fetched contest rating: {rating}")
        # Update the README if the contest rating is successfully fetched
        update_readme(rating)
        print(f"[INFO] Updated LeetCode contest rating to {rating}")
    else:
        print("[ERROR] Failed to fetch LeetCode contest rating.")

# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()

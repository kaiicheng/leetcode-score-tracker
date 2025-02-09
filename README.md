# leetcode-score-tracker

Program automatically update the LeetCode rating score.


![LeetCode](https://img.shields.io/badge/LeetCode-1724-orange?style=flat&logo=leetcode&logoColor=white)

## Overview
This repository contains a Python script and GitHub Actions workflow to fetch your LeetCode contest rating and display it in your GitHub repository as a badge. The workflow automatically updates the rating periodically or when manually triggered.



## How to Use

### Prerequisites
1. **Python 3.x**
   - Ensure you have Python 3.x installed on your local machine or runner.
2. **LeetCode Account**
   - A valid LeetCode username to fetch the contest rating.
3. **GitHub Personal Access Token (PAT)**
   - A token with `repo` permissions for pushing changes to your repository.

### Steps to Set Up

1. **Clone the Repository**
   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
   ```

2. **Install Dependencies**
   Install the required Python libraries.
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Script**
   Update the script `update_score.py` with your LeetCode username:
   ```python
   LEETCODE_USERNAME = "your-username"
   ```

4. **Test Locally**
   Run the script locally to verify it works as expected:
   ```bash
   python update_score.py
   ```

5. **Add Secrets to GitHub Repository**
   - Navigate to **Settings > Secrets and variables > Actions** in your repository.
   - Add the following secrets:
     - `GH_PAT`: Your GitHub Personal Access Token (with `repo` permissions).
     - `GITHUB_TOKEN`: Automatically provided by GitHub for Actions (no manual setup needed).

6. **Configure GitHub Actions Workflow**
   The provided workflow file `update.yml` is pre-configured to:
   - Run every 5 minutes (`*/5 * * * *`).
   - Update the `README.md` and generate a `badge.svg` file with your LeetCode rating.



## Workflow Details

### Example Workflow File (`update.yml`)
```yaml
name: Update LeetCode Score

on:
  schedule:
    - cron: "*/5 * * * *" # Run every 5 minutes
  workflow_dispatch:

permissions:
  contents: write # Allow writing to the repository

jobs:
  update-readme:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python3 -m pip install --upgrade pip setuptools wheel
        python3 -m pip install requests pyyaml

    - name: Update LeetCode score
      run: |
        python3 update_score.py
      env:
        GH_PAT: ${{ secrets.GH_PAT }}
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    - name: Commit changes
      run: |
        git config --global user.name "github-actions[bot]"
        git config --global user.email "github-actions[bot]@users.noreply.github.com"
        git add README.md badge.svg
        git commit -m "Auto update LeetCode score" || true
        git push https://x-access-token:${{ secrets.GH_PAT }}@github.com/<your-username>/<your-repo>.git main
```

## Troubleshooting

### Common Issues

#### **403 Error: Permission Denied**
- **Cause**: Missing or incorrect permissions for `GH_PAT`.
- **Solution**:
  1. Ensure `GH_PAT` has `repo` permissions.
  2. Add `GH_PAT` to **Settings > Secrets and variables > Actions**.

#### **Branch Protection Rules**
- **Cause**: `main` branch is protected.
- **Solution**:
  - Temporarily disable branch protection rules.
  - Alternatively, modify the workflow to create a Pull Request instead of directly pushing changes:
    ```yaml
    - name: Create Pull Request
      uses: peter-evans/create-pull-request@v5
      with:
        commit-message: "Auto update LeetCode score"
        branch: auto-update-branch
        title: "Auto update LeetCode score"
    ```

#### **Token Not Working**
- **Cause**: Incorrect token configuration.
- **Solution**:
  - Regenerate a Personal Access Token with `repo` permissions.
  - Update the `GH_PAT` secret in your repository.

#### **Badge or README Not Updating**
- **Cause**: Files not added to the commit.
- **Solution**:
  - Ensure `git add README.md badge.svg` is included in the workflow.


## Additional Notes

- **Testing Locally**:
  Before deploying the workflow, run the script locally to ensure correct behavior.
- **Custom Badge Design**:
  You can customize the badge by editing the `generate_svg` function in `update_score.py`.
- **Documentation Contributions**:
  Feel free to contribute improvements to this guide or the repository by opening a Pull Request.

---

This guide provides everything you need to fetch your LeetCode rating and automate updates using GitHub Actions. Happy coding!


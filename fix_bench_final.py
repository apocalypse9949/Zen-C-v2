with open(".github/workflows/bench.yml", "r") as f:
    content = f.read()

# I will just write a python script that completely rewrites the workflow file safely based on the original.
import subprocess
subprocess.run(["git", "checkout", "main", ".github/workflows/bench.yml"])

with open(".github/workflows/bench.yml", "r") as f:
    content = f.read()

old_step = """    - name: Ensure benchmark branch exists
      if: github.ref == 'refs/heads/main'
      run: |
        git config user.name "github-actions[bot]"
        git config user.email "github-actions[bot]@users.noreply.github.com"
        # Try to fetch gh-pages; if it doesn't exist on remote, create it locally as an orphan
        git fetch origin gh-pages || git checkout --orphan gh-pages
        git checkout main"""

# We just remove the branch fetch entirely for PRs. The if condition says refs/heads/main, so it only runs on main.
# WAIT! The fetch error in CI said:
# command git failed with args '-c user.name=... fetch origin gh-pages:gh-pages'
# The error came from line 21, which means it was INSIDE `benchmark-action/github-action-benchmark@v1` !!
# Oh, the error was inside the ACTION, not my manual step!
# Look at the annotation: "Message: Command 'git' failed with args '... switch gh-pages': fatal: invalid reference: gh-pages"
# Ah! The previous error was: "fetch origin gh-pages:gh-pages" failing.
# Then I added "skip-fetch-gh-pages: true".
# Then the next CI run failed with "switch gh-pages".
# So the action is STILL trying to switch to gh-pages and failing because the branch doesn't exist locally!

# This means if skip-fetch-gh-pages: true is set, the action assumes the branch exists locally, so it does `git switch gh-pages` and fails!

# So we MUST ensure the branch exists locally!
# That means we SHOULD keep the "Ensure benchmark branch exists" step, and just modify it to NOT fail on fetch.
# Or, if it's a PR, skip everything benchmark related?
# The action itself has `auto-push: ${{ github.ref == 'refs/heads/main' }}`. So it only pushes on main.
# But it still tries to switch to gh-pages on PRs to run the threshold check against the previous run!

# Let's fix the Ensure branch step to gracefully create the branch if fetch fails.
new_step = """    - name: Ensure benchmark branch exists
      run: |
        git config user.name "github-actions[bot]"
        git config user.email "github-actions[bot]@users.noreply.github.com"
        git fetch origin gh-pages:gh-pages || git branch gh-pages || git checkout --orphan gh-pages || true
        git checkout main"""

content = content.replace(old_step, new_step)

if "skip-fetch-gh-pages: true" not in content:
    content = content.replace("fail-on-alert: true", "fail-on-alert: true\n        skip-fetch-gh-pages: true")

with open(".github/workflows/bench.yml", "w") as f:
    f.write(content)

# Pushing to GitHub

## One-time setup

1. **Create a new repo on GitHub** (github.com → New repository). Do **not** add a README or .gitignore (you already have them).

2. **Add the remote and push** (replace `YOUR_USERNAME` and `YOUR_REPO` with your repo):

   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

---

## Option A: Push to main and keep working (simplest)

- Work as usual, then when you want to save to GitHub:
  ```bash
  git add .
  git commit -m "Describe your changes"
  git push
  ```

---

## Option B: Use a branch + Pull Request (PR)

Good if you want `main` to stay “clean” and merge changes via PR.

1. **Create and switch to a dev branch:**
   ```bash
   git checkout -b dev
   ```

2. **Push the branch:**
   ```bash
   git push -u origin dev
   ```

3. **Day-to-day work:** Edit code on `dev`, then:
   ```bash
   git add .
   git commit -m "Describe your changes"
   git push
   ```

4. **When you want to update main:** On GitHub, open your repo → you’ll see “dev had recent pushes” → click **Compare & pull request** → create the PR, then **Merge**. After that, optionally update local main:
   ```bash
   git checkout main
   git pull
   git checkout dev
   git merge main
   ```

You’re now set to push; use Option A for a simple workflow or Option B for branch + PR.

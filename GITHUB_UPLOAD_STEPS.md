# 📤 How to Upload Project to GitHub

## Step-by-Step Guide

### Step 1: Initialize Git Repository (if not already done)

Open PowerShell in your project folder and run:

```powershell
cd C:\Users\harsh\OneDrive\Desktop\ahoum
git init
```

### Step 2: Add All Files to Git

```powershell
git add .
```

This will add all files (except those in .gitignore)

### Step 3: Make Your First Commit

```powershell
git commit -m "Initial commit: Events Platform with Django backend and React frontend"
```

### Step 4: Create GitHub Repository

1. Go to https://github.com and sign in
2. Click the **"+"** icon in the top right corner
3. Click **"New repository"**
4. Fill in:
   - **Repository name**: `events-platform` (or any name you like)
   - **Description**: "Full-stack events management platform with Django and React"
   - **Visibility**: Choose Public or Private
   - **DO NOT** check "Initialize with README" (we already have one)
   - **DO NOT** add .gitignore or license (we already have them)
5. Click **"Create repository"**

### Step 5: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```powershell
# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/events-platform.git

# Rename default branch to main (if needed)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

### Step 6: Enter GitHub Credentials

When you push, you'll be asked for:
- **Username**: Your GitHub username
- **Password**: Use a Personal Access Token (not your GitHub password)

**To create a Personal Access Token:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name and select scope: `repo`
4. Click "Generate token"
5. Copy the token and use it as your password

### Alternative: Using GitHub CLI (Easier)

If you have GitHub CLI installed:

```powershell
# Install GitHub CLI first (if not installed)
# Download from: https://cli.github.com/

# Login to GitHub
gh auth login

# Create and push repository
gh repo create events-platform --public --source=. --remote=origin --push
```

## ✅ After Uploading

1. **Verify**: Go to your GitHub repository page and check that all files are there
2. **Update README**: The README.md should already be visible on the repository homepage
3. **Add Topics**: Click on repository → About → Add topics like: `django`, `react`, `events-platform`, `fullstack`

## 📝 Important Notes

### Files NOT Uploaded (by .gitignore):
- `.env` file (contains secrets - should NEVER be uploaded)
- `venv/` folder (Python virtual environment)
- `node_modules/` folder (npm dependencies)
- `db.sqlite3` (database file)
- `__pycache__/` folders (Python cache)

### Files Uploaded:
- ✅ All source code
- ✅ README.md
- ✅ requirements.txt
- ✅ package.json
- ✅ All configuration files (except .env)

## 🔄 Future Updates

When you make changes, use these commands:

```powershell
# Check what changed
git status

# Add changed files
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push
```

## 🆘 Troubleshooting

### If you get "remote origin already exists":
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

### If you get authentication errors:
- Make sure you're using Personal Access Token, not password
- Or use SSH keys instead of HTTPS

### If you want to use SSH (optional):
```powershell
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add SSH key to GitHub: Settings → SSH and GPG keys → New SSH key
# Then use SSH URL:
git remote set-url origin git@github.com:YOUR_USERNAME/REPO_NAME.git
```


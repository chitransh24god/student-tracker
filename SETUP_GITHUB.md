# GitHub Setup Guide

## Step-by-Step Instructions

### 1. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `student-tracker` (or your preferred name)
3. Description: `Student Attendance & Engagement Tracker - Streamlit App`
4. Choose **Public** (so Streamlit Cloud can deploy it)
5. Click "Create repository"

### 2. Initialize Local Git Repository

```bash
cd d:\Downloads\python cec

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Student Tracker Streamlit app"
```

### 3. Add Remote and Push

Replace `yourusername` with your GitHub username:

```bash
# Add remote repository
git remote add origin https://github.com/yourusername/student-tracker.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### 4. Verify on GitHub

1. Go to https://github.com/yourusername/student-tracker
2. You should see all your files

---

## Quick Commands

### Push after making changes:
```bash
git add .
git commit -m "Description of changes"
git push
```

### Check status:
```bash
git status
```

### View commit history:
```bash
git log --oneline
```

### Update local files from remote:
```bash
git pull
```

---

## Deploy to Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Sign in with GitHub account
3. Click "New app"
4. Select:
   - Repository: `yourusername/student-tracker`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
5. Click "Deploy"

Your app will be live at: `https://yourusername-student-tracker.streamlit.app`

---

## GitHub Authentication (First Time Only)

If prompted for authentication:

### Using HTTPS with Personal Access Token:
```bash
git remote set-url origin https://yourusername:your_token@github.com/yourusername/student-tracker.git
```

[Create token here](https://github.com/settings/tokens)

### Or use SSH:
```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add to GitHub: https://github.com/settings/ssh/new

# Use SSH URL
git remote set-url origin git@github.com:yourusername/student-tracker.git
```

---

## File Structure in GitHub

```
student-tracker/
├── streamlit_app.py              # Streamlit app
├── models.py                     # Database models
├── generate_data.py              # Generate test data
├── requirements_streamlit.txt    # Dependencies
├── attendance.db                 # SQLite database (ignore in git)
├── README_STREAMLIT.md           # Documentation
├── SETUP_GITHUB.md              # This file
├── .gitignore                   # Files to ignore
└── [other files]
```

---

## Tips

✅ **Always pull before pushing** to avoid conflicts:
```bash
git pull
git add .
git commit -m "Your message"
git push
```

✅ **Use meaningful commit messages**:
- ❌ Bad: "update"
- ✅ Good: "Add user authentication for students"

✅ **Commit frequently** with small, logical changes

✅ **.gitignore** prevents large files from being uploaded:
- `venv/` - Virtual environment
- `*.db` - Large database files
- `__pycache__/` - Python cache

---

## Troubleshooting

### "fatal: not a git repository"
```bash
git init
```

### "failed to push"
```bash
# Pull first
git pull origin main

# Then push
git push origin main
```

### "filename too long" (Windows)
```bash
git config --global core.longpaths true
```

---

## Next Steps

1. Set up GitHub repository (follow steps above)
2. Push code to GitHub
3. Deploy to Streamlit Cloud
4. Share your app URL!

**Your app will be live and accessible to anyone with the link!**

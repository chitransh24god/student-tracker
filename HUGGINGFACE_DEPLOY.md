# Deploy to Hugging Face Spaces

## What is Hugging Face Spaces?

Hugging Face Spaces is a **free hosting platform** specifically designed for machine learning and data applications. It's perfect for Streamlit apps because:

✅ **Completely Free** - No credit card required, no trial limits  
✅ **Built for Streamlit** - Official Streamlit support  
✅ **Auto-Deploy from GitHub** - Push code → app updates automatically  
✅ **Always Available** - No sleep/cold start delays like other free platforms  
✅ **Permanent Storage** - Supports SQLite databases  

## Deployment Steps

### Step 1: Create a Hugging Face Account
1. Go to **https://huggingface.co**
2. Click **"Sign Up"** (or log in if you already have an account)
3. Complete email verification

### Step 2: Create a New Space
1. Click your profile icon (top right)
2. Select **"New Space"**
3. Or go directly to: **https://huggingface.co/new-space**

### Step 3: Configure Your Space
- **Space name**: `student-tracker` (or any name you prefer)
- **License**: Select any (e.g., "MIT" or "Other")
- **Space SDK**: Select **"Streamlit"**
- **Visibility**: Choose "Public" or "Private"
- Click **"Create Space"**

### Step 4: Connect Your GitHub Repository
1. In the space, go to **"Settings"** (top menu)
2. Scroll to **"Repository Contents"**
3. Select **"Connect a Repository"**
4. Choose **"github"**
5. Select: **`chitransh24god/student-tracker`**
6. Branch: **`main`**
7. Click **"Connect"**

### Step 5: Wait for Deployment
The app will automatically:
1. Clone your repository
2. Install dependencies from `requirements.txt`
3. Run `streamlit run streamlit_app.py`
4. Be live within 2-3 minutes

### Done! 🎉

Your app is now live at:
```
https://huggingface.co/spaces/YOUR_USERNAME/student-tracker
```

## What Auto-Updates Your App?

Every time you push to GitHub:
```bash
git add .
git commit -m "Update app"
git push origin main
```

The space automatically pulls the latest code and redeploys within 2-3 minutes.

## Important Files

- ✅ `streamlit_app.py` - Your main app
- ✅ `requirements.txt` - Dependencies (already configured)
- ✅ `.streamlit/config.toml` - Settings (already set up)
- ✅ `attendance.db` - Database (auto-created)

## Troubleshooting

### App shows "No Space found"
- Wait 5 minutes for first deployment
- Refresh the page

### "ModuleNotFoundError"
- Check `requirements.txt` has all needed packages
- Push changes to GitHub
- Space auto-redeploys

### App won't load
- Check **"Logs"** tab in space settings
- Look for error messages
- Update `requirements.txt` and push again

### Database issues
- The database persists between restarts
- First run auto-initializes with sample data
- Check `attendance.db` is in your repo (or will be created)

## Free Tier Limits

- CPU: 2x shared
- RAM: 16GB (plenty for Streamlit)
- Disk: Persistent storage for SQLite
- Uptime: 99% (basically always available)

**No storage limits, no bandwidth limits, no payment ever needed.**

## Next Steps

1. **Push your latest code** to GitHub
2. **Go to Hugging Face** and create a Space
3. **Connect your GitHub repo**
4. **Wait 2-3 minutes**
5. **Share your app URL!**

---

## Quick Links

- Hugging Face: https://huggingface.co
- My Spaces: https://huggingface.co/spaces/YOUR_USERNAME
- Streamlit Docs: https://docs.streamlit.io
- Support: https://discuss.huggingface.co

**That's it! No more payments, no configuration headaches. Just push your code and it works!** 🚀

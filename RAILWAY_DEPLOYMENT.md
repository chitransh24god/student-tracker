# Railway.app Deployment Guide for Student Tracker

## What is Railway.app?
Railway is a modern cloud platform that makes deploying web apps simple. It's perfect for Streamlit apps and provides:
- ✅ Free tier with $5/month credit
- ✅ Automatic GitHub integration
- ✅ Python 3.11 support (compatible with all packages)
- ✅ Simple, fast deployment

## Deployment Steps

### Step 1: Connect GitHub to Railway
1. Go to **https://railway.app**
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub"**
4. Authorize Railway to access your GitHub account
5. Select your `student-tracker` repository

### Step 2: Railway Auto-Detection
Railway will automatically detect:
- ✅ `Procfile` (how to run your app)
- ✅ `requirements.txt` (Python dependencies)
- ✅ `runtime.txt` (Python 3.11)

### Step 3: Configure Environment Variables (Optional)
If your app uses any environment variables (database connections, API keys), add them in Railway:
1. Go to your project in Railway dashboard
2. Click "Variables"
3. Add any needed environment variables

### Step 4: Deploy
1. Click **"Deploy"**
2. Railway will build and deploy automatically
3. Get your app URL from the Railway dashboard
4. Your app will be live!

## Files Created for Railway

- **`Procfile`** - Tells Railway how to start your Streamlit app
- **`runtime.txt`** - Specifies Python 3.11 (compatible with all packages)
- **`.streamlit/config.toml`** - Streamlit settings optimized for Railway
- **`requirements.txt`** - Minimal, tested dependencies

## What to Push to GitHub

```bash
cd "d:\path\to\student-tracker"
git add Procfile runtime.txt requirements.txt .streamlit/
git commit -m "Add Railway deployment configuration"
git push origin main
```

Railway will automatically detect the changes and redeploy!

## Troubleshooting

### If Deploy Fails:
1. Check Railway dashboard logs (Deployments → View Logs)
2. Most common issue: missing `requirements.txt` packages
3. Solution: Update `requirements.txt` and push to GitHub

### If App is Slow to Load:
- First load takes 30-60s on free tier (normal)
- Subsequent loads are faster

### If App Goes Offline:
- Free tier auto-sleeps if no traffic for 15 mins
- Just visit the URL again to wake it up

## Application URL
Once deployed, your app will be at: `https://student-tracker-[random-id].railway.app`

## Cost
- Free tier: $5/month credit (usually enough for hobby projects)
- Pay-as-you-go after that (~$0.000116/hour for basic compute)

## Next Steps
1. Push these files to your GitHub repository
2. Go to railway.app
3. Connect your GitHub repo
4. Click Deploy
5. Wait 2-3 minutes
6. Your app is live! 🚀

---

**Questions?** Visit https://docs.railway.app

# Deployment Guide - Solar Fish Dryer ML System

This guide explains how to deploy your Solar Fish Dryer ML System online so it's accessible from anywhere.

## 🎯 Deployment Options

### Option 1: Render.com (Recommended - Easiest)
- ✅ FREE tier available
- ✅ Automatic deployments from GitHub
- ✅ Built-in HTTPS
- ✅ Can host both backend and frontend
- ✅ No credit card required

### Option 2: Backend on Render + Frontend on Vercel
- ✅ Both have FREE tiers
- ✅ Fastest frontend performance (Vercel)
- ✅ Automatic deployments
- ✅ Best for production apps

### Option 3: Railway.app
- ✅ FREE $5/month credit
- ✅ Very easy deployment
- ✅ Great developer experience

---

## 🚀 Option 1: Deploy Everything on Render.com (Simplest)

### Step 1: Prepare Your Repository

1. **Push your code to GitHub** (if not already done):
```bash
# If you haven't set up GitHub yet
git remote add origin https://github.com/YOUR_USERNAME/model-regression.git
git branch -M main
git push -u origin main
```

### Step 2: Sign Up for Render.com

1. Go to [https://render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended)
4. Authorize Render to access your repositories

### Step 3: Deploy Backend

1. **Click "New +" → "Web Service"**

2. **Connect your repository:**
   - Find `model-regression` in the list
   - Click "Connect"

3. **Configure the service:**
   ```
   Name: solar-fish-dryer-backend
   Region: Choose closest to you
   Branch: main (or claude/solar-fish-dryer-predictor-...)
   Root Directory: (leave blank)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn --bind 0.0.0.0:$PORT backend:app
   ```

4. **Choose plan:**
   - Select "Free" plan
   - Click "Create Web Service"

5. **Wait for deployment** (5-10 minutes first time)
   - You'll see logs showing:
     - Installing packages
     - Training ML models
     - Server starting

6. **Copy your backend URL:**
   - Will look like: `https://solar-fish-dryer-backend.onrender.com`
   - **Save this URL!** You'll need it for the frontend

### Step 4: Test Backend

Visit these URLs in your browser (replace with your actual URL):

```
https://solar-fish-dryer-backend.onrender.com/api/health
```

Should return:
```json
{
  "status": "healthy",
  "models_trained": true
}
```

**✅ Backend is deployed!**

### Step 5: Deploy Frontend (Option A - Using Claude.ai)

**Easiest method:**

1. Copy the contents of `frontend-production.jsx`

2. Edit line to add your backend URL:
```javascript
const API_URL = 'https://solar-fish-dryer-backend.onrender.com/api';
```

3. Paste into Claude.ai conversation
4. Claude will render it as an interactive artifact
5. **Share the artifact URL** with others!

**That's it! Your app is live!**

### Step 5: Deploy Frontend (Option B - Using Render Static Site)

1. **Create a simple React app structure:**

First, create these files in your repository:

**package.json:**
```json
{
  "name": "solar-fish-dryer-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "recharts": "^2.5.0",
    "lucide-react": "^0.263.1"
  },
  "scripts": {
    "build": "echo 'Frontend build complete'"
  }
}
```

**public/index.html:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solar Fish Dryer ML System</title>
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <style>
        body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; }
    </style>
</head>
<body>
    <div id="root"></div>
    <script>
        // API URL - REPLACE WITH YOUR RENDER BACKEND URL
        const API_URL = 'https://solar-fish-dryer-backend.onrender.com/api';
    </script>
    <script src="/app.js"></script>
</body>
</html>
```

2. **Deploy as Static Site on Render:**
   - New + → Static Site
   - Connect repository
   - Build command: `echo "Static site"`
   - Publish directory: `public`

---

## 🚀 Option 2: Backend on Render + Frontend on Vercel (Best Performance)

### Part A: Deploy Backend on Render

Follow **Option 1, Steps 1-4** above to deploy backend.

Copy your backend URL: `https://your-app.onrender.com`

### Part B: Deploy Frontend on Vercel

1. **Sign up for Vercel:**
   - Go to [https://vercel.com](https://vercel.com)
   - Sign up with GitHub

2. **Prepare Frontend for Vercel:**

Create these files in your repo:

**vercel.json:**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "public/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/public/$1"
    }
  ],
  "env": {
    "REACT_APP_API_URL": "https://your-backend-url.onrender.com/api"
  }
}
```

3. **Deploy to Vercel:**
   - Click "Add New..." → "Project"
   - Import your repository
   - Configure:
     - Framework Preset: Other
     - Build Command: (leave empty)
     - Output Directory: public
   - Add Environment Variable:
     - Name: `REACT_APP_API_URL`
     - Value: `https://your-backend-url.onrender.com/api`
   - Click "Deploy"

4. **Your frontend is live!**
   - URL: `https://your-project.vercel.app`

---

## 🚀 Option 3: Railway.app (Easiest for beginners)

### Step 1: Deploy Backend

1. **Sign up:**
   - Go to [https://railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create new project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure:**
   - Railway auto-detects Python
   - Add environment variables:
     - `PORT`: (auto-set by Railway)
     - `FLASK_ENV`: production

4. **Deploy:**
   - Click "Deploy"
   - Wait 5-10 minutes
   - Copy your URL: `https://your-app.up.railway.app`

5. **Test:** Visit `https://your-app.up.railway.app/api/health`

### Step 2: Use Frontend with Claude.ai

Use the same Claude.ai method from Option 1!

---

## 🧪 Testing Your Deployed App

### Test Backend Endpoints

```bash
# Health check
curl https://your-backend-url.com/api/health

# Get metrics
curl https://your-backend-url.com/api/metrics

# Make prediction
curl -X POST https://your-backend-url.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 32,
    "humidity": 55,
    "solar_radiation": 850,
    "wind_speed": 3.2,
    "initial_moisture": 78,
    "fish_thickness": 2.0
  }'
```

### Test Frontend

1. Open your frontend URL
2. Check backend connection status (should be green)
3. Click "Train Models" (if needed)
4. Adjust sliders
5. Click "Predict Drying Rate"
6. Verify results appear

---

## 🔧 Environment Variables

### Backend Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `PORT` | (auto-set) | Port number (Render/Railway set automatically) |
| `FLASK_ENV` | production | Enables production mode |
| `PYTHON_VERSION` | 3.11.0 | Python version to use |

### Frontend Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `REACT_APP_API_URL` | https://your-backend.com/api | Backend API URL |

---

## ⚡ Important: Free Tier Limitations

### Render.com Free Tier
- ✅ 750 hours/month (enough for one app)
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ First request after spin-down takes 30-60 seconds
- ✅ Automatic HTTPS
- ✅ 100GB bandwidth/month

**Fix for spin-down:**
- Use a monitoring service like [UptimeRobot](https://uptimerobot.com) (free)
- Pings your app every 5 minutes to keep it awake

### Vercel Free Tier
- ✅ Unlimited websites
- ✅ 100GB bandwidth/month
- ✅ Always on (no spin-down)
- ✅ Super fast CDN

### Railway Free Tier
- ✅ $5 credit/month
- ✅ ~500 hours of runtime
- ⚠️ Spins down after inactivity
- ✅ Easy to use

---

## 🐛 Troubleshooting Deployment

### Backend Issues

**Problem: "Application Error" or 503**
- Check build logs in Render dashboard
- Verify all packages in requirements.txt install successfully
- Check Python version matches (3.11)

**Problem: Models not training on startup**
- Check logs for errors
- Verify numpy/scikit-learn installed correctly
- May need more memory (upgrade from free tier)

**Problem: CORS errors in browser**
- Verify flask-cors is installed
- Check CORS configuration in backend.py
- Ensure frontend uses correct backend URL

### Frontend Issues

**Problem: "Backend Disconnected"**
- Check backend URL is correct
- Verify backend is running: visit `/api/health`
- Check browser console for errors

**Problem: Blank page**
- Check browser console for JavaScript errors
- Verify all React libraries loaded
- Check index.html structure

### Performance Issues

**Problem: First request very slow**
- Normal for Render free tier after spin-down
- Wait 30-60 seconds for wake-up
- Use UptimeRobot to keep app awake

**Problem: Predictions timing out**
- Increase gunicorn timeout in Procfile:
  ```
  web: gunicorn --timeout 120 --bind 0.0.0.0:$PORT backend:app
  ```

---

## 📊 Monitoring Your Deployment

### Check Backend Health

Set up monitoring with [UptimeRobot](https://uptimerobot.com):

1. Sign up (free)
2. Add monitor:
   - Type: HTTP(s)
   - URL: `https://your-backend.com/api/health`
   - Interval: 5 minutes
3. Get alerts if app goes down

### View Logs

**Render.com:**
- Dashboard → Your service → Logs tab
- Real-time logs of all requests and errors

**Railway.app:**
- Project → Deployments → View Logs
- Real-time streaming logs

**Vercel:**
- Project → Deployments → Function Logs
- Request logs and errors

---

## 🔄 Updating Your Deployment

### Automatic Updates (Recommended)

Both Render and Vercel support automatic deployments:

1. **Push code to GitHub:**
```bash
git add .
git commit -m "Updated ML models"
git push
```

2. **Automatic redeployment:**
   - Render/Railway detect the push
   - Automatically rebuild and redeploy
   - Takes 2-5 minutes

3. **Verify update:**
   - Check deployment logs
   - Test the new features

### Manual Updates

**Render.com:**
- Dashboard → Your service → Manual Deploy → Deploy latest commit

**Railway.app:**
- Project → Deployments → Redeploy

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid Plans | Best For |
|----------|-----------|------------|----------|
| **Render** | 750 hrs/mo | $7/month | Full-stack apps |
| **Vercel** | Unlimited | $20/month | Frontend hosting |
| **Railway** | $5 credit/mo | $5/month | Quick deploys |
| **Heroku** | $0 (removed) | $7/month | Legacy apps |

**Recommended combo (100% FREE):**
- Backend: Render.com (Free)
- Frontend: Vercel or Claude.ai artifact
- Monitoring: UptimeRobot (Free)

**Total cost: $0/month** 🎉

---

## 🎓 Next Steps After Deployment

1. **Share your app:**
   - Send the frontend URL to colleagues
   - Embed in your website
   - Add to your portfolio

2. **Collect real data:**
   - Follow DATA_COLLECTION_GUIDE.md
   - Upload via the web interface
   - Retrain models with your data

3. **Monitor usage:**
   - Set up UptimeRobot
   - Check logs regularly
   - Monitor API usage

4. **Improve the app:**
   - Add authentication (if needed)
   - Store user data
   - Add more features
   - Optimize performance

---

## 📝 Quick Deployment Checklist

### Before Deployment
- [ ] Code pushed to GitHub
- [ ] `requirements.txt` includes `gunicorn`
- [ ] Backend tested locally
- [ ] Frontend tested locally

### Backend Deployment
- [ ] Sign up for hosting platform
- [ ] Create new web service
- [ ] Connect GitHub repository
- [ ] Configure build/start commands
- [ ] Set environment variables
- [ ] Deploy and test `/api/health`
- [ ] Copy backend URL

### Frontend Deployment
- [ ] Update API URL in frontend code
- [ ] Choose deployment method
- [ ] Deploy frontend
- [ ] Test full application
- [ ] Verify predictions work

### Post-Deployment
- [ ] Set up monitoring
- [ ] Share app URL
- [ ] Document for team
- [ ] Plan for updates

---

## 🆘 Need Help?

**Render.com Support:**
- Docs: https://render.com/docs
- Community: https://community.render.com

**Vercel Support:**
- Docs: https://vercel.com/docs
- Community: https://github.com/vercel/vercel/discussions

**Railway Support:**
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway

**General Issues:**
- Check logs first
- Test locally
- Verify environment variables
- Check CORS settings
- Ensure backend URL is correct

---

## 🎉 Success!

Once deployed, your Solar Fish Dryer ML System will be accessible from anywhere in the world! Share the URL and start predicting drying rates online!

**Your deployed app URLs:**
- Backend API: `https://your-backend.onrender.com`
- Frontend: `https://your-frontend.vercel.app` or Claude.ai artifact
- Health Check: `https://your-backend.onrender.com/api/health`

Happy predicting! 🐟☀️

# Frontend Deployment Guide

Quick guide to deploy the Solar Fish Dryer React frontend online.

## 🎯 Three Options

### Option 1: Render.com Static Site (Easiest!)

**Perfect if you already have your backend on Render**

1. **Update Backend URL** in `public/index.html` (line 70):
   ```javascript
   const API_URL = 'https://YOUR-BACKEND-URL.onrender.com/api';
   ```

2. **Deploy to Render:**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Static Site"
   - Connect your repository
   - Configure:
     - **Name**: `solar-fish-dryer-frontend`
     - **Build Command**: `echo "Static site"`
     - **Publish Directory**: `public`
   - Click "Create Static Site"

3. **Done!** Your app will be live at:
   ```
   https://solar-fish-dryer-frontend.onrender.com
   ```

---

### Option 2: Vercel (Best Performance - FREE!)

**Fastest option with global CDN**

1. **Update Backend URL** in `public/index.html` (line 70):
   ```javascript
   const API_URL = 'https://YOUR-BACKEND-URL.onrender.com/api';
   ```

2. **Deploy to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub
   - Click "Add New..." → "Project"
   - Import your repository
   - Vercel auto-detects configuration
   - Click "Deploy"

3. **Done!** Your app will be live at:
   ```
   https://your-project.vercel.app
   ```

---

### Option 3: Netlify (Alternative)

1. **Update Backend URL** in `public/index.html`

2. **Deploy to Netlify:**
   - Go to [netlify.com](https://netlify.com)
   - Drag & drop the `public` folder
   - Or connect GitHub repository

3. **Done!** Your app will be live at:
   ```
   https://your-site.netlify.app
   ```

---

## 🔧 Important: Update Backend URL

**BEFORE deploying**, edit `public/index.html` line 70:

```javascript
// Replace this:
const API_URL = 'https://solar-fish-dryer-backend.onrender.com/api';

// With YOUR actual backend URL:
const API_URL = 'https://YOUR-ACTUAL-BACKEND.onrender.com/api';
```

To find your backend URL:
1. Go to your Render dashboard
2. Click on your backend service
3. Copy the URL (e.g., `https://solar-fish-dryer-backend.onrender.com`)
4. Add `/api` at the end

---

## 🧪 Test Locally First

```bash
# Serve the frontend locally
cd public
python -m http.server 8080

# Open browser to:
http://localhost:8080
```

Make sure:
- ✅ Backend status shows "Connected"
- ✅ Models status shows "Trained"
- ✅ Can make predictions

---

## 📝 Deployment Checklist

- [ ] Backend deployed and working
- [ ] Backend URL copied
- [ ] Updated `public/index.html` line 70 with backend URL
- [ ] Tested locally with `python -m http.server`
- [ ] Committed changes to GitHub
- [ ] Deployed frontend to Render/Vercel/Netlify
- [ ] Visited frontend URL in browser
- [ ] Confirmed backend connection
- [ ] Made test prediction

---

## 🎨 Customization

### Change Title
Edit `public/index.html` line 6:
```html
<title>Your Custom Title</title>
```

### Change Colors
The app uses Tailwind CSS. Common color classes:
- `bg-blue-500` → Background blue
- `text-green-800` → Text green
- `from-blue-50 to-orange-50` → Gradient

### Add Logo
Add your logo image to `public/` folder and update line 12:
```html
<img src="/your-logo.png" alt="Logo" className="w-10 h-10" />
```

---

## 🚀 Auto-Deploy (Recommended)

Set up automatic deployments so every push to GitHub redeploys:

**Render:**
- Already auto-deploys from GitHub
- Every push triggers new deployment

**Vercel:**
- Already auto-deploys from GitHub
- Every push triggers new deployment
- Fastest deployment (~30 seconds)

**Netlify:**
- Settings → Build & Deploy → Continuous Deployment
- Enable auto-deploy from GitHub

---

## 🔍 Troubleshooting

### "Backend Disconnected"

**Check 1: Is backend URL correct?**
```javascript
// In index.html, verify this matches your actual backend:
const API_URL = 'https://your-actual-backend.onrender.com/api';
```

**Check 2: Is backend running?**
Visit: `https://your-backend.onrender.com/api/health`

Should return:
```json
{
  "status": "healthy",
  "models_trained": true
}
```

**Check 3: CORS enabled?**
Backend should have `flask-cors` enabled (already included in backend.py)

### "Models Not Trained"

**Solution:** Click the "Train / Retrain Models" button in the web interface.

Wait 10-30 seconds for training to complete.

### Blank Page

**Check browser console** (F12 → Console):
- Look for JavaScript errors
- Check if external libraries loaded (React, Recharts)
- Verify backend URL is accessible

### Charts Not Showing

**This is expected** - charts only appear AFTER you make a prediction!

1. Adjust input sliders
2. Click "Predict Drying Rate"
3. Charts will appear with results

---

## 💰 Cost

All three options are **100% FREE**:

| Platform | Free Tier | Build Time | Performance |
|----------|-----------|------------|-------------|
| **Render** | Unlimited static sites | ~30 sec | Good |
| **Vercel** | Unlimited | ~20 sec | Excellent (CDN) |
| **Netlify** | Unlimited | ~40 sec | Good (CDN) |

**Recommended:** Vercel (fastest deployment + best performance)

---

## 🎉 Success!

Once deployed, you'll have:
- ✅ Professional ML web app
- ✅ Accessible from anywhere
- ✅ Shareable URL
- ✅ Auto-deploys on updates
- ✅ 100% FREE hosting!

Share your URL with colleagues, add to your portfolio, or use for your fish drying business!

---

## 📚 Next Steps

1. **Collect real data** - Follow DATA_COLLECTION_GUIDE.md
2. **Upload your data** - Use the CSV upload button in the app
3. **Retrain models** - Click "Train / Retrain Models"
4. **Get accurate predictions** - Specific to YOUR solar dryer!

---

## 🆘 Need Help?

- Frontend issues: Check browser console (F12)
- Backend issues: Check Render logs
- CORS errors: Verify flask-cors in requirements.txt
- 404 errors: Check publish directory is set to `public`

**Still stuck?** The issue is usually the backend URL in `index.html` line 70!

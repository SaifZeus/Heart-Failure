# 🚀 Deployment Guide - Heart Failure Prediction Dashboard

This guide provides step-by-step instructions for deploying your Streamlit dashboard.

## 📋 Pre-Deployment Checklist

- [ ] All dependencies installed locally and tested
- [ ] Application runs successfully with `streamlit run app.py`
- [ ] Input validation works correctly
- [ ] All visualizations render properly
- [ ] No errors in the console

## 🌐 Deployment Options

### Option 1: Streamlit Community Cloud (Recommended - FREE)

**Why Streamlit Cloud?**
- ✅ Free hosting for public apps
- ✅ One-click deployment from GitHub
- ✅ Automatic SSL certificate
- ✅ Easy updates via git push
- ✅ Built-in monitoring

**Steps:**

1. **Prepare Your Repository**
   ```bash
   # Initialize git (if not already)
   git init
   
   # Add files
   git add app.py requirements.txt README.md .gitignore
   
   # Commit
   git commit -m "Initial commit: Heart Failure Prediction Dashboard"
   
   # Create GitHub repository and push
   git remote add origin https://github.com/yourusername/heart-failure-dashboard.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your GitHub repository
   - Choose `app.py` as the main file
   - Click "Deploy"
   
3. **Your app will be live at:**
   ```
   https://yourusername-heart-failure-dashboard-app-xxxxx.streamlit.app
   ```

**Custom Domain (Optional):**
- Go to App Settings → General → Custom subdomain
- Set your custom URL

---

### Option 2: Heroku

**Prerequisites:**
- Heroku account (free tier available)
- Heroku CLI installed

**Steps:**

1. **Create Additional Files**

   Create `Procfile`:
   ```
   web: sh setup.sh && streamlit run app.py
   ```

   Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/

   echo "\
   [general]\n\
   email = \"your-email@domain.com\"\n\
   " > ~/.streamlit/credentials.toml

   echo "\
   [server]\n\
   headless = true\n\
   enableCORS=false\n\
   port = $PORT\n\
   " > ~/.streamlit/config.toml
   ```

2. **Deploy**
   ```bash
   # Login to Heroku
   heroku login
   
   # Create app
   heroku create your-app-name
   
   # Deploy
   git push heroku main
   
   # Open app
   heroku open
   ```

**Cost:** Free tier available, scales with usage

---

### Option 3: Google Cloud Run

**Why Cloud Run?**
- Pay only for what you use
- Automatic scaling
- Container-based deployment

**Steps:**

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8080

   CMD streamlit run app.py --server.port=8080 --server.address=0.0.0.0
   ```

2. **Deploy**
   ```bash
   # Build and deploy
   gcloud run deploy heart-failure-app \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

**Cost:** ~$0 for low traffic (free tier: 2M requests/month)

---

### Option 4: AWS EC2

**Steps:**

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t2.micro (free tier eligible)
   - Open port 8501 in security group

2. **Setup**
   ```bash
   # SSH into instance
   ssh -i your-key.pem ubuntu@your-instance-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and pip
   sudo apt install python3-pip -y
   
   # Clone repository
   git clone https://github.com/yourusername/heart-failure-dashboard.git
   cd heart-failure-dashboard
   
   # Install dependencies
   pip3 install -r requirements.txt
   
   # Run with nohup (runs in background)
   nohup streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &
   ```

3. **Setup Domain (Optional)**
   - Point your domain to EC2 IP
   - Setup Nginx as reverse proxy
   - Install SSL with Let's Encrypt

**Cost:** ~$0-5/month (free tier for first year)

---

### Option 5: Docker + Any Cloud

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build and Run:**
```bash
# Build
docker build -t heart-failure-app .

# Run locally
docker run -p 8501:8501 heart-failure-app

# Push to Docker Hub
docker tag heart-failure-app yourusername/heart-failure-app
docker push yourusername/heart-failure-app
```

**Deploy to:**
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform

---

## 🔒 Security Best Practices

### Environment Variables

For sensitive data, use environment variables:

1. **Create `.streamlit/secrets.toml`** (local only)
   ```toml
   [api_keys]
   model_key = "your-secret-key"
   ```

2. **Access in code:**
   ```python
   import streamlit as st
   api_key = st.secrets["api_keys"]["model_key"]
   ```

3. **On Streamlit Cloud:**
   - Go to App Settings → Secrets
   - Add your secrets in TOML format

### Rate Limiting

Add rate limiting for production:
```python
import streamlit as st
from datetime import datetime, timedelta

if 'last_prediction' not in st.session_state:
    st.session_state.last_prediction = None

def check_rate_limit():
    if st.session_state.last_prediction:
        time_diff = datetime.now() - st.session_state.last_prediction
        if time_diff < timedelta(seconds=5):
            return False
    return True

# Before prediction
if check_rate_limit():
    # Make prediction
    st.session_state.last_prediction = datetime.now()
else:
    st.warning("Please wait before making another prediction.")
```

---

## 📊 Monitoring & Analytics

### Streamlit Cloud Analytics
- View app metrics in Streamlit Cloud dashboard
- Monitor usage, errors, and performance

### Google Analytics (Optional)

Add to your app:
```python
import streamlit.components.v1 as components

# Google Analytics tracking
ga_code = """
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
"""
components.html(ga_code, height=0)
```

---

## 🔧 Performance Optimization

### 1. Caching
Already implemented with `@st.cache_resource` for model loading

### 2. Lazy Loading
```python
# Load heavy libraries only when needed
if predict_button:
    import heavy_library
```

### 3. Compression
Enable gzip in config:
```toml
# .streamlit/config.toml
[server]
enableXsrfProtection = true
enableCORS = false
enableStaticServing = true
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** App won't start
```bash
# Solution: Check logs
streamlit run app.py --logger.level=debug
```

**Issue:** Memory errors
```bash
# Solution: Increase container memory or optimize data loading
# Use smaller datasets or implement pagination
```

**Issue:** Slow predictions
```bash
# Solution: 
# 1. Use lighter model
# 2. Implement model caching
# 3. Use GPU if available
```

### Debugging in Production

Add logging:
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Your code
    logger.info("Prediction successful")
except Exception as e:
    logger.error(f"Error: {e}")
    st.error("An error occurred. Please try again.")
```

---

## 📈 Scaling Considerations

### For High Traffic

1. **Use a CDN** for static assets
2. **Implement caching** at multiple levels
3. **Consider load balancing** with multiple instances
4. **Use a database** instead of in-memory storage
5. **Optimize model size** (quantization, pruning)

### Cost Optimization

| Platform | Free Tier | Best For |
|----------|-----------|----------|
| Streamlit Cloud | Unlimited | Personal projects, demos |
| Heroku | 550 hrs/month | Small apps, testing |
| Google Cloud Run | 2M requests/month | Production apps |
| AWS EC2 | 750 hrs/month (1 year) | Full control needed |

---

## ✅ Post-Deployment Checklist

- [ ] App loads without errors
- [ ] All features work as expected
- [ ] Mobile responsiveness verified
- [ ] SSL certificate active (HTTPS)
- [ ] Analytics configured
- [ ] Monitoring set up
- [ ] Backup strategy in place
- [ ] Documentation updated
- [ ] Custom domain configured (if applicable)

---

## 📞 Support Resources

- **Streamlit Docs:** https://docs.streamlit.io
- **Streamlit Forum:** https://discuss.streamlit.io
- **Heroku Docs:** https://devcenter.heroku.com
- **Google Cloud Docs:** https://cloud.google.com/run/docs

---

**Need Help?** Open an issue in the GitHub repository or consult the Streamlit community forum.

**Happy Deploying! 🚀**

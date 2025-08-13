# Deployment Guide

This guide will help you deploy the Learning Platform to various hosting services.

## Prerequisites

- Git repository with your code
- Account on your chosen hosting platform
- Basic understanding of web deployment

## Option 1: Render (Recommended for Beginners)

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub account
3. Verify your email

### Step 2: Connect Repository
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select the repository containing your learning platform

### Step 3: Configure Service
- **Name**: `learning-platform` (or your preferred name)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Plan**: Free (or paid for more resources)

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait for build to complete (5-10 minutes)
3. Your app will be available at `https://your-app-name.onrender.com`

## Option 2: Vercel

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Deploy
```bash
# In your project directory
vercel
```

### Step 3: Follow Prompts
- Link to existing project: No
- Project name: learning-platform
- Directory: ./
- Override settings: No

### Step 4: Access Your App
Your app will be deployed to `https://your-app-name.vercel.app`

## Option 3: Heroku

### Step 1: Install Heroku CLI
Download from [heroku.com](https://heroku.com)

### Step 2: Login and Create App
```bash
heroku login
heroku create your-app-name
```

### Step 3: Deploy
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Step 4: Open App
```bash
heroku open
```

## Option 4: Railway

### Step 1: Create Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub

### Step 2: Deploy
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository
4. Railway will auto-detect Python and deploy

## Environment Variables

For production, set these environment variables:

```bash
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=your-database-url
```

## Database Setup

### SQLite (Default)
- Works out of the box
- Good for small to medium applications
- No additional setup required

### PostgreSQL (Recommended for Production)
1. Add `psycopg2-binary` to requirements.txt
2. Set `DATABASE_URL` environment variable
3. Update database connection in app.py

## SSL/HTTPS

Most platforms provide SSL certificates automatically:
- Render: Automatic HTTPS
- Vercel: Automatic HTTPS
- Heroku: Automatic HTTPS
- Railway: Automatic HTTPS

## Custom Domain

### Render
1. Go to your service settings
2. Click "Custom Domains"
3. Add your domain
4. Update DNS records

### Vercel
1. Go to project settings
2. Click "Domains"
3. Add your domain
4. Update DNS records

## Monitoring and Logs

### Render
- View logs in the dashboard
- Set up alerts for errors
- Monitor performance metrics

### Vercel
- View function logs
- Monitor analytics
- Set up error tracking

### Heroku
```bash
heroku logs --tail
heroku addons:create papertrail
```

## Performance Optimization

1. **Enable Caching**
   - Static files caching
   - Database query caching

2. **Database Optimization**
   - Add indexes for frequently queried fields
   - Use connection pooling

3. **Static Files**
   - Use CDN for static assets
   - Compress images and CSS

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check requirements.txt
   - Verify Python version
   - Check for syntax errors

2. **App Won't Start**
   - Check start command
   - Verify port configuration
   - Check environment variables

3. **Database Errors**
   - Verify database URL
   - Check database permissions
   - Ensure tables are created

### Debug Commands

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Test locally
python app.py

# Check logs
heroku logs --tail  # Heroku
vercel logs         # Vercel
```

## Security Checklist

- [ ] Set strong SECRET_KEY
- [ ] Enable HTTPS
- [ ] Set up proper CORS
- [ ] Validate user inputs
- [ ] Use environment variables for secrets
- [ ] Regular security updates

## Backup Strategy

1. **Database Backup**
   - Regular automated backups
   - Store backups securely
   - Test restore procedures

2. **Code Backup**
   - Use Git for version control
   - Regular commits and pushes
   - Multiple deployment environments

## Cost Optimization

1. **Free Tiers**
   - Render: Free tier available
   - Vercel: Generous free tier
   - Heroku: Free tier discontinued
   - Railway: Free tier available

2. **Scaling**
   - Start with free tiers
   - Monitor usage
   - Upgrade only when needed

## Support Resources

- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [Heroku Documentation](https://devcenter.heroku.com)
- [Railway Documentation](https://docs.railway.app)

---

**Need Help?** Check the platform-specific documentation or contact support. 
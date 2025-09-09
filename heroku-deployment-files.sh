#!/bin/bash

# =============================================
# SIMPLE HEROKU DEPLOYMENT FOR MIT PROJECT
# =============================================

echo "🚀 MIT Fraud Detection - Heroku Deployment"
echo "=========================================="
echo ""

# Step 1: Create all necessary files
echo "📝 Creating deployment files..."

# Create requirements.txt
cat > requirements.txt << 'EOF'
flask==2.3.2
flask-cors==4.0.0
gunicorn==21.2.0
openai==0.28.0
EOF

echo "✅ requirements.txt created"

# Create Procfile
cat > Procfile << 'EOF'
web: gunicorn app:app
EOF

echo "✅ Procfile created"

# Create runtime.txt
cat > runtime.txt << 'EOF'
python-3.11.6
EOF

echo "✅ runtime.txt created"

# Create .gitignore
cat > .gitignore << 'EOF'
*.pyc
__pycache__/
venv/
.env
.DS_Store
EOF

echo "✅ .gitignore created"

# Step 2: Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo ""
    echo "⚠️  Heroku CLI not found. Installing..."
    echo ""
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew tap heroku/brew && brew install heroku
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl https://cli-assets.heroku.com/install.sh | sh
    else
        # Windows (Git Bash)
        echo "Please download Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi
fi

echo ""
echo "📦 All files created! Now let's deploy to Heroku"
echo ""

# Step 3: Initialize Git repository
if [ ! -d .git ]; then
    echo "Initializing Git repository..."
    git init
fi

# Step 4: Login to Heroku
echo "🔐 Please login to Heroku..."
heroku login

# Step 5: Create Heroku app
echo ""
read -p "Enter a name for your Heroku app (or press Enter for random name): " app_name

if [ -z "$app_name" ]; then
    heroku create
else
    heroku create $app_name
fi

# Step 6: Set environment variables
echo ""
echo "🔑 Setting up API keys..."
echo ""
echo "You have 2 options for the LLM:"
echo "1) Use OpenAI (requires API key - costs money but works great)"
echo "2) Skip LLM setup (agents will use simple responses)"
echo ""
read -p "Enter choice (1-2): " llm_choice

if [ "$llm_choice" == "1" ]; then
    read -p "Enter your OpenAI API key: " openai_key
    heroku config:set OPENAI_API_KEY=$openai_key
    echo "✅ OpenAI configured"
else
    heroku config:set OPENAI_API_KEY=your-api-key-here
    echo "✅ Using fallback responses (no LLM)"
fi

# Step 7: Deploy to Heroku
echo ""
echo "🚀 Deploying to Heroku..."
echo ""

# Add files to git
git add .
git commit -m "Initial deployment of MIT Fraud Detection System"

# Push to Heroku
git push heroku main || git push heroku master

# Step 8: Open the app
echo ""
echo "✅ Deployment complete!"
echo ""
echo "Opening your app..."
heroku open

echo ""
echo "=========================================="
echo "🎉 SUCCESS! Your app is live!"
echo ""
echo "What you can do now:"
echo "  • View logs: heroku logs --tail"
echo "  • Change API key: heroku config:set OPENAI_API_KEY=new-key"
echo "  • Scale app: heroku ps:scale web=1"
echo "  • Add database: heroku addons:create heroku-postgresql:hobby-dev"
echo ""
echo "For your MIT presentation:"
echo "  • Share the Heroku URL with your professors"
echo "  • The app will stay live for free (550 hours/month)"
echo "  • You can update anytime with: git push heroku main"
echo ""
echo "=========================================="
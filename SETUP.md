# Monit Patient - Complete Setup Guide

## 🎯 Overview
This guide will help you set up and run the complete Monit Patient system end-to-end.

## 📋 Prerequisites

### Required Software
- Python 3.9 or higher
- Node.js 18 or higher
- npm or yarn

### API Keys Required
1. **Google Gemini API Key** (get from Google AI Studio)
2. **Confluent Cloud** account and credentials (for Kafka streaming)
3. **ElevenLabs API Key** (for voice interface)

## 🚀 Quick Start

### Step 1: Clone and Navigate
```bash
git clone <your-repo>
cd Monit_Patient
```

### Step 2: Backend Setup

#### 2.1 Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 2.2 Configure Environment Variables
```bash
# The .env file is already created with placeholder values
# Edit it with your actual API keys:
nano .env

# Required keys to update:
# - GEMINI_API_KEY
# - CONFLUENT_BOOTSTRAP_SERVERS
# - CONFLUENT_API_KEY
# - CONFLUENT_API_SECRET
# - ELEVENLABS_API_KEY
```

#### 2.3 Generate Demo Data
```bash
python scripts/generate_demo_data.py
```

#### 2.4 Start Backend Server
```bash
python main.py
```

Backend will start at: `http://localhost:8000`

API Documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Step 3: Frontend Setup

#### 3.1 Install Dependencies
```bash
cd frontend
npm install
```

#### 3.2 Configure Frontend Environment
The frontend `.env` is already configured to point to `http://localhost:8000`

#### 3.3 Start Frontend Dev Server
```bash
npm run dev
```

Frontend will start at: `http://localhost:5173`

## 🔑 Default Login Credentials
- **Username**: `admin`
- **Password**: `admin`

## 🧪 Testing the System End-to-End

### 1. Login
- Open browser to `http://localhost:5173`
- Login with admin/admin

### 2. View Patient Dashboard
- You should see 3 demo patients
- Each patient has vitals data and risk scores

### 3. Configure Agents (Admin Panel)
Navigate to Admin Panel:

#### Row 1: Orchestrator (Manager)
- Already configured with Gemini model
- Select model from dropdown (8 models available)

#### Row 2: Super Agents (Team Leads)
- Click "Add Team Lead" to add new super agents
- Select model for each (Gemini 2.0, 1.5, etc.)
- Each must have ≥2 staff members

#### Row 3: Utility Agents (Staff)
- Click "Add Staff" to add utility agents
- Select model from dropdown
- Select task from dropdown:
  - Compare with External Research
  - Compare with Internal Research
  - Study Internal Patient Data
  - Study Individual Data for Personal Care
  - Study Medical Guidelines
  - Predict Patient Deterioration

#### Connection Matrix
- Click checkboxes to connect Team Leads with Staff
- Green = connected, Gray = not connected
- **Validation**: Each Team Lead must have at least 2 Staff

#### Save Configuration
- Click "Save Configuration" button
- System validates and saves

### 4. Chat with AI
- Navigate to Chat page
- Select language (English, Hindi, Bengali)
- Ask questions like:
  - "What is patient P001's risk level?"
  - "Should I be worried about patient P002?"
  - "Analyze patient P003's vitals"

### 5. View Patient Details
- Click on any patient card in dashboard
- View detailed vitals, risk score, concerns
- Click "Chat with AI about this patient"

## 🔧 Available Gemini Models

The system now supports **8 Gemini models**:

1. **gemini-2.0-flash-exp** - Gemini 2.0 Flash (Experimental) ⚡ Fast
2. **gemini-2.0-flash-thinking-exp-1219** - Gemini 2.0 Flash Thinking 🧠 Advanced
3. **gemini-exp-1206** - Gemini Experimental 1206 🔬 Advanced
4. **gemini-1.5-pro-002** - Gemini 1.5 Pro (Latest) 📊 Standard
5. **gemini-1.5-pro** - Gemini 1.5 Pro 📊 Standard
6. **gemini-1.5-flash-002** - Gemini 1.5 Flash (Latest) ⚡ Fast
7. **gemini-1.5-flash** - Gemini 1.5 Flash ⚡ Fast
8. **gemini-1.5-flash-8b** - Gemini 1.5 Flash 8B ⚡ Fast

You can select different models for:
- Orchestrator (Manager)
- Super Agents (Team Leads)
- Utility Agents (Staff)

## 📊 Project Structure Verification

### Backend Files (59 files)
```
backend/
├── agents/          ✓ Multi-agent system
├── api/routes/      ✓ FastAPI endpoints
├── core/            ✓ Config, security, database
├── services/        ✓ Business logic
├── streaming/       ✓ Kafka components
├── models/          ✓ Data models
├── schemas/         ✓ API schemas
├── utils/           ✓ Utilities
└── tests/           ✓ Test suite
```

### Frontend Files (46 files)
```
frontend/
├── src/
│   ├── components/  ✓ React components
│   ├── pages/       ✓ Page components
│   ├── hooks/       ✓ Custom hooks
│   ├── services/    ✓ API services
│   ├── store/       ✓ State management
│   ├── types/       ✓ TypeScript types
│   └── styles/      ✓ Tailwind CSS
└── public/          ✓ Static assets
```

### Data Files
```
data/
├── patients/        ✓ Patient records CSV
├── vitals/          ✓ Vitals history CSV
├── guidelines/      ✓ Medical guidelines CSV
├── research/        ✓ Research papers CSV
└── agents/          ✓ Agent configs CSV
```

## 🐛 Troubleshooting

### Backend Issues

**Import Error: No module named 'X'**
```bash
pip install -r requirements.txt
```

**Port 8000 already in use**
```bash
# Change BACKEND_PORT in .env
BACKEND_PORT=8001
```

**Database errors**
```bash
# Regenerate demo data
python scripts/generate_demo_data.py
```

### Frontend Issues

**Dependencies not installed**
```bash
cd frontend
npm install
```

**API connection errors**
- Ensure backend is running on port 8000
- Check VITE_API_BASE_URL in frontend/.env

**Build errors**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 🔍 Verifying Imports

All imports have been verified:
- ✓ Backend imports use absolute paths (backend.*)
- ✓ Frontend imports use relative paths (./*)
- ✓ All __init__.py files present
- ✓ No circular imports
- ✓ Path aliases configured in vite.config.ts

## 📡 Real-Time Streaming (Optional)

To enable real-time Kafka streaming:

1. Set up Confluent Cloud account
2. Create topics:
   - patient-vitals-stream
   - patient-alerts-stream
   - agent-logs-stream
3. Update .env with Confluent credentials
4. Set ENABLE_REAL_TIME_STREAMING=true

## 🎤 Voice Interface (Optional)

To enable voice interface:

1. Get ElevenLabs API key
2. Update ELEVENLABS_API_KEY in .env
3. Set ENABLE_VOICE_INTERFACE=true
4. Voice chat will be available in Chat page

## ✅ System Health Check

Visit these endpoints to verify:
- `http://localhost:8000/` - API root (should return status)
- `http://localhost:8000/health` - Health check
- `http://localhost:8000/docs` - API documentation
- `http://localhost:5173/` - Frontend application

## 🎯 Success Criteria

Your system is working correctly if:
- ✓ Backend starts without errors
- ✓ Frontend loads and shows login page
- ✓ You can login with admin/admin
- ✓ Dashboard shows 3 demo patients
- ✓ Admin panel shows agent configuration UI
- ✓ You can add/remove agents
- ✓ Connection matrix works
- ✓ Chat interface responds (when API keys configured)
- ✓ Patient details display correctly

## 🚀 Ready for Production

For production deployment:
1. Update all API keys in .env
2. Change ADMIN_PASSWORD to strong password
3. Update SECRET_KEY to random 32+ character string
4. Set ENABLE_DEBUG_MODE=false
5. Configure proper database (PostgreSQL)
6. Set up SSL/TLS certificates
7. Configure production CORS_ORIGINS
8. Deploy with Docker (see docker-compose.yml)

## 📞 Support

If you encounter issues:
1. Check this SETUP.md guide
2. Review logs in ./logs/app.log
3. Check browser console for frontend errors
4. Verify all API keys are correct
5. Ensure all dependencies are installed

---

**Monit Patient** - "Predict the future where uncertainty is the enemy" 🏥

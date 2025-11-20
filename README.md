# Monit Patient

**"Predict the future where uncertainty is the enemy"**

AI-powered real-time patient monitoring system that predicts critical health deterioration before it happens, giving healthcare providers crucial time to intervene.

## 🎯 Overview

**Monit Patient** combines **Confluent Cloud's real-time data streaming**, **Google Gemini's advanced AI capabilities**, and **ElevenLabs' multilingual voice interface** to create an intelligent guardian system for ICU patients.

### Key Features

- **Multi-Agent AI System**: Hierarchical agent architecture with Orchestrator (Manager), Super Agents (Team Leads), and Utility Agents (Staff)
- **Real-Time Streaming**: Confluent Kafka for continuous vital signs monitoring
- **Voice Interface**: ElevenLabs-powered multilingual chat (English, Hindi, Bengali, etc.)
- **Predictive Analytics**: Early warning detection for sepsis, cardiac events, respiratory failure
- **Admin Configuration**: Drag-and-drop agent hierarchy builder
- **Google Grounding Search**: Integration with medical research databases

## 🏗️ Architecture

### Agent Hierarchy

```
Orchestrator Agent (Manager)
├── Super Agent 1 (Medical Analysis Team)
│   ├── Utility Agent: Patient Data Analyst
│   └── Utility Agent: Individual Care Specialist
└── Super Agent 2 (Research Team)
    ├── Utility Agent: External Research Analyst
    └── Utility Agent: Guidelines Specialist
```

### Data Flow

```
ICU Monitor → Kafka Producer → Confluent Cloud
                                       ↓
                              Kafka Consumer
                                       ↓
                              Stream Processor
                                       ↓
                         [Anomaly Detection]
                                       ↓
                              Agent System
                                       ↓
                         Alerts + Notifications
                                       ↓
                              WebSocket
                                       ↓
                            Frontend Dashboard
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+ (for frontend)
- Confluent Cloud account
- Google Cloud account (Gemini API)
- ElevenLabs API key

### Installation

1. **Clone repository**
```bash
git clone <repository-url>
cd Monit_Patient
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys and credentials
```

4. **Generate demo data**
```bash
python scripts/generate_demo_data.py
```

5. **Run backend server**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📋 API Endpoints

### Agent Management

- `POST /api/agents/configure` - Configure agent hierarchy
- `GET /api/agents/configuration` - Get current configuration
- `POST /api/agents/query` - Query agent system
- `GET /api/agents/available-models` - List available models
- `GET /api/agents/available-tasks` - List available tasks
- `GET /api/agents/status` - Get agent system status

### Patient Management

- `GET /api/patients/` - Get all patients
- `GET /api/patients/{patient_id}` - Get specific patient
- `POST /api/patients/` - Create new patient
- `GET /api/patients/{patient_id}/vitals` - Get patient vitals
- `POST /api/patients/vitals` - Add vital signs
- `GET /api/patients/{patient_id}/risk-score` - Calculate risk score

### Chat & Voice

- `POST /api/chat/text` - Text-based chat
- `POST /api/chat/voice` - Voice-based chat
- `POST /api/chat/text-to-speech` - Convert text to speech
- `GET /api/chat/voices` - Get available voices

### Alerts

- `GET /api/alerts/` - Get active alerts
- `POST /api/alerts/{alert_id}/acknowledge` - Acknowledge alert
- `POST /api/alerts/{alert_id}/resolve` - Resolve alert

## 🔧 Configuration

### Agent Configuration Example

```json
{
  "config_name": "Hospital ICU Configuration",
  "orchestrator": {
    "agent_id": "orch-001",
    "name": "Main Orchestrator",
    "agent_type": "orchestrator",
    "model": "gemini-2.0-flash-exp"
  },
  "super_agents": [
    {
      "agent_id": "super-001",
      "name": "Medical Analysis Team",
      "agent_type": "super",
      "model": "gemini-2.0-flash-exp"
    }
  ],
  "utility_agents": [
    {
      "agent_id": "util-001",
      "name": "Patient Data Analyst",
      "agent_type": "utility",
      "model": "gemini-2.0-flash-exp",
      "task": "study_patient_data"
    },
    {
      "agent_id": "util-002",
      "name": "External Research Analyst",
      "agent_type": "utility",
      "model": "gemini-2.0-flash-exp",
      "task": "compare_external_research"
    }
  ],
  "connections": {
    "super-001": ["util-001", "util-002"]
  }
}
```

### Available Utility Agent Tasks

1. **compare_external_research** - Search medical research using Google grounding
2. **compare_internal_research** - Query hospital's internal database
3. **study_patient_data** - Analyze patterns across patients
4. **study_individual_data** - Deep dive into single patient
5. **study_medical_guidelines** - Reference clinical guidelines
6. **predict_deterioration** - Predictive analytics for patient decline

## 📊 Project Structure

```
Monit_Patient/
├── backend/
│   ├── agents/            # Multi-agent system
│   ├── api/               # FastAPI routes
│   ├── core/              # Configuration, security, database
│   ├── services/          # Business logic
│   ├── models/            # Data models
│   ├── schemas/           # API schemas
│   ├── streaming/         # Kafka components
│   └── utils/             # Utilities
├── data/                  # CSV database
├── scripts/               # Utility scripts
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
└── .env.example           # Environment template
```

## 🧪 Testing

Run tests:
```bash
pytest backend/tests/
```

## 🐳 Docker Deployment

```bash
docker-compose up -d
```

## 🤝 Contributing

This is a hackathon project. Contributions welcome!

## 📝 License

MIT License - see LICENSE file

## 🏆 Hackathon Challenges

This project integrates:
- ✅ **Confluent Cloud** - Real-time patient vitals streaming
- ✅ **Google Gemini** - Multi-agent AI system with grounding search
- ✅ **ElevenLabs** - Multilingual voice interface

## 📞 Support

For questions or issues, please open a GitHub issue.

---

Built with ❤️ for saving lives through AI-powered predictive healthcare.

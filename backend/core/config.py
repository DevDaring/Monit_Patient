"""Configuration management using pydantic-settings."""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Google Cloud & Gemini
    GOOGLE_APPLICATION_CREDENTIALS: str = "./service-account-key.json"
    GOOGLE_PROJECT_ID: str = "your-gcp-project-id"
    GOOGLE_CLOUD_REGION: str = "us-central1"
    GEMINI_API_KEY: str = "your-gemini-api-key-here"
    GEMINI_MODEL_NAME: str = "gemini-2.0-flash-exp"
    GEMINI_MAX_TOKENS: int = 8192
    GEMINI_TEMPERATURE: float = 0.7

    # Confluent Cloud (Kafka)
    CONFLUENT_BOOTSTRAP_SERVERS: str = "pkc-xxxxx.us-east-1.aws.confluent.cloud:9092"
    CONFLUENT_API_KEY: str = "your-confluent-api-key"
    CONFLUENT_API_SECRET: str = "your-confluent-api-secret"
    CONFLUENT_CLUSTER_ID: str = "lkc-xxxxx"
    KAFKA_TOPIC_PATIENT_VITALS: str = "patient-vitals-stream"
    KAFKA_TOPIC_ALERTS: str = "patient-alerts-stream"
    KAFKA_TOPIC_AGENT_LOGS: str = "agent-logs-stream"
    KAFKA_CONSUMER_GROUP: str = "monit-patient-consumer-group"

    # ElevenLabs Voice
    ELEVENLABS_API_KEY: str = "your-elevenlabs-api-key"
    ELEVENLABS_VOICE_ID: str = "21m00Tcm4TlvDq8ikWAM"
    ELEVENLABS_MODEL: str = "eleven_multilingual_v2"
    ELEVENLABS_STABILITY: float = 0.5
    ELEVENLABS_SIMILARITY_BOOST: float = 0.75

    # Database (CSV)
    USE_CSV_DATABASE: bool = True
    CSV_PATIENT_DATA_PATH: str = "./data/patients/patient_records.csv"
    CSV_VITALS_DATA_PATH: str = "./data/vitals/vitals_history.csv"
    CSV_MEDICAL_GUIDELINES_PATH: str = "./data/guidelines/medical_guidelines.csv"

    # FastAPI Backend
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    BACKEND_RELOAD: bool = True
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # Agent Configuration
    MAX_ORCHESTRATOR_AGENTS: int = 1
    MAX_SUPER_AGENTS: int = 3
    MAX_UTILITY_AGENTS: int = 6
    AGENT_TIMEOUT_SECONDS: int = 30
    AGENT_MAX_RETRIES: int = 3

    # Alert System
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "your-email@gmail.com"
    SMTP_PASSWORD: str = "your-app-specific-password"
    ALERT_EMAIL_FROM: str = "alerts@monitpatient.com"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""

    # Logging & Monitoring
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "./logs/app.log"
    ENABLE_DEBUG_MODE: bool = False

    # Security
    SECRET_KEY: str = "your-secret-key-min-32-chars-long-random-string"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 1440
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "change-this-password"

    # Feature Flags
    ENABLE_REAL_TIME_STREAMING: bool = True
    ENABLE_VOICE_INTERFACE: bool = True
    ENABLE_MULTI_AGENT_SYSTEM: bool = True
    ENABLE_EMAIL_ALERTS: bool = True

    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS_ORIGINS string to list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

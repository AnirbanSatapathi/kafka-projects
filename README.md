# Scalable Clickstream Ingestion Pipeline
A high-throughput, fault-tolerant distributed system for ingesting, buffering, and persisting real-time user clickstream events. This project decouples data reception from processing using Kafka, ensuring high availability and protecting the database from traffic spikes.![licensed-image](https://github.com/user-attachments/assets/fa0f6a32-a0c2-481f-940f-2841a861bc6a)
**🚀 Architecture**
The system is split between a Local Client (Producer/Worker) and a Remote Server (Infrastructure).

Ingestion API (FastAPI): Acts as the "Front Door". Validates incoming JSON events and pushes them to Kafka immediately (Async).

Message Broker (Kafka KRaft): Buffers events. Decouples the API from the Database.

Stream Worker (Python): Consumes events in batches. Manages offsets manually to ensure "At-Least-Once" delivery.

Storage (PostgreSQL): Persistent storage using bulk inserts (COPY/execute_values) for performance.

Data Flow: Client (POST Request) → FastAPI → Kafka Topic (raw_events) → Python Worker (Batch Buffer) → PostgreSQL

**🛠️ Tech Stack**
Language: Python 3.10+

API Framework: FastAPI, Uvicorn, Pydantic

Messaging: Apache Kafka (KRaft Mode - No Zookeeper)

Database: PostgreSQL 15

Infrastructure: Docker & Docker Compose

Libraries: confluent-kafka, psycopg2-binary, python-dotenv

**⚙️ Setup & Installation**
Prerequisite: (Linux Server)
The infrastructure runs on a remote server (or local Docker).

Deploy Docker Services: Use the docker-compose.yml to start Kafka and Postgres.

Bash

docker compose up -d
Initialize Database: The init.sql script creates the required tables automatically on startup.

Create Kafka Topic:

Bash

docker exec -it kafka kafka-topics.sh --create --topic raw_events --bootstrap-server localhost:9094 --partitions 3 --replication-factor 1
Prerequisite: Local Environment (Laptop)
Clone the Repository:

Bash

git clone
cd clickstream-ingest
Create Virtual Environment & Install Dependencies:

Bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r ingestion_api/requirements.txt
Configure Environment Variables: Create a .env file in the root directory:

Ini, TOML

# KAFKA
KAFKA_BOOTSTRAP_SERVERS=Hostname -I (in Linux)
KAFKA_SASL_USER=admin
KAFKA_SASL_PASS=your_password
KAFKA_TOPIC=raw_events
KAFKA_GROUP_ID=event_ingestors

# DATABASE
DB_HOST=Hostname -I (in Linux)
DB_PORT=
DB_NAME=events_db
DB_USER=your_user
DB_PASS=your_password

Bash
cd ingestion_api
uvicorn main:app --reload
# Running at http://127.0.0.1:8000
Terminal 2: Background Worker
Starts the consumer to process the Kafka queue.

Bash
python consumer/worker.py
# Logs will show: "Processing batch of size X..."
**🧪 Testing the Pipeline**
Open Swagger UI: Go to http://127.0.0.1:8000/docs

Send a Test Event:

JSON

{
  "event_id": "c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a33",
  "user_id": 101,
  "event_type": "checkout",
  "page": "/checkout/success",
  "event_time": "2026-01-13T10:20:00Z"
}
Verify in Worker: You should see the batch commit log in Terminal 2.

Verify in Database:

SQL

SELECT * FROM events;
📂 Project Structure
Plaintext

clickstream-ingest/
├── consumer/
│   ├── db.py           # Database connection & bulk insert logic
│   ├── worker.py       # Kafka consumer with batching logic
│   └── requirements.txt
├── ingestion_api/
│   ├── main.py         # FastAPI routes
│   ├── producer.py     # Kafka producer wrapper
│   ├── schemas.py      # Pydantic data models
│   └── requirements.txt
├── docker-compose.yml  # Infrastructure (Kafka + Postgres)
├── init.sql            # SQL Schema definition
├── .env                # (Not committed)
└── README.md

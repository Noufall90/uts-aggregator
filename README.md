# 🛰️ Event Log Aggregator (Pub-Sub Dedup Service)

Sistem ini adalah layanan **event aggregator** berbasis arsitektur **Publish–Subscribe (Pub-Sub)** yang dirancang untuk mengumpulkan, memproses, dan melakukan *deduplication* terhadap event dari berbagai sumber.
Dibangun dengan **FastAPI**, **aiosqlite**, dan berjalan dalam **Docker**.

---

## 🚀 Fitur Utama

* 📨 **Event Ingestion** – menerima event tunggal atau batch melalui endpoint `POST /publish`.
* 🔁 **Idempotent Consumer** – mencegah pemrosesan ulang event yang sama berdasarkan `(topic, event_id)`.
* 💾 **Deduplication Persistent Store** – menyimpan data event unik di SQLite agar tahan restart.
* 📊 **Monitoring & Statistik** – menyediakan endpoint `GET /stats` untuk memantau metrik sistem.
* 🔍 **Event Querying** – `GET /events?topic=...` untuk mengambil daftar event unik berdasarkan topik.
* ⚙️ **Dockerized** – mudah dijalankan melalui Docker Compose atau image tunggal.


---

## 🧰 Cara Menjalankan

### 1️⃣ Build dan Jalankan Docker

```bash
docker build -t event-aggregator .
docker run -p 8080:8080 event-aggregator
```

Atau gunakan **docker-compose.yml**:

```bash
docker-compose up
```

Server akan aktif di:

```
http://localhost:8080
```

---

## 📬 API Endpoints

### **1. POST /publish**

Menerima satu atau beberapa event JSON.

#### 📥 Contoh Request (Single Event)

```json
{
  "topic": "test",
  "event_id": "abc123",
  "timestamp": "2025-10-24T15:12:30Z",
  "source": "sensor-A",
  "payload": {
    "temperature": 32.1,
    "humidity": 70
  }
}
```

#### 📥 Contoh Request (Batch Event)

```json
[
  {
    "topic": "test",
    "event_id": "abc123",
    "timestamp": "2025-10-24T15:12:30Z",
    "source": "sensor-A",
    "payload": {"value": 100}
  },
  {
    "topic": "test",
    "event_id": "abc124",
    "timestamp": "2025-10-24T15:12:35Z",
    "source": "sensor-B",
    "payload": {"value": 200}
  }
]
```

#### 📤 Contoh Response

```json
{
  "received": 2,
  "unique_processed": 2,
  "duplicate_dropped": 0,
  "status": "ok"
}
```

---

### **2. GET /events?topic=test**

Mengambil semua event unik berdasarkan topik tertentu.

#### 📤 Contoh Response

```json
[
  {
    "topic": "test",
    "event_id": "abc123",
    "timestamp": "2025-10-24T15:12:30Z",
    "source": "sensor-A",
    "payload": {
      "temperature": 32.1,
      "humidity": 70
    }
  },
  {
    "topic": "test",
    "event_id": "abc124",
    "timestamp": "2025-10-24T15:12:35Z",
    "source": "sensor-B",
    "payload": {
      "value": 200
    }
  }
]
```

---

### **3. GET /stats**

Menampilkan statistik sistem agregator.

#### 📤 Contoh Response

```json
{
  "received": 11,
  "unique_processed": 3,
  "duplicate_dropped": 8,
  "topics": ["hai", "Hai", "test"],
  "uptime": 487.32017636299133
}
```

---

## 📘 Spesifikasi Teknis

| Komponen      | Teknologi                    |
| ------------- | ---------------------------- |
| Bahasa        | Python 3.11                  |
| Framework     | FastAPI                      |
| Database      | SQLite (via aiosqlite)       |
| Container     | Docker                       |
| Arsitektur    | Pub-Sub, Idempotent Consumer |
| Tipe Delivery | At-least-once                |

---

## Video Youtube


```
https://youtu.be/_fCYRU0EJ78
```

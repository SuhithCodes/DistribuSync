# 🌐 DistribuSync - Distributed File System & Computation Service

A robust distributed system implementation featuring file synchronization and remote computation capabilities using RPyC (Remote Python Call).

## 🚀 Features

### 1. File System Operations

- **Upload**: Transfer files to server with automatic replication
- **Delete**: Remove files from both client and server
- **Rename**: Modify file names across the distributed system
- **Auto-Sync**: Real-time synchronization between client and server directories

### 2. Computation Services

- **Synchronous Operations**
  - Addition of numbers
  - Array sorting
- **Asynchronous Operations**
  - Non-blocking addition
  - Non-blocking array sorting

## 📁 Project Structure

```
project/
├── client/
│   ├── client.py           # Main client interface
│   ├── sync_client.py      # File synchronization client
│   ├── async_client.py     # Asynchronous computation client
│   ├── UPLOADS/           # Client-side upload directory
│   └── SYNCHRONIZED/      # Auto-sync directory
├── server/
│   ├── file_server.py      # File operation server
│   ├── computation_server.py# Computation service
│   ├── async_server.py     # Async computation handler
│   └── MASTER/            # Server-side file storage
```

## 🛠️ Setup & Installation

1. Install Python 3.x
2. Install required packages:
   ```bash
   pip install rpyc
   ```

## 🚦 Running the Application

1. Start the servers:

   ```bash
   # Start file server
   python server/file_server.py

   # Start computation server
   python server/computation_server.py

   # Start async server
   python server/async_server.py
   ```

2. Run the client:
   ```bash
   python client/client.py
   ```

## 💡 Key Features Explained

### Auto-Synchronization

- Files in the client's SYNCHRONIZED folder automatically sync with the server's MASTER folder
- Changes are detected and propagated every second
- Uses helper threads for continuous monitoring

### File Operations

- **Upload**: Files are stored in client's UPLOAD folder and server's MASTER folder
- **Delete**: Removes files from both client and server locations
- **Rename**: Updates file names across the distributed system

### Computation Services

- **Sync Operations**: Immediate response for add and sort operations
- **Async Operations**: Non-blocking computations in separate terminals

## 🔒 Security & Implementation Details

- UTF-8 encoding for file transfers
- Error handling for file operations
- Thread-safe synchronization
- Robust client-server communication using RPyC

## 👥 Contributors

- Suhith Ghanathay

## 📝 License

This project is part of CSE5306 Distributed Systems coursework. All rights reserved.

---

_Note: This project demonstrates distributed systems concepts including Remote Procedure Calls (RPC), synchronization, and client-server architecture using Python and RPyC framework._

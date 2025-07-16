# 🌐 DistribuSync - Distributed File System & Computation Service

A robust distributed system implementation featuring file synchronization and remote computation capabilities using RPyC (Remote Python Call). DistribuSync enables seamless file operations and distributed computation between clients and servers, demonstrating core distributed systems concepts such as RPC, synchronization, and concurrency.

---

## 🏷️ Tags
- Distributed Systems
- File Synchronization
- Remote Procedure Call (RPC)
- Python
- RPyC
- Client-Server Architecture
- Asynchronous Programming
- Threading
- Coursework

---

## 🖥️ Tech Stack
- **Language:** Python 3.x
- **Core Library:** [RPyC](https://rpyc.readthedocs.io/en/latest/) (Remote Python Call)
- **Standard Libraries:** os, threading, time, concurrent.futures, subprocess
- **Concurrency:** Python threading, thread-safe operations
- **Platform:** Cross-platform (tested on Windows)

---

## 📚 What is DistribuSync?
DistribuSync is a distributed file system and computation service designed for educational and practical exploration of distributed systems. It allows users to:
- Seamlessly synchronize files between client and server directories in real time
- Perform file operations (upload, delete, rename, list, download) across the network
- Execute both synchronous and asynchronous remote computations (addition, array sorting) via RPC
- Demonstrate thread-safe, concurrent, and robust client-server communication

---

## 🚀 Features

### File System Operations
- **Upload:** Transfer files from client to server with automatic replication
- **Delete:** Remove files from both client and server
- **Rename:** Modify file names across the distributed system
- **List:** View files stored on the server
- **Download:** Retrieve files from the server to the client
- **Auto-Sync:** Real-time synchronization between client and server directories (every second)
- **Thread-Safe:** All file operations are protected by locks for concurrency safety

### Computation Services
- **Synchronous Operations:**
  - Addition of numbers
  - Array sorting
- **Asynchronous Operations:**
  - Non-blocking addition (with callback)
  - Non-blocking array sorting (with callback)
- **Multiple Servers:** Dedicated servers for file operations, synchronous computation, and asynchronous computation

### Architecture & Concurrency
- **Client-Server Model:** Clear separation of client and server logic
- **Threaded Servers:** All servers use Python threading for concurrent request handling
- **Helper Threads:** Clients use background threads for continuous folder monitoring and user interaction
- **Callback Mechanism:** Asynchronous computation results are delivered via callback functions

---

## 📁 Project Structure

```
project/
├── client/
│   ├── client.py           # Main client interface (menus, user interaction)
│   ├── sync_client.py      # File synchronization client (auto-sync logic)
│   ├── async_client.py     # Asynchronous computation client (callback handling)
│   ├── UPLOADS/           # Client-side upload directory
│   └── SYNCHRONIZED/      # Auto-sync directory
├── server/
│   ├── file_server.py      # File operation server (upload, delete, rename, list)
│   ├── computation_server.py# Computation service (sync/async add, sort)
│   ├── async_server.py     # Async computation handler (alternative port)
│   └── MASTER/            # Server-side file storage
```

---

## 🛠️ Setup & Installation

1. Install Python 3.x
2. Install required packages:
   ```bash
   pip install rpyc
   ```

---

## 🚦 Running the Application

1. Start the servers (in separate terminals):

   ```bash
   # Start file server
   python server/file_server.py

   # Start computation server
   python server/computation_server.py

   # Start async server (optional, for alternative async port)
   python server/async_server.py
   ```

2. Run the client (in a new terminal):
   ```bash
   python client/client.py
   ```

---

## 💡 Implementation Notes

- **Auto-Synchronization:**
  - The `client/SYNCHRONIZED` folder is monitored by a background thread.
  - Any file changes (add, modify, delete, rename) are detected and propagated to the server's `MASTER` folder every second.
  - Thread-safe operations ensure consistency and prevent race conditions.
- **File Operations:**
  - All file operations are exposed as RPC methods on the server.
  - The client can upload, delete, rename, list, and download files using menu-driven commands.
- **Computation Services:**
  - Synchronous and asynchronous computation (add, sort) are available via RPC.
  - Asynchronous operations use callback objects to receive results without blocking the client.
- **Threading:**
  - Both client and server use Python threads for concurrency.
  - The client uses helper threads for file operations and background sync.
- **Error Handling:**
  - Robust error handling for file not found, connection errors, and invalid operations.
- **Extensibility:**
  - Modular design allows for easy extension of file and computation services.

---

## 🚀 Deployment Notes

- **Multi-Terminal Setup:** Each server (file, computation, async) should be started in its own terminal window for full functionality.
- **Environment Variables:** Server addresses and ports can be configured via environment variables if needed.
- **Cross-Platform:** The project is designed to run on Windows but is compatible with any OS supporting Python and RPyC.
- **Dependencies:** Only Python 3.x and RPyC are required.
- **Testing:** Test file operations and computations using the provided client menus. For async operations, observe non-blocking behavior and callback results.

---

## 👥 Contributors

- Suhith Ghanathay

## 📝 License

This project is part of CSE5306 Distributed Systems coursework. All rights reserved.

---

_Note: DistribuSync demonstrates distributed systems concepts including Remote Procedure Calls (RPC), synchronization, concurrency, and client-server architecture using Python and the RPyC framework._

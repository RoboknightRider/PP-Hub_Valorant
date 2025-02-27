**Decentralized Peer-to-Peer File Sharing System**

**Team Members**
Divya Jyoti Bagchi (223014182)
Arko Sarker (223014165)
Asif Ahamad (223014215)
Md. Ashraf -Ul- Alam Rabbi (223014159)
Md. Ferdous Hasan Adar (223014172)

**Problem Statement**
Traditional centralized file-sharing platforms often suffer from issues such as high server costs, single points of failure, censorship, and slow download speeds due to bottlenecks. A peer-to-peer (P2P) network allows users to share files directly with each other, reducing dependency on centralized servers, improving availability, and ensuring efficient data distribution. This project aims to develop a decentralized P2P file-sharing system that enables fast, secure, and scalable file transfers using distributed networking principles.

**Objectives**
Develop a fully decentralized P2P system that allows users to upload and download files efficiently.
Implement a robust search and indexing mechanism to locate shared files quickly.
Ensure data integrity and security by integrating encryption and verification mechanisms.
Optimize bandwidth usage and performance using techniques such as chunk-based transfers.
Provide a user-friendly interface for seamless interaction with the system.

**Proposed Solution**
Technology Stack
Programming Languages: Python, JavaScript
Frameworks & Libraries: Flask/Django (backend), React.js (frontend).
Databases: SQLite, NoSQL (for distributed file metadata storage)
Networking: WebSockets, TCP/UDP, BitTorrent protocol
Security: AES Encryption, Hashing (SHA-256 for file verification)
Core Features
Decentralized File Sharing: Users can upload/download files without a central server.
File Chunking & Seeding: Files are split into chunks, enabling parallel downloads.
Search & Discovery: A distributed indexing mechanism to locate files efficiently.
Security & Verification: Encryption and hashing to ensure data integrity and privacy.
User-Friendly Interface: Web-based and CLI-based interaction for ease of use.
Innovative Aspects
Distributed Indexing: Reduces reliance on a single database for file tracking.
Optimized Bandwidth Usage: By allowing partial file sharing, multiple users can contribute to file transfers simultaneously.
Enhanced Privacy & Security: No central server, reducing vulnerability to attacks and censorship with only ULAB gmail login access. File has to be approved by moderators before uploading.

**Methodology**
Software Development Methodology
Agile methodology with iterative development, regular testing, and feature enhancements.
System Architecture
Peer Nodes: Users acting as both clients and servers.
Tracker Nodes (Optional): To help bootstrap connections before full decentralization.
Distributed Hash Table (DHT): For decentralized file indexing.
Chunk-based File Transfer: Each file is divided into smaller pieces for efficient downloads.
Expected Challenges & Risks
Network Latency & Speed Variations: Performance may differ based on peer availability.
Security Concerns: Preventing malicious file sharing or data breaches.
Data Persistence: Handling cases where all seeders go offline.

**Expected Outcomes**
A functional, scalable P2P file-sharing system.
A secure and efficient file transfer mechanism without relying on centralized servers.
Improved resilience against censorship and system failures.
A well-documented and user-friendly platform for easy adoption.

**Tools & Resources Needed**
Development Tools: VS Code, Postman (API testing), Git/GitHub
Networking Tools: Wireshark (for protocol analysis), Ngrok (for remote testing)
Hosting (for tracker nodes, if required): self-hosted servers
Security Libraries: PyCryptodome, OpenSSL.

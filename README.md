# Decentralized Peer-to-Peer File Sharing System

## Team Members (Valorant)
- Divya Jyoti Bagchi (223014182)
- Arko Sarker (223014165)
- Asif Ahamad (223014215)
- Md. Ashraf -Ul- Alam Rabbi (223014159)
- Md. Ferdous Hasan Adar (223014172)

## Problem Statement
Traditional centralized file-sharing platforms often face issues such as high server costs, single points of failure, censorship, and slow download speeds due to bottlenecks. A peer-to-peer (P2P) network can address these challenges by allowing users to share files directly with each other, reducing reliance on centralized servers, improving availability, and ensuring efficient data distribution. This project aims to develop a decentralized P2P file-sharing system that enables fast, secure, and scalable file transfers using distributed networking principles.

## Objectives
- Develop a fully decentralized P2P system for efficient file upload and download.
- Implement a robust search and indexing mechanism for easy file discovery.
- Ensure data integrity and security with encryption and verification mechanisms.
- Optimize bandwidth usage through chunk-based file transfers.
- Provide a user-friendly interface for seamless interaction.

## Proposed Solution

### Technology Stack
- **Programming Languages**: Python, JavaScript
- **Frameworks & Libraries**: Flask/Django (Backend), React.js (Frontend)
- **Databases**: SQLite, NoSQL (for distributed file metadata storage)
- **Networking**: WebSockets, TCP/UDP, BitTorrent protocol
- **Security**: AES Encryption, SHA-256 (for file verification)

### Core Features
- **Decentralized File Sharing**: Upload and download files without a central server.
- **File Chunking & Seeding**: Files are split into chunks to enable parallel downloads.
- **Search & Discovery**: Distributed indexing mechanism for efficient file location.
- **Security & Verification**: AES encryption and hashing to ensure data integrity and privacy.
- **User-Friendly Interface**: Both web-based and CLI-based interaction for ease of use.

### Innovative Aspects
- **Distributed Indexing**: Reduces reliance on a single database for file tracking.
- **Optimized Bandwidth Usage**: Users can share parts of files, contributing to faster downloads.
- **Enhanced Privacy & Security**: No central server reduces vulnerability to attacks and censorship. File uploads require approval from moderators, and only ULAB Gmail logins can access files.

## Methodology

### Software Development Methodology
We will follow **Agile** methodology, allowing for iterative development with frequent testing and feature enhancements.

### System Architecture
- **Peer Nodes**: Users act as both clients and servers.
- **Tracker Nodes (Optional)**: Assist in bootstrapping connections before full decentralization.
- **Distributed Hash Table (DHT)**: A decentralized system for file indexing.
- **Chunk-based File Transfer**: Files are split into smaller pieces for efficient distribution.

### Expected Challenges & Risks
- **Network Latency & Speed Variations**: Performance may vary based on peer availability.
- **Security Concerns**: Preventing malicious file sharing or data breaches.
- **Data Persistence**: Handling scenarios where all seeders go offline.

## Expected Outcomes
- A **functional** and **scalable** P2P file-sharing system.
- A **secure** and **efficient** file transfer mechanism with no centralized server.
- **Improved resilience** against censorship and system failures.
- A **well-documented** and **user-friendly** platform for adoption.

## Tools & Resources Needed

- **Development Tools**: VS Code, Postman (for API testing), Git/GitHub
- **Networking Tools**: Wireshark (for protocol analysis), Ngrok (for remote testing)
- **Hosting (if needed)**: Self-hosted servers for tracker nodes
- **Security Libraries**: PyCryptodome, OpenSSL

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

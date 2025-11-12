# 🛡️ Web Secure Simulator

**Web Secure Simulator** is a safe, educational cyber-attack simulation platform designed to demonstrate the **lifecycle of a network attack** — from reconnaissance to exploitation — entirely within a **controlled and non-destructive environment**.

---

## 🚀 Features

- 🔍 **Real Reconnaissance:** Uses `nmap` to perform safe scans on a lab-only target (Metasploitable).  
- ⚙️ **Heuristic Vulnerability Detection:** Flask backend parses scan data and identifies probable vulnerabilities.  
- 💻 **Simulated Exploitation:** Generates realistic, non-destructive exploit reports for learning purposes.  
- 🧾 **Detailed Reports:** Provides risk assessments, simulated shell outputs, and remediation suggestions.  
- 🔒 **Lab-Safe Design:** Built for isolated environments — no real-world exploitation or harm possible.

---

## 🧠 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | Python (Flask) |
| **Frontend** | HTML, CSS, JavaScript |
| **Tools** | Nmap, Netcat |
| **Environment** | Kali Linux (Attacker VM), Metasploitable 2 (Target VM) |

---

pip install -r requirements.txt
python app.py
Open your browser and navigate to:
👉 http://127.0.0.1:5000


🧪 Lab Setup

Attacker Machine: Kali Linux
Target Machine: Metasploitable 2
Network Mode: Host-only or Internal Network
Tools Used: Nmap, Netcat, Flask, Python 3


👨‍💻 Authors

Ammiel Peters
School of Computer Science and Engineering
Vellore Institute of Technology, Vellore
📧 ammielpeters009@gmail.com

Aniruddha Jadhav
School of Computer Science and Engineering
Vellore Institute of Technology, Vellore
📧 aniruddhajadhav71@gmail.com

⚠️ Disclaimer

This project is developed solely for educational and research purposes.
All scans and simulations must be conducted within an isolated lab environment.
The authors are not responsible for misuse or unauthorized deployment of this software.
## 🧩 Architecture Overview

🧾 Declaration

We hereby declare that this project and its report have been entirely created by the authors listed above.
No part of this project or documentation has been generated using Artificial Intelligence (AI) tools.
All content, analysis, and implementation are original and created for academic purposes.


# 🚀 Call Centre Agent - Quick Start Guide
## Production-Grade Security Setup

**For**: Network-Restricted Environments  
**Security Level**: ✅ **Enterprise-Grade**  
**Setup Time**: 20-30 minutes (first time)  
**Internet Required**: Only during initial setup

---

## 📋 Prerequisites (5 minutes)

Before starting, ensure you have:

### **Required Software**
- ✅ **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- ✅ **Git** (for cloning the repository)
- ✅ **Web Browser** (Chrome, Firefox, Edge, Safari)

### **System Requirements**
- ✅ **8GB RAM minimum** (16GB recommended)
- ✅ **20GB free disk space** (for Docker images and models)
- ✅ **Multi-core CPU** (model downloads are CPU-intensive)

### **Install Docker Desktop** (if not already installed)
1. **Windows**: Download from https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe
2. **Mac**: Download from https://desktop.docker.com/mac/main/amd64/Docker.dmg
3. **Linux**: Follow instructions at https://docs.docker.com/engine/install/

---

## 🔽 Step 1: Clone the Repository (2 minutes)

### **📁 Choose Your Installation Location**
You can install this project **anywhere** on your system. Popular choices:
- **Windows**: `C:\Users\YourName\Documents`, `D:\Projects`, `C:\Development`
- **Mac**: `~/Documents`, `~/Projects`, `~/Development`  
- **Linux**: `~/projects`, `/opt/projects`, `~/development`

```bash
# Open Command Prompt, PowerShell, or Terminal
# Navigate to where you want the project (choose any location you prefer)
cd C:\Users\%USERNAME%\Documents  # (Windows example)
# OR cd D:\Projects                # (Windows - different drive)  
# OR cd ~/Documents                # (Mac/Linux example)
# OR any folder of your choice - NO restrictions!

# Clone the repository
git clone https://github.com/LinoGoncalves/call-centre-agent.git

# Navigate into the project
cd call-centre-agent

# Verify files are present
dir  # (Windows) or ls -la (Mac/Linux)
```

**✅ Expected Output**: You should see files including:
- `docker-compose.secure.yml`
- `Dockerfile.secure`
- `SECURITY_ASSESSMENT.md`
- `security_validation.py`

---

## 🔒 Step 2: Launch Production-Grade Environment (20-25 minutes)

### **Start the Secure Docker Environment**

```bash
# ⚠️ IMPORTANT: Always use the SECURE version
docker-compose -f docker-compose.secure.yml up --build
```

**What Happens During Build:**
- ✅ **Security-hardened container** creation
- ✅ **AI model downloads** (HuggingFace, spaCy, NLTK) - cached for offline use
- ✅ **60+ Python packages** installation for AI/ML development
- ✅ **Enterprise security** setup (authentication, localhost-only access)

### **⏱️ Build Progress Indicators**

**Phase 1** (5-10 minutes): Base system setup
```
[+] Building Docker image...
Step 1/15: FROM python:3.13.1-slim-bookworm AS base
```

**Phase 2** (10-15 minutes): AI model downloads
```
Downloading sentence transformers...
Downloading classification models...
Model downloads complete!
```

**Phase 3** (2-3 minutes): Service startup
```
Creating call-centre-secure ... done
Starting MLflow tracking server...
Starting JupyterLab...
🔒 All services started in SECURE mode!
```

### **✅ Success Indicators**
You'll see:
```
🔒 All services started in SECURE mode!
📋 Access Information:
  JupyterLab: http://localhost:8888 (token required)
  MLflow: http://localhost:5000 (localhost only)
  Prefect: http://localhost:4200 (localhost only)
🔐 Security Features: Authentication, localhost-only, non-root
🔑 Jupyter Token: [32-character secure token]
```

---

## 🔑 Step 3: Get Your Secure Access Token (30 seconds)

### **Method A: From Build Output**
Look for this line in the terminal output:
```
🔑 Jupyter Token: AbCdEf123456789... (32 characters)
```

### **Method B: From Container Logs**
If you missed it, get it from logs:

**Windows (PowerShell/CMD):**
```bash
docker logs call-centre-secure | findstr "Jupyter Token"
```

**Mac/Linux (Terminal):**
```bash
docker logs call-centre-secure | grep "Jupyter Token"
```

**✅ Copy the token** - you'll need it for access!

---

## 🌟 Step 4: Access Your Development Environment (1 minute)

### **Open JupyterLab (Secure)**
1. **Open your web browser**
2. **Navigate to**: `http://localhost:8888`
3. **Enter your token** when prompted (from Step 3)
4. **Click "Log in"**

**✅ Success**: You should see the JupyterLab interface with your project files!

---

## 🎯 Step 5: Launch the Streamlit Demo (2 minutes)

### **Option A: From JupyterLab Interface**

1. **In JupyterLab**, navigate to the `src/ui/` folder
2. **Right-click** on `streamlit_demo.py`
3. **Select "Open With" → "Terminal"**
4. **Run the command**:
   ```bash
   streamlit run streamlit_demo.py --server.port 8501 --server.address 127.0.0.1
   ```

### **Option B: From Terminal/Command Line**

```bash
# Access the container shell
docker exec -it call-centre-secure /bin/bash

# Navigate to the UI directory
cd /app/src/ui

# Launch Streamlit demo
streamlit run streamlit_demo.py --server.port 8501 --server.address 127.0.0.1
```

### **Access the Streamlit Demo**
1. **Open a new browser tab**
2. **Navigate to**: `http://localhost:8501`
3. **🎉 Your Call Centre Agent Demo is now running!**

---

## ✅ Step 6: Verify Everything Works (2 minutes)

### **Test the Demo Application**
1. **In the Streamlit interface**, enter a sample support ticket:
   ```
   "My internet connection keeps dropping every few minutes. I've tried restarting my router but the problem persists. Can someone help me troubleshoot this issue?"
   ```

2. **Click "Classify Ticket"**

3. **✅ Expected Result**: You should see:
   - **Department**: Technical Support
   - **Priority**: Medium/High
   - **Confidence Score**: 85%+
   - **Processing details** in the logs

### **Run Security Validation** (Optional but Recommended)

```bash
# In a new terminal/command prompt window
cd call-centre-agent
python security_validation.py
```

**✅ Expected Output**:
```
✅ PRODUCTION READY - All critical security tests passed
🏆 Environment meets enterprise security standards
```

---

## 🎯 Quick Reference - All Services

Once everything is running, you have access to:

| **Service** | **URL** | **Purpose** | **Authentication** |
|-------------|---------|-------------|-------------------|
| **🎯 Streamlit Demo** | http://localhost:8501 | **Main Application** | None (localhost only) |
| **🔬 JupyterLab** | http://localhost:8888 | Interactive development | **Token required** |
| **📊 MLflow** | http://localhost:5000 | ML experiment tracking | None (localhost only) |
| **⚡ Prefect** | http://localhost:4200 | Workflow orchestration | None (localhost only) |

---

## 🛠️ Common Commands

### **Manage the Environment**
```bash
# Stop all services
docker-compose -f docker-compose.secure.yml down

# Start services (after initial build)
docker-compose -f docker-compose.secure.yml up -d

# View all running containers
docker ps

# View logs
docker logs call-centre-secure

# Access container shell
docker exec -it call-centre-secure /bin/bash
```

### **Restart Just the Streamlit Demo**
```bash
# If the demo stops running
docker exec -it call-centre-secure pkill -f streamlit
docker exec -it call-centre-secure streamlit run /app/src/ui/streamlit_demo.py --server.port 8501 --server.address 127.0.0.1
```

---

## 🚨 Troubleshooting

### **Problem: Can I install this anywhere on my computer?**
**✅ YES! Absolutely no restrictions on installation location.**
- Install in any folder: Documents, Desktop, D: drive, etc.
- No administrator rights needed for the project folder
- Docker handles all internal paths automatically
- All examples in this guide work from any location

### **Problem: Docker build fails**
**Solution:**
```bash
# Clean Docker cache and retry
docker system prune -f
docker-compose -f docker-compose.secure.yml up --build --no-cache
```

### **Problem: Port 8888 already in use**
**Solution:**
```bash
# Check what's using the port
netstat -an | findstr "8888"  # Windows
netstat -an | grep "8888"    # Mac/Linux

# Stop conflicting service or use different port
# Edit docker-compose.secure.yml: change "127.0.0.1:9999:8888"
```

### **Problem: Can't access Streamlit demo**
**Solution:**
```bash
# Check if Streamlit is running
docker exec -it call-centre-secure ps aux | grep streamlit

# If not running, start it:
docker exec -it call-centre-secure streamlit run /app/src/ui/streamlit_demo.py --server.port 8501 --server.address 127.0.0.1
```

### **Problem: Out of disk space**
**Solution:**
```bash
# Clean up Docker
docker system prune -a
docker volume prune
```

---

## 🔒 Security Features Active

Your environment includes these **enterprise-grade security features**:

- ✅ **Strong Authentication**: 32-byte cryptographic tokens
- ✅ **Localhost-Only Access**: No external network exposure
- ✅ **Non-Root Execution**: All processes run as unprivileged user
- ✅ **Container Isolation**: Read-only filesystem, capability restrictions
- ✅ **Resource Limits**: Memory and CPU limits to prevent DoS
- ✅ **Network Isolation**: Services only accessible from localhost

---

## 🎉 Success! You Now Have:

✅ **Production-grade secure environment** running  
✅ **Complete AI development stack** with 60+ packages  
✅ **Streamlit demo application** accessible at http://localhost:8501  
✅ **JupyterLab development environment** for customization  
✅ **Offline-capable setup** with pre-cached AI models  
✅ **Enterprise security** with authentication and isolation  

## 🚀 Next Steps

1. **Test the demo** with your own support tickets
2. **Explore JupyterLab** for customization and development
3. **Review the code** in `/app/src/` directories
4. **Experiment with different AI models** (all pre-installed)
5. **Scale up** for production use with your data

---

## 📞 Support & Resources

- **📋 Full Documentation**: `DOCKER-DEV_SETUP_GUIDE.md`
- **🔒 Security Details**: `SECURITY_ASSESSMENT.md`
- **🎯 Complete Solution**: `FINAL_SOLUTION_SUMMARY.md`
- **🧪 Testing**: Run `python security_validation.py`

**🏆 Enjoy your secure, enterprise-grade AI development environment!**

---

*This setup provides you with a complete, offline-capable AI development environment that meets enterprise security standards while enabling full productivity for call centre agent development.*

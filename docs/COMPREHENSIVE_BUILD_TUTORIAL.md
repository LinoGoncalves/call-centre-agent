# 🎓 Complete Call Centre AI Agent Tutorial: From Ground Up

> **Target Audience**: IT Professional with 15+ years experience, strong SQL background, beginner Python, basic ML/AI knowledge, working in Telco billing support

> **Learning Objectives**: Build production-ready AI-powered call centre classification system from scratch, understanding every component and design decision

> **Time Investment**: 20-30 hours over 2-3 weeks

> **Outcome**: Fully functional AI agent system with Gemini LLM integration, complete understanding of architecture, and ability to maintain/extend the system

---

## 📋 Table of Contents

1. [Project Overview & Architecture](#1-project-overview--architecture)
2. [Prerequisites & Environment Setup](#2-prerequisites--environment-setup)
3. [Phase 1: Foundation - Understanding the Data](#phase-1-foundation---understanding-the-data)
4. [Phase 2: Core ML Model - Traditional Classifier](#phase-2-core-ml-model---traditional-classifier)
5. [Phase 3: AI Enhancement - Gemini LLM Integration](#phase-3-ai-enhancement---gemini-llm-integration)
6. Phase 4: User Interface - Streamlit Demo → See [PHASE_4_STREAMLIT_UI.md](tutorial/PHASE_4_STREAMLIT_UI.md)
7. Phase 5: Testing & Validation → See [PHASE_5_TESTING_VALIDATION.md](tutorial/PHASE_5_TESTING_VALIDATION.md)
8. Phase 6: Deployment & Production → See [PHASE_6_PRODUCTION_DEPLOYMENT.md](tutorial/PHASE_6_PRODUCTION_DEPLOYMENT.md)
9. Troubleshooting Guide → See individual phase tutorials
10. Next Steps & Extensions → See [ROADMAP.md](../ROADMAP.md) and [BACKLOG.md](../BACKLOG.md)

---

## 1. Project Overview & Architecture

### 🎯 What Are We Building?

A sophisticated AI-powered call centre ticket classification system that:

- **Analyzes** customer support tickets in natural language
- **Classifies** tickets into departments (Technical, Billing, Sales, etc.)
- **Determines** sentiment (Positive, Negative, Neutral)
- **Assesses** urgency levels (Low, Medium, High, Critical)
- **Provides** AI-powered reasoning for all decisions
- **Routes** tickets to appropriate departments automatically

### 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                            │
│              (Streamlit Web Application)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              ENHANCED CLASSIFIER                             │
│     (Orchestrates Traditional + AI Models)                   │
└──────┬──────────────────────────────┬───────────────────────┘
       │                              │
       ▼                              ▼
┌──────────────────┐         ┌──────────────────────────┐
│ TRADITIONAL ML   │         │   GEMINI LLM AI          │
│  (Scikit-learn)  │         │  (Google Gemini Pro)     │
│                  │         │                          │
│ • Fast           │         │ • Deep Understanding     │
│ • Offline        │         │ • Contextual Reasoning   │
│ • Baseline       │         │ • Complex Analysis       │
└──────────────────┘         └──────────────────────────┘
       │                              │
       └──────────────┬───────────────┘
                      ▼
         ┌────────────────────────┐
         │   FINAL PREDICTION     │
         │  • Department          │
         │  • Sentiment           │
         │  • Urgency             │
         │  • AI Reasoning        │
         └────────────────────────┘
```

### 💡 Key Design Decisions (Why We Built It This Way)

**1. Hybrid ML Approach (Traditional + LLM)**
- **Why**: Best of both worlds - fast baseline + intelligent reasoning
- **SQL Analogy**: Like using indexed lookups (fast) + full-text search (comprehensive)
- **Benefit**: System works offline with traditional model, enhanced when LLM available

**2. Google Gemini LLM Integration**
- **Why**: State-of-the-art language understanding, free tier available
- **Telco Context**: Understands billing terminology, technical jargon, customer sentiment
- **Benefit**: Human-like reasoning explanations for audit trails

**3. Streamlit for UI**
- **Why**: Rapid prototyping, Python-native, perfect for ML demos
- **SQL Analogy**: Like building quick reports with SQL queries vs full web app
- **Benefit**: Focus on ML logic, not frontend complexity

**4. Modular Architecture**
- **Why**: Separation of concerns - models, UI, business logic independent
- **Benefit**: Easy to test, maintain, and extend individual components

---

## 2. Prerequisites & Environment Setup

### 📚 Knowledge Prerequisites

**You Should Be Comfortable With:**
- ✅ Command line / terminal operations
- ✅ SQL queries and database concepts
- ✅ Basic programming logic (if/else, loops, functions)
- ✅ Reading JSON and CSV data
- ✅ Telco domain knowledge (billing, technical support, customer service)

**You Will Learn:**
- 🎓 Python fundamentals (with SQL analogies)
- 🎓 Machine Learning basics (classification, training, prediction)
- 🎓 LLM integration patterns
- 🎓 Modern Python project structure
- 🎓 Testing and validation strategies

### 🛠️ Required Software

#### 1. Install Python 3.11+

**Windows:**
```powershell
# Download from python.org or use winget
winget install Python.Python.3.11

# Verify installation
python --version
# Should show: Python 3.11.x
```

**Mac/Linux:**
```bash
# Use homebrew (Mac) or apt (Linux)
brew install python@3.11  # Mac
# OR
sudo apt install python3.11  # Ubuntu/Debian

# Verify
python3 --version
```

#### 2. Install Git

```powershell
# Windows
winget install Git.Git

# Mac
brew install git

# Verify
git --version
```

#### 3. Install VS Code (Recommended IDE)

```powershell
# Windows
winget install Microsoft.VisualStudioCode

# Install Python extension in VS Code
code --install-extension ms-python.python
```

### 🔧 Environment Setup - Step by Step

#### Step 1: Create Project Directory

```powershell
# Create your project folder
mkdir C:\Projects\call-centre-agent
cd C:\Projects\call-centre-agent

# Initialize git repository
git init
```

> **SQL Analogy**: Think of this like creating a new database schema - you're setting up the structure for your project.

#### Step 2: Create Python Virtual Environment

```powershell
# Create isolated Python environment (like a sandbox)
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate

# Mac/Linux:
source .venv/bin/activate

# You should see (.venv) in your prompt
```

> **Why Virtual Environment?**: Isolates project dependencies, prevents conflicts. Like having separate database instances for dev/test/prod.

#### Step 3: Create Project Structure

```powershell
# Create directory structure
mkdir src
mkdir src\models
mkdir src\ui
mkdir tests
mkdir data
mkdir models
mkdir docs
mkdir scripts

# Create __init__.py files (makes directories importable)
New-Item src\__init__.py
New-Item src\models\__init__.py
New-Item src\ui\__init__.py
New-Item tests\__init__.py
```

**Your structure should look like:**
```
call-centre-agent/
├── .venv/                  # Virtual environment (git ignored)
├── src/                    # Source code
│   ├── models/             # ML models
│   ├── ui/                 # User interface
│   └── __init__.py
├── tests/                  # Test files
├── data/                   # Training data
├── models/                 # Saved model files
├── docs/                   # Documentation
└── scripts/                # Utility scripts
```

#### Step 4: Create Requirements File

Create `requirements.txt` in your project root:

```txt
# Core ML & Data Science
scikit-learn==1.3.2        # Traditional ML algorithms
pandas==2.1.4              # Data manipulation (think: SQL in Python)
numpy==1.26.2              # Numerical computing

# Google Gemini LLM
google-generativeai==0.3.1 # Gemini API client

# Web UI
streamlit==1.29.0          # Interactive web interface

# Utilities
python-dotenv==1.0.0       # Environment variable management
beautifulsoup4==4.12.2     # HTML parsing & sanitization
lxml==4.9.3                # XML/HTML processing

# Testing
pytest==7.4.3              # Testing framework
```

#### Step 5: Install Dependencies

```powershell
# Install all packages
pip install -r requirements.txt

# Verify installation
pip list
```

> **This May Take 5-10 Minutes**: Python is downloading and installing all packages. Grab a coffee! ☕

#### Step 6: Get Google Gemini API Key

1. **Go to**: https://makersuite.google.com/app/apikey
2. **Sign in** with your Google account
3. **Click**: "Create API Key"
4. **Copy** the key (starts with `AIza...`)

**Create `.env` file** in project root:

```env
GOOGLE_API_KEY=AIzaSy...your-actual-key-here...
```

> **Security Warning**: NEVER commit `.env` to git! Add it to `.gitignore`.

#### Step 7: Create .gitignore

Create `.gitignore` file:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
*.egg-info/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp

# Models (too large for git)
models/*.pkl
models/*.joblib

# Data
data/*.csv
data/*.json

# OS
.DS_Store
Thumbs.db
```

---

## Phase 1: Foundation - Understanding the Data

### 🎯 Learning Objectives
- Understand ticket structure and classification categories
- Create sample training data
- Learn pandas DataFrame operations (SQL equivalents)

### 📊 Understanding Call Centre Tickets

#### Ticket Components

A typical call centre ticket contains:

```python
{
    "ticket_id": "TKT-20250102-001",
    "description": "Customer complaint text here...",
    "department": "Billing",        # Target: What we want to predict
    "sentiment": "Negative",         # Target: Customer emotion
    "urgency": "High"                # Target: Priority level
}
```

#### Classification Categories

**Departments** (Where to route):
- `Technical Support` - Network issues, device problems, connectivity
- `Billing` - Invoices, payments, account charges
- `Sales` - New services, upgrades, product inquiries
- `Customer Service` - General inquiries, account management
- `Retention` - Cancellations, complaints, service recovery

**Sentiment** (How customer feels):
- `Positive` - Happy, satisfied, grateful
- `Neutral` - Informational, factual
- `Negative` - Frustrated, angry, dissatisfied

**Urgency** (How quickly to respond):
- `Low` - General inquiries, non-critical
- `Medium` - Service affecting one user
- `High` - Multiple users affected, financial impact
- `Critical` - Complete outage, legal/regulatory issues

### 💾 Creating Training Data

#### Step 1: Create Sample Dataset

Create `data/training_tickets.csv`:

```csv
description,department,sentiment,urgency
"Internet has been down for 3 days. Multiple calls no resolution. Business severely impacted.",Technical Support,Negative,Critical
"Please explain last month's invoice charges. Several items unclear.",Billing,Neutral,Medium
"Interested in upgrading to fiber optic service. What packages available?",Sales,Positive,Low
"How do I reset my account password?",Customer Service,Neutral,Low
"Cancelling service due to poor speeds and high costs. Very disappointed.",Retention,Negative,High
"Bill shows charges for international calls I never made. Need immediate refund.",Billing,Negative,High
"Constant buffering during peak hours for past week. Unacceptable service quality.",Technical Support,Negative,High
"Thank you for quick resolution of my billing query yesterday!",Customer Service,Positive,Low
"Router keeps dropping connection every hour. Restarting doesn't help.",Technical Support,Neutral,Medium
"Want to add mobile line to existing account. Family plan options?",Sales,Neutral,Low
```

> **Create More Data**: For production, you need 500-1000 examples. Start with 50-100 for learning.

#### Step 2: Load and Explore Data (SQL Parallels)

Create `scripts/explore_data.py`:

```python
"""
Data Exploration Script
Like running SELECT queries to understand your database
"""

import pandas as pd

# Load data (equivalent to: SELECT * FROM training_tickets)
df = pd.read_csv('data/training_tickets.csv')

# View first rows (equivalent to: SELECT TOP 10 * FROM training_tickets)
print("First 10 tickets:")
print(df.head(10))

# Count by department (equivalent to: SELECT department, COUNT(*) FROM tickets GROUP BY department)
print("\nTickets per department:")
print(df['department'].value_counts())

# Count by sentiment
print("\nSentiment distribution:")
print(df['sentiment'].value_counts())

# Count by urgency
print("\nUrgency levels:")
print(df['urgency'].value_counts())

# Get statistics (equivalent to: SELECT AVG(LENGTH(description)) FROM tickets)
print("\nDescription length statistics:")
print(df['description'].str.len().describe())

# Find tickets with specific keyword (equivalent to: WHERE description LIKE '%billing%')
billing_tickets = df[df['description'].str.lower().str.contains('bill')]
print(f"\nTickets mentioning 'bill': {len(billing_tickets)}")

# Complex query example (SQL: WHERE department = 'Billing' AND urgency = 'High')
high_urgency_billing = df[(df['department'] == 'Billing') & (df['urgency'] == 'High')]
print(f"\nHigh urgency billing tickets: {len(high_urgency_billing)}")
```

**Run the script:**

```powershell
python scripts\explore_data.py
```

### 📝 Pandas vs SQL Cheat Sheet

| SQL Operation | Pandas Equivalent | Description |
|--------------|-------------------|-------------|
| `SELECT * FROM table` | `df.head()` | View data |
| `SELECT col FROM table` | `df['col']` | Select column |
| `WHERE col = value` | `df[df['col'] == value]` | Filter rows |
| `GROUP BY col` | `df.groupby('col')` | Group data |
| `COUNT(*)` | `df['col'].value_counts()` | Count values |
| `ORDER BY col` | `df.sort_values('col')` | Sort data |
| `JOIN` | `pd.merge(df1, df2)` | Combine datasets |
| `DISTINCT col` | `df['col'].unique()` | Unique values |

### ✅ Phase 1 Checkpoint

**Verify you can:**
- [ ] Load CSV data into pandas DataFrame
- [ ] Filter and query data (SQL-like operations)
- [ ] Understand ticket structure and categories
- [ ] View statistics and distributions

**Common Issues:**
- **"File not found"**: Check your current directory with `pwd`
- **"Module not found"**: Activate virtual environment
- **"Encoding errors"**: Add `encoding='utf-8'` to `read_csv()`

---

## Phase 2: Core ML Model - Traditional Classifier

### 🎯 Learning Objectives
- Understand text classification pipeline
- Train a scikit-learn model
- Evaluate model performance
- Save/load trained models

### 🧠 Machine Learning Fundamentals

#### What is Classification?

**SQL Analogy**:
```sql
-- Classification is like creating rules:
CASE 
    WHEN description LIKE '%internet down%' THEN 'Technical Support'
    WHEN description LIKE '%bill%' OR '%invoice%' THEN 'Billing'
    ELSE 'Customer Service'
END
```

But ML **learns** these patterns automatically from examples!

#### The ML Pipeline

```
Raw Text → Preprocessing → Feature Extraction → ML Model → Prediction
   ↓            ↓                  ↓                ↓           ↓
"Internet    Lowercase,      Convert to         Train      Department:
 down 3      remove          numbers/vectors    model      Technical
 days"       noise           (TF-IDF)                      Support
```

### 📝 Step-by-Step: Building the Classifier

#### Step 1: Create the Traditional Classifier

Create `src/models/traditional_classifier.py`:

```python
"""
Traditional ML Classifier
Uses scikit-learn for text classification
"""

import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from pathlib import Path


class TraditionalClassifier:
    """
    Text classifier using TF-IDF + Naive Bayes
    
    Think of it like creating an intelligent CASE WHEN statement
    that learns patterns from your data.
    """
    
    def __init__(self):
        """Initialize the classifier pipeline"""
        # TF-IDF: Converts text to numbers (like indexing text for search)
        # Naive Bayes: Fast, simple classification algorithm
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=500,        # Keep top 500 important words
                ngram_range=(1, 2),      # Use 1-word and 2-word phrases
                stop_words='english'     # Ignore common words (the, is, at)
            )),
            ('classifier', MultinomialNB())  # The ML algorithm
        ])
        
        self.is_trained = False
    
    def train(self, texts, labels):
        """
        Train the model on examples
        
        SQL Analogy: Like building an index on a column
        The model learns patterns from your training data
        
        Args:
            texts (list): List of ticket descriptions
            labels (list): List of correct departments
        """
        print(f"Training on {len(texts)} examples...")
        
        # Fit the model (learn patterns)
        self.pipeline.fit(texts, labels)
        self.is_trained = True
        
        print("Training complete!")
    
    def predict(self, text):
        """
        Predict department for new ticket
        
        SQL Analogy: Like running a SELECT with learned rules
        
        Args:
            text (str): Ticket description
            
        Returns:
            str: Predicted department
        """
        if not self.is_trained:
            raise ValueError("Model not trained! Call train() first.")
        
        prediction = self.pipeline.predict([text])[0]
        return prediction
    
    def predict_batch(self, texts):
        """
        Predict for multiple tickets at once
        
        Args:
            texts (list): List of ticket descriptions
            
        Returns:
            list: Predicted departments
        """
        if not self.is_trained:
            raise ValueError("Model not trained! Call train() first.")
        
        predictions = self.pipeline.predict(texts)
        return predictions
    
    def evaluate(self, texts, true_labels):
        """
        Test model accuracy
        
        Like running a query and checking if results match expectations
        
        Args:
            texts (list): Test ticket descriptions
            true_labels (list): Correct departments
            
        Returns:
            dict: Performance metrics
        """
        predictions = self.predict_batch(texts)
        
        # Calculate accuracy (% correct)
        accuracy = accuracy_score(true_labels, predictions)
        
        # Detailed report (precision, recall per category)
        report = classification_report(true_labels, predictions)
        
        return {
            'accuracy': accuracy,
            'report': report
        }
    
    def save(self, filepath='models/telco_ticket_classifier.pkl'):
        """
        Save trained model to disk
        
        Like exporting a database view for reuse
        
        Args:
            filepath (str): Where to save the model
        """
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        
        # Create directory if it doesn't exist
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        # Save model
        joblib.dump(self.pipeline, filepath)
        print(f"Model saved to {filepath}")
    
    def load(self, filepath='models/telco_ticket_classifier.pkl'):
        """
        Load trained model from disk
        
        Like restoring a saved database view
        
        Args:
            filepath (str): Where to load the model from
        """
        self.pipeline = joblib.load(filepath)
        self.is_trained = True
        print(f"Model loaded from {filepath}")


# Example usage / Testing
if __name__ == "__main__":
    # Load training data
    df = pd.read_csv('data/training_tickets.csv')
    
    # Split into training and test sets (80/20 split)
    # Like creating separate dev and test databases
    X_train, X_test, y_train, y_test = train_test_split(
        df['description'],      # Input: ticket text
        df['department'],       # Output: department label
        test_size=0.2,          # 20% for testing
        random_state=42         # Reproducible split
    )
    
    # Create and train classifier
    classifier = TraditionalClassifier()
    classifier.train(X_train.tolist(), y_train.tolist())
    
    # Evaluate on test set
    results = classifier.evaluate(X_test.tolist(), y_test.tolist())
    
    print(f"\nAccuracy: {results['accuracy']:.2%}")
    print("\nDetailed Report:")
    print(results['report'])
    
    # Save the model
    classifier.save()
    
    # Test prediction
    test_ticket = "My internet has been down for 2 days. Need urgent help."
    prediction = classifier.predict(test_ticket)
    print(f"\nTest Prediction:")
    print(f"Ticket: {test_ticket}")
    print(f"Predicted Department: {prediction}")
```

#### Step 2: Train Your First Model

```powershell
# Make sure you're in project root and .venv is activated
python src\models\traditional_classifier.py
```

**Expected Output:**
```
Training on 8 examples...
Training complete!

Accuracy: 100.00%

Detailed Report:
              precision    recall  f1-score   support

      Billing       1.00      1.00      1.00         1
Technical ...       1.00      1.00      1.00         1

Model saved to models/telco_ticket_classifier.pkl

Test Prediction:
Ticket: My internet has been down for 2 days. Need urgent help.
Predicted Department: Technical Support
```

### 📊 Understanding Model Performance Metrics

**Accuracy**: Overall % correct
- `90%` = 9 out of 10 predictions correct
- **SQL Analogy**: `SELECT COUNT(*) WHERE prediction = actual / COUNT(*)`

**Precision**: When model says "Billing", how often is it actually Billing?
- `High Precision` = Few false positives
- **Important for**: Avoiding misrouting tickets

**Recall**: Of all actual Billing tickets, how many did we catch?
- `High Recall` = Few false negatives  
- **Important for**: Not missing urgent tickets

**F1-Score**: Balance between precision and recall
- `1.0` = Perfect, `0.5` = Mediocre, `<0.3` = Poor

### ✅ Phase 2 Checkpoint

**Verify you can:**
- [ ] Train a text classification model
- [ ] Make predictions on new text
- [ ] Evaluate model performance
- [ ] Save and load trained models

**Common Issues:**
- **"Not enough data"**: Need at least 20-30 examples per category
- **"Poor accuracy"**: Add more varied training examples
- **"Model file not found"**: Check `models/` directory exists

---

## Phase 3: AI Enhancement - Gemini LLM Integration

*[Tutorial continues with remaining phases...]*

### 🎯 Learning Objectives
- Integrate Google Gemini LLM API
- Combine traditional ML with LLM intelligence
- Implement ensemble prediction logic
- Handle AI responses and reasoning

*[Content continues with detailed Gemini integration, enhanced classifier implementation, UI development, testing, deployment, and troubleshooting sections...]*

---

## 📚 Learning Resources

### Python for SQL Professionals
- [Python for Data Analysis (Book)](https://wesmckinney.com/book/) - By pandas creator
- [SQL to Pandas](https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html) - Official comparison guide

### Machine Learning Basics
- [Google's ML Crash Course](https://developers.google.com/machine-learning/crash-course) - Free, beginner-friendly
- [Scikit-learn Tutorials](https://scikit-learn.org/stable/tutorial/index.html) - Official docs

### LLM and Gemini
- [Google Gemini Documentation](https://ai.google.dev/docs) - Official API docs
- [Prompt Engineering Guide](https://www.promptingguide.ai/) - Best practices

### Telco Domain Knowledge
- [Telco ML Use Cases](https://github.com/topics/telecom-machine-learning) - Industry examples
- [Customer Service AI](https://cloud.google.com/solutions/contact-center) - Google Cloud patterns

---

## 🎯 Success Criteria

By the end of this tutorial, you should be able to:

✅ Build a complete ML classification system from scratch
✅ Integrate modern LLM APIs (Gemini) with traditional ML
✅ Create interactive web UIs with Streamlit
✅ Test and validate ML model performance
✅ Deploy and maintain the system in production
✅ Explain architectural decisions to stakeholders
✅ Troubleshoot common issues independently
✅ Extend the system with new features

**Most Importantly**: You'll understand *why* each component exists and *how* they work together!

---

This tutorial was assembled using the repository's Agentic Framework. For orchestration patterns and workflows see:

- `.github/chatmodes/agent-orchestrator.md` — Master Orchestrator (canonical)
- `docs/AGENTIC_FRAMEWORK_GUIDE.md` — Detailed framework guide (HITL, agents, templates)

For general project questions, refer to the project README and `docs/PROJECT_STRUCTURE.md`.


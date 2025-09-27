# telkom-call-centre - Project Brief

## Project Overview

**Type**: ml-model
**Created**: 2025-09-27
**Duration**: 1 week
**Budget**: R50,000
**Primary Stakeholder**: Human Product Owner

## Problem Statement

Develop an automated call centre ticket classification system to improve allocation efficiency and ensure timely resolution of customer issues for a typical telecommunications firm.

## Requirements

### Functional Requirements

1. **Text Classification System**: Automatically categorize incoming customer tickets/transcripts into predefined categories
2. **Automated Allocation**: Route classified tickets to appropriate support teams/agents
3. **Real-time Processing**: Process and classify tickets in near real-time for immediate allocation
4. **Multi-category Classification**: Support multiple ticket types (billing, technical, sales, complaints, network issues)

### Non-Functional Requirements

1. **Accuracy**: Minimum 85% classification accuracy on test data
2. **Performance**: Process tickets within 2 seconds
3. **Scalability**: Handle up to 1000 tickets per hour
4. **Availability**: 99.5% uptime during business hours

### Data Requirements

- **Source**: Mock transcript data simulating typical telecoms customer interactions
- **Volume**: Generate 5000+ mock tickets across various categories
- **Categories**: Billing issues, technical support, sales inquiries, complaints, network problems, account management

## Architecture

### High-Level System Design

```text
Customer Ticket → Text Preprocessing → ML Classification Model → Category Assignment → Automated Routing → Support Team
```

### Components

1. **Data Ingestion Layer**: Ticket intake and preprocessing
2. **ML Model Service**: Text classification using transformer-based model
3. **Routing Engine**: Automated allocation based on classification results
4. **Monitoring Dashboard**: Performance metrics and model drift detection
5. **API Layer**: RESTful endpoints for integration

## Technology Stack

### ML/Data Science Stack

- **Language**: Python 3.13+
- **ML Framework**: scikit-learn, transformers (HuggingFace)
- **Text Processing**: spaCy, NLTK
- **Data Manipulation**: pandas, numpy
- **Model Serving**: FastAPI

### Infrastructure & DevOps

- **Environment Management**: uv
- **Testing**: pytest, pytest-cov (80% coverage minimum)
- **Code Quality**: ruff (formatting/linting), mypy (type checking)
- **Version Control**: git with proper branching strategy
- **Documentation**: Markdown, Sphinx

### Mock Data Generation

- **Synthetic Data**: faker, custom telecoms scenario generators
- **Data Augmentation**: Text variation techniques
- **Data Validation**: great-expectations or similar

## Success Criteria

### Primary Success Metrics

1. **Classification Accuracy**: ≥85% on holdout test set
2. **Processing Speed**: <2 seconds per ticket classification
3. **System Integration**: Successful API deployment with documented endpoints
4. **Code Quality**: 80% test coverage, passing all linting/type checks

### Secondary Success Metrics

1. **Model Interpretability**: Clear feature importance and decision explanations
2. **Scalability Demonstration**: Proof of concept for 1000 tickets/hour
3. **Documentation Quality**: Complete technical and user documentation
4. **Deployment Readiness**: Production-ready containerized solution

### Business Value Metrics

1. **Time Savings**: Demonstrate potential reduction in manual ticket routing time
2. **Accuracy Improvement**: Show improvement over random/current manual allocation
3. **Cost Effectiveness**: Solution development within R50k budget

## Timeline

### Week 1 Breakdown (7 days)

- **Days 1-2**: Requirements finalization, mock data generation strategy
- **Days 3-4**: Model development, training, and initial validation
- **Days 5-6**: MLOps pipeline, testing, and documentation
- **Day 7**: Final integration, Human PO review, and handoff

### Key Milestones

1. **Day 2**: Mock data generation complete (2000+ samples)
2. **Day 4**: Trained model achieving ≥85% accuracy
3. **Day 6**: Deployed API with monitoring
4. **Day 7**: Complete documentation and PO sign-off

## Deliverables

1. Trained ML model for ticket classification
2. Mock dataset (5000+ telecoms tickets)
3. FastAPI service for model serving
4. Automated testing suite (80%+ coverage)
5. Deployment documentation and scripts
6. Performance monitoring dashboard
7. Technical and user documentation
8. Final presentation to Human Product Owner

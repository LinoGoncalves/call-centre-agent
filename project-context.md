# Project Context for AI Development Handover

**Generated:** September 28, 2025  
**Project:** Telco Call Centre Agent System  
**Location:** `c:\DEV\call-centre-agent`

## Executive Summary

This is a sophisticated multi-agent call centre system for telecommunications companies that leverages Google's Gemini AI for enhanced sentiment analysis and ticket classification. The system features a Streamlit demo interface with advanced HTML sanitization, auto-expanding panels, and comprehensive agent-based architecture.

## Recent Development Session Context

### Primary Objectives Completed
1. ✅ **HTML Display Bug Resolution**: Resolved persistent HTML tags appearing in sentiment analysis reasoning text despite multiple cleaning attempts
2. ✅ **UI Consistency**: Achieved styling consistency across UI panels 
3. ✅ **Auto-Expanding Panels**: Implemented dynamic panel sizing with scrollbar fallbacks

### Technical Challenges Overcome
- **HTML Sanitization**: Implemented multi-layer cleaning (BeautifulSoup + regex + character-level)
- **Streamlit Components**: Resolved iframe rendering issues with `components.html`
- **Dynamic Sizing**: Developed mathematical height estimation algorithm for auto-expanding panels
- **JavaScript Integration**: Used `textContent` assignment to prevent HTML interpretation

### Current System Status
- **Demo Running**: Streamlit interface accessible via `python launch_demo.py`
- **HTML Prevention**: Guaranteed via JavaScript `textContent` assignment
- **Panel Sizing**: Auto-expanding with scrollbar fallback (base 220px + 28px per estimated line)
- **Styling**: Consistent gray background with blue borders, sentiment-based text coloring

## Project Architecture

### Core Components

#### 1. **Enhanced Classification System** (`enhanced_classifier.py`)
- **Purpose**: LLM integration with Gemini AI for sentiment analysis and ticket classification
- **Key Features**:
  - Multi-stage HTML sanitization at source level
  - Sentiment scoring with confidence metrics
  - Priority level assignment (P0_IMMEDIATE → P3_STANDARD)
  - Escalation requirement detection
- **Critical Code**: Nuclear HTML cleaning before return, BeautifulSoup parsing, regex pattern removal

#### 2. **Streamlit Demo Interface** (`streamlit_demo.py`)
- **Purpose**: Interactive web interface for testing and demonstration
- **Key Features**:
  - HTML-safe rendering via `components.html` with JavaScript `textContent`
  - Auto-expanding panels with mathematical height estimation
  - Debug mode for HTML cleaning validation
  - Sentiment-based color coding and emoji indicators
- **Critical Code**: `display_sentiment_analysis()` function with iframe isolation and scrollbar fallback

#### 3. **Multi-Agent System** (`telco-call-centre/`)
- **Master Agent**: Central coordination (`master-agent.md`)
- **Sub-Agents**: 20+ specialized agents including:
  - Business Analyst, Cloud Engineer, Data Scientist, DevOps Engineer
  - QA Engineer, Security Expert, Solutions Architect, Technical Writer
  - Each with specific expertise and development standards
- **Standards**: Comprehensive development guidelines in `development-standards/`

### Data Flow Architecture
```
Customer Ticket → Gemini API → enhanced_classifier.py → Nuclear HTML Cleaning → 
streamlit_demo.py → JavaScript textContent → HTML-Safe Display
```

## Technical Implementation Details

### HTML Sanitization Pipeline (Multi-Layer Defense)
1. **Source Level** (`enhanced_classifier.py`): BeautifulSoup + regex + character-level cleaning
2. **Display Level** (`streamlit_demo.py`): Additional cleaning + HTML entity decoding  
3. **Render Level**: JavaScript `textContent` assignment (prevents HTML interpretation)

### Auto-Expanding Panel Algorithm
```python
base_height = 220  # Headers, badges, controls
chars_per_line = 65  # Conservative estimate
estimated_lines = max(4, len(text) // chars_per_line + newlines + 3)
total_height = min(700, base_height + (estimated_lines * 28))  # 28px per line
```

### Streamlit Components Integration
- **Method**: `components.html()` with iframe isolation
- **Styling**: Inline styles required (CSS classes don't inherit in iframes)
- **Height**: Mathematical estimation more reliable than JavaScript auto-resize
- **Scrolling**: Dual-level (container + text area) with `overflow-y: auto`

## Key Files and Locations

### Primary Development Files
- `enhanced_classifier.py` - Core AI classification engine
- `streamlit_demo.py` - Main demo interface  
- `launch_demo.py` - Demo launcher script
- `main.py` - API endpoint (currently in `src/api/`)

### Configuration and Environment
- `.env` - Google API key and environment variables
- `pyproject.toml` - Python dependencies and project metadata
- `requirements.txt` - Alternative dependency specification

### Agent System
- `telco-call-centre/master-agent.md` - Central agent coordination
- `telco-call-centre/sub-agents/` - Specialized agent definitions (20+ files)
- `telco-call-centre/development-standards/` - Coding standards and guidelines
- `telco-call-centre/templates/` - Project templates and frameworks

## Development Environment Setup

### Prerequisites
```bash
# Python 3.11+ recommended
# Google API key for Gemini AI
# Virtual environment (.venv)
```

### Installation & Launch
```bash
cd c:\DEV\call-centre-agent
# Activate virtual environment
.venv\Scripts\activate
# Install dependencies  
pip install -r requirements.txt
# Launch demo
python launch_demo.py
```

### Environment Variables Required
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

## Current Technical State

### Working Features ✅
- Sentiment analysis with confidence scoring
- Priority level assignment and escalation detection
- HTML-safe text rendering (no HTML tags visible)
- Auto-expanding panels with scrollbar fallback
- Multi-agent system architecture
- Comprehensive development standards

### Known Technical Decisions
1. **HTML Prevention**: JavaScript `textContent` chosen over `innerHTML` to guarantee no HTML rendering
2. **Panel Sizing**: Mathematical estimation preferred over complex JavaScript auto-resize messaging
3. **Styling Approach**: Inline styles in iframes vs CSS class inheritance (iframe isolation)
4. **Scrollbar Strategy**: Dual-level scrolling (container + text area) for maximum compatibility

### Debug Features Available
- HTML cleaning validation mode (`debug_html` session state)
- Raw API response inspection
- Multi-stage cleaning process visibility

## Dependencies and Integrations

### Core Dependencies
- `streamlit` - Web interface framework
- `google-generativeai` - Gemini AI integration
- `beautifulsoup4` - HTML parsing and cleaning
- `python-dotenv` - Environment variable management
- `plotly` - Data visualization components

### External Integrations
- **Google Gemini AI**: Primary LLM for classification and reasoning
- **Streamlit Components**: For advanced HTML rendering in iframe isolation

## Development Standards and Guidelines

The project follows comprehensive development standards located in `telco-call-centre/development-standards/`:
- API design patterns and reference templates
- Architectural principles and cloud resource policies
- Secure coding checklist and security policies
- Testing strategy and documentation style guides
- MLOps pipeline standards and SRE handbook

## Future Development Considerations

### Immediate Opportunities
1. **API Integration**: Expand `src/api/main.py` for production endpoints
2. **Database Integration**: Implement ticket persistence and history
3. **Agent Orchestration**: Activate multi-agent workflow system
4. **Performance Optimization**: Cache frequently used classification results

### Technical Debt Areas
1. **Error Handling**: Enhance API failure resilience
2. **Testing Coverage**: Implement comprehensive unit and integration tests
3. **Configuration Management**: Centralize settings and feature flags
4. **Monitoring**: Add logging and performance metrics

### Architectural Evolution
- Consider microservices architecture for agent system
- Implement message queuing for agent communication
- Add authentication and authorization layers
- Integrate with actual telecommunications systems and databases

## Debugging and Troubleshooting

### Common Issues and Solutions
1. **HTML Tags Visible**: Verify JavaScript `textContent` assignment is working
2. **Panel Height Issues**: Check mathematical height calculation parameters
3. **Streamlit Port Conflicts**: Use `taskkill /F /IM python.exe /T` to clear processes
4. **API Failures**: Verify Google API key in `.env` file

### Development Commands
```bash
# Stop all Python processes
taskkill /F /IM python.exe /T

# Launch demo
python launch_demo.py

# Direct Streamlit run (alternative)
python -m streamlit run streamlit_demo.py --server.port=8502

# Test classification directly
python -c "from enhanced_classifier import GeminiEnhancedClassifier; ..."
```

## Contact and Handover Notes

This project represents a sophisticated integration of modern AI capabilities with enterprise-grade call centre requirements. The multi-agent architecture provides excellent scalability for different specialized tasks, while the current implementation focuses on robust sentiment analysis with bulletproof HTML handling.

The recent development session successfully resolved critical UI/UX issues around HTML sanitization and panel sizing, establishing a solid foundation for continued development. Future AI assistants should focus on expanding the agent orchestration capabilities and production-ready API development.

**Key Success Factors:**
- Comprehensive HTML sanitization at multiple levels
- Mathematical height estimation for reliable UI behavior  
- Iframe isolation for secure component rendering
- Multi-agent architecture for specialized expertise
- Extensive development standards and guidelines

This handover document provides the essential context needed to continue development efficiently and maintain the high technical standards established in this project.
# Configuration Directory

This directory contains user-specific configuration files for the Call Centre Agent system.

## Files

### `user_config.example.json` (Committed to Git)
Template configuration file showing available options and default values.

**Copy this file to create your personal configuration:**
```bash
copy user_config.example.json user_config.json
```

### `user_config.json` (Ignored by Git)
Your personal configuration file. This file is auto-generated when you run the application and save preferences through the UI.

**This file contains:**
- LLM provider preference (Gemini, Ollama, etc.)
- Vector database preference (Pinecone, ChromaDB, etc.)
- UI preferences (theme, visualization settings)
- Debug mode settings
- Performance thresholds

**Note**: This file is excluded from version control via `.gitignore` because it contains user-specific settings.

## Configuration Options

```json
{
  "llm_provider": "Gemini Pro (Cloud)",        // LLM service to use
  "vector_provider": "Pinecone (Cloud)",       // Vector database to use
  "show_pipeline_viz": true,                   // Show pipeline visualization
  "debug_mode": false,                         // Enable debug logging
  "ensemble_weight": 0.7,                      // Weight for ensemble routing
  "other_threshold": 0.6,                      // Threshold for "Other" category
  "auto_initialize": true,                     // Auto-initialize on startup
  "preferences": {
    "theme": "default",                        // UI theme
    "show_cost_info": true,                    // Display cost information
    "show_performance_metrics": true           // Display performance metrics
  }
}
```

## Provider Options

### LLM Providers
- `"Gemini Pro (Cloud)"` - Google's Gemini AI (requires API key)
- `"Ollama (Local)"` - Local Ollama models
- Other providers as configured

### Vector Providers
- `"Pinecone (Cloud)"` - Cloud-based vector database (requires API key)
- `"ChromaDB (Local)"` - Local vector database (no API key needed)

## Usage

The application automatically:
1. Looks for `config/user_config.json` on startup
2. Falls back to default values if not found
3. Creates the file when you save preferences through the UI

## Manual Configuration

You can manually edit `user_config.json` to set preferences before launching the application.

**Example - Use local providers:**
```json
{
  "llm_provider": "Ollama (Local)",
  "vector_provider": "ChromaDB (Local)",
  "show_pipeline_viz": true,
  "debug_mode": false
}
```

## Security Note

Never commit `user_config.json` to version control if it contains sensitive information or API keys. The file is already excluded via `.gitignore`.

## Related Files

- **Code**: `src/models/config_manager.py` - Configuration management logic
- **UI**: `src/ui/streamlit_demo.py` - Loads and saves preferences

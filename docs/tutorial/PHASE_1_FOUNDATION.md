# Phase 1: Foundation — Data, Python, and Reproducible Workflows

**Estimated Time**: 4-6 hours
**Prerequisites**: Basic SQL knowledge, command-line comfort
**File References**: `docs/COMPREHENSIVE_BUILD_TUTORIAL.md`, `src/models/enhanced_classifier.py`

---

This phase brings your SQL expertise into Python and prepares robust, reproducible data workflows. The aim is to teach data engineering and preprocessing patterns you will reuse across model training, LLM prompts, and production inference.

Key outcomes:
- Create a reproducible Python environment
- Load and explore ticket data with pandas (SQL -> pandas idioms)
- Build robust preprocessing pipelines for text data
- Validate and version datasets
- Prepare production-ready training inputs (TF-IDF / tokenization)

---

## 1. Environment & Reproducibility

1. Use a virtual environment per project (.venv). Activate it before installing dependencies.

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Pin dependencies using `requirements.txt` or `pyproject.toml` + lockfile. Record Python version (e.g., 3.11.x) in README.

3. Use `pre-commit` hooks for formatting and linting in CI. Example checks: black, ruff, isort, and markdownlint for docs.

---

## 2. Data Loading — treat CSV like a table

You already think in SQL. Here are direct pandas equivalents.

- Read CSV (SQL: SELECT * FROM tickets)
```python
import pandas as pd
df = pd.read_csv('data/tickets.csv')
```

- Filter (SQL WHERE):
```python
df_filtered = df[df['category'] == 'BILLING']
```

- Group / Aggregate (SQL GROUP BY):
```python
counts = df.groupby('category').size().reset_index(name='count')
```

- JOINs (SQL JOIN):
```python
users = pd.read_csv('data/users.csv')
df = df.merge(users, on='user_id', how='left')
```

When reading large datasets, use `dtype` hints and `usecols` to reduce memory footprint.

---

## 3. Data Validation & Schema

For production, validate incoming data. Two pragmatic options:

- Lightweight: Simple assertions + `pandas` checks
```python
assert 'text' in df.columns
assert df['text'].notnull().all()
```

- Stronger: Use `pandera` or `pydantic` for schema validation

Example `pandera` schema:
```python
import pandera as pa
schema = pa.DataFrameSchema({'ticket_id': pa.Column(int), 'text': pa.Column(str), 'created_at': pa.Column(pa.DateTime)})
schema.validate(df)
```

Benefits:
- Early detection of upstream ETL problems
- Clear error messages for data owners

---

## 4. Text Preprocessing — deterministic & auditable

Text preprocessing must be deterministic and reversible where possible.

Minimal pipeline (production-ready):
1. Unicode normalization (NFC)
2. Trim whitespace, collapse repeated punctuation
3. Remove control characters, keep punctuation useful for meaning
4. Lowercasing (optional — depends on tokenizer)
5. Replace account numbers / PII with tokens (PII redaction)
6. Preserve currency and numeric amounts (useful for billing)

Example implementation sketch (refer to `src/models/enhanced_classifier.py` preprocessing functions):
```python
import re
import unicodedata

def normalize_text(s: str) -> str:
    s = '' if s is None else s
    s = unicodedata.normalize('NFC', s)
    s = re.sub(r'\s+', ' ', s).strip()
    # Replace account numbers (simple pattern)
    s = re.sub(r'\b\d{6,}\b', '<ACCOUNT_NUM>', s)
    return s
```

**Note on PII:** Do NOT send raw PII to LLMs. Mask or hash sensitive fields before sending externally.

---

## 5. Feature Extraction for Text

Two main approaches used in this project:

1. Traditional TF-IDF (fast, deterministic)
2. Tokenization (for LLM prompts — lightweight normalization, preserve sentence structure)

TF-IDF pipeline using scikit-learn (production pattern):
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1,2), max_df=0.85, min_df=5)),
])
X = pipeline.fit_transform(df['text'])
```

Key considerations:
- ngram_range: include bigrams for domain-specific phrases ("late fee")
- max_df/min_df: remove extremely rare or overly common tokens
- use `CountVectorizer` + `TfidfTransformer` if you need raw counts separately

---

## 6. Train/Validation/Test Splits & Versioning

- Use stratified splits on the target category for balanced evaluation:
```python
from sklearn.model_selection import train_test_split
train, test = train_test_split(df, stratify=df['category'], test_size=0.2, random_state=42)
```

- Save dataset versions with semantic naming (e.g., `tickets_v2025-09-01.csv`) and include a `manifest.json` with checksum and row counts.

- Record preprocessing pipeline parameters alongside model metadata (vectorizer vocabulary, stopwords list)

---

## 7. Data Sampling & Synthetic Data

Telco ticket distribution is often imbalanced (e.g., many 'BILLING' tickets). Strategies:
- Up-sample minority classes carefully (with augmentation)
- Synthetic generation: template-based or use LLMs to generate variations

Template-based example:
```
"I was charged {amount} for {service} but I didn't opt-in"
```
Plug in amounts and service names to create diverse examples.

---

## 8. Quick Reference: SQL -> Pandas Patterns

- SELECT col1, col2 FROM t WHERE col = 'X' -> df.loc[df['col'] == 'X', ['col1','col2']]
- SELECT count(*) FROM t GROUP BY col -> df.groupby('col').size().reset_index(name='count')
- JOIN -> df.merge(other, on='key', how='left')

---

## 9. Practical Exercise (45-90 minutes)

1. Load `data/tickets_sample.csv` (or `data/sample_tickets.json`) into pandas
2. Build a preprocessing function `clean_ticket_text` that performs normalization + PII masking
3. Build a TF-IDF pipeline and persist it to `models/tfidf_v1.joblib`
4. Choose a small subset and create `train.csv`, `val.csv`, `test.csv` with stratified sampling

Verification:
- Check pipeline transforms without errors
- Confirm saved artifacts exist and can be loaded

---

## 10. Production Tips & Gotchas

- Always pin random seeds (numpy, sklearn) when training to improve reproducibility
- Store vectorizer vocabulary with the model; vocab drift causes production mismatches
- Avoid leaking test data into training via global-fit operations
- Mask PII before any remote calls
- Monitor dataset schema changes via CI checks

---

## 11. Next Steps

When complete, proceed to **Phase 2: Traditional ML**, where you will build and validate baseline models using the pipelines you created here.

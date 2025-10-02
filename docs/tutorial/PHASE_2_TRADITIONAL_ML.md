# Phase 2: Traditional ML — Building the Baseline Classifier

**Estimated Time**: 6-8 hours
**Prerequisites**: Phase 1 complete (clean data, TF-IDF pipeline)
**File References**: `src/models/` (classic ML code), `models/` saved artifacts

---

This phase gives you a deep understanding of the traditional ML stack used as the system baseline: feature pipelines, model families, hyperparameter tuning, calibration, explainability, and saving/loading artifacts for production.

## 1. Choice of Algorithms

Why we use these models in this project:
- **Logistic Regression (LogReg)**: Fast, interpretable, good baseline for text classification
- **Random Forest (RF)**: Robust to noisy features, handles non-linearities
- **Ensemble (Stacking/Weighted)**: Combine strengths of multiple models for robustness

## 2. Model Pipeline (Production pattern)

```python
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

pipeline_lr = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1,2), max_df=0.85, min_df=5)),
    ('clf', LogisticRegression(class_weight='balanced', max_iter=1000))
])

pipeline_rf = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1,2), max_df=0.85, min_df=5)),
    ('clf', RandomForestClassifier(n_estimators=200))
])
```

### Key considerations
- Use `class_weight='balanced'` for imbalanced datasets
- Precompute TF-IDF vocabulary and persist it for production

---

## 3. Hyperparameter Tuning & Validation

### Grid Search vs Randomized Search
- **GridSearchCV**: exhaustive, good for small parameter spaces
- **RandomizedSearchCV**: efficient for larger search spaces

```python
from sklearn.model_selection import RandomizedSearchCV
param_distributions = {
    'clf__C': [0.01, 0.1, 1, 10],
    'clf__penalty': ['l2']
}
search = RandomizedSearchCV(pipeline_lr, param_distributions, n_iter=10, cv=5, scoring='f1_macro')
search.fit(X_train, y_train)
```

### Cross-validation patterns
- **StratifiedKFold** for classification
- **GroupKFold** when tickets have user_id groups to avoid leakage

---

## 4. Model Calibration

Probability estimates from RF/LogReg may be poorly calibrated. Use `CalibratedClassifierCV` when probabilities matter (for OTHER threshold, SLA decisions):

```python
from sklearn.calibration import CalibratedClassifierCV
calibrated_rf = CalibratedClassifierCV(base_estimator=rf, cv=5)
calibrated_rf.fit(X_train, y_train)
```

---

## 5. Evaluations & Metrics

Important: Use multiple metrics for classification
- **Accuracy** (overall, not sufficient for imbalanced data)
- **Precision / Recall / F1 (per-class and macro-averaged)**
- **Confusion matrix** - for category confusion analysis
- **ROC-AUC / PR-AUC** - use per-class or one-vs-rest for multiclass
- **Calibration plots** - verify predicted probability correctness

```python
from sklearn.metrics import classification_report, confusion_matrix
print(classification_report(y_test, y_pred))
```

---

## 6. Explainability

Use `eli5` or `sklearn.inspection` for feature importance and per-prediction explanation.

```python
import eli5
eli5.show_weights(search.best_estimator_.named_steps['clf'], top=50)
```

For per-sample explanations:
```python
import shap
explainer = shap.Explainer(search.best_estimator_.named_steps['clf'], X_train)
shap_values = explainer(X_test)
shap.plots.bar(shap_values)
```

---

## 7. Model Persistence & Versioning

Save model artifacts and metadata:
- `models/tfidf_v1.joblib` — TF-IDF vectorizer
- `models/logreg_v1.joblib` — Logistic regression model
- `models/ensemble_v1.joblib` — Combined ensemble
- `models/manifest.json` — Model metadata (training date, dataset checksum, params)

```python
import joblib
joblib.dump(pipeline, 'models/logreg_v1.joblib')
```

---

## 8. Training Automation

Use an orchestration script (`scripts/train.py`) to standardize training runs:
- Accept CLI args for dataset path, model type, output path
- Save artifacts and manifest
- Log run metrics to `runs/` directory

Example CLI (Click or argparse):
```python
python scripts/train.py --data data/train.csv --model logreg --out models/logreg_v1.joblib
```

---

## 9. Integration with Enhanced Classifier

Traditional pipelines are wrapped by the `GeminiEnhancedClassifier` to allow ensemble weights. Interface contract expected by the enhanced classifier:

```
class BaseTraditionalModel:
    def predict(self, texts: List[str]) -> List[str]:
        ...
    def predict_proba(self, texts: List[str]) -> np.ndarray:
        ...
```

Ensure your saved model follows this contract when loaded in production.

---

## 10. Practical Exercise (3-4 hours)

1. Implement the pipelines above and run a hyperparameter search for `LogisticRegression` and `RandomForest`.
2. Calibrate the best RF model.
3. Evaluate on a held-out test set and write a summary report (confusion matrix, per-class F1, calibration plot).
4. Persist artifacts and update `models/manifest.json` with metadata.

---

## 11. Next Steps

Proceed to Phase 3: LLM integration and ensemble strategies. Ensure you have persisted model artifacts and recorded training metadata.

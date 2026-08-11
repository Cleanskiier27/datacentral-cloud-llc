# AI Training Pipeline Setup & Deployment Guide
# NetworkBuster Machine Learning Infrastructure

## 🤖 AI Training Pipeline Overview

The NetworkBuster AI Training Pipeline is a comprehensive system for:
- Training machine learning models on visitor behavior and performance data
- Managing datasets in Azure Blob Storage
- Registering and versioning trained models
- Processing training jobs from Azure Storage Queue
- Continuous model monitoring and optimization

---

## 📦 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Azure Storage Queue                         │
│           (ai-training-jobs notifications)                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│         Training Orchestrator Service                        │
│  • Monitor queue for new jobs                               │
│  • Execute training workflows                               │
│  • Manage model lifecycle                                   │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
    ┌────────┐  ┌────────┐  ┌────────┐
    │Dataset │  │Trainer │  │Registry│
    │Manager │  │ Engine │  │Service │
    └────────┘  └────────┘  └────────┘
        │            │            │
        └────────────┼────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
   ┌──────────────┐         ┌──────────────┐
   │ AI Training  │         │   ML Models  │
   │ Datasets     │         │  Container   │
   │ Container    │         │              │
   └──────────────┘         └──────────────┘
```

---

## 🎯 Available Models

### 1. Visitor Behavior Model
- **Type:** Neural Network (TensorFlow)
- **Purpose:** Predict visitor engagement patterns
- **Inputs:** User interactions, session data, behavior metrics
- **Output:** Engagement score, churn probability
- **Update Frequency:** Daily

### 2. Sustainability Predictor
- **Type:** Random Forest
- **Purpose:** Forecast sustainability metrics
- **Inputs:** Energy usage, carbon footprint, resource allocation
- **Output:** Sustainability trends, optimization recommendations
- **Update Frequency:** Weekly

### 3. Performance Optimizer
- **Type:** Gradient Boosting
- **Purpose:** Optimize system performance
- **Inputs:** Response times, error rates, throughput metrics
- **Output:** Performance recommendations, bottleneck identification
- **Update Frequency:** Hourly

### 4. Content Recommender
- **Type:** Collaborative Filtering
- **Purpose:** Recommend relevant content to visitors
- **Inputs:** User preferences, content metadata, interaction history
- **Output:** Personalized content recommendations
- **Update Frequency:** Real-time

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install azure-storage-blob
pip install azure-storage-queue
pip install tensorflow scikit-learn
pip install pandas numpy
```

### Environment Variables
```powershell
$env:AZURE_STORAGE_ACCOUNT_NAME = "<your-storage-account-name>"
$env:AZURE_STORAGE_ACCOUNT_KEY = "<your-storage-key>"
$env:AZURE_STORAGE_CONNECTION_STRING = "<your-connection-string>"
```

### Basic Usage

**Initialize Pipeline:**
```python
from ai_training_pipeline import initialize_pipeline

pipeline = await initialize_pipeline(connection_string)
```

**Train Single Model:**
```python
trainer = ModelTrainer('visitor-behavior-model')
result = await trainer.train_model('./datasets/visitor-behavior-data.csv')
```

**List Available Datasets:**
```python
manager = TrainingDatasetManager(connection_string)
datasets = manager.list_datasets()
```

**Register Trained Model:**
```python
registry = ModelRegistry(connection_string)
await registry.register_model(
    model_name='visitor-behavior-model',
    version='1.0',
    metadata={...},
    blob_path='ml-models/visitor-behavior-v1'
)
```

---

## 📊 Training Data Format

### Visitor Behavior Data (CSV)
```csv
session_id,user_id,timestamp,page,duration,clicks,scroll_depth,device,browser
s001,u001,2025-01-01T10:00:00,home,45,3,0.8,mobile,chrome
s002,u002,2025-01-01T10:05:00,blog,120,5,0.95,desktop,firefox
```

### Sustainability Metrics (CSV)
```csv
timestamp,energy_kwh,carbon_kg,memory_percent,cpu_percent,requests
2025-01-01T10:00:00,2.3,1.8,65,45,1200
2025-01-01T10:05:00,2.1,1.6,62,42,1150
```

### Performance Data (CSV)
```csv
timestamp,endpoint,response_time_ms,error_rate,throughput_rps,cache_hit_rate
2025-01-01T10:00:00,/api/data,45,0.1,500,0.85
2025-01-01T10:05:00,/api/search,120,0.5,200,0.72
```

### User Content Interactions (CSV)
```csv
user_id,content_id,interaction_type,timestamp,duration_sec,rating
u001,c001,view,2025-01-01T10:00:00,30,4
u002,c002,click,2025-01-01T10:05:00,15,3
```

---

## 🔄 Training Pipeline Workflow

### Step 1: Dataset Preparation
1. Collect raw data from Azure Log Analytics
2. Clean and preprocess data
3. Upload to `ai-training-datasets` container
4. Create training/validation/test splits

### Step 2: Job Submission
1. Add training job to `ai-training-jobs` queue
2. Include model config and dataset reference
3. Set priority and timeout parameters

### Step 3: Model Training
1. Orchestrator picks up job from queue
2. Downloads dataset from blob storage
3. Trains model with specified parameters
4. Monitors training progress and metrics

### Step 4: Model Evaluation
1. Evaluate model on test dataset
2. Calculate performance metrics (accuracy, precision, recall, etc.)
3. Compare against baseline models

### Step 5: Model Registration
1. Register model in ModelRegistry
2. Save trained model to `ml-models` container
3. Update model metadata and version
4. Tag as "available" or "deprecated"

### Step 6: Deployment
1. Models available for inference services
2. Real-time overlay queries latest model
3. Content recommender uses registered models
4. Performance optimizer provides recommendations

---

## 🛠️ Configuration Options

### Training Parameters
```python
{
    'visitor-behavior-model': {
        'type': 'neural-network',
        'epochs': 100,              # Training epochs
        'batch_size': 32,           # Batch size
        'learning_rate': 0.001,     # Learning rate
        'dropout': 0.3,             # Dropout rate
        'activation': 'relu'        # Activation function
    }
}
```

### Model Versions
- Each model can have multiple versions
- Format: `model-name:version-number`
- Latest model deployed by default
- Older versions available for rollback

### Queue Configuration
- Queue name: `ai-training-jobs`
- Visibility timeout: 30 minutes
- Max retries: 3
- TTL: 7 days

---

## 📈 Monitoring & Logging

### Training Metrics Tracked
- Training loss over epochs
- Validation accuracy
- Training time
- Memory usage
- GPU utilization (if available)

### Model Performance Metrics
- Accuracy / F1 Score
- Precision & Recall
- AUC-ROC
- Confusion Matrix
- Feature Importance

### System Metrics
- Queue length
- Job completion time
- Model storage usage
- Training service uptime

### Logging Levels
```python
logging.DEBUG    # Detailed training steps
logging.INFO     # Job status and milestones
logging.WARNING  # Performance issues
logging.ERROR    # Training failures
```

---

## 🔐 Security & Best Practices

### Access Control
- Use Azure Managed Identity for authentication
- Store credentials in Azure Key Vault
- Enable storage account firewall
- Use SAS tokens with time expiration

### Data Privacy
- Anonymize PII in datasets
- Enable encryption at rest
- Use TLS for data in transit
- Regular data retention cleanup

### Model Safety
- Version all models
- Keep model metadata with code
- Test models before deployment
- Monitor prediction drift

### Cost Optimization
- Use spot instances for training
- Clean up old datasets/models
- Monitor storage costs
- Schedule off-peak training

---

## 🚨 Troubleshooting

### Training Job Fails
```
Error: Queue message processing failed
Solution: Check AZURE_STORAGE_CONNECTION_STRING environment variable
```

### Dataset Not Found
```
Error: Blob not found in ai-training-datasets
Solution: Verify dataset is uploaded with correct blob name
```

### Model Performance Degradation
```
Issue: Model accuracy dropping over time
Solution: Retrain with latest data, check for dataset drift
```

### GPU Memory Error
```
Error: CUDA out of memory
Solution: Reduce batch_size or use gradient accumulation
```

### Queue Timeout
```
Error: Message not processed within visibility timeout
Solution: Increase timeout or optimize training efficiency
```

---

## 📋 Deployment Checklist

- [ ] Azure Storage Account created
- [ ] ai-training-datasets container created
- [ ] ml-models container created
- [ ] ai-training-jobs queue created
- [ ] Storage credentials configured
- [ ] Python dependencies installed
- [ ] Connection string set in environment
- [ ] Training datasets uploaded
- [ ] Pipeline script deployed
- [ ] Logging configured
- [ ] Monitoring alerts set up
- [ ] First model trained successfully

---

## 🎓 Advanced Topics

### Hyperparameter Tuning
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 150, 200],
    'max_depth': [10, 15, 20],
    'learning_rate': [0.01, 0.1, 0.5]
}

grid_search = GridSearchCV(model, param_grid)
```

### Transfer Learning
```python
from tensorflow.keras.applications import VGG16

base_model = VGG16(weights='imagenet', include_top=False)
x = base_model.output
# Add custom layers...
```

### Model Ensembling
```python
from sklearn.ensemble import VotingClassifier

ensemble = VotingClassifier(
    estimators=[
        ('rf', RandomForestClassifier()),
        ('gb', GradientBoostingClassifier()),
        ('xgb', XGBClassifier())
    ]
)
```

### Automated ML
```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import AutoML

automl = AutoML(
    task="classification",
    primary_metric="accuracy"
)
```

---

## 📚 Resources

- **TensorFlow Documentation:** https://www.tensorflow.org/docs
- **Scikit-learn Guide:** https://scikit-learn.org
- **Azure Storage SDK:** https://docs.microsoft.com/azure/storage/
- **MLflow Model Registry:** https://mlflow.org

---

**Status:** Reference guide for the `ai-training-pipeline.py` module and `training/` folder in this repository.

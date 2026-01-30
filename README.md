# AI Training Pipeline

A universal, production-ready training pipeline supporting both PyTorch and TensorFlow frameworks.

## Features

- 🔥 **Dual Framework Support**: Seamlessly switch between PyTorch and TensorFlow
- 📊 **Training Monitoring**: Built-in metrics tracking, logging, and visualization
- 💾 **Checkpoint Management**: Automatic model checkpointing with best model saving
- ⚡ **Early Stopping**: Prevents overfitting with configurable patience
- 🎯 **Easy Configuration**: JSON-based configuration system
- 📈 **Training History**: Automatic tracking and saving of training metrics
- 🖥️ **Device Agnostic**: Automatic GPU/CPU detection and usage

## Installation

```bash
# Clone the repository
cd C:\NetworkBuster\Git\ai-training-pipeline

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from train_pipeline import TrainingConfig, TrainingPipeline

# Create configuration
config = TrainingConfig(
    model_name="my_model",
    framework="pytorch",  # or "tensorflow"
    epochs=10,
    batch_size=32,
    learning_rate=0.001
)

# Initialize pipeline
pipeline = TrainingPipeline(config)

# Build model
model = pipeline.build_pytorch_model(input_shape=(28, 28), num_classes=10)

# Train (assuming you have train_loader and val_loader)
model = pipeline.train_pytorch(model, train_loader, val_loader, num_classes=10)

# Evaluate
pipeline.evaluate(model, test_loader)
```

### Run Demo

```bash
# PyTorch demo
python train_pipeline.py

# For TensorFlow, edit train_pipeline.py and change:
# framework="tensorflow"
```

## Configuration Options

```python
TrainingConfig(
    model_name="default_model",          # Model identifier
    framework="pytorch",                  # "pytorch" or "tensorflow"
    epochs=10,                           # Number of training epochs
    batch_size=32,                       # Batch size
    learning_rate=0.001,                 # Learning rate
    optimizer="adam",                    # Optimizer type
    loss_function="cross_entropy",       # Loss function
    data_dir="./data",                   # Data directory
    output_dir="./outputs",              # Output directory
    checkpoint_dir="./checkpoints",      # Checkpoint directory
    log_dir="./logs",                    # Log directory
    validation_split=0.2,                # Validation split ratio
    random_seed=42,                      # Random seed
    device="auto",                       # "auto", "cpu", "cuda", "mps"
    save_best_only=True,                 # Save only best model
    early_stopping_patience=5            # Early stopping patience
)
```

## Project Structure

```
ai-training-pipeline/
├── train_pipeline.py       # Main training pipeline
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── outputs/               # Training outputs (created automatically)
├── checkpoints/           # Model checkpoints (created automatically)
└── logs/                  # Training logs (created automatically)
```

## Custom Model Integration

### PyTorch

```python
def build_custom_pytorch_model():
    import torch.nn as nn
    
    class CustomModel(nn.Module):
        def __init__(self):
            super().__init__()
            # Define your architecture here
            
        def forward(self, x):
            # Define forward pass
            return x
    
    return CustomModel()
```

### TensorFlow

```python
def build_custom_tensorflow_model():
    import tensorflow as tf
    
    model = tf.keras.Sequential([
        # Add your layers here
    ])
    
    return model
```

## Training Outputs

After training, you'll find:

- **Checkpoints**: Best model saved in `checkpoints/`
- **Training History**: JSON file with loss/accuracy metrics in `outputs/`
- **Logs**: TensorBoard logs in `logs/` (TensorFlow only)

## Visualize Training (TensorFlow)

```bash
tensorboard --logdir=./logs
```

## Advanced Features

### Custom Data Loading

```python
# PyTorch
from torch.utils.data import Dataset, DataLoader

class CustomDataset(Dataset):
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

train_loader = DataLoader(CustomDataset(X_train, y_train), 
                          batch_size=32, shuffle=True)
```

### Save and Load Config

```python
# Save
config.save("config.json")

# Load
config = TrainingConfig.load("config.json")
```

## GPU Support

The pipeline automatically detects and uses available GPUs:

- **PyTorch**: CUDA-enabled GPUs
- **TensorFlow**: CUDA or Metal (Apple Silicon)

Override with:
```python
config = TrainingConfig(device="cpu")  # Force CPU
```

## Examples

See `train_pipeline.py` main() function for a complete working example with synthetic data.

## License

MIT License - Feel free to use in your projects!

## Contributing

Contributions welcome! Please feel free to submit issues and pull requests.

## Support

For issues or questions, please open an issue on GitHub.

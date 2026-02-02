#!/usr/bin/env python3
"""
AI Training Pipeline - Universal training framework supporting PyTorch and TensorFlow
"""
import os
import json
import time
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass, asdict
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class TrainingConfig:
    """Training configuration dataclass"""
    model_name: str = "default_model"
    framework: str = "pytorch"  # "pytorch" or "tensorflow"
    epochs: int = 10
    batch_size: int = 32
    learning_rate: float = 0.001
    optimizer: str = "adam"
    loss_function: str = "cross_entropy"
    data_dir: str = "./data"
    output_dir: str = "./outputs"
    checkpoint_dir: str = "./checkpoints"
    log_dir: str = "./logs"
    validation_split: float = 0.2
    random_seed: int = 42
    device: str = "auto"  # "auto", "cpu", "cuda", "mps"
    save_best_only: bool = True
    early_stopping_patience: int = 5
    
    def save(self, path: str):
        """Save config to JSON file"""
        with open(path, 'w') as f:
            json.dump(asdict(self), f, indent=2)
    
    @classmethod
    def load(cls, path: str):
        """Load config from JSON file"""
        with open(path, 'r') as f:
            return cls(**json.load(f))


class TrainingPipeline:
    """Universal training pipeline for deep learning models"""
    
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.framework = config.framework.lower()
        self.setup_directories()
        self.setup_device()
        self.history = {
            'train_loss': [],
            'train_acc': [],
            'val_loss': [],
            'val_acc': []
        }
        
        logger.info(f"Initialized {self.framework.upper()} training pipeline")
        logger.info(f"Device: {self.device}")
    
    def setup_directories(self):
        """Create necessary directories"""
        for dir_path in [self.config.output_dir, self.config.checkpoint_dir, self.config.log_dir]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def setup_device(self):
        """Setup compute device (CPU/GPU)"""
        if self.framework == "pytorch":
            import torch
            if self.config.device == "auto":
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
            else:
                self.device = self.config.device
        elif self.framework == "tensorflow":
            import tensorflow as tf
            if self.config.device == "auto":
                gpus = tf.config.list_physical_devices('GPU')
                self.device = "GPU" if gpus else "CPU"
            else:
                self.device = self.config.device
    
    def build_pytorch_model(self, input_shape: tuple, num_classes: int):
        """Build a sample PyTorch model"""
        import torch
        import torch.nn as nn
        
        class SimpleNet(nn.Module):
            def __init__(self, input_size, num_classes):
                super(SimpleNet, self).__init__()
                self.flatten = nn.Flatten()
                self.fc1 = nn.Linear(input_size, 128)
                self.relu1 = nn.ReLU()
                self.dropout1 = nn.Dropout(0.2)
                self.fc2 = nn.Linear(128, 64)
                self.relu2 = nn.ReLU()
                self.dropout2 = nn.Dropout(0.2)
                self.fc3 = nn.Linear(64, num_classes)
            
            def forward(self, x):
                x = self.flatten(x)
                x = self.fc1(x)
                x = self.relu1(x)
                x = self.dropout1(x)
                x = self.fc2(x)
                x = self.relu2(x)
                x = self.dropout2(x)
                x = self.fc3(x)
                return x
        
        input_size = int(np.prod(input_shape))
        model = SimpleNet(input_size, num_classes)
        return model.to(self.device)
    
    def build_tensorflow_model(self, input_shape: tuple, num_classes: int):
        """Build a sample TensorFlow model"""
        import tensorflow as tf
        
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=input_shape),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(num_classes, activation='softmax')
        ])
        
        return model
    
    def train_pytorch(self, model, train_loader, val_loader, num_classes: int):
        """Train PyTorch model"""
        import torch
        import torch.nn as nn
        import torch.optim as optim
        
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=self.config.learning_rate)
        
        best_val_loss = float('inf')
        patience_counter = 0
        
        logger.info("Starting PyTorch training...")
        
        for epoch in range(self.config.epochs):
            # Training phase
            model.train()
            train_loss = 0.0
            train_correct = 0
            train_total = 0
            
            for batch_idx, (data, target) in enumerate(train_loader):
                data, target = data.to(self.device), target.to(self.device)
                
                optimizer.zero_grad()
                output = model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
                _, predicted = torch.max(output.data, 1)
                train_total += target.size(0)
                train_correct += (predicted == target).sum().item()
            
            avg_train_loss = train_loss / len(train_loader)
            train_acc = 100 * train_correct / train_total
            
            # Validation phase
            model.eval()
            val_loss = 0.0
            val_correct = 0
            val_total = 0
            
            with torch.no_grad():
                for data, target in val_loader:
                    data, target = data.to(self.device), target.to(self.device)
                    output = model(data)
                    loss = criterion(output, target)
                    
                    val_loss += loss.item()
                    _, predicted = torch.max(output.data, 1)
                    val_total += target.size(0)
                    val_correct += (predicted == target).sum().item()
            
            avg_val_loss = val_loss / len(val_loader)
            val_acc = 100 * val_correct / val_total
            
            # Update history
            self.history['train_loss'].append(avg_train_loss)
            self.history['train_acc'].append(train_acc)
            self.history['val_loss'].append(avg_val_loss)
            self.history['val_acc'].append(val_acc)
            
            logger.info(f"Epoch {epoch+1}/{self.config.epochs} - "
                       f"Train Loss: {avg_train_loss:.4f}, Train Acc: {train_acc:.2f}% - "
                       f"Val Loss: {avg_val_loss:.4f}, Val Acc: {val_acc:.2f}%")
            
            # Save best model
            if avg_val_loss < best_val_loss:
                best_val_loss = avg_val_loss
                patience_counter = 0
                checkpoint_path = os.path.join(self.config.checkpoint_dir, 
                                              f"{self.config.model_name}_best.pth")
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'loss': avg_val_loss,
                }, checkpoint_path)
                logger.info(f"Saved best model to {checkpoint_path}")
            else:
                patience_counter += 1
            
            # Early stopping
            if patience_counter >= self.config.early_stopping_patience:
                logger.info(f"Early stopping triggered after {epoch+1} epochs")
                break
        
        return model
    
    def train_tensorflow(self, model, train_data, val_data, num_classes: int):
        """Train TensorFlow model"""
        import tensorflow as tf
        
        # Compile model
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=self.config.learning_rate),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Setup callbacks
        callbacks = [
            tf.keras.callbacks.ModelCheckpoint(
                filepath=os.path.join(self.config.checkpoint_dir, 
                                     f"{self.config.model_name}_best.h5"),
                save_best_only=self.config.save_best_only,
                monitor='val_loss',
                verbose=1
            ),
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=self.config.early_stopping_patience,
                restore_best_weights=True,
                verbose=1
            ),
            tf.keras.callbacks.TensorBoard(
                log_dir=self.config.log_dir,
                histogram_freq=1
            )
        ]
        
        logger.info("Starting TensorFlow training...")
        
        # Train model
        history = model.fit(
            train_data,
            validation_data=val_data,
            epochs=self.config.epochs,
            callbacks=callbacks,
            verbose=1
        )
        
        # Update history
        self.history['train_loss'] = history.history['loss']
        self.history['train_acc'] = [acc * 100 for acc in history.history['accuracy']]
        self.history['val_loss'] = history.history['val_loss']
        self.history['val_acc'] = [acc * 100 for acc in history.history['val_accuracy']]
        
        return model
    
    def save_training_history(self):
        """Save training history to JSON"""
        history_path = os.path.join(self.config.output_dir, 
                                    f"{self.config.model_name}_history.json")
        with open(history_path, 'w') as f:
            json.dump(self.history, f, indent=2)
        logger.info(f"Saved training history to {history_path}")
    
    def evaluate(self, model, test_loader):
        """Evaluate model on test data"""
        if self.framework == "pytorch":
            return self._evaluate_pytorch(model, test_loader)
        elif self.framework == "tensorflow":
            return self._evaluate_tensorflow(model, test_loader)
    
    def _evaluate_pytorch(self, model, test_loader):
        """Evaluate PyTorch model"""
        import torch
        
        model.eval()
        test_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(self.device), target.to(self.device)
                output = model(data)
                _, predicted = torch.max(output.data, 1)
                total += target.size(0)
                correct += (predicted == target).sum().item()
        
        accuracy = 100 * correct / total
        logger.info(f"Test Accuracy: {accuracy:.2f}%")
        return accuracy
    
    def _evaluate_tensorflow(self, model, test_data):
        """Evaluate TensorFlow model"""
        results = model.evaluate(test_data, verbose=1)
        accuracy = results[1] * 100
        logger.info(f"Test Accuracy: {accuracy:.2f}%")
        return accuracy


def create_sample_data(num_samples: int = 1000, input_shape: tuple = (28, 28), 
                       num_classes: int = 10, framework: str = "pytorch"):
    """Create sample synthetic data for demonstration"""
    logger.info(f"Creating sample dataset: {num_samples} samples, shape {input_shape}, {num_classes} classes")
    
    X = np.random.randn(num_samples, *input_shape).astype(np.float32)
    y = np.random.randint(0, num_classes, num_samples)
    
    # Split into train/val/test
    train_size = int(0.7 * num_samples)
    val_size = int(0.15 * num_samples)
    
    X_train, y_train = X[:train_size], y[:train_size]
    X_val, y_val = X[train_size:train_size+val_size], y[train_size:train_size+val_size]
    X_test, y_test = X[train_size+val_size:], y[train_size+val_size:]
    
    if framework == "pytorch":
        import torch
        from torch.utils.data import TensorDataset, DataLoader
        
        train_dataset = TensorDataset(torch.FloatTensor(X_train), torch.LongTensor(y_train))
        val_dataset = TensorDataset(torch.FloatTensor(X_val), torch.LongTensor(y_val))
        test_dataset = TensorDataset(torch.FloatTensor(X_test), torch.LongTensor(y_test))
        
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
        test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
        
        return train_loader, val_loader, test_loader
    
    elif framework == "tensorflow":
        import tensorflow as tf
        
        train_data = tf.data.Dataset.from_tensor_slices((X_train, y_train)).batch(32).prefetch(tf.data.AUTOTUNE)
        val_data = tf.data.Dataset.from_tensor_slices((X_val, y_val)).batch(32).prefetch(tf.data.AUTOTUNE)
        test_data = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(32).prefetch(tf.data.AUTOTUNE)
        
        return train_data, val_data, test_data


def main():
    """Main training function"""
    # Create configuration
    config = TrainingConfig(
        model_name="demo_model",
        framework="pytorch",  # Change to "tensorflow" to use TensorFlow
        epochs=5,
        batch_size=32,
        learning_rate=0.001,
        early_stopping_patience=3
    )
    
    # Save config
    config.save(os.path.join(config.output_dir, "config.json"))
    
    # Initialize pipeline
    pipeline = TrainingPipeline(config)
    
    # Create sample data
    input_shape = (28, 28)
    num_classes = 10
    
    if config.framework == "pytorch":
        train_loader, val_loader, test_loader = create_sample_data(
            num_samples=1000, 
            input_shape=input_shape, 
            num_classes=num_classes,
            framework="pytorch"
        )
        
        # Build and train model
        model = pipeline.build_pytorch_model(input_shape, num_classes)
        model = pipeline.train_pytorch(model, train_loader, val_loader, num_classes)
        
        # Evaluate
        pipeline.evaluate(model, test_loader)
        
    elif config.framework == "tensorflow":
        train_data, val_data, test_data = create_sample_data(
            num_samples=1000,
            input_shape=input_shape,
            num_classes=num_classes,
            framework="tensorflow"
        )
        
        # Build and train model
        model = pipeline.build_tensorflow_model(input_shape, num_classes)
        model = pipeline.train_tensorflow(model, train_data, val_data, num_classes)
        
        # Evaluate
        pipeline.evaluate(model, test_data)
    
    # Save training history
    pipeline.save_training_history()
    
    logger.info("Training pipeline completed successfully!")


if __name__ == "__main__":
    main()

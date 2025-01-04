# Task 2: AI Model for Medical Image Classification

## Overview

This task focuses on the development and deployment of an **AI model** capable of classifying medical images into categories of key organs such as the **heart**, **brain**, **liver**, and **limbs**. The system leverages deep learning techniques for accurate predictions and includes a user-friendly GUI for interaction.

The project integrates a pre-trained model for feature extraction and fine-tunes it on a custom dataset of medical images.

---

## Features

### Model Training and Evaluation
- **Pre-trained Model**: Utilizes a state-of-the-art pre-trained CNN (e.g., ResNet, VGG) for feature extraction.
- **Fine-tuning**: Adapts the model to medical image classification.
- **Performance Metrics**: Provides accuracy, precision, recall, and F1 score for evaluation.

### GUI Interface
- **Upload Functionality**: Allows users to upload images for prediction.
- **Predicted Results**: Displays the predicted organ category with confidence scores.

### Scalability
- Designed for expansion to additional organ categories and datasets.

---

## Installation

### Prerequisites
- Python 3.8 or later
- Required libraries:
  - `tensorflow` or `torch` (depending on the model)
  - `numpy`
  - `matplotlib`
  - `Pillow`
  - `PyQt5`

---

## Application Interface

### 1. GUI Components
- **Upload Button**: Load a medical image for classification.
- **Prediction Output**: Displays the predicted organ category with confidence.

### 2. Training Process
- Command-line-based interface for monitoring model training progress.
- Generates performance metrics and visualizations of model accuracy/loss.

 ---

 ## Technical Details

### Model Architecture

- **Base Model**: Utilizes a pre-trained convolutional neural network (e.g., ResNet50 or EfficientNet).
- **Classifier Head**:
  - Fully connected layers for classification.
  - Output layer with softmax activation for multi-class classification.

### Dataset

- Images categorized into organ types (e.g., heart, brain, liver, limbs).
- Dataset split into training, validation, and testing subsets.

### Training Pipeline

- **Image Preprocessing**: Resizing, normalization, and data augmentation.
- **Optimization**: Adam optimizer with learning rate scheduling.
- **Loss Function**: Categorical cross-entropy.

### Evaluation

- **Confusion Matrix**: Visualizes classification performance.
- **Metrics**: Accuracy, precision, recall, F1-score.

---

## Known Limitations

- Limited to the pre-defined categories (heart, brain, liver, limbs).
- Requires a high-quality labeled dataset for optimal performance.

---

## Future Enhancements

- Extend support to additional organ categories.
- Integrate explainability tools like Grad-CAM for model interpretability.
- Automate dataset preprocessing and augmentation.

 

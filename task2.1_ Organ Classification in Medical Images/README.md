# Task 2: AI Model for Medical Image Classification

## Overview

This task focuses on the development and deployment of an **AI model** capable of classifying medical images into categories of key organs such as the **breast**, **brain**, **kidney**, and **lungs**. The system leverages deep learning techniques for accurate predictions and includes a user-friendly GUI for interaction.

The project Uses transfer learning with VGG16, the model achieves robust performance with an organized dataset and effective preprocessing.

---
## Features

### Model Training and Evaluation
- **Pre-trained Model**: Utilizes a state-of-the-art pre-trained CNN ( VGG) for feature extraction.  
- **Fine-tuning**: Adapts the model to medical image classification.
- **Performance Metrics**: Provides accuracy, precision, recall, and F1 score for evaluation.

### GUI Interface
- **Upload Functionality**: Allows users to upload images for prediction.
- **Predicted Results**: Displays the predicted organ category with confidence scores.
<img src="https://github.com/abdullah-gamil05/ImageBasedAnatomy_Tasks/blob/main/assets/prediction1.png" alt="Result 1" width="600" />

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

### How to Run
1. Clone the repository:

```bash
git clone https://github.com/abdullah-gamil05/task2.1_Organ Classification in Medical Images.git
```
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

  - Uses VGG16 pre-trained on ImageNet for feature extraction.
  - Adapts grayscale images to RGB for compatibility with VGG16.
  - Includes additional Dense layers for classification.
  - 
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

 ## Acknowledgements
- **Datasets**:
  - Brain Tumor MRI Dataset
  - Breast Cancer Patient MRIs
  - Liver Dataset
  - Cardiomegaly Disease Prediction Dataset
- **Pre-trained Model**: VGG16 weights from ImageNet


 

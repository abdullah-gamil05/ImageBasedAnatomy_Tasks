# Installation Guide for Task 2: Classification Model

## Prerequisites
1. Ensure you have Python 3.7 or above installed. You can download it from [python.org](https://www.python.org/).
2. Install `pip`, the Python package manager, if not already available.
3. (Optional) Set up a virtual environment for the project:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate    # On Windows
   ```

## Steps
1. Clone the repository:
   ```bash
   git clone <repository_link>
   ```
2. Navigate to the project directory:
   ```bash
   cd task2_classification_model
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python src/main.py
   ```

## Notes
- Ensure TensorFlow supports your system (e.g., CPU or GPU).
- Use the `data/` folder to place your training and testing datasets.

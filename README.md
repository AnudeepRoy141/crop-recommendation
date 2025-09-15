A machine learning-based crop recommendation system that suggests the most suitable crop to grow based on soil and environmental parameters. The project uses Python, scikit-learn, and a dataset containing features like nitrogen, phosphorus, potassium, temperature, humidity, pH, and rainfall. The model predicts the best crop for given conditions, helping farmers make data-driven decisions.

## Features

- Predicts optimal crop based on user input
- Utilizes a trained machine learning model (Random Forest)
- Simple CLI or web interface for predictions
- Easy to extend with more data or features

## Getting Started

1. **Clone the repository:**

**Contributors:**  
- [Anudeep Roy](https://github.com/AnudeepRoy)  
- [Protyay Banerjee](https://github.com/Protyay-Banerjee)  

We both collaborated to create this repository and wrote all the code.
    ```bash
    git clone https://github.com/AnudeepRoy/crop-recommendation.git
    cd crop-recommendation
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application:**
    ```bash
    # To run this Streamlit app, use the following command in your terminal:
    streamlit run app.py
    ```

## Usage

- Input soil and weather parameters when prompted.
- The system will output the recommended crop.

## Dataset

The dataset includes:
- Nitrogen, Phosphorus, Potassium levels
- Temperature, Humidity, pH, Rainfall
- Crop label

## Model

- Random Forest Classifier trained on the dataset
- Model accuracy and evaluation metrics available in the notebook

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

## License

All rights reserved. This project is not licensed for free use, distribution, or modification without explicit permission from the author.

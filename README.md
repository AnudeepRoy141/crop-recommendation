A RAG based crop recommendation system that suggests the most suitable crop to grow based on soil and environmental parameters. The project uses Python, scikit-learn, and a dataset containing features like nitrogen, phosphorus, potassium, temperature, humidity, pH, and rainfall. The model predicts the best crop for given conditions, helping farmers make data-driven decisions.

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

### Realtime Crop Data (optional)

`data/crop_database.py` can pull realtime crop metadata when these environment variables are set:

- `CROP_API_URL`: HTTPS endpoint returning a JSON list (or an object with `data` list) of crops
- `CROP_API_KEY`: API key for authorization (sent as `Authorization: Bearer` and `x-api-key`)
- `CROP_API_CACHE_TTL_SECONDS` (optional): Cache TTL in seconds, default `900`

Example run:

```bash
CROP_API_URL="https://api.example.com/v1/crops" \
CROP_API_KEY="your_api_key_here" \
streamlit run app.py
```

Notes:
- If the API fails or is not configured, the app falls back to the built‑in static dataset.
- Realtime data are normalized and merged with static defaults (by `name`) to keep required fields intact.

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

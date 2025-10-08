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

## Real-time Market Pricing (API-key, non-government)

This project now supports optional real-time crop price updates from a commercial API provider (excluding open government APIs). When enabled, live INR prices per quintal are fetched at runtime and used to recompute ROI and profit across recommendations and dashboards.

### What changed
- A new `LivePriceProvider` in `utils/data_analyzer.py` fetches prices via API key.
- `get_crop_database(region=None)` in `data/crop_database.py` attempts to replace each crop's `market_price` with a live value if credentials are set, then recomputes `profit_margin` and `roi`.
- `get_suitable_crops_for_climate(...)` accepts a `region` and uses `get_crop_database(region)` so pages receive updated prices.

### Configure
Set the following environment variables (for example in your shell or process manager):

```bash
export MARKET_API_BASE_URL="https://your-commercial-provider.example.com"
export MARKET_API_KEY="<your_api_key>"
export MARKET_API_TIMEOUT=8   # optional (seconds)
```

Expected request contract (provider-agnostic):
- Method: GET `{BASE}/v1/prices?crop_name=<name>&region=<India or state>`
- Headers: `Authorization: Bearer <API_KEY>`; `Accept: application/json`
- Response JSON example:

```json
{ "crop_name": "Soybean", "currency": "INR", "unit": "quintal", "price": 4800 }
```

Notes:
- Units are normalized: `quintal` kept as-is, `ton/tonne` divided by 10, `kg` multiplied by 100.
- Only `INR` currency is accepted; other currencies are ignored.
- If the API is unreachable or returns unexpected data, the system silently falls back to static default prices bundled in `data/crop_database.py`.

### Region-awareness
When a region is selected in the UI, that region name is forwarded to the price query (`region` param) to allow providers to return region-specific prices.

### Disable live pricing
Simply omit `MARKET_API_BASE_URL` and `MARKET_API_KEY` to continue using static prices.

### Scope
This integration avoids open government APIs per project requirements and is intended for commercial/third-party data sources only.

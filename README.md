# stockmeme
 Stock and Option Prediction AI built with LLM and LSTM model

## Installation

### Method 1: Using pip with requirements.txt
1. Clone the repository
```bash
git clone https://github.com/yourusername/stockmeme.git
cd stockmeme
```

2. Install dependencies using pip
```bash
pip install -r requirements.txt
```

### Method 2: Install as a package
1. Clone the repository
```bash
git clone https://github.com/yourusername/stockmeme.git
cd stockmeme
```

2. Install as a package
```bash
pip install -e .
```

### Environment Setup
Create a `.env` file in the root directory with your API keys:
```
OPENROUTER_API_KEY=your_openrouter_api_key
```

## Usage

### Local Development
Run the server locally:
```bash
python server.py
```

Access the API at `http://localhost:5000/result/<stock_symbol>/<model>`

Example:
```
http://localhost:5000/result/NVDA/deepseek-r1
```

### Deployment
The project includes files for deployment to platforms like Heroku:
- `Procfile` - Specifies the command to run the server
- `runtime.txt` - Specifies the Python version (3.9.18)

To deploy to Heroku:
```bash
heroku create
git push heroku main
```

## Available Models
- deepseek-r1
- deepseek-v3
- gemini-flash-lite-2.0
- gemini-flash-thinking-exp
- gemini-pro-2.0

## Troubleshooting

### Package Installation Issues
If you encounter installation errors, particularly with pandas:
1. Try using a Python version between 3.7 and 3.11 (3.9 recommended)
2. Install numpy first: `pip install numpy==1.24.3`
3. Then install other requirements: `pip install -r requirements.txt`

### API Key Issues
If you receive authentication errors:
1. Verify your OPENROUTER_API_KEY is correct
2. Check if you have reached API rate limits
3. Try a different LLM model in your request

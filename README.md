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

3. Set up environment variables
Create a `.env` file in the root directory with your API keys:
```
OPENROUTER_API_KEY=your_openrouter_api_key
```

## Usage

1. Run the server
```bash
python server.py
```

2. Access the API at `http://localhost:5000/result/<stock_symbol>/<model>`

Example:
```
http://localhost:5000/result/NVDA/deepseek-r1
```

## Available Models
- deepseek-r1
- deepseek-v3
- gemini-flash-lite-2.0
- gemini-flash-thinking-exp
- gemini-pro-2.0

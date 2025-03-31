from setuptools import setup, find_packages

setup(
    name="stockmeme",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-dotenv",
        "requests",
        "pandas",
        "google-search-results",
        "googlesearch-python",
        "openai",
        "flask",
        "flask-cors",
        "python-dateutil",
    ],
    author="",
    author_email="",
    description="Stock and Option Prediction AI built with LLM and LSTM model",
    keywords="stock, prediction, AI, LLM, LSTM",
    url="https://github.com/yourusername/stockmeme",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
) 
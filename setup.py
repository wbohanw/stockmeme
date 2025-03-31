from setuptools import setup, find_packages

setup(
    name="stockmeme",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-dotenv==1.0.0",
        "requests==2.31.0",
        "pandas==1.5.3",
        "google-search-results==2.4.2",
        "googlesearch-python==1.2.3",
        "openai==1.12.0",
        "flask==2.3.3",
        "flask-cors==4.0.0",
        "python-dateutil==2.8.2",
        "numpy==1.24.3",
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
    python_requires=">=3.7, <3.12",
) 
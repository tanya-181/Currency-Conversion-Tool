# Currency Conversion Tool using LangChain

A simple currency conversion tool built using LangChain, Google Gemini, and ExchangeRate API.

## Overview

This project demonstrates how an LLM can use external tools to perform a currency conversion.

The application uses two tools:

1. `get_conversion_factor`
   - Fetches the exchange rate between two currencies using ExchangeRate API.

2. `convert`
   - Converts a given amount using the exchange rate.

## Architecture

User Query
    ↓
Google Gemini
    ↓
Tool Call
    ↓
get_conversion_factor
    ↓
ExchangeRate API
    ↓
Conversion Rate
    ↓
convert
    ↓
Final Currency Value

## Technologies Used

- Python
- LangChain
- Google Gemini
- ExchangeRate API
- python-dotenv
- Requests

## Example

Input:

"What is the conversion factor between SGD and INR, and based on that can you convert 20 SGD to INR?"

The application:

1. Identifies the required currencies.
2. Calls the currency conversion API.
3. Retrieves the conversion rate.
4. Uses the `convert` tool to calculate the converted amount.
5. Returns the final result.

Install dependensies by:
pip install -r requirements.txt

Create a .env file:
GOOGLE_API_KEY=your_google_gemini_api_key
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key

Run the application:
python currency_conversion_tool.py

**Key LangChain Concepts Demonstrated**
Tool creation using @tool
Tool binding using bind_tools()
Tool calls
Tool execution using .invoke()
InjectedToolArg
Message history
Calling external APIs from tools


Learning Outcome:
This project demonstrates how an LLM can interact with external APIs through LangChain tools instead of relying only on its internal knowledge.

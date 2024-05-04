"""
This is a simple FastAPI server that provides random quotes
based on a specified category.

To launch this server from bash, navigate to the directory containing this file and run the following command:
uvicorn main:app --reload

To test the server from the terminal, you can use curl or any other HTTP client. Here's an example using curl:
curl http://localhost:8000/quote/{category}

Also, you can access the server from a web browser by visiting the following URL:

http://localhost:8000/static/index.html

Replace {category} with the desired category for the quote.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
import pandas as pd
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.staticfiles import StaticFiles


data = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    global data
    data["quotes"] = pd.read_csv("quotes.csv")
    yield

    # Clean up and release the resources
    # Normally, like database connections, server-based caches, etc.
    # For a simple memory based variables, don't really need to
    # del, but for demonstration purposes, we are doing it here.
    del data


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/quote/{category}")
@app.get("/quote")
async def get_random_quote(category: str = "None", format: str = "txt"):
    """
    Get a random quote from the specified category.

    Parameters:
    - category (str): The category of the quote.
    - format (str): The desired response format. Default is "txt".

    Returns:
    - dict: A dictionary containing the random quote. If no quotes are found for the specified category, an error message is returned.
    """

    quotes = data["quotes"]

    if "category" in quotes.columns:
        # Filter quotes based on the category
        filtered_quotes = quotes[quotes["category"].str.contains(category, case=False)]

        if not filtered_quotes.empty:
            # Select a random quote
            random_quote = filtered_quotes.sample(n=1)
            return get_response(random_quote["quote"].values[0], format)

    # Select a random quote if no category or no quotes found for the specified category
    random_quote = quotes.sample(n=1)
    return get_response(random_quote["quote"].values[0], format)


def get_response(quote: str, format: str = "txt"):
    """
    Get the appropriate response based on the desired format.

    Parameters:
    - quote (str): The quote to be included in the response.
    - format (str): The desired response format.

    Returns:
    - Response: The appropriate response object based on the desired format.
    """
    if format == "txt":
        return PlainTextResponse(quote + "\n")
    elif format == "json":
        return JSONResponse({"quote": quote})
    else:
        return PlainTextResponse("Supported formats: txt, json, and xml.")

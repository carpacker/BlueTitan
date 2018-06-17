This project is home to a suite of API wrappers relevant to cryptocurrency, specifically exchanges and mining pool sites. The API is organized by those two categories and includes a generic API for both. In the future this readme will offer a comprehensive description of the intricacies of the generic APIs.

# General

The API system is organized as follows: each separate conceptual grouping is contained within its own folders (ExchangeAPIs, MiningAPIS), each grouping has a .py container script for all API wrappers and derivative calls pertaining to a specific entity (ExchangesAPIS --> Binance, Bittrex, ...) an each grouping has a genericAPI which provides formatting and standardization of inputs and outputs.
Each grouping will have a README.md describing how the inputs and outputs are standardized. This will be formatted in a manner like:

TODO

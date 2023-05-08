# Measuring Starlink Latency from RIPE Atlas

## Authors: Ben Kogan, Margia Rounok, Robert Zhao

This repository contains the code we used to:
- Request the probes connected to the Starlink network
- Create ping measurment every 15 minutes for one day
- Retrieve the results with average RTTs over time for each probe
- Plot the results for analysis

To run the code, enter:
`python main.py`

The code currently retrieves the results from our measurement and saves the plot images to the "graphs/combined" directory. By default, the plots combine all of the results from each probes into one plot for each region, but you can specify the "separate" command-line argument to plot each probe separately. These will be saved to the "graphs/separate" directory. 

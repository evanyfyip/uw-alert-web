# Component Specification 
The document should have sections for.
Software components. High level description of the software components such as: data manager, which provides a simplified interface to your data and provides application specific features (e.g., querying data subsets); and visualization manager, which displays data frames as a plot. Describe at least 3 components specifying: what it does, inputs it requires, and outputs it provides. If you have more significant components in your system, we highly suggest documenting those as well.
Interactions to accomplish use cases. Describe how the above software components interact to accomplish your use cases. Include at least one interaction diagram.
Preliminary plan. A list of tasks in priority order.

## Software Component

**Front End manager:**
The Front End manager implements the front end and back end connection by using flask to display a plotly plot through HTML and javascript on a webpage. 
The Front End manager requires a figure produced by the plot manager in order to return a JSON variable that encodes the visualization. 
The Front End manager returns a render template that communicates with the HTML file in the current directory to display the JSON dump as a visualzation on a webpage. 

**Visualization Manager:** The visualization manager implements the creation of a plotly plot using data scraped from the UW Alerts Webpage. 

The visualization manager requires numerous python packages, ranging from pandas, geopandas, plotly, and matplotlib. It also requires a csv file which indicates incidents of crime and the area.

The visualization manager returns the figure visualization of the map of seattle/u-district which lines indicating which areas are deemed unsafe at the current moment. 

**Text Manager:**

The text manager implements the parsing/scraping of the UW alerts website in order to update the application with new incidents of crime.

The text manager requires 

The text manager returns the csv file with crime incidents with severity, time, location, and radius. 

## Preliminary Plan


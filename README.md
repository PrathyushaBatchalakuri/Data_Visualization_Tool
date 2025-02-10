# Data Visualization Tool

### Introduction
This project involves enabling users to upload incident-related PDF files or provide URLs to such files, dynamically validate inputs, and generate visualizations. The visualizations include clustering scatter plots, bar charts, and heatmaps to analyze incident data patterns.

---
## How to Install
1. Ensure you have `pipenv` installed on your system. If not, install it with:
    ```bash
    pip install pipenv
    ```

2. Install the project's dependencies:
    ```bash
    pipenv install
    ```

## How to Run


Start the application:

```bash
pipenv run python app.py
```
* Open a web browser and navigate to http://127.0.0.1:5000/.
* On the web page:
    * Enter PDF URLs: Input one or more URLs separated by commas.
    * Upload PDFs: Use the file upload interface to upload one or more local PDF files.
* Click "Generate Visualizations" to process the files and view results in the dynamically generated visualizations page.

## Output

An interactive webpage displaying three insightful visuals.

---
## Features

- **Dynamic Input Handling**: Users can input either URLs of PDF files or upload local PDF files dynamically. Warnings and validations ensure a seamless user experience.
- **Interactive Visualizations**: The tool generates detailed visualizations for better insights into the incident data:
  - Clustering scatter plots to identify patterns and groupings.
  - Bar graphs to compare the frequency of incident types.
  - Heatmaps to highlight areas with the highest incident intensity.
- **Responsive Design**: The UI is designed with Bootstrap to ensure compatibility across devices and screen sizes.
---
## Code Structure

- app.py: The main application entry point that initializes and runs the Flask server to serve the web interface and handle input requests for processing and visualization.
- main.py: Contains core logic for processing uploaded PDFs or URLs, extracting data, and generating visualizations.
- index.html: Main landing page where users can input URLs or upload files.
- form-validation.js: JavaScript code handling dynamic validations and input management.
- results.html: Page displaying the generated visualizations, including clustering, bar graphs, and heatmaps.
---
## Resources Used  

### Frontend  
- **HTML**:  
  - Used to structure the user interface (`index.html` and `results.html`).  
  - Includes Bootstrap for responsive design and consistent styling.  
- **CSS**:  
  - Custom styles in `index.html` and `results.html` to enhance visual appeal.  
- **JavaScript**:  
  - Validation and dynamic input handling implemented in `form-validation.js`.  
  - Event handling for file inputs and URL validation.  

### Backend  
- **Python**:  
  - Flask framework used in `app.py` to handle routing and serve web pages.  
  - Core logic in `main.py` for fetching PDFs, extracting data, and generating visualizations.  

### Libraries and Frameworks  
- **Bootstrap (4.5.2)**:  
  - Provides a mobile-friendly, responsive design.  
  - Used for buttons, containers, and form styling.  
- **Flask**:  
  - Lightweight Python web framework for serving the application.  
- **Python Libraries**:  
  - Libraries for PDF data extraction (not explicitly shown but assumed, e.g., PyPDF2 or pdfminer).  
  - Visualization generation libraries (e.g., matplotlib, seaborn, or plotly).  





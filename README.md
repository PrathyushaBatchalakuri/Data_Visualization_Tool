# CIS6930, Fall 2024 Project 3 - Data Visualization

#### Name: 
Prathyusha Batchalakuri. Gator link: batchalakuri.p

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
## Key Functions  

### `app.py`  
- **Purpose**: Acts as the main application entry point, initializing and running a Flask server to handle front-end and back-end communication.  
- **Functions**:
  - **Home Page (`/`)**:
    - Serves the `index.html` file, providing the user interface for inputting PDF URLs or uploading PDF files.
  - **Process Inputs (`/process`)**:
    - Accepts user input (PDF files or URLs) from the form.
    - Uses functions from `main.py` to process the data:
      - Downloads or reads the provided PDFs.
      - Extracts data from the PDFs.
      - Generates visualizations based on the extracted data.
    - Returns results to the client or redirects to the `results.html` page.

### `main.py`  
- **Purpose**: Contains the core logic for processing input data and generating visualizations.  
- **Core Functions**:
  - **fetch_incidents(url)**:
    - **Parameters**: `url` - The URL of the PDF to be fetched.
    - **Process**:
      - Takes a URL as input and retrieves the PDF content.
      - Returns the binary data of the fetched PDF for further processing.
  - **extract_data(pdf)**:
    - **Parameters**: `pdf` - Binary data of the fetched or uploaded PDF.
    - **Process**:
      - Extracts structured data from the PDF assuming fields like date/time, location, incident type, etc.
      - Returns the extracted data in a list of dictionaries, where each dictionary represents an incident.
  - **generate_visualizations(data)**:
    - **Parameters**: `data` - Extracted incident data in a structured format.
    - **Process**:
      - Creates visualizations, including:
        - **Clustering Scatter Plot**: Groups incidents based on similarities.
        - **Bar Graph**: Shows the frequency of different incident types.
        - **Heatmap**: Highlights regions with high incident density.
      - Returns the visualizations, ready for display in `results.html`.
### `index.html`  
- **Purpose**: Serves as the primary user interface for the application, enabling users to input data and interact with the tool.  
- **Features**:
  - **Input for PDF URLs**:
    - Users can enter URLs to PDFs in a textarea input.
    - Provides a "Clear URLs" button to reset the field.
  - **Dynamic File Uploads**:
    - Users can upload one or more PDF files using dynamically added input fields.
    - Includes a button to add new file input fields and a warning system to avoid conflicts between URLs and file uploads.
  - **Form Submission**:
    - A "Generate Visualizations" button submits the form data to the back-end for processing.
  - **Responsive Design**:
    - Styled using Bootstrap for consistent layout and mobile-friendly display.


### `form-validation.js`  
#### validateInputs  
- **Process**: Dynamically ensures that only URLs or file uploads are active at a time to avoid conflicts. Provides warnings if both options are used simultaneously.

#### addFileInput  
- **Process**: Dynamically adds new file input fields to allow multiple uploads.

#### resetWarnings  
- **Process**: Resets the warning messages to ensure user guidance is updated dynamically.

### `results.html`  
- **Purpose**: Displays the generated visualizations with descriptions to help users analyze the data.  
- **Visualizations**:
  - **Clustering Scatter Plot**: Groups incidents by patterns and commonalities.
  - **Bar Graph**: Compares the frequency of incident types.
  - **Heatmap**: Highlights incident intensity and hotspots.

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

---

## Bugs and Assumptions  

### Assumptions  

   - PDF files or URLs provided by users follow a structured format containing extractable fields.  
   - Data in the PDFs is well-organized and does not contain unexpected variations.  
   - Users will input either URLs or upload files, but not both simultaneously, as enforced by validation logic in `form-validation.js`.  
   - Users will provide valid URLs or properly formatted PDF files.  

### Known Bugs  
   - If JavaScript is disabled in the browser, input validation for URLs and file uploads will not work as expected.  
   - The application may fail to extract data from PDFs that deviate from the expected structure or format.  
   - Missing fields or unexpected characters in the PDFs could lead to errors or partial data extraction.  
   - Uploading very large PDF files may exceed server handling capacity, leading to performance degradation or crashes.  
   - Complex datasets might cause visualizations to render slowly or inconsistently on the results page.  

---

## Video Demonstration
[![Watch the video](https://img.youtube.com/vi/ejB9q7kE7y4/0.jpg)](https://www.youtube.com/watch?v=ejB9q7kE7y4)




import sqlite3
import urllib.request
from pypdf import PdfReader
import ssl
import certifi
import os
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use("Agg")  # Use the Agg backend for non-GUI environments
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import seaborn as sns


# Fetch incidents from a URL
def fetchincidents(url):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
    }
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request, context=ssl_context)
    pdf_data = response.read()
    return pdf_data

# Extract incidents from PDF data
def extractincidents(pdf_data):
    pdf_buffer = BytesIO(pdf_data)
    reader = PdfReader(pdf_buffer)
    incidents = []
    for page in reader.pages:
        text = page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False)
        if text:
            lines = text.split("\n")
            for line in lines:
                if not line.strip():
                    continue
                parts = line.split("  ")
                parts = [part.strip() for part in parts if part.strip()]
                if len(parts) == 5:
                    try:
                        incident = {
                            'date_time': parts[0],
                            'incident_number': parts[1],
                            'location': parts[2],
                            'nature': parts[3],
                            'incident_ori': parts[4],
                        }
                        incidents.append(incident)
                    except IndexError:
                        continue
    return incidents

# Combine data from multiple PDFs
def load_data_from_pdfs(sources):
    combined_data = []
    for source in sources:
        try:
            if source.startswith("http"):  # URL
                print(f"Processing URL: {source}")
                pdf_data = fetchincidents(source)
            else:  # Local file
                print(f"Processing Local File: {source}")
                with open(source, "rb") as f:
                    pdf_data = f.read()

            incidents = extractincidents(pdf_data)
            combined_data.extend(incidents)
        except Exception as e:
            print(f"Error processing {source}: {e}")
    return pd.DataFrame(combined_data)


# Create database
def createdb():
    db_filename = "resources/normanpd.db"
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS incidents")
    cursor.execute('''CREATE TABLE incidents (
                        incident_time TEXT,
                        incident_number TEXT UNIQUE,
                        incident_location TEXT,
                        nature TEXT,
                        incident_ori TEXT
                      )''')
    conn.commit()
    return conn

# Populate database
def populatedb(db, incidents):
    cursor = db.cursor()
    for incident in incidents:
        cursor.execute('''INSERT OR IGNORE INTO incidents 
                          (incident_time, incident_number, incident_location, nature, incident_ori)
                          VALUES (?, ?, ?, ?, ?)''', 
                       (incident['date_time'], incident['incident_number'], 
                        incident['location'], incident['nature'], incident['incident_ori']))
    db.commit()

# Visualization 1: Clustering
def plot_clustering(df, save_path=None):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import LabelEncoder

    le = LabelEncoder()
    df['nature_encoded'] = le.fit_transform(df['nature'])
    df['location_encoded'] = le.fit_transform(df['location'])

    clustering_features = df[['nature_encoded', 'location_encoded']]
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['cluster'] = kmeans.fit_predict(clustering_features)

    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(
        df['nature_encoded'], df['location_encoded'], c=df['cluster'], cmap='tab10', s=50
    )
    plt.colorbar(scatter, label="Cluster")
    plt.title("Clustering of Incidents by Nature and Location", fontsize=16)
    plt.xlabel("Nature (Encoded)", fontsize=12)
    plt.ylabel("Location (Encoded)", fontsize=12)
    plt.tight_layout()

    if isinstance(save_path, BytesIO):
        canvas = FigureCanvas(plt.gcf())
        canvas.print_png(save_path)
    else:
        plt.savefig(save_path)

    plt.close()



# Visualization 2: Bar Graph
import plotly.express as px
from io import BytesIO

def plot_bar_graph(df, save_path=None):
    # Calculate incident counts
    incident_counts = df['nature'].value_counts().reset_index()
    incident_counts.columns = ['Incident Type', 'Number of Incidents']

    # Create the interactive bar graph
    fig = px.bar(
        incident_counts,
        x='Incident Type',
        y='Number of Incidents',
        text='Number of Incidents',
        title="Comparison of Incident Frequencies Across PDFs",
    )

    # Customize the layout for better readability
    fig.update_layout(
        xaxis_title="Incident Type",
        yaxis_title="Number of Incidents",
        xaxis=dict(tickangle=45),
        title=dict(font_size=20),
        template="plotly_white",
    )

    fig.update_traces(texttemplate='%{text}', textposition='outside')

    # Save to file or return as HTML
    if save_path:
        with open(save_path, "w") as f:
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    else:
        fig.show()



    # Visualization 3: Heatmap of Incidents by Nature and Location
def plot_heatmap(df, save_path=None):
    import matplotlib.pyplot as plt
    import seaborn as sns
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

    # Filter for the top 10 most frequent incident natures and locations
    top_natures = df['nature'].value_counts().head(10).index
    top_locations = df['location'].value_counts().head(10).index
    filtered_df = df[df['nature'].isin(top_natures) & df['location'].isin(top_locations)]

    # Create a pivot table for the heatmap
    pivot_table = pd.pivot_table(
        filtered_df, values='incident_number', index='nature', columns='location',
        aggfunc='count', fill_value=0
    )

    # Create the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(
        pivot_table, cmap='YlGnBu', annot=True, fmt='d', cbar=True,
        linewidths=0.5, linecolor='gray'
    )

    plt.title("Heatmap of Incidents (Top 10 Natures and Locations)", fontsize=16)
    plt.xlabel("Incident Location", fontsize=12)
    plt.ylabel("Incident Nature", fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()

    # Save to file or BytesIO
    if isinstance(save_path, BytesIO):
        canvas = FigureCanvas(plt.gcf())
        canvas.print_png(save_path)
    else:
        plt.savefig(save_path)

    plt.close()



# Main function
def main():
    # List of PDF URLs to process
    pdf_urls = [
        "https://www.normanok.gov/sites/default/files/documents/2024-12/2024-12-05_daily_incident_summary.pdf",
        "https://www.normanok.gov/sites/default/files/documents/2024-12/2024-12-04_daily_incident_summary.pdf",
        # Add more URLs as needed
    ]

    # Load data from multiple PDFs
    df = load_data_from_pdfs(pdf_urls)

    # Create and populate the database
    db = createdb()
    populatedb(db, df.to_dict(orient='records'))
    db.close()

    # Generate visualizations
    print("Generating Visualization 1: Clustering...")
    plot_clustering(df)

    print("Generating Visualization 2: Comparison as Bar Graph...")
    plot_bar_graph(df)

    print("Generating Visualization 3: Heatmap of Incidents by Nature and Location...")
    plot_heatmap(df)

if __name__ == "__main__":
    main()

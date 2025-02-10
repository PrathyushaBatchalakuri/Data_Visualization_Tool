from flask import Flask, request, render_template
import os
from main import load_data_from_pdfs
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

app = Flask(__name__, template_folder="src/templates")


# Define upload folder
UPLOAD_FOLDER = "project0/resources"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get URLs from the form
        pdf_urls = request.form.get("pdf_urls", "").split(",")
        pdf_urls = [url.strip() for url in pdf_urls if url.strip()]

        # Handle uploaded files
        uploaded_files = request.files.getlist("pdf_files")
        local_file_paths = []

        for file in uploaded_files:
            if file.filename:
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)
                local_file_paths.append(file_path)

        # Combine all sources (URLs and local files)
        combined_sources = pdf_urls + local_file_paths

        if not combined_sources:
            return "No PDFs provided. Please upload files or enter URLs."

        try:
            # Process the PDFs
            df = load_data_from_pdfs(combined_sources)

            # Generate interactive visualizations
            clustering_fig = plot_clustering(df)
            bar_graph_fig = plot_bar_graph(df)
            heatmap_fig = plot_heatmap(df)

            # Render the results page with interactive graphs
            return render_template(
                "results.html",
                clustering_graph=clustering_fig.to_html(full_html=False),
                bar_graph=bar_graph_fig.to_html(full_html=False),
                heatmap=heatmap_fig.to_html(full_html=False),
            )
        except Exception as e:
            return f"An error occurred: {e}"

    return render_template("index.html")


def plot_clustering(df):
    # Encode categorical variables for clustering
    df['nature_encoded'] = pd.factorize(df['nature'])[0]
    df['location_encoded'] = pd.factorize(df['location'])[0]

    # Create a scatter plot for clustering
    fig = px.scatter(
        df, x='nature_encoded', y='location_encoded',
        color=df['nature'],
        title="Clustering of Incidents by Nature and Location",
        labels={'nature_encoded': 'Nature (Encoded)', 'location_encoded': 'Location (Encoded)'}
    )
    return fig


def plot_bar_graph(df):
    # Create a bar chart for incident frequencies
    incident_counts = df['nature'].value_counts().reset_index()
    incident_counts.columns = ['Incident Type', 'Count']

    fig = px.bar(
        incident_counts, x='Incident Type', y='Count',
        title="Comparison of Incident Frequencies Across PDFs",
        labels={'Count': 'Number of Incidents', 'Incident Type': 'Incident Type'}
    )
    fig.update_layout(xaxis=dict(tickangle=45))
    return fig


def plot_heatmap(df):
    # Filter for top incidents
    top_natures = df['nature'].value_counts().head(10).index
    top_locations = df['location'].value_counts().head(10).index
    filtered_df = df[df['nature'].isin(top_natures) & df['location'].isin(top_locations)]

    # Create pivot table for heatmap
    pivot_table = pd.pivot_table(
        filtered_df, values='incident_number', index='nature', columns='location',
        aggfunc='count', fill_value=0
    )

    # Create heatmap using Plotly
    fig = go.Figure(
        data=go.Heatmap(
            z=pivot_table.values,
            x=pivot_table.columns,
            y=pivot_table.index,
            colorscale='YlGnBu'
        )
    )
    fig.update_layout(
        title="Heatmap of Incidents (Top 10 Natures and Locations)",
        xaxis=dict(title="Incident Location"),
        yaxis=dict(title="Incident Nature")
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)

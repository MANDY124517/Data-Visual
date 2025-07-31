# Nuclear Isotope Economics - Data Visualization App

An interactive Streamlit application for exploring nuclear isotopes used in non-energy applications and their economic impact.

## Features

- **3D Isotope Visualizer**: Interactive 3D visualization of isotopes with atomic structure
- **Economic Comparison**: Cost analysis and market value estimation
- **Application Explorer**: Detailed breakdown of medical, industrial, and research applications
- **Interactive Filters**: Filter isotopes by half-life and application type

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   streamlit run app.py
   ```

3. **Open your browser** and navigate to the URL shown in the terminal (usually `http://localhost:8501`)

## Dependencies

- `streamlit`: Web application framework
- `plotly`: Interactive plotting library
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computing
- `Pillow`: Image processing (PIL)

## Usage

1. **3D Isotope Visualizer Tab:**
   - Explore isotopes in 3D space (protons vs neutrons vs half-life)
   - Use sidebar filters to focus on specific isotopes
   - Click on isotopes for detailed information

2. **Economic Comparison Tab:**
   - View cost vs production scatter plots
   - Analyze market value by isotope
   - Understand economic insights

3. **Isotope Applications Tab:**
   - Explore different application sectors
   - Learn about economic impact
   - View market statistics

## Troubleshooting

If you encounter any issues:

1. **Make sure all dependencies are installed:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Check Python version:** The app requires Python 3.8 or higher

3. **Port conflicts:** If port 8501 is busy, Streamlit will automatically use the next available port

4. **Browser issues:** Try refreshing the page or clearing browser cache

## Data Sources

The isotope data in this application is sample data for demonstration purposes. In a production environment, this would be connected to real databases or APIs containing current nuclear isotope information.

## License

This project is for educational and demonstration purposes. 
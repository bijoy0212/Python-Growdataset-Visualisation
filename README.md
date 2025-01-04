### README: GrowData Sensor Visualisation

---

#### Overview
This Python script visualises GrowData sensor locations across the United Kingdom. It overlays sensor data points onto a UK map and provides interactive features such as tooltips and highlights to display sensor-specific information when hovered over. The script also includes a cleaning process to ensure the dataset is accurate and relevant.

---

#### Features
1. **Dataset Loading:**
   - Reads the sensor data from a CSV file into a Pandas DataFrame for further processing and visualisation.

2. **Map Overlay:**
   - Displays sensor locations on a geographic map of the UK.
   - Plots data points within defined latitude and longitude boundaries.

3. **Data Cleaning:**
   - Extracts and retains only the core serial number from the `Serial` column.
   - Corrects mislabelled `Latitude` and `Longitude` columns.
   - Filters data to include only sensors within the UK’s geographical boundaries.

4. **Interactive Tooltips:**
   - Shows detailed information about each sensor, including:
     - Serial number
     - Latitude and longitude
     - Sensor type
     - Operational start and end times

5. **Highlighting:**
   - Highlights the hovered sensor point for easy identification.


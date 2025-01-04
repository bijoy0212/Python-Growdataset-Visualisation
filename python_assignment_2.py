import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnnotationBbox, TextArea
from PIL import Image

def main():
    try:
        # Loading the dataset
        file_path = 'GrowLocations.csv'
        data = pd.read_csv(file_path)

        # Cleaning the Serial column to retain only the core number
        if 'Serial' in data.columns:
            data['Serial'] = data['Serial'].str.extract(r'(\bPI[0-9A-Z]+\b)')

        # Fixing the Latitude and Longitude column labels
        data_corrected = data.rename(columns={"Latitude": "Longitude", "Longitude": "Latitude"})

        # Defining the bounding box for the UK map
        bounding_box = {
            "lon_min": -10.592,
            "lon_max": 1.6848,
            "lat_min": 50.681,
            "lat_max": 57.985
        }

        # Filtering data to include only valid latitude/longitude values and within the UK bounding box
        filtered_data = data_corrected[
            (data_corrected['Latitude'] >= bounding_box['lat_min']) &
            (data_corrected['Latitude'] <= bounding_box['lat_max']) &
            (data_corrected['Longitude'] >= bounding_box['lon_min']) &
            (data_corrected['Longitude'] <= bounding_box['lon_max'])
        ]

        # Loading the UK map image
        map_image_path = 'map7.png'
        map_image = Image.open(map_image_path)

        # Plotting the corrected sensor locations over the map
        fig, ax = plt.subplots(figsize=(12, 10))

        # Displaying the map with bounding box
        ax.imshow(map_image, extent=[bounding_box['lon_min'], bounding_box['lon_max'], 
                                      bounding_box['lat_min'], bounding_box['lat_max']])

        # Plotting the sensor locations
        scatter = ax.scatter(filtered_data['Longitude'], filtered_data['Latitude'], 
                              c='blue', s=20, alpha=0.6, label='Sensor Locations')

        # Adding title, labels, and legend
        ax.set_title("Plot of GrowData Sensors Over UK")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.legend()

        # Creating a tooltip container to display when hoverd over sensors
        tooltip = AnnotationBbox(TextArea(""), (0, 0), xybox=(50, 50), xycoords='data',
                                  boxcoords="offset points", bboxprops=dict(boxstyle="round", fc="w"))
        tooltip.set_visible(False)
        ax.add_artist(tooltip)

        # Creating a highlight marker
        highlight, = ax.plot([], [], 'ro', markersize=10, alpha=0.7) 

        # Updates the tooltip and highlights a scatter point when the mouse hovers over it
        def on_hover(event):
            if event.inaxes == ax:
                contains, index = scatter.contains(event)
                if contains:
                    point_index = index["ind"][0]
                    sensor_details = filtered_data.iloc[point_index]
                    
                    tooltip_text = (
                        f"Serial: {sensor_details.get('Serial', 'N/A')}\n"
                        f"Longitude: {sensor_details['Longitude']:.4f}\n"
                        f"Latitude: {sensor_details['Latitude']:.4f}\n"
                        f"SensorType: {sensor_details.get('SensorType', 'N/A')}\n"
                        f"BeginTime: {sensor_details.get('BeginTime', 'N/A')}\n"
                        f"EndTime: {sensor_details.get('EndTime', 'N/A')}"
                    )
                    tooltip.get_children()[0].set_text(tooltip_text)

                    tooltip.xy = (sensor_details['Longitude'], sensor_details['Latitude'])
                    tooltip.set_visible(True)

                    highlight.set_data([sensor_details['Longitude']], [sensor_details['Latitude']]) 
                    highlight.set_visible(True)
                else:
                    # Hides the tooltips and highlights if not hovering over any point
                    tooltip.set_visible(False)
                    highlight.set_visible(False)
            else:
                # Hides the tooltips and highlights if outside the axes
                tooltip.set_visible(False)
                highlight.set_visible(False)
            fig.canvas.draw_idle()

        # Connecting the hover event to the function
        fig.canvas.mpl_connect("motion_notify_event", on_hover)

        plt.show()

    except FileNotFoundError as e:
        print(f"Error: File not found. Please ensure the file exists at the specified path. {e}")

    except KeyError as e:
        print(f"Error: Missing expected column in the dataset. {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
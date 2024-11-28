import os
import string
import random

import matplotlib.pyplot as plt


def __generate_random_filename(length=10):
    """Generates a random string of specified length for filenames."""
    return ''.join(random.choices(string.ascii_letters, k=length))


def draw_chart(data: dict, show: bool = False, image: str = None,
               save_path: str = None, subfolder_name: str = 'charts'):
    """
        Creates a bar chart to visualize data and optionally displays or saves it.

        Parameters:
            data (dict): A dictionary with categories as keys and counts as values.
            show (bool): If True, displays the chart interactively. Default is False.
            image (str): An optional name to associate with the chart (e.g., related to an image).
            save_path (str): The directory where the chart will be saved. If None, the chart is not saved.
            subfolder_name (str): The subdirectory name where the chart will be stored (default is 'charts').

        Returns:
            None: The function does not return a value. If `save_path` is provided, the chart is saved
            to the specified directory.

        Notes:
            - If both `show` is False and `save_path` is None, the function will print a message
              indicating that the call is ineffective.
            - Saved charts will use the provided `image` name if available; otherwise, a random name
              will be generated using `generate_random_filename()`.

        Example Usage:
            data = {'l_half_ripened': 4, 'l_green': 9, 'b_half_ripened': 2, 'l_fully_ripened': 1}
            draw_chart(data, show=True, image="example_image", save_path="output_folder")
        """
    if show is False and save_path is None:
        return

    categories = list(data.keys())
    counts = list(data.values())

    file_name = image if image else __generate_random_filename()

    plt.figure(figsize=(10, 6))
    plt.bar(categories, counts, color='skyblue', edgecolor='black')
    plt.xlabel('Tomato Sizes', fontsize=12)
    plt.ylabel('Counts', fontsize=12)
    plt.title(f'Tomato Ripeness Distribution{" in " + image if image else ""}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    if show:
        plt.show()

    if save_path is not None:
        os.makedirs(os.path.join(save_path, subfolder_name), exist_ok=True)
        chart_path = os.path.join(save_path, subfolder_name, f'{file_name}')
        plt.savefig(chart_path, dpi=300)
        print(f"Chart saved at: {chart_path}")

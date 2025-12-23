import os
import webbrowser

# Get the absolute path of the demo.html file
html_path = os.path.abspath("demo.html")

# Convert to file URL format
file_url = f"file://{html_path}"

# Open the URL in the default web browser
print(f"Opening demo at: {file_url}")
webbrowser.open(file_url)
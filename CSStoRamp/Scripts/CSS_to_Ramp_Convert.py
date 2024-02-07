import re


def onSetupParameters(scriptOp):
	page = scriptOp.appendCustomPage('Custom')
	p = page.appendFloat('Valuea', label='Value A')
	p = page.appendFloat('Valueb', label='Value B')
	return

# called whenever custom pulse parameter is pushed
def onPulse(par):
	return

def onCook(scriptOp):
	scriptOp.clear()

# Function to convert hex color to RGBA
def hex_to_rgba(hex_color):
    # Expand shorthand hex notation to full form if necessary
    if len(hex_color) == 4:  # accounts for the leading '#'
        hex_color = '#' + ''.join([c*2 for c in hex_color[1:]])
    elif len(hex_color) != 7:
        raise ValueError(f"Invalid hex color: {hex_color}")
    # Convert the hex to RGB and then to 0-1 range
    r, g, b = [int(hex_color[i:i+2], 16) / 255.0 for i in range(1, 7, 2)] # skip the leading '#'
    # Alpha value is always 1 (100%)
    a = 1.0
    return (r, g, b, a)

# Retrieve the CSS gradient string from 'text1' DAT and ensure it's a string
css_gradient = str(op('text1').text)
print(f"CSS Gradient: {css_gradient}")  # Debugging print

# Parse the CSS gradient string to extract colors and positions
color_stops = re.findall(r'(#(?:[0-9a-fA-F]{3}){1,2})\s*(\d+\.?\d*)%', css_gradient)
print(f"Color Stops: {color_stops}")  # Debugging print

# Initialize list to store converted colors and positions
converted_stops = []

for hex_color, position in color_stops:
    try:
        rgba = hex_to_rgba(hex_color)
        normalized_position = float(position) / 100.0
        # Append the normalized position first, then the rgba values
        converted_stops.append([normalized_position] + list(rgba))
    except ValueError as e:
        print(e)  # Print the error message

# Now, fill the Table DAT with these values
table_dat = op('table1')  # Replace 'table1' with the exact name of your Table DAT

# Clear the table and add the headers
table_dat.clear()
table_dat.appendRow(['pos', 'r', 'g', 'b', 'a'])

# Fill the table with the converted values
for stop in converted_stops:
    table_dat.appendRow(stop)
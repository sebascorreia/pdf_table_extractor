import pdfplumber
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector, Button
from matplotlib.patches import Rectangle

# --- CONFIG ---
PDF_PATH = "data\PE1_4DP.pdf"
PAGE_NUM = 2  # change if needed

boxes = []
column_lines = []
current_mode = {'mode': 'box'}  # Mutable so we can change it in button callbacks

# --- Store patch references ---
box_patches = []
column_lines_patches = []

# --- Load PDF Page ---
with pdfplumber.open(PDF_PATH) as pdf:
    page = pdf.pages[PAGE_NUM]
    im = page.to_image(resolution=150)

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)  # make space for buttons
ax.imshow(im.original)
plt.gca().invert_yaxis()
ax.set_title("🟥 Draw table boxes or 🟩 click column lines")

# --- Drawing Elements ---
box_selector = None

# --- Mode Buttons ---
def set_mode_box(event):
    current_mode['mode'] = 'box'
    print("🔲 Switched to BOX mode")

def set_mode_column(event):
    current_mode['mode'] = 'column'
    print("📍 Switched to COLUMN mode")

axbox = plt.axes([0.3, 0.05, 0.15, 0.075])
axcol = plt.axes([0.5, 0.05, 0.15, 0.075])
btn_box = Button(axbox, 'Box Mode')
btn_col = Button(axcol, 'Column Mode')
btn_box.on_clicked(set_mode_box)
btn_col.on_clicked(set_mode_column)

# --- Box Drawing ---
def onselect_box(eclick, erelease):
    x0, y0 = round(eclick.xdata, 2), round(eclick.ydata, 2)
    x1, y1 = round(erelease.xdata, 2), round(erelease.ydata, 2)
    x_min, x_max = sorted([x0, x1])
    y_min, y_max = sorted([y0, y1])
    bbox = (x_min, y_min, x_max, y_max)
    boxes.append(bbox)

    # Draw persistent rectangle with picker enabled
    rect = plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min,
                         linewidth=2, edgecolor='red', facecolor='none', picker=True)
    ax.add_patch(rect)
    box_patches.append(rect)
    fig.canvas.draw()
    print(f"📦 Box: (x0={x_min}, top={y_min}, x1={x_max}, bottom={y_max})")

box_selector = RectangleSelector(ax, onselect_box,
                                 useblit=False,
                                 button=[1],  # left click
                                 minspanx=5, minspany=5,
                                 spancoords='pixels',
                                 interactive=True)

# --- Column Click Handler ---
def onclick(event):
    if event.button == 1 and event.inaxes == ax:
        if current_mode['mode'] == 'column' and event.xdata:
            x = round(event.xdata, 2)
            column_lines.append(x)
            line = ax.axvline(x, color='green', linestyle='--', linewidth=2, picker=5)
            column_lines_patches.append(line)
            fig.canvas.draw()
            print(f"📍 Column line at x = {x}")

fig.canvas.mpl_connect('button_press_event', onclick)

# --- Drag & Delete Handlers ---
drag_data = {'patch': None, 'type': None, 'offset': (0, 0)}

def on_pick(event):
    # Pick box
    if isinstance(event.artist, Rectangle):
        drag_data['patch'] = event.artist
        drag_data['type'] = 'box'
        mouse_event = event.mouseevent
        drag_data['offset'] = (mouse_event.xdata, mouse_event.ydata)
    # Pick column line
    elif hasattr(event.artist, 'get_xdata'):
        drag_data['patch'] = event.artist
        drag_data['type'] = 'column'
        mouse_event = event.mouseevent
        drag_data['offset'] = (mouse_event.xdata, )

def on_motion(event):
    if drag_data['patch'] is not None and event.xdata and event.ydata:
        if drag_data['type'] == 'box':
            rect = drag_data['patch']
            dx = event.xdata - drag_data['offset'][0]
            dy = event.ydata - drag_data['offset'][1]
            rect.set_x(rect.get_x() + dx)
            rect.set_y(rect.get_y() + dy)
            drag_data['offset'] = (event.xdata, event.ydata)
            fig.canvas.draw()
        elif drag_data['type'] == 'column':
            line = drag_data['patch']
            x = event.xdata
            line.set_xdata([x, x])
            fig.canvas.draw()

def on_release(event):
    if drag_data['patch'] is not None:
        # Update data structures
        if drag_data['type'] == 'box':
            rect = drag_data['patch']
            idx = box_patches.index(rect)
            boxes[idx] = (rect.get_x(), rect.get_y(),
                          rect.get_x() + rect.get_width(),
                          rect.get_y() + rect.get_height())
        elif drag_data['type'] == 'column':
            line = drag_data['patch']
            idx = column_lines_patches.index(line)
            x = line.get_xdata()[0]
            column_lines[idx] = round(x, 2)
        drag_data['patch'] = None
        drag_data['type'] = None

def on_right_click(event):
    # Delete box or column on right-click
    if event.button == 3 and event.inaxes == ax:
        # Check for box
        for i, rect in enumerate(box_patches):
            contains, _ = rect.contains(event)
            if contains:
                rect.remove()
                del box_patches[i]
                del boxes[i]
                fig.canvas.draw()
                return
        # Check for column
        for i, line in enumerate(column_lines_patches):
            x = line.get_xdata()[0]
            if abs(event.xdata - x) < 5:  # tolerance
                line.remove()
                del column_lines_patches[i]
                del column_lines[i]
                fig.canvas.draw()
                return

fig.canvas.mpl_connect('pick_event', on_pick)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('button_press_event', on_right_click)

plt.show()

# --- Final Output ---
print("\n✅ Final table areas (bounding boxes):")
for i, box in enumerate(boxes, 1):
    print(f"Box {i}: {box}")

print("\n✅ Final column x-positions:")
print(sorted(column_lines))
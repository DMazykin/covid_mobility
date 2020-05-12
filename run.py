#Import
import dash
from ui import page_layout
from server import app


app.layout = page_layout

import callbacks

if __name__ == "__main__":
    app.run_server(debug=True)
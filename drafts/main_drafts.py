table = QTableWidget(self)  # Create a table
table.setColumnCount(3)  # Set three columns
table.setRowCount(1)  # and one row

# Set the table headers
table.setHorizontalHeaderLabels(["Header 1", "Header 2", "Header 3"])

# Set the tooltips to headings
table.horizontalHeaderItem(0).setToolTip("Column 1 ")
table.horizontalHeaderItem(1).setToolTip("Column 2 ")
table.horizontalHeaderItem(2).setToolTip("Column 3 ")

# Set the alignment to the headers
table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight)

# Fill the first line
table.setItem(0, 0, QTableWidgetItem("Text in column 1"))
table.setItem(0, 1, QTableWidgetItem("Text in column 2"))
table.setItem(0, 2, QTableWidgetItem("Text in column 3"))

# Do the resize of the columns by content
table.resizeColumnsToContents()
I dedicated myself to developing a Desktop application focused on weather forecasting, integrating various technologies to create a complete solution: an ETL pipeline that performs data extraction via API, transformation distributed between SQL and Python, and final loading into automatically organized CSV files.

🟢 What does the app do?  
1️⃣ Allows the user to select the city to be analyzed through a graphical interface.
2️⃣ Consumes meteorological data in JSON format from WeatherAPI.
3️⃣ Stores the data in a MySQL database created and configured automatically.
4️⃣ Processes information with SQL queries, generating structured datasets for analysis.
5️⃣ Returns the processed data to Python for vector operations with NumPy and final adjustments.
6️⃣ Generates charts with Matplotlib to visualize meteorological information.
7️⃣ Displays results in dashboards (CustomTkinter), with 4 tabs:
🌡️ Temperature
💧 Humidity
🌧️ Precipitation (rain/snow)
📊 General Panel with current data and projections
8️⃣ Includes a button that automatically exports the data to CSV files, creating an organized directory hierarchy, enabling further analysis in Excel, Power BI, and other tools.

📖 Technologies and concepts applied:

▪️NumPy – vector operations

▪️Pandas – data cleaning and export

▪️MySQL + mysql-connector-python – structured storage and processing

▪️Requests – API consumption

▪️OS – directory and file automation

▪️Matplotlib – data visualization

▪️CustomTkinter – interactive graphical interface

▪️SQL – queries and modeling

▪️OOP – code organization and reuse

▪️Advanced Python – use of decorators and custom exceptions

Complete ETL pipeline: API JSON → SQL → NumPy → GUI/Pandas → CSV

Modularization – separation of code into packages and modules, facilitating maintenance and scalability

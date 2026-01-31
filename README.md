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

![first](https://media.licdn.com/dms/image/v2/D4D22AQFdsabtRD0-Tg/feedshare-shrink_2048_1536/B4DZpXTc..GsAw-/0/1762401309389?e=1771459200&v=beta&t=rPUS9PxBBlhfK7385r0lanbvShL2lmEcryxQBc0hKDg)

![second](https://media.licdn.com/dms/image/v2/D4D22AQHPt5zQGb4VRA/feedshare-shrink_2048_1536/B4DZpXTc_IGsAw-/0/1762401309354?e=1771459200&v=beta&t=GE_m32IznMPhBNSeNCH3KmkuVWLTnMVNdxA7Vf5-vjM)

![third](https://media.licdn.com/dms/image/v2/D4D22AQG2vutlM4QI7g/feedshare-shrink_1280/B4DZpXTc.NGwAw-/0/1762401309374?e=1771459200&v=beta&t=LR26Mn5Tn2XKGVERhkDVLYn82jjXWJOovo6oo6Ow0H4)

![forth](https://media.licdn.com/dms/image/v2/D4D22AQHr_fU6myNe-Q/feedshare-shrink_2048_1536/B4DZpXTc_NIMAw-/0/1762401309348?e=1771459200&v=beta&t=XoHf47QtK9NNqaJBQ3FF57tzyMSCm9fp5sFFYnn73Uk)

![fifth](https://media.licdn.com/dms/image/v2/D4D22AQGuE06TprWdHg/feedshare-shrink_1280/B4DZpXTc_RKIAs-/0/1762401309067?e=1771459200&v=beta&t=HWwFvRR26B3ze91qke_5Joh15iNQJ-zOx29aWcvrzbg)

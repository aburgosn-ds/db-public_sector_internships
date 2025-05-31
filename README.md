# Database Project: Public Sector Internship Offers
Database to manage and analyse internship offers for the public sector.

## Description
This project implements a relational database system to store, process, and analyze information about internship offers in the Peruvian public sector. It includes an automated ETL pipeline that performs web scraping of the site https://www.convocatoriasdetrabajo.com/ to extract both structured data and full HTML content.

Extracted content is processed using the Gemini Product (Google Generative AI API) to perform semantic cleaning, key information extraction, and inference, generating normalized JSON outputs. The transformed data is then inserted into a MySQL database hosted on Amazon RDS.

The ETL process runs daily on an Amazon EC2 instance, and data is accessed for visualization and analysis using Power BI, which connects to the database via an SSH tunnel.

## Technologies Used
- Database: MySQL (Amazon RDS)
- Backent and ETL: Python 3, BeautifulSoup, SQLAlchemy, Google Gemini API (GenAI)
- Deployment & Automation: Amazon EC2, cron jobs
- Analysis and Visualization: Power BI

## Project Structure

📂 sql/ → SQL scripts for table and database creation.

📂 src/ → Main code of the project:

    📂 components/ → Modules for extraction and transformation.
    
    📂 database/ → Database conection, queries, and inserts.
    
    📂 models/ → Table class models definition.
    
    📂 utils/ → Auxiliar Functions.

    📂 constants/ → Table class models definition.
    
📂 scripts/ → Execution that performs ETL, once or schedulered.

📂 data/ → JSON data files used in the project.

📂 dashboards/ → Visualizations and reports.

## Database ERD
![ERD db-public_sector_internships](https://github.com/user-attachments/assets/02fb5bcc-d75f-48e1-870a-d12174a3f80f)



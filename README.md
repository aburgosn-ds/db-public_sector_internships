# Database Project: Public Sector Internship Offers
Database to manage and analyse internship offers for the public sector.

## Description
This project implements a relational database system to store, process and analyse information about internship offers in the peruvian public sector. Includes ETL (extract, transform, and load data) that gather information from the webpage https://www.convocatoriasdetrabajo.com/, process and normalize data with Gemini NLP and store in a relational database daily. Database and automatic execution is implemented with Amazon RDS and Amazon EC2. 

## Technologies Used
- Database: MySQL (Amazon RDS)
- Backent and ETL: Python 3, Gemini NLP, SQLAlchemy
- Analysis and Visualization: Pandas, Power BI
- Deployment: Amazon EC2

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



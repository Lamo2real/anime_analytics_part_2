# anime_analytics_part_2
this project is concluded of ETL from S3 to AWS Glue and loaded into Redshift


```bash
/etl-pipeline-repo/
├── .github/workflows/          # CI/CD automation
├──          ├── deploy.yaml
├──          └── testing_script.yaml
├── venv/ 
├── etl/                        # ETL logic (e.g. Airflow DAGs, Glue scripts, etc.)
│   └── jobs/
├── infrastructure/             # Terraform/CDK/etc. for Redshift, S3, etc.
├── migrations/                 # SQL or dbt-based migration scripts
│   ├── migration_db.py
│   ├── README.md
│   └── sql/
│        ├── 00_create_data_warehouse.sql
│        ├── 01_create_database.sql
│        ├── 02_create_schema.sql
│        ├── 03_create_dim_studio.sql
│        ├── 04_create_dim_genre.sql
│        ├── 05_create_fact_aniem.sql
│        └── 06_create_bridge_anime_genre.sql
├── tests/                      # Data quality or unit tests
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

### Table of Contents
1. [Start-up Package](#start-up-package)

</br>
</br>
</br>
</br>
2024_04_22_add_customer_dim.sql
2024_04_23_update_fact_sales.sql




## Start-up Package 
### Good practice when working on multiple python projects </br></br>
when starting the project make sure to create a virtual envrironment in the root of the project directory as followed:

- step 1:</br>
**check your cuurent directory**
```bash
pwd
```
make sure to be in the root ending with `**/anime_analytics_part_2`
</br></br>

- step 2: </br>
**create the python environment:**
```bash
python3 -m venv venv
```
</br>

- step 3:
**enter the virtual environment with this command**
```bash
source venv/bin/activate
```
#### these steps should activate you into a virtual environment where if you install any dependencies or extras you merely place them into this environment, outside it, you cant access them


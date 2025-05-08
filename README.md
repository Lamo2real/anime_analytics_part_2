# anime_analytics_part_2
this project is concluded of ETL from S3 to AWS Glue and loaded into Snowflake


```bash
/etl-pipeline-repo/
├── .github/workflows/          # CI/CD automation
├──          ├── deploy.yaml
├──          └── testing_script.yaml
├── venv/ 
├── etl/                        # ETL logic (e.g. Airflow DAGs, Glue scripts, etc.)
│   └── jobs/
├── infrastructure/             # Terraform/CDK/etc. for snowflake, S3, etc.
├── migrations/                 # SQL or dbt-based migration scripts
│   ├── migration_db.py
│   ├── README.md
│   └── sql/
│        ├── 00_create_data_warehouse.sql
│        ├── 01_create_database.sql
│        ├── 02_use_database.sql
│        ├── 03_create_schema.sql
│        ├── 04_use_schema.sql
│        ├── 05_create_dim_studio.sql
│        ├── 06_create_dim_genre.sql
│        ├── 07_create_fact_aniem.sql
│        └── 08_create_bridge_anime_genre.sql
├── tests/                      # Data quality or unit tests
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

### Table of Contents
1. [Start-up Package](#start-up-package)
2. [Database Migration Script](#database-migration-script)

</br>
</br>
</br>
</br>



## Start-up Package 
### Good practice when working on multiple python projects </br></br>
when starting the project make sure to create a virtual envrironment in the root of the project directory as followed:

- step 1:</br>
**check your current directory**
```bash
pwd
```


make sure to be in the root ending with `**/anime_analytics_part_2`
</br></br>

- step 2: </br>
**create the python environment:**
```bash
python3 -m venv etl_venv
```
</br>

- step 3: </br>
**enter the virtual environment with this command**
</br>

`linux`
```bash
source etl_venv/bin/activate
```
</br>

`windows`
```powershell
.\etl_venv\Scripts\Activate
```
#### these steps should activate you into a virtual environment where if you install any dependencies or extras you merely place them into this environment, outside it, you cant access them

- step 4: </br>
**deactivate/escape environment**
```bash
deactivate
```

</br>
</br>
</br>

## Database Migration Script
#### Read the README in `./application/migrations/` directory

# anime_analytics_part_2
this project is concluded of ETL from S3 to AWS Glue and loaded into Redshift


```bash
/etl-pipeline-repo/
├── etl/                         # ETL logic (e.g. Airflow DAGs, Glue scripts, etc.)
│   └── jobs/
├── infrastructure/             # Terraform/CDK/etc. for Redshift, S3, etc.
├── migrations/                 # SQL or dbt-based migration scripts
│   ├── 2024_04_22_add_customer_dim.sql
│   ├── 2024_04_23_update_fact_sales.sql
├── tests/                      # Data quality or unit tests
├── requirements.txt
├── README.md
└── .github/workflows/          # CI/CD automation
```

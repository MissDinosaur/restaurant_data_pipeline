## Restaurant Data Pipeline
There are two data sources to be processed in this project. All are related to restaurant order information.

One is jaffle dataset which contains 6 csv file. Another is an Azure Blob SA URL which contains one JSONL file support_tickets.jsonl.

The data workflow uses a bronze-silver-gold layered approach: ingestion  -->  transformation  -->  analytics  -->  reporting.
- ingestion (Bronze): Extract data
- transformation (Silver): Transform or process data
- analytics (Gold): Aggragate data as per business need
- reporting: Export analytic results into csv file for a better check.


### 1. Jaffle Data
It's a 1 year sample spanning from 2016 to 2017, and includes the following tables:

- `raw_customers`: customers who have placed orders
- `raw_orders`: orders placed by customers for food and drinks
- `raw_items`: the individual items that make up an order
- `raw_products`: the products that are available to order
- `raw_stores`: the stores where orders are placed
- `raw_supplies`: the supplies that are used to make products

Because jaffle dataset consists of six clean, flat CSV tables which are structured and well-defined, therefore ETL techinque is selected here.

Unlike the JSONL data source, these CSVs don’t need heavy schema inference or nested parsing. 

So, transformations (like joins, type casting, enrichment) are cheap and predictable — perfect for an ETL-style pipeline:
- Extract: Read CSVs
- Transform: Clean, join, derive features locally (e.g., total order value)
- Load: Store transformed tables (like analytics_orders) into reporting folder

```text
data/
├── 01_raw/            <-- raw CSVs
├── 02_intermediate/   <-- transformed joins (cast types, enrich)
├── 03_primary/        <-- analytics aggregates
└── 04_reporting/      <-- exports
```

### 2. Support_tickets Data
support_tickets.jsonl is about the restaurant order details, having ticket_id, order_id, status and sentiment, etc., fileds. 

Below is one sample.

```json
{
    "ticket_id": "TCK-317F60A0AA", 
    "customer_external_id": 139, 
    "order_id": "aba833b7-59d0-4244-8f73-ca03aa83e38b", "channel": "chat", "priority": "medium", 
    "status": "open", "category": "delivery", "subject": "Water near when very.", 
    "body": "Sell seek decade take human now trade here. Finally able election maybe international let week.", 
    "sentiment": {"model": "demo", "score": 0.21}, 
    "sla_due_at": "2017-01-27T08:32:43Z", "first_response_at": "2016-11-16T03:05:31Z", 
    "resolved_at": "2016-11-09T02:57:51Z", "tags": ["vip"], 
    "agent_id": "AG-050", "updated_at": "2017-05-27T11:14:58Z", "ingested_at": "2025-10-24T14:16:48Z"
}
```

Because this support_tickets data source is semi-structured (JSON Lines), so ELT techinque is better for its data modeling.



This is ELT by design:
- Extract --> load from Azure Blob
- Load --> store raw file in 01_raw folder
- Transform --> cleaning, aggregation, analytics nodes

```text
data/
├── 01_raw/                <-- raw support_tickets
├── 02_intermediate/       <-- cleaned/normalized
├── 03_primary/            <-- analytics tables (sentiment, ticket counts)
└── 04_reporting/          <-- exported CSV/Excel
```

### Technical Stack
In this project, **Kedro** is chosen here to orchestrate the data workflow. As it 
- Enforces a layered architecture (raw --> intermediate --> analytics) which is required in this assignment.
- Perfect for modular, local development before deploying to orchestration.
- Integrates easily with Airflow/Prefect/Dagster later if needed.

### Project Structure
```text
restaurant_pipeline/
├── conf/
│   └── base/
│       ├── catalog.yml        # Define the data ocurring in the kedro pipeline
│       ├── parameters.yml     # Define paarameters used in kedro pipeline
│       └── logging.yml
├── data/
│   ├── 01_raw/                 # Bronze: raw CSVs
│   ├── 02_intermediate/        # Silver: cleaned + joined data
│   ├── 03_primary/             # Gold: analytics-ready marts
│   └── 04_reporting/           # Export data into a csv-ready file
├── src/
│   ├── data_pipeline/
│   │   ├── __init__.py
│   │   ├── pipelines/
│   │   │   ├── jaffle_data/        # pipelines of jaffle data source
│   │   │   │   ├── ingestion
│   │   │   │   ├── transformation
│   │   │   │   ├── analytics
│   │   │   │   └── reporting
│   │   │   └── support_tickets/    # pipelines of support_tickets.jsonl
│   └── └── pipeline_registry.py    # main functiion entry
│   
├── README.md
├── pyproject.toml
└── requirements.txt
```

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-folder-name>
   ```

2. Create a virtual environment named <venvName> (Recommended Python version==3.11.0):
   ```bash
   python -m venv <venvName>  # Replace <venvName> by your venv name 
   ```

3. Activate the virtual environment <venvName>:
   ```bash
   # Replace <venvName> by your venv name 

   # Windows (CMD/Powershell)
   <venvName>\Scripts\activate

   # Windows (git bash)
   source <venvName>/Scripts/activate

   # macOS/Linux
   source <venvName>/bin/activate

   # if you wanna quit the current virtual environment
   deactivate
   ```

4. Install the dependencies (Recommended Python version==3.11.0):
   ```bash
   pip install -r requirements.txt
   ```

5. Run the commands as you need.
   
   **For jaffle data source:** 
   ```bash
   kedro run --pipeline=jaffle_ingestion
   kedro run --pipeline=jaffle_transformation
   kedro run --pipeline=jaffle_analytics
   kedro run --pipeline=jaffle_reporting
   ```
   After the last commands ```kedro run --pipeline=jaffle_reporting``` runs, fact_order_metrics.csv will be generated in folder /data/04_reporting/. It describes: 1. the Average order value, i.e., the average price 2. the Number of tickets of each order.
   
   **For support_tickets:** 
   ```bash
   kedro run --pipeline=support_tickets 
   ```
   The command above will trigger nodes of ingestion, transformation, analytics, and reporting sequentially. And finally, you will get two csv files, namely avg_score_per_order.csv and tickets_per_order.csv in folder /data/04_reporting/. 
   
   avg_score_per_order.csv tells us the average sentiment score in each order while tickets_per_order.csv give us the information about the number of tickets for each order.

   But if you only want trigger one or two of these nodes, instead of the whole piepline, you can run the commands shown as below.
   ```bash
   kedro run --pipeline=support_tickets --from-nodes "export_avg_score,export_tickets_count"
   ```
   Or
   ```bash
   kedro run --pipeline=support_tickets --from-nodes "export_avg_score"
   ```
   Place the node name after the parameter --from-nodes as you need.

### END
from pathlib import Path
import json, argparse, subprocess
import pandas as pd
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.engine import URL
BASE = Path(__file__).resolve().parent

def run(use_mysql=False):
    df = pd.read_csv(BASE / "customer_shopping_behavior.csv")
    missing = int(df["Review Rating"].isna().sum())
    df["Review Rating"] = df.groupby("Category")["Review Rating"].transform(lambda x: x.fillna(x.median()))
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df = df.rename(columns={"purchase_amount_(usd)": "purchase_amount"})
    df["age_group"] = pd.qcut(df.age, 4, labels=["Young Adult", "Adult", "Middle-aged", "Senior"])
    df["purchase_frequency_days"] = df.frequency_of_purchases.map({"Fortnightly":14,"Weekly":7,"Monthly":30,"Quarterly":90,"Bi-Weekly":14,"Annually":365,"Every 3 Months":90})
    if df.discount_applied.equals(df.promo_code_used):
        df = df.drop(columns="promo_code_used")
    assert not df.isna().any().any(), "Unresolved missing data"
    assert df.customer_id.is_unique, "Duplicate customer IDs"
    out = BASE / "results"
    out.mkdir(exist_ok=True)
    df.to_csv(out / "customer_cleaned.csv", index=False)
    summary = {"rows":len(df), "revenue_usd":float(df.purchase_amount.sum()), "average_purchase":round(float(df.purchase_amount.mean()),2), "ratings_imputed":missing, "mysql_verified":False}
    if use_mysql:
        command = "$ErrorActionPreference='Stop'; Import-Module ($PSHOME+'\\Modules\\Microsoft.PowerShell.Security\\Microsoft.PowerShell.Security.psd1'); $c=Import-Clixml -LiteralPath (Join-Path $env:LOCALAPPDATA 'CustomerSalesInsights/credential.xml'); @{user=$c.UserName;password=$c.GetNetworkCredential().Password}|ConvertTo-Json -Compress"
        result = subprocess.run(["powershell.exe","-NoProfile","-Command",command],capture_output=True,text=True,check=True)
        cred = json.loads(result.stdout)
        config = json.loads((BASE / "mysql_config.json").read_text())
        url = URL.create("mysql+pymysql", username=cred["user"], password=cred["password"], host=config["host"], port=config["port"])
        server = create_engine(url,connect_args={"connect_timeout":10})
        with server.begin() as conn:
            conn.execute(text("CREATE DATABASE IF NOT EXISTS customer_behavior"))
        server.dispose()
        engine = create_engine(url.set(database="customer_behavior"))
        if inspect(engine).has_table("customer"):
            existing = pd.read_sql("SELECT * FROM customer", engine)
            expected = df.copy()
            expected["age_group"] = expected.age_group.astype(str)
            pd.testing.assert_frame_equal(existing.sort_values("customer_id").reset_index(drop=True)[expected.columns], expected.sort_values("customer_id").reset_index(drop=True),check_dtype=False)
            print("Existing table matches the source; reused without changes.")
        else:
            df.to_sql("customer",engine,index=False,if_exists="fail")
        with engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM customer")).scalar_one()
            assert count == len(df)
            sql = (BASE / "customer_behavior_sql_queries.sql").read_text()
            queries = []
            for statement in sql.split(";"):
                query = "\n".join(line for line in statement.splitlines() if not line.strip().startswith("--")).strip()
                if query and not query.upper().startswith("USE "):
                    queries.append(query)
            assert len(queries)==10
            for i,query in enumerate(queries,1):
                pd.read_sql(text(query),conn).to_csv(out / f"q{i:02d}.csv",index=False)
        engine.dispose()
        summary["mysql_verified"] = True
        summary["queries_passed"] = 10
    (out / "verification.json").write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mysql",action="store_true")
    args = parser.parse_args()
    try:
        run(args.mysql)
    except Exception as exc:
        # Driver exceptions can contain connection details, so only expose the type.
        print("Setup failed:",type(exc).__name__,". Check credentials, MySQL permissions, or an existing mismatched customer table.")
        raise SystemExit(1)

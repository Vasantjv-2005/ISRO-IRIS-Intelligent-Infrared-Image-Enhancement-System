import asyncio
import os
import sys
from pathlib import Path

# Ensure backend directory is in python path
sys.path.insert(0, str(Path(__file__).parent.resolve()))

from app.database.mongodb import mongodb, get_database

async def cleanup():
    print("Connecting to MongoDB to clean report collections...")
    await mongodb.connect()
    db = get_database()
    
    # Clear reports collection
    res_reports = await db["reports"].delete_many({})
    print(f"Deleted {res_reports.deleted_count} documents from 'reports' collection.")
    
    # Clean reports folder on disk
    reports_dir = Path("reports")
    if reports_dir.exists():
        for pdf in reports_dir.glob("*.pdf"):
            if pdf.name != "CHANDRA_09_FULL_MISSION_REPORT.pdf":
                try:
                    pdf.unlink()
                    print(f"Removed disk report: {pdf}")
                except Exception as e:
                    print(f"Could not remove {pdf}: {e}")

    outputs_reports_dir = Path("outputs/reports")
    if outputs_reports_dir.exists():
        for pdf in outputs_reports_dir.glob("*.pdf"):
            try:
                pdf.unlink()
                print(f"Removed disk report: {pdf}")
            except Exception as e:
                print(f"Could not remove {pdf}: {e}")

    await mongodb.disconnect()
    print("=== All existing reports have been removed from the website ===")

if __name__ == "__main__":
    asyncio.run(cleanup())

import asyncio
from app.storage import reports

async def auto_delete(report_id):
    await asyncio.sleep(120)

    if report_id in reports:
        del reports[report_id]
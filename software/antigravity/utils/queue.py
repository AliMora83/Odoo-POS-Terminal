"""
utils/queue.py — Offline queue processing logic (Step 6).
Handles FIFO replay of transactions stored in ESP32 flash on reconnect.
"""


async def process_queue(queued_transactions: list[dict]) -> list[dict]:
    """
    Process a list of queued transactions in FIFO order.
    Each transaction contains local_ref, timestamp, order_payload, payment_payload.

    Returns a list of results per transaction.
    Step 6 implementation pending.
    """
    # TODO: implement during Step 6
    raise NotImplementedError("Offline queue processing not yet implemented — Step 6.")

import hashlib
import asyncio


def compute_hash(list_1, list_2):
    combined_str = "".join(list_1 + list_2)
    return hashlib.sha256(combined_str.encode()).hexdigest()


async def transformer_function(text: str) -> str:
    await asyncio.sleep(0.1)  # Simulate delay
    return text.upper()

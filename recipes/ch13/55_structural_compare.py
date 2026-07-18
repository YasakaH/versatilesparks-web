"""
Recipe 55 (V2): Structural Page Comparison

Compare DOM structure (tag tree) between runs to detect website
changes that could break extraction. Uses common/visual_diff.py.
"""
import asyncio
from common.visual_diff import compare_regions


async def main():
    yesterday = '<table><tr><td>Product</td></tr></table>'
    today = '<table></table>'
    diff = compare_regions(yesterday, today)
    print(f"Difference: {diff}")


if __name__ == "__main__":
    asyncio.run(main())

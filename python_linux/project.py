#!/usr/bin/env python3
"""
Donia Said
Khadija Fakhri
Restaurant Order Management System
ENCS3130 Linux Laboratory
Second Summer Semester, 2024/2025
"""

import re
from typing import List, Dict, Optional

class InvoiceHandler:
    def __init__(self, invoice_file: str = "daily_invoices.txt"):
        self.invoice_file = invoice_file
        self.menu_items = ['Hummous', 'Fool', 'Falafel', 'Tea', 'Cola', 'Water']

    def _extract_order_type(self, content: str) -> Optional[str]:
        match = re.search(r'Order Type:\s*(In|Out)', content, re.IGNORECASE)
        return match.group(1) if match else None

    def _extract_items(self, content: str) -> List[Dict]:
        items = []
        lines = content.splitlines()
        in_items = False
        for line in lines:
            if "ITEMS ORDERED:" in line.upper():
                in_items = True
                continue
            if in_items and ("INVOICE END" in line.upper() or not line.strip()):
                break
            if in_items:
                item_data = self._parse_item_line(line)
                if item_data:
                    items.append(item_data)
        return items

    def _parse_item_line(self, line: str) -> Optional[Dict]:
        pattern = r'([A-Za-z]+):\s*(\d+)\s+\w+\s*@\s*([\d.]+)\s*=\s*([\d.]+)'
        match = re.match(pattern, line.strip())
        if match:
            return {
                "item": match.group(1),
                "quantity": int(match.group(2)),
                "price": float(match.group(3)),
                "total": float(match.group(4))
            }
        return None

    def read_all_invoices(self) -> List[Dict]:
        try:
            with open(self.invoice_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: {self.invoice_file} not found.")
            return []

        sections = content.split("INVOICE #")
        all_orders = []

        for section in sections:
            if not section.strip():
                continue
            order_type = self._extract_order_type(section)
            items = self._extract_items(section)
            if order_type and items:
                for item in items:
                    item["type"] = order_type
                    all_orders.append(item)
        return all_orders


def main():
    handler = InvoiceHandler()
    orders = handler.read_all_invoices()
    print("Extracted Orders (sample):")
    for order in orders[:5]:
        print(order)
    print(f"Total orders extracted: {len(orders)}")


if __name__ == "__main__":
    main()

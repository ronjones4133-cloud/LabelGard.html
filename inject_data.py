#!/usr/bin/env python3
"""
LabelGard™ — Data Injector
Merges the full uomData and CUSTOMERS arrays from your original source file
into the new labelgard_v1.html shell.

Usage:
  python3 inject_data.py <original_source.html> <labelgard_v1.html>

Example:
  python3 inject_data.py "Vision Industries Label Generator.html" labelgard_v1.html

The script overwrites labelgard_v1.html in place.
"""
import sys, re

if len(sys.argv) < 3:
    print(__doc__)
    sys.exit(1)

src_file   = sys.argv[1]
shell_file = sys.argv[2]

print(f"Reading source: {src_file}")
with open(src_file, 'r', encoding='utf-8') as f:
    src = f.read()

print(f"Reading shell:  {shell_file}")
with open(shell_file, 'r', encoding='utf-8') as f:
    shell = f.read()

# ── Extract uomData ──
m_uom = re.search(r'(const uomData\s*=\s*\{.*?\};)', src, re.DOTALL)
if not m_uom:
    print("ERROR: Could not find 'const uomData = {...};' in source file.")
    sys.exit(1)
uom_block = m_uom.group(1)
entry_count = uom_block.count('":')
print(f"  uomData: {entry_count:,} entries found")

# ── Extract CUSTOMERS ──
m_cust = re.search(r'(const CUSTOMERS\s*=\s*\[.*?\];)', src, re.DOTALL)
if not m_cust:
    print("ERROR: Could not find 'const CUSTOMERS = [...];' in source file.")
    sys.exit(1)
cust_block = m_cust.group(1)
cust_count = cust_block.count('"no"')
print(f"  CUSTOMERS: {cust_count:,} records found")

# ── Inject ──
if '__UOMDATA_PLACEHOLDER__' not in shell:
    print("ERROR: Shell file does not contain __UOMDATA_PLACEHOLDER__")
    print("       Has this file already been injected?")
    sys.exit(1)
if '__CUSTOMERS_PLACEHOLDER__' not in shell:
    print("ERROR: Shell file does not contain __CUSTOMERS_PLACEHOLDER__")
    sys.exit(1)

shell = shell.replace('const uomData = __UOMDATA_PLACEHOLDER__;', uom_block)
shell = shell.replace('const CUSTOMERS = __CUSTOMERS_PLACEHOLDER__;', cust_block)

with open(shell_file, 'w', encoding='utf-8') as f:
    f.write(shell)

size_kb = len(shell) / 1024
print(f"\nDone! {shell_file} updated — {size_kb:,.0f} KB")
print("Open labelgard_v1.html in your browser to verify.")

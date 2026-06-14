# LabelGard™

**Browser-based customer receiving label generator for Microsoft Dynamics 365 Business Central.**

LabelGard generates 6×4 landscape customer receiving labels with Code128 barcodes directly from a BC Sales Order Lines export. No installation, no backend, no data leaves your machine.

LabelGard is part of the **ItemSync™** family of item master data tools for Business Central.

---

## What it does

LabelGard produces one label per carton per line item from a standard BC Sales Order Lines export. Each label includes:

| Field | Source |
|---|---|
| **To / From** | Customer ship-to address (from lookup) and Vision Industries Group |
| **Part # barcode** | Customer's Item Reference No. — falls back to Vision part # if blank |
| **Parts Description** | Large-format text from SO line Description field |
| **Quantity barcode** | Carton quantity from hardcoded UOM data (BOX entries) |
| **Customer PO # barcode** | Entered at order details step |
| **Vendor # barcode** | Vision part # — read as "Vision is the vendor to the customer" |

---

## How to use it

1. Open `LabelGard.html` in any modern browser.
2. **Step 1 — Order Details:** Search for a customer by name or number. Address fields auto-populate from the embedded ship-to lookup (699 records). Enter the Customer PO #.
3. **Step 2 — Upload Sales Order:** Upload the BC Sales Order Lines export (.xlsx). Required columns: `No.`, `Item Reference No.`, `Description`, `Quantity`.
4. **Review the preview table.** Carton Qty and Vendor Part # are both editable before generating. Items with no UOM match are flagged with a warning badge and default to 1.
5. Click **Generate & Preview Labels** to render all labels.
6. Use **🖨 Print All Labels** to send to your label printer.

---

## Per-item reprint

After generating, each line item group displays a **↺ Reprint this item** button. Clicking it:

- Reads the current Carton Qty and Vendor Part # from the preview table
- Removes the existing labels for that item
- Re-renders with the updated values at the end of the container
- Recalculates the total label count

This allows mid-run corrections without regenerating the entire batch.

---

## Discrepancy report

The **📋 Copy Discrepancy Report** button in the print bar compares every line item's current values against system defaults (UOM lookup and original Item Reference No. from the SO). Any deviation is captured in a plain-text report:

```
Customer Receiving Label — Data Discrepancy Report
Generated: Jun 14, 2026 10:32 AM
Customer: PELLA CORPORATION
PO: PO-123456

1760.104 — Pivot Bar Assy
  Carton Qty: system=4000, used=2000

19541.005 — Corner Latch
  Vendor Part #: system=UV708800, used=UV708801
```

One click copies the report to clipboard. The warehouse team can paste it directly into an email or ticket to the UOM or master data owner — no decisions required about who to send what.

If no overrides were made, the report confirms that all values match system defaults.

---

## Label format

| Dimension | Value |
|---|---|
| Size | 6 × 4 inches, landscape |
| Barcode format | Code128 |
| Print layout | One label per page via `@page { size: 6in 4in }` |

---

## Embedded data

LabelGard embeds two data sets directly in the HTML file — no uploads or external lookups required at runtime.

| Data set | Source | Records |
|---|---|---|
| UOM (BOX quantities) | BC UOM Config Package export | ~10,800 items |
| Ship-to lookup | BC Customer / Ship-to Address export | 699 ship-to records |

UOM values serve as the system default for carton quantity. If a Vision part number has no BOX entry in the UOM data, LabelGard defaults to 1 and flags the item with a warning badge in the preview table.

---

## Technical notes

- Runs entirely in the browser. No server, no API calls, no data transmission.
- Reads BC Sales Order Lines exports directly — standard BC export format, no reformatting required.
- Built with vanilla JavaScript + SheetJS + JsBarcode.
- Single HTML file — no dependencies to install or manage.

---

## Attribution

Built by [Ron Jones](https://www.linkedin.com/in/ronjones4133/) · Supply Chain & ERP Systems

© 2026 ItemSync™ · All rights reserved · Source code proprietary  
Not affiliated with Microsoft Corporation or Integrated Warehouse Solutions.

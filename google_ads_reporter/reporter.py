"""Terminal output using the rich library."""

from collections import OrderedDict
from typing import Any

from rich.console import Console
from rich.table import Table


def _max(rows: list[dict[str, Any]], key: str) -> Any:
    """Return the maximum value for *key* across rows, or 0 if no rows."""
    if not rows:
        return 0
    return max(row[key] for row in rows)


def _maybe_highlight(value: Any, max_value: Any, formatted: str) -> str:
    """Wrap *formatted* in bold green if *value* is the non-zero maximum."""
    if value == max_value and max_value and max_value > 0:
        return f"[bold green]{formatted}[/bold green]"
    return formatted


def print_report(
    account_id: str,
    rows: list[dict[str, Any]],
    weekly_ranges: list[tuple[str, str]],
) -> None:
    """Render one formatted table per week of campaign stats, plus a summary.

    Within each weekly table, the highest Impressions, Clicks, CTR, and
    Conversions values are highlighted in bold green.

    Args:
        account_id: The Google Ads account ID.
        rows: Cleaned list of dicts from the processor (must include
            ``week_start`` and ``week_end`` keys).
        weekly_ranges: The full list of (start, end) tuples (most recent first)
            so that tables appear in that order even if a week has no data.
    """
    console = Console()

    # Group rows by (week_start, week_end) preserving insertion order
    week_groups: OrderedDict[tuple[str, str], list[dict[str, Any]]] = OrderedDict()
    for ws, we in weekly_ranges:
        week_groups[(ws, we)] = []

    for row in rows:
        key = (row["week_start"], row["week_end"])
        if key in week_groups:
            week_groups[key].append(row)

    grand_total_cost = 0.0
    grand_total_clicks = 0

    for (week_start, week_end), week_rows in week_groups.items():
        table = Table(
            title=f"Account: {account_id}  ({week_start} to {week_end})"
        )
        table.add_column("Campaign", style="cyan", no_wrap=True)
        table.add_column("Impressions", justify="right")
        table.add_column("Clicks", justify="right")
        table.add_column("CTR", justify="right")
        table.add_column("Cost", justify="right")
        table.add_column("CPC", justify="right")
        table.add_column("Conversions", justify="right")

        max_imp = _max(week_rows, "impressions")
        max_clicks = _max(week_rows, "clicks")
        max_ctr = _max(week_rows, "ctr")
        max_conv = _max(week_rows, "conversions")
        week_cost = 0.0
        week_clicks = 0

        for row in week_rows:
            table.add_row(
                row["campaign_name"],
                _maybe_highlight(row["impressions"], max_imp, f"{row['impressions']:,}"),
                _maybe_highlight(row["clicks"], max_clicks, f"{row['clicks']:,}"),
                _maybe_highlight(row["ctr"], max_ctr, f"{row['ctr'] * 100:.1f}%"),
                f"${row['cost']:,.2f}",
                f"${row['cpc']:,.2f}",
                _maybe_highlight(row["conversions"], max_conv, f"{row['conversions']}"),
            )
            week_cost += row["cost"]
            week_clicks += row["clicks"]

        console.print()
        console.print(table)
        console.print(
            f"[bold]Weekly spend:[/bold] ${week_cost:,.2f}   "
            f"[bold]Weekly clicks:[/bold] {week_clicks:,}"
        )

        grand_total_cost += week_cost
        grand_total_clicks += week_clicks

    # Grand total across all weeks
    console.print()
    console.print(
        "[bold]─── 8-Week Totals ───[/bold]"
    )
    console.print(
        f"[bold]Total spend:[/bold] ${grand_total_cost:,.2f}   "
        f"[bold]Total clicks:[/bold] {grand_total_clicks:,}"
    )
    console.print()


def print_error(account_id: str, message: str) -> None:
    """Display an error message for a specific account.

    Args:
        account_id: The Google Ads account ID that caused the error.
        message: The error description.
    """
    console = Console()
    console.print(f"[bold red]Error for account {account_id}:[/bold red] {message}")
    console.print()
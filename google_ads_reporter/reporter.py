"""Terminal output using the rich library."""

from typing import Any

from rich.console import Console
from rich.table import Table


def print_report(
    account_id: str,
    rows: list[dict[str, Any]],
    start_date: str,
    end_date: str,
) -> None:
    """Render a formatted table of campaign stats and a summary line.

    Args:
        account_id: The Google Ads account ID.
        rows: Cleaned list of dicts from the processor.
        start_date: Start date in YYYY-MM-DD format.
        end_date: End date in YYYY-MM-DD format.
    """
    console = Console()

    # Build the table
    table = Table(title=f"Account: {account_id}  ({start_date} to {end_date})")
    table.add_column("Campaign", style="cyan", no_wrap=True)
    table.add_column("Impressions", justify="right")
    table.add_column("Clicks", justify="right")
    table.add_column("CTR", justify="right")
    table.add_column("Cost", justify="right")
    table.add_column("CPC", justify="right")
    table.add_column("Conversions", justify="right")

    total_cost = 0.0
    total_clicks = 0

    for row in rows:
        table.add_row(
            row["campaign_name"],
            f"{row['impressions']:,}",
            f"{row['clicks']:,}",
            f"{row['ctr'] * 100:.1f}%",
            f"${row['cost']:,.2f}",
            f"${row['cpc']:,.2f}",
            f"{row['conversions']}",
        )
        total_cost += row["cost"]
        total_clicks += row["clicks"]

    console.print()
    console.print(table)

    # Summary line
    console.print(
        f"[bold]Total spend:[/bold] ${total_cost:,.2f}   "
        f"[bold]Total clicks:[/bold] {total_clicks:,}"
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
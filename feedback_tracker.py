import asyncclick as click

from core.scrapper import WBFeedbacksScrapper
from core.utils import (
    client_manager,
    common_headers,
    feedbacks_to_table,
    tortoise_context_manager,
)
from core.processing import create_new_feedbacks

@click.command()
@click.option(
    "--article",
    required=True,
    help="WB product article.",
)
@click.option(
    "--valuation",
    required=False,
    default=3,
    help="Product valuation from feedbacks.",
)
@click.option(
    "--day-limit",
    required=False,
    default=3,
    help="The number of recent days from feedbacks was published.",
)
@click.option(
    "--show",
    required=False,
    default=False,
    help="Tabulate and show founded feedbacks.",
)
@click.option(
    "--save",
    required=False,
    default=True,
    help="Save filtered feedbacks in db.",
)
@click.option(
    "--product-root",
    required=False,
    help="Product root, which allows you to get feedbacks faster.",
)
async def feedback_tracker(
    article: int,
    valuation: int,
    day_limit: int,
    show: bool,
    save: bool,
    product_root: int | None,
) -> None:
    """Track and process Wildberries product feedbacks by filters."""
    with client_manager(headers=common_headers()) as client:
        scrapper = WBFeedbacksScrapper(
            article=article,
            client=client,
            root=product_root,
        )
        feedbacks = scrapper.get_feedbacks(
            valuation=valuation,
            day_limit=day_limit,
        )
        if not feedbacks:
            click.echo("Feedbacks are not found!")
            return
        click.echo(f"found {len(feedbacks)} feedbacks")
        if show:
            click.echo(feedbacks_to_table(feedbacks))
        if save:
            async with tortoise_context_manager():
                await create_new_feedbacks(
                    product_article=article,
                    feedbacks=feedbacks,
                )


if __name__ == "__main__":
    feedback_tracker()

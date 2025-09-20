import asyncclick as click

from core.scrapper import WBFeedbacksScrapper
from core.utils import client_manager, tortoise_context_manager
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
    help="User product valuation from feedback.",
)
@click.option(
    "--day-limit",
    required=False,
    default=3,
    help="The number of recent days for which feedback was published.",
)
@click.option(
    "--product-root",
    required=False,
    help="Product root, which allows you to get feedbacks faster",
)
async def feedback_tracker(
    article: int,
    valuation: int,
    day_limit: int,
    product_root: int | None = None,
) -> None:
    with client_manager() as client:
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
        click.echo(f"find {len(feedbacks)} feedbacks")
        async with tortoise_context_manager():
            await create_new_feedbacks(
                product_article=article,
                feedbacks=feedbacks,
            )


if __name__ == "__main__":
    feedback_tracker()

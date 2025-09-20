import asyncio

from . import schemas, models

DEFAULT_FEEDBACKS_BATCH = 100

async def process_chunk(
    product_article: int,
    chunk: list[schemas.Feedback],
) -> None:
    """Return None and create new Feedback db instances from chunk."""
    feedbacks_ids = [feedback.id for feedback in chunk]
    existing = await models.Feedback().filter(
        product_article=product_article,
        id__in=feedbacks_ids,
    ).values_list(
        "id",
        flat=True,
    )
    to_create = [
        models.Feedback(
            id=feedback.id,
            username=feedback.username,
            product_article=product_article,
            valuation=feedback.valuation,
            comment=feedback.comment,
            pros=feedback.pros,
            cons=feedback.cons,
            created_on_wb=feedback.created_on_wb,
        )
        for feedback in chunk
        if feedback.id not in existing
    ]
    if to_create:
        await models.Feedback.bulk_create(to_create)


async def create_new_feedbacks(
    *,
    product_article: int,
    feedbacks: list[schemas.Feedback],
    batch_size: int = DEFAULT_FEEDBACKS_BATCH,
) -> None:
    """Return None and split feedbacks to process them asynchronously."""
    tasks = []
    for i in range(0, len(feedbacks), batch_size):
        chunk = feedbacks[i:i + batch_size]
        tasks.append(process_chunk(product_article, chunk))

    await asyncio.gather(*tasks)

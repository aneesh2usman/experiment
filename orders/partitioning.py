from dateutil.relativedelta import relativedelta
from psqlextra.partitioning import (
    PostgresPartitioningManager,
    PostgresCurrentTimePartitioningStrategy,
    PostgresTimePartitionSize,
)
from psqlextra.partitioning.config import PostgresPartitioningConfig

from orders.models import LineItem, Order

manager = PostgresPartitioningManager(
[
    PostgresPartitioningConfig(
        model=Order,
        strategy=PostgresCurrentTimePartitioningStrategy(
            size=PostgresTimePartitionSize(months=6),
            count=3,
            max_age=relativedelta(years=3),
        ),
    ),
    PostgresPartitioningConfig(
        model=LineItem,
        strategy=PostgresCurrentTimePartitioningStrategy(
            size=PostgresTimePartitionSize(months=6),
            count=3,
            max_age=relativedelta(years=3),
        ),
    )
]

)
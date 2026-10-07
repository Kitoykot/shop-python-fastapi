import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from app.commands.order.cancel_expired_orders import main as cancel_expired_orders


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    scheduler = BlockingScheduler(timezone='UTC')

    scheduler.add_job(
        cancel_expired_orders,
        trigger='interval',
        minutes=1,
        id='cancel_expired_orders',
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()


if __name__ == '__main__':
    main()

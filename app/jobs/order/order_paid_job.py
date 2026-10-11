from app.dto.order.read.data.order_data_dto import OrderDataDto
from app.services.mail.mail_service import MailService


def notify_order_paid(order: OrderDataDto) -> None:
    from config.mail.settings import mail_settings

    mail_service = MailService(
        host=mail_settings.smtp_host,
        port=mail_settings.smtp_port,
        sender=mail_settings.smtp_from,
    )

    mail_service.send(
        recipient=order.user_email,
        subject='Заказ оплачен!',
        body=(
            f'{order.user_name}, ваш заказ на сумму '
            f'{order.total_price} успешно оплачен!'
        ),
    )

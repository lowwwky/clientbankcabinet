import uuid
from decimal import Decimal


# пока заглушка
def send_transfer(operation_id: uuid.UUID, transfer_type: str, recipient: str,
                  bank: str, amount: Decimal) -> str:
    return "Успешно"

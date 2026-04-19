"""Saída de progresso da pipeline (CLI)."""


def line(message: str) -> None:
    print(message)


def total(label: str, count: int) -> None:
    print(f"Total de registros {label}: {count}")


def total_atualizados(label: str, count: int) -> None:
    print(f"Total de registros {label} atualizados: {count}")

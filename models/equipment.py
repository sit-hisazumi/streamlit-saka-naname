from dataclasses import dataclass
from typing import List


@dataclass
class MachineType:
    """加工機タイプ（種類）"""

    name: str  # 加工機名（例: "加工機A"）
    producible_products: List[str]  # 製造可能な製品リスト


@dataclass
class MachineInstance:
    """加工機実体（個別の機械）"""

    machine_type: MachineType  # 所属する加工機タイプ
    instance_name: str  # 個体識別名（例: "A-1"）

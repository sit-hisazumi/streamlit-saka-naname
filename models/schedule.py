from dataclasses import dataclass

from models.equipment import MachineInstance


@dataclass
class ProductionSchedule:
    """生産スケジュール"""

    product_name: str  # 製品名（例: "製品A"）
    quantity: int  # 生産数量
    machine_instance: MachineInstance  # 使用する加工機実体
    start_time: str  # 開始日時（ISO 8601形式）
    end_time: str  # 終了日時（ISO 8601形式）


@dataclass
class MaintenanceSchedule:
    """メンテナンススケジュール"""

    machine_instance: MachineInstance  # メンテナンス対象の加工機実体
    start_time: str  # 開始日時（ISO 8601形式）
    end_time: str  # 終了日時（ISO 8601形式）
    maintenance_type: str  # メンテナンス種別（例: "大規模定期メンテナンス"）

from models.equipment import MachineInstance, MachineType

# 加工機タイプの定義
MACHINE_TYPE_A = MachineType(name="加工機A", producible_products=["製品A", "製品B"])

MACHINE_TYPE_B = MachineType(name="加工機B", producible_products=["製品C", "製品D", "製品E"])

# 加工機実体の定義
MACHINE_INSTANCES = [
    # 加工機A（2台）
    MachineInstance(machine_type=MACHINE_TYPE_A, instance_name="A-1"),
    MachineInstance(machine_type=MACHINE_TYPE_A, instance_name="A-2"),
    # 加工機B（3台）
    MachineInstance(machine_type=MACHINE_TYPE_B, instance_name="B-1"),
    MachineInstance(machine_type=MACHINE_TYPE_B, instance_name="B-2"),
    MachineInstance(machine_type=MACHINE_TYPE_B, instance_name="B-3"),
]

# 加工機タイプ一覧
MACHINE_TYPES = [MACHINE_TYPE_A, MACHINE_TYPE_B]

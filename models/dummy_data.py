from models.equipment import MachineInstance, MachineType
from models.schedule import MaintenanceSchedule, ProductionSchedule

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

# メンテナンススケジュール
# 3ヶ月に1回程度の頻度で、1ヶ月間に1-2台がメンテナンス対象
# 大規模メンテナンスのため、期間中は該当機械の生産が完全停止
MAINTENANCE_SCHEDULES = [
    # B-2の大規模定期メンテナンス（1月20日～24日の5営業日）
    MaintenanceSchedule(
        machine_instance=MACHINE_INSTANCES[3],  # B-2
        start_time="2026-01-20T09:00:00",
        end_time="2026-01-24T17:00:00",
        maintenance_type="大規模定期メンテナンス",
    ),
    # A-1の大規模定期メンテナンス（2月3日～7日の5営業日）
    MaintenanceSchedule(
        machine_instance=MACHINE_INSTANCES[0],  # A-1
        start_time="2026-02-03T09:00:00",
        end_time="2026-02-07T17:00:00",
        maintenance_type="大規模定期メンテナンス",
    ),
]

# 生産スケジュール
# 営業時間: 平日9:00-17:00
# メンテナンス期間中は該当機械の生産をスケジュールしない
PRODUCTION_SCHEDULES = [
    # 第1週（1月15日～17日）
    ProductionSchedule(
        product_name="製品A",
        quantity=150,
        machine_instance=MACHINE_INSTANCES[0],  # A-1
        start_time="2026-01-15T09:00:00",
        end_time="2026-01-15T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品B",
        quantity=120,
        machine_instance=MACHINE_INSTANCES[1],  # A-2
        start_time="2026-01-15T09:00:00",
        end_time="2026-01-15T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品C",
        quantity=180,
        machine_instance=MACHINE_INSTANCES[2],  # B-1
        start_time="2026-01-15T09:00:00",
        end_time="2026-01-15T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品D",
        quantity=140,
        machine_instance=MACHINE_INSTANCES[3],  # B-2
        start_time="2026-01-15T09:00:00",
        end_time="2026-01-15T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品E",
        quantity=160,
        machine_instance=MACHINE_INSTANCES[4],  # B-3
        start_time="2026-01-15T09:00:00",
        end_time="2026-01-15T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品A",
        quantity=130,
        machine_instance=MACHINE_INSTANCES[0],  # A-1
        start_time="2026-01-16T09:00:00",
        end_time="2026-01-16T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品C",
        quantity=200,
        machine_instance=MACHINE_INSTANCES[2],  # B-1
        start_time="2026-01-16T09:00:00",
        end_time="2026-01-16T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品E",
        quantity=150,
        machine_instance=MACHINE_INSTANCES[4],  # B-3
        start_time="2026-01-16T09:00:00",
        end_time="2026-01-16T17:00:00",
    ),
    # 第2週（1月19日～23日）- B-2はメンテナンス中（1/20-24）のため生産なし
    ProductionSchedule(
        product_name="製品B",
        quantity=100,
        machine_instance=MACHINE_INSTANCES[1],  # A-2
        start_time="2026-01-19T09:00:00",
        end_time="2026-01-19T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品C",
        quantity=185,
        machine_instance=MACHINE_INSTANCES[2],  # B-1
        start_time="2026-01-19T09:00:00",
        end_time="2026-01-19T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品A",
        quantity=140,
        machine_instance=MACHINE_INSTANCES[0],  # A-1
        start_time="2026-01-20T09:00:00",
        end_time="2026-01-20T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品C",
        quantity=190,
        machine_instance=MACHINE_INSTANCES[2],  # B-1
        start_time="2026-01-20T09:00:00",
        end_time="2026-01-20T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品E",
        quantity=170,
        machine_instance=MACHINE_INSTANCES[4],  # B-3
        start_time="2026-01-20T09:00:00",
        end_time="2026-01-20T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品B",
        quantity=110,
        machine_instance=MACHINE_INSTANCES[1],  # A-2
        start_time="2026-01-21T09:00:00",
        end_time="2026-01-21T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品D",
        quantity=150,
        machine_instance=MACHINE_INSTANCES[2],  # B-1
        start_time="2026-01-21T09:00:00",
        end_time="2026-01-21T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品A",
        quantity=145,
        machine_instance=MACHINE_INSTANCES[0],  # A-1
        start_time="2026-01-22T09:00:00",
        end_time="2026-01-22T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品C",
        quantity=185,
        machine_instance=MACHINE_INSTANCES[4],  # B-3
        start_time="2026-01-22T09:00:00",
        end_time="2026-01-22T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品B",
        quantity=115,
        machine_instance=MACHINE_INSTANCES[1],  # A-2
        start_time="2026-01-23T09:00:00",
        end_time="2026-01-23T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品E",
        quantity=155,
        machine_instance=MACHINE_INSTANCES[2],  # B-1
        start_time="2026-01-23T09:00:00",
        end_time="2026-01-23T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品A",
        quantity=135,
        machine_instance=MACHINE_INSTANCES[0],  # A-1
        start_time="2026-01-23T09:00:00",
        end_time="2026-01-23T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品C",
        quantity=175,
        machine_instance=MACHINE_INSTANCES[4],  # B-3
        start_time="2026-01-23T09:00:00",
        end_time="2026-01-23T17:00:00",
    ),
    # 第3週（1月26日～30日）
    ProductionSchedule(
        product_name="製品B",
        quantity=125,
        machine_instance=MACHINE_INSTANCES[1],  # A-2
        start_time="2026-01-26T09:00:00",
        end_time="2026-01-26T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品C",
        quantity=195,
        machine_instance=MACHINE_INSTANCES[2],  # B-1
        start_time="2026-01-26T09:00:00",
        end_time="2026-01-26T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品D",
        quantity=135,
        machine_instance=MACHINE_INSTANCES[3],  # B-2
        start_time="2026-01-26T09:00:00",
        end_time="2026-01-26T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品A",
        quantity=150,
        machine_instance=MACHINE_INSTANCES[0],  # A-1
        start_time="2026-01-27T09:00:00",
        end_time="2026-01-27T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品E",
        quantity=165,
        machine_instance=MACHINE_INSTANCES[4],  # B-3
        start_time="2026-01-27T09:00:00",
        end_time="2026-01-27T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品B",
        quantity=105,
        machine_instance=MACHINE_INSTANCES[1],  # A-2
        start_time="2026-01-28T09:00:00",
        end_time="2026-01-28T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品C",
        quantity=175,
        machine_instance=MACHINE_INSTANCES[3],  # B-2
        start_time="2026-01-28T09:00:00",
        end_time="2026-01-28T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品A",
        quantity=140,
        machine_instance=MACHINE_INSTANCES[0],  # A-1
        start_time="2026-01-29T09:00:00",
        end_time="2026-01-29T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品D",
        quantity=150,
        machine_instance=MACHINE_INSTANCES[2],  # B-1
        start_time="2026-01-29T09:00:00",
        end_time="2026-01-29T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品B",
        quantity=120,
        machine_instance=MACHINE_INSTANCES[1],  # A-2
        start_time="2026-01-30T09:00:00",
        end_time="2026-01-30T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品E",
        quantity=160,
        machine_instance=MACHINE_INSTANCES[4],  # B-3
        start_time="2026-01-30T09:00:00",
        end_time="2026-01-30T17:00:00",
    ),
    # 第4週（2月2日～6日）- A-1はメンテナンス中（2/3-7）のため生産なし
    ProductionSchedule(
        product_name="製品B",
        quantity=110,
        machine_instance=MACHINE_INSTANCES[1],  # A-2
        start_time="2026-02-02T09:00:00",
        end_time="2026-02-02T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品C",
        quantity=180,
        machine_instance=MACHINE_INSTANCES[2],  # B-1
        start_time="2026-02-02T09:00:00",
        end_time="2026-02-02T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品D",
        quantity=140,
        machine_instance=MACHINE_INSTANCES[3],  # B-2
        start_time="2026-02-02T09:00:00",
        end_time="2026-02-02T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品E",
        quantity=155,
        machine_instance=MACHINE_INSTANCES[4],  # B-3
        start_time="2026-02-04T09:00:00",
        end_time="2026-02-04T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品B",
        quantity=115,
        machine_instance=MACHINE_INSTANCES[1],  # A-2
        start_time="2026-02-04T09:00:00",
        end_time="2026-02-04T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品C",
        quantity=190,
        machine_instance=MACHINE_INSTANCES[2],  # B-1
        start_time="2026-02-05T09:00:00",
        end_time="2026-02-05T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品D",
        quantity=145,
        machine_instance=MACHINE_INSTANCES[3],  # B-2
        start_time="2026-02-05T09:00:00",
        end_time="2026-02-05T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品B",
        quantity=125,
        machine_instance=MACHINE_INSTANCES[1],  # A-2
        start_time="2026-02-06T09:00:00",
        end_time="2026-02-06T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品E",
        quantity=170,
        machine_instance=MACHINE_INSTANCES[4],  # B-3
        start_time="2026-02-06T09:00:00",
        end_time="2026-02-06T17:00:00",
    ),
    # 第5週（2月9日～13日）
    ProductionSchedule(
        product_name="製品A",
        quantity=145,
        machine_instance=MACHINE_INSTANCES[0],  # A-1
        start_time="2026-02-09T09:00:00",
        end_time="2026-02-09T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品D",
        quantity=150,
        machine_instance=MACHINE_INSTANCES[3],  # B-2
        start_time="2026-02-09T09:00:00",
        end_time="2026-02-09T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品E",
        quantity=160,
        machine_instance=MACHINE_INSTANCES[4],  # B-3
        start_time="2026-02-09T09:00:00",
        end_time="2026-02-09T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品B",
        quantity=120,
        machine_instance=MACHINE_INSTANCES[1],  # A-2
        start_time="2026-02-10T09:00:00",
        end_time="2026-02-10T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品C",
        quantity=195,
        machine_instance=MACHINE_INSTANCES[2],  # B-1
        start_time="2026-02-10T09:00:00",
        end_time="2026-02-10T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品A",
        quantity=135,
        machine_instance=MACHINE_INSTANCES[0],  # A-1
        start_time="2026-02-12T09:00:00",
        end_time="2026-02-12T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品D",
        quantity=140,
        machine_instance=MACHINE_INSTANCES[3],  # B-2
        start_time="2026-02-12T09:00:00",
        end_time="2026-02-12T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品B",
        quantity=115,
        machine_instance=MACHINE_INSTANCES[1],  # A-2
        start_time="2026-02-13T09:00:00",
        end_time="2026-02-13T17:00:00",
    ),
    ProductionSchedule(
        product_name="製品E",
        quantity=175,
        machine_instance=MACHINE_INSTANCES[4],  # B-3
        start_time="2026-02-13T09:00:00",
        end_time="2026-02-13T17:00:00",
    ),
]

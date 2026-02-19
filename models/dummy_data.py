from datetime import date, datetime, time, timedelta

from models.equipment import MachineInstance, MachineType
from models.schedule import MaintenanceSchedule, ProductionSchedule

_START = time(9, 0)
_END = time(17, 0)


def _dt(base_monday: date, day_offset: int, t: time) -> str:
    """base_mondayからのオフセット日数と時刻でISO 8601文字列を生成"""
    return datetime.combine(base_monday + timedelta(days=day_offset), t).isoformat()

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


def get_maintenance_schedules():
    """メンテナンススケジュールを生成（現在週ベース）"""
    today = date.today()
    base_monday = today - timedelta(days=today.weekday())

    return [
        # B-2の大規模定期メンテナンス（第2週火曜～土曜の5営業日）
        MaintenanceSchedule(
            machine_instance=MACHINE_INSTANCES[3],  # B-2
            start_time=_dt(base_monday, 8, _START),
            end_time=_dt(base_monday, 12, _END),
            maintenance_type="大規模定期メンテナンス",
        ),
        # A-1の大規模定期メンテナンス（第4週火曜～土曜の5営業日）
        MaintenanceSchedule(
            machine_instance=MACHINE_INSTANCES[0],  # A-1
            start_time=_dt(base_monday, 22, _START),
            end_time=_dt(base_monday, 26, _END),
            maintenance_type="大規模定期メンテナンス",
        ),
    ]

# 生産スケジュール
# 営業時間: 平日9:00-17:00
# メンテナンス期間中は該当機械の生産をスケジュールしない


def get_production_schedules():
    """生産スケジュールを生成（現在週ベース）"""
    today = date.today()
    base_monday = today - timedelta(days=today.weekday())

    return [
        # 第1週（木曜～金曜）
        ProductionSchedule(
            product_name="製品A",
            quantity=150,
            machine_instance=MACHINE_INSTANCES[0],  # A-1
            start_time=_dt(base_monday, 3, _START),
            end_time=_dt(base_monday, 3, _END),
        ),
        ProductionSchedule(
            product_name="製品B",
            quantity=120,
            machine_instance=MACHINE_INSTANCES[1],  # A-2
            start_time=_dt(base_monday, 3, _START),
            end_time=_dt(base_monday, 3, _END),
        ),
        ProductionSchedule(
            product_name="製品C",
            quantity=180,
            machine_instance=MACHINE_INSTANCES[2],  # B-1
            start_time=_dt(base_monday, 3, _START),
            end_time=_dt(base_monday, 3, _END),
        ),
        ProductionSchedule(
            product_name="製品D",
            quantity=140,
            machine_instance=MACHINE_INSTANCES[3],  # B-2
            start_time=_dt(base_monday, 3, _START),
            end_time=_dt(base_monday, 3, _END),
        ),
        ProductionSchedule(
            product_name="製品E",
            quantity=160,
            machine_instance=MACHINE_INSTANCES[4],  # B-3
            start_time=_dt(base_monday, 3, _START),
            end_time=_dt(base_monday, 3, _END),
        ),
        ProductionSchedule(
            product_name="製品A",
            quantity=130,
            machine_instance=MACHINE_INSTANCES[0],  # A-1
            start_time=_dt(base_monday, 4, _START),
            end_time=_dt(base_monday, 4, _END),
        ),
        ProductionSchedule(
            product_name="製品C",
            quantity=200,
            machine_instance=MACHINE_INSTANCES[2],  # B-1
            start_time=_dt(base_monday, 4, _START),
            end_time=_dt(base_monday, 4, _END),
        ),
        ProductionSchedule(
            product_name="製品E",
            quantity=150,
            machine_instance=MACHINE_INSTANCES[4],  # B-3
            start_time=_dt(base_monday, 4, _START),
            end_time=_dt(base_monday, 4, _END),
        ),
        # 第2週（月曜～金曜）- B-2はメンテナンス中のため生産なし
        ProductionSchedule(
            product_name="製品B",
            quantity=100,
            machine_instance=MACHINE_INSTANCES[1],  # A-2
            start_time=_dt(base_monday, 7, _START),
            end_time=_dt(base_monday, 7, _END),
        ),
        ProductionSchedule(
            product_name="製品C",
            quantity=185,
            machine_instance=MACHINE_INSTANCES[2],  # B-1
            start_time=_dt(base_monday, 7, _START),
            end_time=_dt(base_monday, 7, _END),
        ),
        ProductionSchedule(
            product_name="製品A",
            quantity=140,
            machine_instance=MACHINE_INSTANCES[0],  # A-1
            start_time=_dt(base_monday, 8, _START),
            end_time=_dt(base_monday, 8, _END),
        ),
        ProductionSchedule(
            product_name="製品C",
            quantity=190,
            machine_instance=MACHINE_INSTANCES[2],  # B-1
            start_time=_dt(base_monday, 8, _START),
            end_time=_dt(base_monday, 8, _END),
        ),
        ProductionSchedule(
            product_name="製品E",
            quantity=170,
            machine_instance=MACHINE_INSTANCES[4],  # B-3
            start_time=_dt(base_monday, 8, _START),
            end_time=_dt(base_monday, 8, _END),
        ),
        ProductionSchedule(
            product_name="製品B",
            quantity=110,
            machine_instance=MACHINE_INSTANCES[1],  # A-2
            start_time=_dt(base_monday, 9, _START),
            end_time=_dt(base_monday, 9, _END),
        ),
        ProductionSchedule(
            product_name="製品D",
            quantity=150,
            machine_instance=MACHINE_INSTANCES[2],  # B-1
            start_time=_dt(base_monday, 9, _START),
            end_time=_dt(base_monday, 9, _END),
        ),
        ProductionSchedule(
            product_name="製品A",
            quantity=145,
            machine_instance=MACHINE_INSTANCES[0],  # A-1
            start_time=_dt(base_monday, 10, _START),
            end_time=_dt(base_monday, 10, _END),
        ),
        ProductionSchedule(
            product_name="製品C",
            quantity=185,
            machine_instance=MACHINE_INSTANCES[4],  # B-3
            start_time=_dt(base_monday, 10, _START),
            end_time=_dt(base_monday, 10, _END),
        ),
        ProductionSchedule(
            product_name="製品B",
            quantity=115,
            machine_instance=MACHINE_INSTANCES[1],  # A-2
            start_time=_dt(base_monday, 11, _START),
            end_time=_dt(base_monday, 11, _END),
        ),
        ProductionSchedule(
            product_name="製品E",
            quantity=155,
            machine_instance=MACHINE_INSTANCES[2],  # B-1
            start_time=_dt(base_monday, 11, _START),
            end_time=_dt(base_monday, 11, _END),
        ),
        ProductionSchedule(
            product_name="製品A",
            quantity=135,
            machine_instance=MACHINE_INSTANCES[0],  # A-1
            start_time=_dt(base_monday, 11, _START),
            end_time=_dt(base_monday, 11, _END),
        ),
        ProductionSchedule(
            product_name="製品C",
            quantity=175,
            machine_instance=MACHINE_INSTANCES[4],  # B-3
            start_time=_dt(base_monday, 11, _START),
            end_time=_dt(base_monday, 11, _END),
        ),
        # 第3週（月曜～金曜）
        ProductionSchedule(
            product_name="製品B",
            quantity=125,
            machine_instance=MACHINE_INSTANCES[1],  # A-2
            start_time=_dt(base_monday, 14, _START),
            end_time=_dt(base_monday, 14, _END),
        ),
        ProductionSchedule(
            product_name="製品C",
            quantity=195,
            machine_instance=MACHINE_INSTANCES[2],  # B-1
            start_time=_dt(base_monday, 14, _START),
            end_time=_dt(base_monday, 14, _END),
        ),
        ProductionSchedule(
            product_name="製品D",
            quantity=135,
            machine_instance=MACHINE_INSTANCES[3],  # B-2
            start_time=_dt(base_monday, 14, _START),
            end_time=_dt(base_monday, 14, _END),
        ),
        ProductionSchedule(
            product_name="製品A",
            quantity=150,
            machine_instance=MACHINE_INSTANCES[0],  # A-1
            start_time=_dt(base_monday, 15, _START),
            end_time=_dt(base_monday, 15, _END),
        ),
        ProductionSchedule(
            product_name="製品E",
            quantity=165,
            machine_instance=MACHINE_INSTANCES[4],  # B-3
            start_time=_dt(base_monday, 15, _START),
            end_time=_dt(base_monday, 15, _END),
        ),
        ProductionSchedule(
            product_name="製品B",
            quantity=105,
            machine_instance=MACHINE_INSTANCES[1],  # A-2
            start_time=_dt(base_monday, 16, _START),
            end_time=_dt(base_monday, 16, _END),
        ),
        ProductionSchedule(
            product_name="製品C",
            quantity=175,
            machine_instance=MACHINE_INSTANCES[3],  # B-2
            start_time=_dt(base_monday, 16, _START),
            end_time=_dt(base_monday, 16, _END),
        ),
        ProductionSchedule(
            product_name="製品A",
            quantity=140,
            machine_instance=MACHINE_INSTANCES[0],  # A-1
            start_time=_dt(base_monday, 17, _START),
            end_time=_dt(base_monday, 17, _END),
        ),
        ProductionSchedule(
            product_name="製品D",
            quantity=150,
            machine_instance=MACHINE_INSTANCES[2],  # B-1
            start_time=_dt(base_monday, 17, _START),
            end_time=_dt(base_monday, 17, _END),
        ),
        ProductionSchedule(
            product_name="製品B",
            quantity=120,
            machine_instance=MACHINE_INSTANCES[1],  # A-2
            start_time=_dt(base_monday, 18, _START),
            end_time=_dt(base_monday, 18, _END),
        ),
        ProductionSchedule(
            product_name="製品E",
            quantity=160,
            machine_instance=MACHINE_INSTANCES[4],  # B-3
            start_time=_dt(base_monday, 18, _START),
            end_time=_dt(base_monday, 18, _END),
        ),
        # 第4週（月曜～金曜）- A-1はメンテナンス中のため生産なし
        ProductionSchedule(
            product_name="製品B",
            quantity=110,
            machine_instance=MACHINE_INSTANCES[1],  # A-2
            start_time=_dt(base_monday, 21, _START),
            end_time=_dt(base_monday, 21, _END),
        ),
        ProductionSchedule(
            product_name="製品C",
            quantity=180,
            machine_instance=MACHINE_INSTANCES[2],  # B-1
            start_time=_dt(base_monday, 21, _START),
            end_time=_dt(base_monday, 21, _END),
        ),
        ProductionSchedule(
            product_name="製品D",
            quantity=140,
            machine_instance=MACHINE_INSTANCES[3],  # B-2
            start_time=_dt(base_monday, 21, _START),
            end_time=_dt(base_monday, 21, _END),
        ),
        ProductionSchedule(
            product_name="製品E",
            quantity=155,
            machine_instance=MACHINE_INSTANCES[4],  # B-3
            start_time=_dt(base_monday, 23, _START),
            end_time=_dt(base_monday, 23, _END),
        ),
        ProductionSchedule(
            product_name="製品B",
            quantity=115,
            machine_instance=MACHINE_INSTANCES[1],  # A-2
            start_time=_dt(base_monday, 23, _START),
            end_time=_dt(base_monday, 23, _END),
        ),
        ProductionSchedule(
            product_name="製品C",
            quantity=190,
            machine_instance=MACHINE_INSTANCES[2],  # B-1
            start_time=_dt(base_monday, 24, _START),
            end_time=_dt(base_monday, 24, _END),
        ),
        ProductionSchedule(
            product_name="製品D",
            quantity=145,
            machine_instance=MACHINE_INSTANCES[3],  # B-2
            start_time=_dt(base_monday, 24, _START),
            end_time=_dt(base_monday, 24, _END),
        ),
        ProductionSchedule(
            product_name="製品B",
            quantity=125,
            machine_instance=MACHINE_INSTANCES[1],  # A-2
            start_time=_dt(base_monday, 25, _START),
            end_time=_dt(base_monday, 25, _END),
        ),
        ProductionSchedule(
            product_name="製品E",
            quantity=170,
            machine_instance=MACHINE_INSTANCES[4],  # B-3
            start_time=_dt(base_monday, 25, _START),
            end_time=_dt(base_monday, 25, _END),
        ),
        # 第5週（月曜～金曜）
        ProductionSchedule(
            product_name="製品A",
            quantity=145,
            machine_instance=MACHINE_INSTANCES[0],  # A-1
            start_time=_dt(base_monday, 28, _START),
            end_time=_dt(base_monday, 28, _END),
        ),
        ProductionSchedule(
            product_name="製品D",
            quantity=150,
            machine_instance=MACHINE_INSTANCES[3],  # B-2
            start_time=_dt(base_monday, 28, _START),
            end_time=_dt(base_monday, 28, _END),
        ),
        ProductionSchedule(
            product_name="製品E",
            quantity=160,
            machine_instance=MACHINE_INSTANCES[4],  # B-3
            start_time=_dt(base_monday, 28, _START),
            end_time=_dt(base_monday, 28, _END),
        ),
        ProductionSchedule(
            product_name="製品B",
            quantity=120,
            machine_instance=MACHINE_INSTANCES[1],  # A-2
            start_time=_dt(base_monday, 29, _START),
            end_time=_dt(base_monday, 29, _END),
        ),
        ProductionSchedule(
            product_name="製品C",
            quantity=195,
            machine_instance=MACHINE_INSTANCES[2],  # B-1
            start_time=_dt(base_monday, 29, _START),
            end_time=_dt(base_monday, 29, _END),
        ),
        ProductionSchedule(
            product_name="製品A",
            quantity=135,
            machine_instance=MACHINE_INSTANCES[0],  # A-1
            start_time=_dt(base_monday, 31, _START),
            end_time=_dt(base_monday, 31, _END),
        ),
        ProductionSchedule(
            product_name="製品D",
            quantity=140,
            machine_instance=MACHINE_INSTANCES[3],  # B-2
            start_time=_dt(base_monday, 31, _START),
            end_time=_dt(base_monday, 31, _END),
        ),
        ProductionSchedule(
            product_name="製品B",
            quantity=115,
            machine_instance=MACHINE_INSTANCES[1],  # A-2
            start_time=_dt(base_monday, 32, _START),
            end_time=_dt(base_monday, 32, _END),
        ),
        ProductionSchedule(
            product_name="製品E",
            quantity=175,
            machine_instance=MACHINE_INSTANCES[4],  # B-3
            start_time=_dt(base_monday, 32, _START),
            end_time=_dt(base_monday, 32, _END),
        ),
    ]

# 製品マスタ
PRODUCTS = [
    {"name": "製品A", "stock": 220, "unit": "個"},
    {"name": "製品B", "stock": 185, "unit": "個"},
    {"name": "製品C", "stock": 300, "unit": "個"},
    {"name": "製品D", "stock": 145, "unit": "個"},
    {"name": "製品E", "stock": 250, "unit": "個"},
]

# 注文リスト
ORDERS = [
    {
        "customer": "株式会社サンプル商事",
        "product": "製品A",
        "quantity": 30,
        "delivery_date": "2025-12-20",
        "status": "未出荷",
    },
    {
        "customer": "テスト工業株式会社",
        "product": "製品B",
        "quantity": 50,
        "delivery_date": "2025-12-22",
        "status": "未出荷",
    },
    {
        "customer": "ダミー株式会社",
        "product": "製品C",
        "quantity": 100,
        "delivery_date": "2025-12-25",
        "status": "未出荷",
    },
    {
        "customer": "サンプル物産",
        "product": "製品A",
        "quantity": 20,
        "delivery_date": "2025-12-19",
        "status": "出荷済",
    },
    {
        "customer": "テストトレーディング",
        "product": "製品E",
        "quantity": 75,
        "delivery_date": "2025-12-28",
        "status": "未出荷",
    },
]


def get_transactions():
    """入出庫履歴を生成（現在時刻ベース）"""
    base_date = datetime.now()
    return [
        # 約10週間前から現在までのデータ
        {
            "datetime": (base_date - timedelta(days=70, hours=10)).strftime(
                "%Y-%m-%d %H:%M"
            ),
            "type": "入庫",
            "product": "製品A",
            "quantity": 150,
            "note": "製造完了分",
        },
        {
            "datetime": (base_date - timedelta(days=65, hours=14)).strftime(
                "%Y-%m-%d %H:%M"
            ),
            "type": "出庫",
            "product": "製品A",
            "quantity": 80,
            "note": "サンプル商事向け出荷",
        },
        {
            "datetime": (base_date - timedelta(days=56, hours=9)).strftime(
                "%Y-%m-%d %H:%M"
            ),
            "type": "入庫",
            "product": "製品C",
            "quantity": 200,
            "note": "製造完了分",
        },
        {
            "datetime": (base_date - timedelta(days=49, hours=15)).strftime(
                "%Y-%m-%d %H:%M"
            ),
            "type": "出庫",
            "product": "製品C",
            "quantity": 100,
            "note": "テスト工業向け出荷",
        },
        {
            "datetime": (base_date - timedelta(days=42, hours=11)).strftime(
                "%Y-%m-%d %H:%M"
            ),
            "type": "入庫",
            "product": "製品B",
            "quantity": 120,
            "note": "製造完了分",
        },
        {
            "datetime": (base_date - timedelta(days=35, hours=13)).strftime(
                "%Y-%m-%d %H:%M"
            ),
            "type": "出庫",
            "product": "製品B",
            "quantity": 60,
            "note": "ダミー株式会社向け出荷",
        },
        {
            "datetime": (base_date - timedelta(days=28, hours=10)).strftime(
                "%Y-%m-%d %H:%M"
            ),
            "type": "入庫",
            "product": "製品E",
            "quantity": 180,
            "note": "製造完了分",
        },
        {
            "datetime": (base_date - timedelta(days=21, hours=16)).strftime(
                "%Y-%m-%d %H:%M"
            ),
            "type": "出庫",
            "product": "製品E",
            "quantity": 90,
            "note": "サンプル物産向け出荷",
        },
        {
            "datetime": (base_date - timedelta(days=14, hours=9)).strftime(
                "%Y-%m-%d %H:%M"
            ),
            "type": "入庫",
            "product": "製品D",
            "quantity": 100,
            "note": "製造完了分",
        },
        {
            "datetime": (base_date - timedelta(days=7, hours=14)).strftime(
                "%Y-%m-%d %H:%M"
            ),
            "type": "出庫",
            "product": "製品D",
            "quantity": 45,
            "note": "テストトレーディング向け出荷",
        },
        {
            "datetime": (base_date - timedelta(days=5, hours=10)).strftime(
                "%Y-%m-%d %H:%M"
            ),
            "type": "入庫",
            "product": "製品A",
            "quantity": 100,
            "note": "製造完了分",
        },
        {
            "datetime": (base_date - timedelta(days=4, hours=14)).strftime(
                "%Y-%m-%d %H:%M"
            ),
            "type": "出庫",
            "product": "製品A",
            "quantity": 50,
            "note": "サンプル商事向け出荷",
        },
        {
            "datetime": (base_date - timedelta(days=3, hours=9)).strftime(
                "%Y-%m-%d %H:%M"
            ),
            "type": "入庫",
            "product": "製品B",
            "quantity": 80,
            "note": "製造完了分",
        },
        {
            "datetime": (base_date - timedelta(days=2, hours=16)).strftime(
                "%Y-%m-%d %H:%M"
            ),
            "type": "出庫",
            "product": "製品B",
            "quantity": 30,
            "note": "テスト工業向け出荷",
        },
        {
            "datetime": (base_date - timedelta(days=1, hours=11)).strftime(
                "%Y-%m-%d %H:%M"
            ),
            "type": "入庫",
            "product": "製品E",
            "quantity": 120,
            "note": "製造完了分",
        },
        {
            "datetime": (base_date - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"),
            "type": "出庫",
            "product": "製品C",
            "quantity": 50,
            "note": "ダミー株式会社向け出荷",
        },
        {
            "datetime": (base_date - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
            "type": "入庫",
            "product": "製品A",
            "quantity": 70,
            "note": "製造完了分",
        },
    ]


def initialize_session_state(session_state):
    """セッション状態を初期化（ダミーデータの設定）"""
    # 製品マスタ
    if "products" not in session_state:
        session_state.products = PRODUCTS.copy()

    # 注文リスト
    if "orders" not in session_state:
        session_state.orders = ORDERS.copy()

    # 入出庫履歴
    if "transactions" not in session_state:
        session_state.transactions = get_transactions()

    # メンテナンススケジュール（ダミーデータ + ユーザー入力分）
    if "maintenance_schedules" not in session_state:
        session_state.maintenance_schedules = []

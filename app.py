import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import altair as alt
import plotly.express as px
from models.dummy_data import (
    initialize_session_state,
    MACHINE_INSTANCES,
)
from models import PRODUCTION_SCHEDULES, MAINTENANCE_SCHEDULES
from models.schedule import MaintenanceSchedule

# ページ設定
st.set_page_config(
    page_title="工場在庫管理ダッシュボード",
    page_icon="🏭",
    layout="wide"
)

# ヘルパー関数
def prepare_gantt_data(production_schedules):
    """ProductionScheduleオブジェクトをPlotlyガントチャート用のDataFrame形式に変換"""
    gantt_data = []

    for schedule in production_schedules:
        gantt_data.append({
            'Task': schedule.machine_instance.instance_name,
            'Start': schedule.start_time,
            'Finish': schedule.end_time,
            'Resource': schedule.product_name,
            'Description': f"{schedule.product_name} ({schedule.quantity}個)"
        })

    return pd.DataFrame(gantt_data)

def create_production_gantt_chart():
    """1ヶ月間の生産スケジュールをガントチャート形式で表示"""
    # 現在日から1ヶ月後までのスケジュールをフィルタリング
    today = datetime.now()
    one_month_later = today + timedelta(days=30)

    filtered_production = [
        s for s in PRODUCTION_SCHEDULES
        if today <= datetime.fromisoformat(s.start_time) <= one_month_later
    ]

    # データが空の場合は空のDataFrameを返す
    if not filtered_production:
        return None

    # ガントチャート用データを準備
    gantt_df = prepare_gantt_data(filtered_production)

    # Plotlyタイムラインチャートを作成
    fig = px.timeline(
        gantt_df,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color="Resource",
        text="Description",
        color_discrete_map={
            '製品A': '#1f77b4',  # 青
            '製品B': '#ff7f0e',  # オレンジ
            '製品C': '#2ca02c',  # 緑
            '製品D': '#d62728',  # 赤
            '製品E': '#9467bd'   # 紫
        },
        category_orders={
            'Task': ['A-1', 'A-2', 'B-1', 'B-2', 'B-3']  # 加工機の順序を固定
        }
    )

    # レイアウトをカスタマイズ
    fig.update_layout(
        xaxis_title="日時",
        yaxis_title="加工機",
        height=400,
        showlegend=True,
        legend_title_text="製品",
        hovermode='closest',
        font=dict(family="Arial, sans-serif", size=12)
    )

    # X軸の表示範囲とフォーマット、グリッド線を設定
    fig.update_xaxes(
        range=[today.isoformat(), one_month_later.isoformat()],
        tickformat="%m/%d",
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        dtick=86400000  # 1日ごとにグリッド線を表示 (ミリ秒単位)
    )

    # Y軸にもグリッド線を設定
    fig.update_yaxes(
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1
    )

    return fig

def create_sales_gantt_chart():
    """営業担当用: 製造スケジュールとメンテナンススケジュールを含むガントチャート"""
    # 現在日から1ヶ月後までのスケジュールをフィルタリング
    today = datetime.now()
    one_month_later = today + timedelta(days=30)

    # 製造スケジュールをフィルタリング
    filtered_production = [
        s for s in PRODUCTION_SCHEDULES
        if today <= datetime.fromisoformat(s.start_time) <= one_month_later
    ]

    # メンテナンススケジュールをフィルタリング
    # グローバルのダミーデータとユーザー入力を統合
    user_maintenance = st.session_state.get('maintenance_schedules', [])
    all_maintenance = MAINTENANCE_SCHEDULES + user_maintenance
    filtered_maintenance = [
        s for s in all_maintenance
        if today <= datetime.fromisoformat(s.start_time) <= one_month_later
    ]

    # データが空の場合
    if not filtered_production and not filtered_maintenance:
        return None

    # ガントチャート用データを準備
    gantt_data = []

    # 製造スケジュールを追加
    for schedule in filtered_production:
        gantt_data.append({
            'Task': schedule.machine_instance.instance_name,
            'Start': schedule.start_time,
            'Finish': schedule.end_time,
            'Resource': schedule.product_name,
            'Description': f"{schedule.product_name} ({schedule.quantity}個)"
        })

    # メンテナンススケジュールを追加
    for schedule in filtered_maintenance:
        gantt_data.append({
            'Task': schedule.machine_instance.instance_name,
            'Start': schedule.start_time,
            'Finish': schedule.end_time,
            'Resource': 'メンテナンス',
            'Description': f"{schedule.maintenance_type}"
        })

    gantt_df = pd.DataFrame(gantt_data)

    # Plotlyタイムラインチャートを作成
    fig = px.timeline(
        gantt_df,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color="Resource",
        text="Description",
        color_discrete_map={
            '製品A': '#1f77b4',
            '製品B': '#ff7f0e',
            '製品C': '#2ca02c',
            '製品D': '#d62728',
            '製品E': '#9467bd',
            'メンテナンス': '#7f7f7f'  # グレー
        },
        category_orders={
            'Task': ['A-1', 'A-2', 'B-1', 'B-2', 'B-3']
        }
    )

    # レイアウトをカスタマイズ
    fig.update_layout(
        xaxis_title="日時",
        yaxis_title="加工機",
        height=400,
        showlegend=True,
        legend_title_text="製品/状態",
        hovermode='closest',
        font=dict(family="Arial, sans-serif", size=12)
    )

    # グリッド線を設定
    fig.update_xaxes(
        range=[today.isoformat(), one_month_later.isoformat()],
        tickformat="%m/%d",
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        dtick=86400000
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1
    )

    return fig

# データ初期化
initialize_session_state(st.session_state)

# サイドバー：表示モード選択
st.sidebar.title("📋 メニュー")
view_mode = st.sidebar.radio(
    "表示モード",
    ["ダッシュボード", "製品詳細", "出荷担当", "製造担当", "営業担当"]
)

# 製品詳細モードの場合、製品選択
selected_product = None
if view_mode == "製品詳細":
    st.sidebar.markdown("---")
    selected_product = st.sidebar.selectbox(
        "製品を選択",
        [p["name"] for p in st.session_state.products]
    )

# ヘッダー
if view_mode == "ダッシュボード":
    st.title("🏭 工場在庫管理ダッシュボード")
elif view_mode == "製品詳細":
    st.title(f"🔍 製品詳細: {selected_product}")
elif view_mode == "出荷担当":
    st.title("📦 出荷担当画面")
elif view_mode == "製造担当":
    st.title("🏗️ 製造担当画面")
elif view_mode == "営業担当":
    st.title("💼 営業担当画面")
st.markdown("---")

# ダッシュボード表示
if view_mode == "ダッシュボード":
    # メトリクス表示
    col1, col2, col3 = st.columns(3)

    today = datetime.now().date()
    today_receipts = sum([t["quantity"] for t in st.session_state.transactions
                          if t["type"] == "入庫" and datetime.strptime(t["datetime"], "%Y-%m-%d %H:%M").date() == today])
    today_shipments = sum([t["quantity"] for t in st.session_state.transactions
                           if t["type"] == "出庫" and datetime.strptime(t["datetime"], "%Y-%m-%d %H:%M").date() == today])
    pending_orders = len([o for o in st.session_state.orders if o["status"] == "未出荷"])

    with col1:
        st.metric("本日の入庫", f"{today_receipts}個")
    with col2:
        st.metric("本日の出庫", f"{today_shipments}個")
    with col3:
        st.metric("未出荷注文", f"{pending_orders}件")

    st.markdown("---")

    # 在庫状況の可視化
    st.subheader("📊 製品別在庫状況")

    # 棒グラフ用データ
    products_df = pd.DataFrame(st.session_state.products)

    # Altairを使用して製品ごとに色分けした棒グラフを作成
    chart = alt.Chart(products_df).mark_bar().encode(
        x=alt.X('name:N', title='製品名', sort=None),
        y=alt.Y('stock:Q', title='在庫数'),
        color=alt.Color('name:N', legend=None, scale=alt.Scale(scheme='category10')),
        tooltip=['name', 'stock', 'unit']
    ).properties(
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

    # 在庫一覧テーブル
    st.subheader("📦 在庫一覧")
    st.dataframe(
        products_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # 入庫・出庫フォーム
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("➕ 入庫登録")
        with st.form("receipt_form"):
            receipt_product = st.selectbox(
                "製品を選択",
                [p["name"] for p in st.session_state.products],
                key="receipt_product"
            )
            receipt_quantity = st.number_input(
                "入庫数",
                min_value=1,
                value=10,
                step=1,
                key="receipt_quantity"
            )
            receipt_note = st.text_input(
                "備考（任意）",
                key="receipt_note"
            )
            receipt_submit = st.form_submit_button("入庫を登録")

            if receipt_submit:
                # 在庫更新
                for product in st.session_state.products:
                    if product["name"] == receipt_product:
                        product["stock"] += receipt_quantity

                # 履歴追加
                st.session_state.transactions.insert(0, {
                    "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "type": "入庫",
                    "product": receipt_product,
                    "quantity": receipt_quantity,
                    "note": receipt_note if receipt_note else "-"
                })

                st.success(f"✅ {receipt_product}を{receipt_quantity}個入庫しました")
                st.rerun()

    with col2:
        st.subheader("➖ 出庫登録")
        with st.form("shipment_form"):
            shipment_product = st.selectbox(
                "製品を選択",
                [p["name"] for p in st.session_state.products],
                key="shipment_product"
            )

            # 選択した製品の在庫数を取得
            current_stock = next((p["stock"] for p in st.session_state.products if p["name"] == shipment_product), 0)

            shipment_quantity = st.number_input(
                f"出庫数（在庫: {current_stock}個）",
                min_value=1,
                max_value=current_stock if current_stock > 0 else 1,
                value=min(10, current_stock) if current_stock > 0 else 1,
                step=1,
                key="shipment_quantity"
            )
            shipment_note = st.text_input(
                "備考（任意）",
                key="shipment_note"
            )
            shipment_submit = st.form_submit_button("出庫を登録")

            if shipment_submit:
                if current_stock >= shipment_quantity:
                    # 在庫更新
                    for product in st.session_state.products:
                        if product["name"] == shipment_product:
                            product["stock"] -= shipment_quantity

                    # 履歴追加
                    st.session_state.transactions.insert(0, {
                        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "type": "出庫",
                        "product": shipment_product,
                        "quantity": shipment_quantity,
                        "note": shipment_note if shipment_note else "-"
                    })

                    st.success(f"✅ {shipment_product}を{shipment_quantity}個出庫しました")
                    st.rerun()
                else:
                    st.error(f"❌ 在庫不足です（在庫: {current_stock}個）")

    st.markdown("---")

    # 注文リスト
    st.subheader("📋 注文リスト")
    orders_df = pd.DataFrame(st.session_state.orders)
    st.dataframe(
        orders_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # 入出庫履歴
    st.subheader("📈 入出庫履歴（最新20件）")
    transactions_df = pd.DataFrame(st.session_state.transactions[:20])

    # 色分けのため、typeに応じてスタイリング
    st.dataframe(
        transactions_df,
        use_container_width=True,
        hide_index=True
    )

# 製品詳細表示
elif view_mode == "製品詳細":
    # 選択した製品の情報を取得
    product_info = next((p for p in st.session_state.products if p["name"] == selected_product), None)

    if product_info:
        # 製品関連のトランザクション
        product_transactions = [t for t in st.session_state.transactions if t["product"] == selected_product]

        # 製品関連の注文
        product_orders = [o for o in st.session_state.orders if o["product"] == selected_product]
        pending_quantity = sum([o["quantity"] for o in product_orders if o["status"] == "未出荷"])

        # 上段：メトリクスとクイック操作
        top_col1, top_col2, top_col3 = st.columns([2, 2, 3])

        with top_col1:
            st.metric("現在庫数", f"{product_info['stock']}{product_info['unit']}")

        with top_col2:
            st.metric("未出荷注文数", f"{pending_quantity}{product_info['unit']}")

        with top_col3:
            # クイック操作をダイアログで実装
            quick_col1, quick_col2 = st.columns(2)
            with quick_col1:
                if st.button("➕ 入庫", use_container_width=True, key="open_receipt_dialog"):
                    st.session_state.show_receipt_dialog = True

            with quick_col2:
                if st.button("➖ 出庫", use_container_width=True, key="open_shipment_dialog"):
                    st.session_state.show_shipment_dialog = True

        # ダイアログ：入庫登録
        if st.session_state.get('show_receipt_dialog', False):
            with st.form("receipt_dialog_form"):
                st.subheader("入庫登録")
                receipt_qty = st.number_input("数量", min_value=1, value=10, key="dialog_receipt_qty")
                receipt_note = st.text_input("備考", key="dialog_receipt_note")

                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("登録", use_container_width=True):
                        product_info["stock"] += receipt_qty
                        st.session_state.transactions.insert(0, {
                            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "type": "入庫",
                            "product": selected_product,
                            "quantity": receipt_qty,
                            "note": receipt_note if receipt_note else "-"
                        })
                        st.session_state.show_receipt_dialog = False
                        st.success(f"✅ {receipt_qty}{product_info['unit']}入庫しました")
                        st.rerun()
                with col2:
                    if st.form_submit_button("キャンセル", use_container_width=True):
                        st.session_state.show_receipt_dialog = False
                        st.rerun()

        # ダイアログ：出庫登録
        if st.session_state.get('show_shipment_dialog', False):
            with st.form("shipment_dialog_form"):
                st.subheader("出庫登録")
                shipment_qty = st.number_input(
                    f"数量（在庫: {product_info['stock']}{product_info['unit']}）",
                    min_value=1,
                    max_value=product_info['stock'] if product_info['stock'] > 0 else 1,
                    value=min(10, product_info['stock']) if product_info['stock'] > 0 else 1,
                    key="dialog_shipment_qty"
                )
                shipment_note = st.text_input("備考", key="dialog_shipment_note")

                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("登録", use_container_width=True):
                        if product_info['stock'] >= shipment_qty:
                            product_info["stock"] -= shipment_qty
                            st.session_state.transactions.insert(0, {
                                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "type": "出庫",
                                "product": selected_product,
                                "quantity": shipment_qty,
                                "note": shipment_note if shipment_note else "-"
                            })
                            st.session_state.show_shipment_dialog = False
                            st.success(f"✅ {shipment_qty}{product_info['unit']}出庫しました")
                            st.rerun()
                        else:
                            st.error(f"❌ 在庫不足です")
                with col2:
                    if st.form_submit_button("キャンセル", use_container_width=True):
                        st.session_state.show_shipment_dialog = False
                        st.rerun()

        st.markdown("---")

        # 中段：グラフと入出庫履歴（2カラム）
        mid_col1, mid_col2 = st.columns([3, 2])

        with mid_col1:
            st.subheader("📈 在庫数推移")

            if product_transactions:
                # トランザクションデータをDataFrameに変換
                trans_df = pd.DataFrame(product_transactions)
                trans_df['datetime'] = pd.to_datetime(trans_df['datetime'])
                trans_df = trans_df.sort_values('datetime')

                # 在庫数の推移を計算
                current_stock = product_info['stock']
                stock_history = []

                for idx in range(len(trans_df) - 1, -1, -1):
                    row = trans_df.iloc[idx]
                    stock_history.insert(0, {
                        'datetime': row['datetime'],
                        'stock': current_stock,
                        'type': row['type'],
                        'quantity': row['quantity']
                    })
                    if row['type'] == '入庫':
                        current_stock -= row['quantity']
                    else:
                        current_stock += row['quantity']

                if stock_history:
                    stock_history.insert(0, {
                        'datetime': stock_history[0]['datetime'],
                        'stock': current_stock,
                        'type': '開始',
                        'quantity': 0
                    })

                stock_df = pd.DataFrame(stock_history)

                # 折れ線グラフ（コンパクト版）
                line_chart = alt.Chart(stock_df).mark_line(
                    point=True,
                    color='#3498db'
                ).encode(
                    x=alt.X('datetime:T', title='日時'),
                    y=alt.Y(
                        'stock:Q',
                        title='在庫数',
                        scale=alt.Scale(domain=[0, stock_df['stock'].max() * 1.1])
                    ),
                    tooltip=['datetime:T', 'stock:Q', 'type:N', 'quantity:Q']
                ).properties(
                    height=250
                )

                st.altair_chart(line_chart, use_container_width=True)
            else:
                st.info("まだ入出庫の履歴がありません")

        with mid_col2:
            st.subheader("📜 入出庫履歴")

            if product_transactions:
                trans_df = pd.DataFrame(product_transactions[:8])
                st.dataframe(
                    trans_df[['datetime', 'type', 'quantity', 'note']],
                    use_container_width=True,
                    hide_index=True,
                    height=250
                )
            else:
                st.info("まだ入出庫の履歴がありません")

        st.markdown("---")

        # 下段：関連注文
        st.subheader("📋 関連注文")

        if product_orders:
            orders_df = pd.DataFrame(product_orders)
            st.dataframe(
                orders_df[['customer', 'quantity', 'delivery_date', 'status']],
                use_container_width=True,
                hide_index=True,
                height=200
            )
        else:
            st.info("この製品の注文はありません")

# 出荷担当画面
elif view_mode == "出荷担当":
    # メトリクス表示
    col1, col2, col3 = st.columns(3)

    pending_orders = [o for o in st.session_state.orders if o["status"] == "未出荷"]
    today = datetime.now().date()
    today_shipments = sum([t["quantity"] for t in st.session_state.transactions
                           if t["type"] == "出庫" and datetime.strptime(t["datetime"], "%Y-%m-%d %H:%M").date() == today])
    total_pending_qty = sum([o["quantity"] for o in pending_orders])

    with col1:
        st.metric("未出荷注文", f"{len(pending_orders)}件")
    with col2:
        st.metric("未出荷数量", f"{total_pending_qty}個")
    with col3:
        st.metric("本日出庫数", f"{today_shipments}個")

    st.markdown("---")

    # 生産スケジュール（ガントチャート）
    st.subheader("📅 生産スケジュール(1ヶ月間)")
    gantt_fig = create_production_gantt_chart()

    if gantt_fig is not None:
        st.plotly_chart(gantt_fig, use_container_width=True)
    else:
        st.info("現在の日付から1ヶ月間の生産スケジュールはありません")

    st.markdown("---")

    # 未出荷注文リスト（優先表示）
    st.subheader("📦 未出荷注文リスト")

    if pending_orders:
        # 納期順にソート
        pending_orders_sorted = sorted(pending_orders, key=lambda x: x["delivery_date"])
        orders_df = pd.DataFrame(pending_orders_sorted)

        st.dataframe(
            orders_df,
            use_container_width=True,
            hide_index=True,
            height=300
        )
    else:
        st.info("未出荷の注文はありません")

    st.markdown("---")

    # 2カラム：在庫状況と出庫履歴
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 製品在庫状況")
        products_df = pd.DataFrame(st.session_state.products)

        # 在庫が少ない順にソート
        products_df_sorted = products_df.sort_values('stock')

        st.dataframe(
            products_df_sorted,
            use_container_width=True,
            hide_index=True,
            height=300
        )

    with col2:
        st.subheader("📤 本日の出庫履歴")

        today_shipments_list = [t for t in st.session_state.transactions
                                if t["type"] == "出庫" and datetime.strptime(t["datetime"], "%Y-%m-%d %H:%M").date() == today]

        if today_shipments_list:
            shipments_df = pd.DataFrame(today_shipments_list)
            st.dataframe(
                shipments_df[['datetime', 'product', 'quantity', 'note']],
                use_container_width=True,
                hide_index=True,
                height=300
            )
        else:
            st.info("本日の出庫履歴はまだありません")

# 製造担当画面
elif view_mode == "製造担当":
    # メトリクス表示
    col1, col2, col3 = st.columns(3)

    total_stock = sum([p["stock"] for p in st.session_state.products])
    today = datetime.now().date()
    today_receipts = sum([t["quantity"] for t in st.session_state.transactions
                          if t["type"] == "入庫" and datetime.strptime(t["datetime"], "%Y-%m-%d %H:%M").date() == today])
    week_receipts = sum([t["quantity"] for t in st.session_state.transactions
                         if t["type"] == "入庫" and
                         (datetime.now() - datetime.strptime(t["datetime"], "%Y-%m-%d %H:%M")).days <= 7])

    with col1:
        st.metric("総在庫数", f"{total_stock}個")
    with col2:
        st.metric("本日入庫数", f"{today_receipts}個")
    with col3:
        st.metric("今週入庫数", f"{week_receipts}個")

    st.markdown("---")

    # 生産・メンテナンススケジュール（ガントチャート）
    st.subheader("📅 生産・メンテナンススケジュール(1ヶ月間)")
    manufacturing_gantt_fig = create_sales_gantt_chart()

    if manufacturing_gantt_fig is not None:
        st.plotly_chart(manufacturing_gantt_fig, use_container_width=True)
    else:
        st.info("現在の日付から1ヶ月間のスケジュールはありません")

    st.markdown("---")

    # メンテナンススケジュール入力ボタンとフォーム
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("🔧 メンテナンススケジュール管理")
    with col2:
        toggle_label = (
            "➕ メンテナンス入力"
            if not st.session_state.get('show_maintenance_form', False)
            else "✖️ 閉じる"
        )
        if st.button(toggle_label, key="toggle_maintenance_form"):
            current_state = st.session_state.get('show_maintenance_form', False)
            st.session_state.show_maintenance_form = not current_state
            st.rerun()

    # フォーム表示（トグルがTrueの場合のみ）
    if st.session_state.get('show_maintenance_form', False):
        with st.form("maintenance_schedule_form"):
            st.write("**新規メンテナンススケジュール登録**")

            # 加工機選択
            machine_options = [
                f"{m.instance_name} ({m.machine_type.name})"
                for m in MACHINE_INSTANCES
            ]
            selected_machine_idx = st.selectbox(
                "加工機を選択",
                range(len(MACHINE_INSTANCES)),
                format_func=lambda i: machine_options[i],
                key="maint_machine"
            )

            # 日時入力（2カラム）
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("開始日", key="maint_start_date")
                default_start_time = datetime.strptime("09:00", "%H:%M").time()
                start_time = st.time_input(
                    "開始時刻", value=default_start_time, key="maint_start_time"
                )
            with col2:
                end_date = st.date_input("終了日", key="maint_end_date")
                default_end_time = datetime.strptime("17:00", "%H:%M").time()
                end_time = st.time_input(
                    "終了時刻", value=default_end_time, key="maint_end_time"
                )

            # メンテナンス種別
            maintenance_types = [
                "大規模定期メンテナンス",
                "小規模点検",
                "緊急メンテナンス",
                "その他"
            ]
            selected_type = st.selectbox(
                "メンテナンス種別", maintenance_types, key="maint_type"
            )

            # カスタム種別入力（「その他」選択時）
            custom_type = ""
            if selected_type == "その他":
                custom_type = st.text_input(
                    "メンテナンス種別を入力", key="maint_custom_type"
                )

            # 送信ボタン
            submitted = st.form_submit_button("登録")

            if submitted:
                # バリデーション
                if start_date > end_date or (
                    start_date == end_date and start_time >= end_time
                ):
                    st.error("❌ 終了日時は開始日時より後に設定してください")
                elif selected_type == "その他" and not custom_type:
                    st.error("❌ メンテナンス種別を入力してください")
                else:
                    # ISO 8601形式に変換
                    start_datetime = datetime.combine(
                        start_date, start_time
                    ).isoformat()
                    end_datetime = datetime.combine(
                        end_date, end_time
                    ).isoformat()

                    # MaintenanceScheduleオブジェクト作成
                    final_type = (
                        custom_type if selected_type == "その他" else selected_type
                    )
                    new_schedule = MaintenanceSchedule(
                        machine_instance=MACHINE_INSTANCES[selected_machine_idx],
                        start_time=start_datetime,
                        end_time=end_datetime,
                        maintenance_type=final_type
                    )

                    # セッション状態に追加
                    if 'maintenance_schedules' not in st.session_state:
                        st.session_state.maintenance_schedules = []
                    st.session_state.maintenance_schedules.append(new_schedule)

                    # フォームを閉じる
                    st.session_state.show_maintenance_form = False

                    machine_name = MACHINE_INSTANCES[selected_machine_idx]
                    success_msg = (
                        f"✅ {machine_name.instance_name} の"
                        f"メンテナンススケジュールを登録しました"
                    )
                    st.success(success_msg)
                    st.rerun()

    # 登録済みメンテナンススケジュール一覧
    if st.session_state.get('maintenance_schedules'):
        st.write("**登録済みメンテナンススケジュール**")

        for idx, schedule in enumerate(st.session_state.maintenance_schedules):
            col1, col2 = st.columns([5, 1])
            with col1:
                start_str = datetime.fromisoformat(
                    schedule.start_time
                ).strftime('%Y/%m/%d %H:%M')
                end_str = datetime.fromisoformat(
                    schedule.end_time
                ).strftime('%Y/%m/%d %H:%M')
                display_text = (
                    f"🔧 {schedule.machine_instance.instance_name}: "
                    f"{schedule.maintenance_type} "
                    f"({start_str} - {end_str})"
                )
                st.text(display_text)
            with col2:
                if st.button("削除", key=f"delete_maint_{idx}"):
                    st.session_state.maintenance_schedules.pop(idx)
                    st.rerun()

    st.markdown("---")

    # 製品別在庫状況（棒グラフ）
    st.subheader("📊 製品別在庫状況")

    products_df = pd.DataFrame(st.session_state.products)

    chart = alt.Chart(products_df).mark_bar().encode(
        x=alt.X('name:N', title='製品名', sort=None),
        y=alt.Y('stock:Q', title='在庫数'),
        color=alt.Color('name:N', legend=None, scale=alt.Scale(scheme='category10')),
        tooltip=['name', 'stock', 'unit']
    ).properties(
        height=300
    )

    st.altair_chart(chart, use_container_width=True)

    st.markdown("---")

    # 2カラム：入庫フォームと履歴
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("➕ 入庫登録")
        with st.form("manufacturing_receipt_form"):
            receipt_product = st.selectbox(
                "製品を選択",
                [p["name"] for p in st.session_state.products],
                key="mfg_receipt_product"
            )
            receipt_quantity = st.number_input(
                "入庫数",
                min_value=1,
                value=10,
                step=1,
                key="mfg_receipt_quantity"
            )
            receipt_note = st.text_input(
                "備考（任意）",
                key="mfg_receipt_note",
                value="製造完了分"
            )
            receipt_submit = st.form_submit_button("入庫を登録")

            if receipt_submit:
                # 在庫更新
                for product in st.session_state.products:
                    if product["name"] == receipt_product:
                        product["stock"] += receipt_quantity

                # 履歴追加
                st.session_state.transactions.insert(0, {
                    "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "type": "入庫",
                    "product": receipt_product,
                    "quantity": receipt_quantity,
                    "note": receipt_note if receipt_note else "-"
                })

                st.success(f"✅ {receipt_product}を{receipt_quantity}個入庫しました")
                st.rerun()

    with col2:
        st.subheader("📥 最近の入庫履歴")

        recent_receipts = [t for t in st.session_state.transactions if t["type"] == "入庫"][:10]

        if recent_receipts:
            receipts_df = pd.DataFrame(recent_receipts)
            st.dataframe(
                receipts_df[['datetime', 'product', 'quantity', 'note']],
                use_container_width=True,
                hide_index=True,
                height=300
            )
        else:
            st.info("入庫履歴はまだありません")

# 営業担当画面
elif view_mode == "営業担当":
    # メトリクス表示
    col1, col2, col3 = st.columns(3)

    total_orders = len(st.session_state.orders)
    pending_orders = len([o for o in st.session_state.orders if o["status"] == "未出荷"])
    shipped_orders = len([o for o in st.session_state.orders if o["status"] == "出荷済み"])

    with col1:
        st.metric("総注文数", f"{total_orders}件")
    with col2:
        st.metric("未出荷", f"{pending_orders}件")
    with col3:
        st.metric("出荷済み", f"{shipped_orders}件")

    st.markdown("---")

    # 生産・メンテナンススケジュール（ガントチャート）
    st.subheader("📅 生産・メンテナンススケジュール(1ヶ月間)")
    sales_gantt_fig = create_sales_gantt_chart()

    if sales_gantt_fig is not None:
        st.plotly_chart(sales_gantt_fig, use_container_width=True)
    else:
        st.info("現在の日付から1ヶ月間のスケジュールはありません")

    st.markdown("---")

    # 注文一覧
    st.subheader("📋 注文一覧")

    # ステータス別にタブ表示
    tab1, tab2, tab3 = st.tabs(["すべて", "未出荷", "出荷済み"])

    with tab1:
        orders_df = pd.DataFrame(st.session_state.orders)
        st.dataframe(
            orders_df,
            use_container_width=True,
            hide_index=True,
            height=300
        )

    with tab2:
        pending = [o for o in st.session_state.orders if o["status"] == "未出荷"]
        if pending:
            pending_df = pd.DataFrame(pending)
            st.dataframe(
                pending_df,
                use_container_width=True,
                hide_index=True,
                height=300
            )
        else:
            st.info("未出荷の注文はありません")

    with tab3:
        shipped = [o for o in st.session_state.orders if o["status"] == "出荷済み"]
        if shipped:
            shipped_df = pd.DataFrame(shipped)
            st.dataframe(
                shipped_df,
                use_container_width=True,
                hide_index=True,
                height=300
            )
        else:
            st.info("出荷済みの注文はありません")

    st.markdown("---")

    # 2カラム：製品別在庫と納期カレンダー
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📦 製品別在庫状況")

        products_df = pd.DataFrame(st.session_state.products)

        # 各製品の未出荷注文数を計算
        for idx, product in enumerate(st.session_state.products):
            pending_qty = sum([o["quantity"] for o in st.session_state.orders
                             if o["product"] == product["name"] and o["status"] == "未出荷"])
            products_df.loc[idx, "pending"] = pending_qty

        st.dataframe(
            products_df[['name', 'stock', 'pending', 'unit']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "name": "製品名",
                "stock": "在庫数",
                "pending": "未出荷数",
                "unit": "単位"
            },
            height=300
        )

    with col2:
        st.subheader("📅 納期予定")

        # 未出荷注文を納期順にソート
        pending_orders_list = [o for o in st.session_state.orders if o["status"] == "未出荷"]
        pending_orders_sorted = sorted(pending_orders_list, key=lambda x: x["delivery_date"])

        if pending_orders_sorted:
            delivery_df = pd.DataFrame(pending_orders_sorted)
            st.dataframe(
                delivery_df[['delivery_date', 'customer', 'product', 'quantity']],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "delivery_date": "納期",
                    "customer": "顧客",
                    "product": "製品",
                    "quantity": "数量"
                },
                height=300
            )
        else:
            st.info("納期予定はありません")

# フッター
st.markdown("---")
st.caption("🏭 工場在庫管理ダッシュボード - プロトタイプ版")

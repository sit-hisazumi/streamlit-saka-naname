import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import altair as alt

# ページ設定
st.set_page_config(
    page_title="工場在庫管理ダッシュボード",
    page_icon="🏭",
    layout="wide"
)

# 初期ダミーデータの作成
def initialize_dummy_data():
    """初期データとダミーデータを作成"""

    # 製品マスタ
    if 'products' not in st.session_state:
        st.session_state.products = [
            {"name": "製品A", "stock": 220, "unit": "個"},
            {"name": "製品B", "stock": 185, "unit": "個"},
            {"name": "製品C", "stock": 300, "unit": "個"},
            {"name": "製品D", "stock": 145, "unit": "個"},
            {"name": "製品E", "stock": 250, "unit": "個"},
        ]

    # 注文リスト（ダミーデータ）
    if 'orders' not in st.session_state:
        st.session_state.orders = [
            {
                "customer": "株式会社サンプル商事",
                "product": "製品A",
                "quantity": 30,
                "delivery_date": "2025-12-20",
                "status": "未出荷"
            },
            {
                "customer": "テスト工業株式会社",
                "product": "製品B",
                "quantity": 50,
                "delivery_date": "2025-12-22",
                "status": "未出荷"
            },
            {
                "customer": "ダミー株式会社",
                "product": "製品C",
                "quantity": 100,
                "delivery_date": "2025-12-25",
                "status": "未出荷"
            },
            {
                "customer": "サンプル物産",
                "product": "製品A",
                "quantity": 20,
                "delivery_date": "2025-12-19",
                "status": "出荷済"
            },
            {
                "customer": "テストトレーディング",
                "product": "製品E",
                "quantity": 75,
                "delivery_date": "2025-12-28",
                "status": "未出荷"
            },
        ]

    # 入出庫履歴（ダミーデータ）
    if 'transactions' not in st.session_state:
        base_date = datetime.now()
        st.session_state.transactions = [
            # 約10週間前から現在までのデータ
            {
                "datetime": (base_date - timedelta(days=70, hours=10))
                .strftime("%Y-%m-%d %H:%M"),
                "type": "入庫",
                "product": "製品A",
                "quantity": 150,
                "note": "製造完了分"
            },
            {
                "datetime": (base_date - timedelta(days=65, hours=14))
                .strftime("%Y-%m-%d %H:%M"),
                "type": "出庫",
                "product": "製品A",
                "quantity": 80,
                "note": "サンプル商事向け出荷"
            },
            {
                "datetime": (base_date - timedelta(days=56, hours=9))
                .strftime("%Y-%m-%d %H:%M"),
                "type": "入庫",
                "product": "製品C",
                "quantity": 200,
                "note": "製造完了分"
            },
            {
                "datetime": (base_date - timedelta(days=49, hours=15))
                .strftime("%Y-%m-%d %H:%M"),
                "type": "出庫",
                "product": "製品C",
                "quantity": 100,
                "note": "テスト工業向け出荷"
            },
            {
                "datetime": (base_date - timedelta(days=42, hours=11))
                .strftime("%Y-%m-%d %H:%M"),
                "type": "入庫",
                "product": "製品B",
                "quantity": 120,
                "note": "製造完了分"
            },
            {
                "datetime": (base_date - timedelta(days=35, hours=13))
                .strftime("%Y-%m-%d %H:%M"),
                "type": "出庫",
                "product": "製品B",
                "quantity": 60,
                "note": "ダミー株式会社向け出荷"
            },
            {
                "datetime": (base_date - timedelta(days=28, hours=10))
                .strftime("%Y-%m-%d %H:%M"),
                "type": "入庫",
                "product": "製品E",
                "quantity": 180,
                "note": "製造完了分"
            },
            {
                "datetime": (base_date - timedelta(days=21, hours=16))
                .strftime("%Y-%m-%d %H:%M"),
                "type": "出庫",
                "product": "製品E",
                "quantity": 90,
                "note": "サンプル物産向け出荷"
            },
            {
                "datetime": (base_date - timedelta(days=14, hours=9))
                .strftime("%Y-%m-%d %H:%M"),
                "type": "入庫",
                "product": "製品D",
                "quantity": 100,
                "note": "製造完了分"
            },
            {
                "datetime": (base_date - timedelta(days=7, hours=14))
                .strftime("%Y-%m-%d %H:%M"),
                "type": "出庫",
                "product": "製品D",
                "quantity": 45,
                "note": "テストトレーディング向け出荷"
            },
            {
                "datetime": (base_date - timedelta(days=5, hours=10))
                .strftime("%Y-%m-%d %H:%M"),
                "type": "入庫",
                "product": "製品A",
                "quantity": 100,
                "note": "製造完了分"
            },
            {
                "datetime": (base_date - timedelta(days=4, hours=14))
                .strftime("%Y-%m-%d %H:%M"),
                "type": "出庫",
                "product": "製品A",
                "quantity": 50,
                "note": "サンプル商事向け出荷"
            },
            {
                "datetime": (base_date - timedelta(days=3, hours=9))
                .strftime("%Y-%m-%d %H:%M"),
                "type": "入庫",
                "product": "製品B",
                "quantity": 80,
                "note": "製造完了分"
            },
            {
                "datetime": (base_date - timedelta(days=2, hours=16))
                .strftime("%Y-%m-%d %H:%M"),
                "type": "出庫",
                "product": "製品B",
                "quantity": 30,
                "note": "テスト工業向け出荷"
            },
            {
                "datetime": (base_date - timedelta(days=1, hours=11))
                .strftime("%Y-%m-%d %H:%M"),
                "type": "入庫",
                "product": "製品E",
                "quantity": 120,
                "note": "製造完了分"
            },
            {
                "datetime": (base_date - timedelta(hours=5))
                .strftime("%Y-%m-%d %H:%M"),
                "type": "出庫",
                "product": "製品C",
                "quantity": 50,
                "note": "ダミー株式会社向け出荷"
            },
            {
                "datetime": (base_date - timedelta(hours=2))
                .strftime("%Y-%m-%d %H:%M"),
                "type": "入庫",
                "product": "製品A",
                "quantity": 70,
                "note": "製造完了分"
            },
        ]

# データ初期化
initialize_dummy_data()

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

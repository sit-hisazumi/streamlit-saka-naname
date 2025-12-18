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
            {"name": "製品A", "stock": 120, "unit": "個"},
            {"name": "製品B", "stock": 85, "unit": "個"},
            {"name": "製品C", "stock": 200, "unit": "個"},
            {"name": "製品D", "stock": 45, "unit": "個"},
            {"name": "製品E", "stock": 150, "unit": "個"},
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
            {
                "datetime": (base_date - timedelta(days=5, hours=10)).strftime("%Y-%m-%d %H:%M"),
                "type": "入庫",
                "product": "製品A",
                "quantity": 100,
                "note": "製造完了分"
            },
            {
                "datetime": (base_date - timedelta(days=5, hours=8)).strftime("%Y-%m-%d %H:%M"),
                "type": "入庫",
                "product": "製品C",
                "quantity": 150,
                "note": "製造完了分"
            },
            {
                "datetime": (base_date - timedelta(days=4, hours=14)).strftime("%Y-%m-%d %H:%M"),
                "type": "出庫",
                "product": "製品A",
                "quantity": 50,
                "note": "サンプル商事向け出荷"
            },
            {
                "datetime": (base_date - timedelta(days=3, hours=9)).strftime("%Y-%m-%d %H:%M"),
                "type": "入庫",
                "product": "製品B",
                "quantity": 80,
                "note": "製造完了分"
            },
            {
                "datetime": (base_date - timedelta(days=2, hours=16)).strftime("%Y-%m-%d %H:%M"),
                "type": "出庫",
                "product": "製品B",
                "quantity": 30,
                "note": "テスト工業向け出荷"
            },
            {
                "datetime": (base_date - timedelta(days=1, hours=11)).strftime("%Y-%m-%d %H:%M"),
                "type": "入庫",
                "product": "製品E",
                "quantity": 120,
                "note": "製造完了分"
            },
            {
                "datetime": (base_date - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"),
                "type": "出庫",
                "product": "製品C",
                "quantity": 50,
                "note": "ダミー株式会社向け出荷"
            },
        ]

# データ初期化
initialize_dummy_data()

# サイドバー：表示モード選択
st.sidebar.title("📋 メニュー")
view_mode = st.sidebar.radio(
    "表示モード",
    ["ダッシュボード", "製品詳細"]
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
else:
    st.title(f"🔍 製品詳細: {selected_product}")
st.markdown("---")

# ダッシュボード表示
if view_mode == "ダッシュボード":
    # メトリクス表示
    col1, col2, col3, col4 = st.columns(4)

    total_stock = sum([p["stock"] for p in st.session_state.products])
    today = datetime.now().date()
    today_receipts = sum([t["quantity"] for t in st.session_state.transactions
                          if t["type"] == "入庫" and datetime.strptime(t["datetime"], "%Y-%m-%d %H:%M").date() == today])
    today_shipments = sum([t["quantity"] for t in st.session_state.transactions
                           if t["type"] == "出庫" and datetime.strptime(t["datetime"], "%Y-%m-%d %H:%M").date() == today])
    pending_orders = len([o for o in st.session_state.orders if o["status"] == "未出荷"])

    with col1:
        st.metric("総在庫数", f"{total_stock}個")
    with col2:
        st.metric("本日の入庫", f"{today_receipts}個")
    with col3:
        st.metric("本日の出庫", f"{today_shipments}個")
    with col4:
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
else:
    # 選択した製品の情報を取得
    product_info = next((p for p in st.session_state.products if p["name"] == selected_product), None)

    if product_info:
        # メトリクス表示
        col1, col2 = st.columns(2)

        # 製品関連のトランザクション
        product_transactions = [t for t in st.session_state.transactions if t["product"] == selected_product]

        # 製品関連の注文
        product_orders = [o for o in st.session_state.orders if o["product"] == selected_product]
        pending_quantity = sum([o["quantity"] for o in product_orders if o["status"] == "未出荷"])

        with col1:
            st.metric("現在庫数", f"{product_info['stock']}{product_info['unit']}")
        with col2:
            st.metric("未出荷注文数", f"{pending_quantity}{product_info['unit']}")

        st.markdown("---")

        # 在庫数推移グラフ
        st.subheader("📈 在庫数推移")

        if product_transactions:
            # トランザクションデータをDataFrameに変換
            trans_df = pd.DataFrame(product_transactions)
            trans_df['datetime'] = pd.to_datetime(trans_df['datetime'])
            trans_df = trans_df.sort_values('datetime')

            # 在庫数の推移を計算（最新から過去に遡って計算）
            # 現在の在庫数から逆算
            current_stock = product_info['stock']
            stock_history = []

            # 最新のトランザクションから逆順に処理
            for idx in range(len(trans_df) - 1, -1, -1):
                row = trans_df.iloc[idx]
                stock_history.insert(0, {
                    'datetime': row['datetime'],
                    'stock': current_stock,
                    'type': row['type'],
                    'quantity': row['quantity']
                })
                # 過去の在庫数を逆算
                if row['type'] == '入庫':
                    current_stock -= row['quantity']
                else:  # 出庫
                    current_stock += row['quantity']

            # 最も古い時点の在庫も追加
            if stock_history:
                stock_history.insert(0, {
                    'datetime': stock_history[0]['datetime'],
                    'stock': current_stock,
                    'type': '開始',
                    'quantity': 0
                })

            stock_df = pd.DataFrame(stock_history)

            # Altairで折れ線グラフ作成
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
                height=300
            )

            st.altair_chart(line_chart, use_container_width=True)
        else:
            st.info("まだ入出庫の履歴がありません")

        st.markdown("---")

        # 2カラムレイアウト
        col1, col2 = st.columns(2)

        with col1:
            # 注文情報
            st.subheader("📋 関連注文")

            if product_orders:
                orders_df = pd.DataFrame(product_orders)
                st.dataframe(
                    orders_df,
                    use_container_width=True,
                    hide_index=True
                )

                st.metric("未出荷注文数", f"{pending_quantity}{product_info['unit']}")
            else:
                st.info("この製品の注文はありません")

        with col2:
            # 入出庫履歴
            st.subheader("📜 入出庫履歴（最新10件）")

            if product_transactions:
                trans_df = pd.DataFrame(product_transactions[:10])
                st.dataframe(
                    trans_df[['datetime', 'type', 'quantity', 'note']],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("まだ入出庫の履歴がありません")

        st.markdown("---")

        # クイック操作
        st.subheader("⚡ クイック操作")
        col1, col2 = st.columns(2)

        with col1:
            with st.form("quick_receipt"):
                st.write("**入庫登録**")
                quick_receipt_qty = st.number_input(
                    "入庫数",
                    min_value=1,
                    value=10,
                    step=1,
                    key="quick_receipt_qty"
                )
                quick_receipt_note = st.text_input("備考", key="quick_receipt_note")

                if st.form_submit_button("入庫"):
                    product_info["stock"] += quick_receipt_qty
                    st.session_state.transactions.insert(0, {
                        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "type": "入庫",
                        "product": selected_product,
                        "quantity": quick_receipt_qty,
                        "note": quick_receipt_note if quick_receipt_note else "-"
                    })
                    st.success(f"✅ {quick_receipt_qty}{product_info['unit']}入庫しました")
                    st.rerun()

        with col2:
            with st.form("quick_shipment"):
                st.write("**出庫登録**")
                quick_shipment_qty = st.number_input(
                    f"出庫数（在庫: {product_info['stock']}{product_info['unit']}）",
                    min_value=1,
                    max_value=product_info['stock'] if product_info['stock'] > 0 else 1,
                    value=min(10, product_info['stock']) if product_info['stock'] > 0 else 1,
                    step=1,
                    key="quick_shipment_qty"
                )
                quick_shipment_note = st.text_input("備考", key="quick_shipment_note")

                if st.form_submit_button("出庫"):
                    if product_info['stock'] >= quick_shipment_qty:
                        product_info["stock"] -= quick_shipment_qty
                        st.session_state.transactions.insert(0, {
                            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "type": "出庫",
                            "product": selected_product,
                            "quantity": quick_shipment_qty,
                            "note": quick_shipment_note if quick_shipment_note else "-"
                        })
                        st.success(f"✅ {quick_shipment_qty}{product_info['unit']}出庫しました")
                        st.rerun()
                    else:
                        st.error(f"❌ 在庫不足です")

# フッター
st.markdown("---")
st.caption("🏭 工場在庫管理ダッシュボード - プロトタイプ版")

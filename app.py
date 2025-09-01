import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import requests

# -------------------------------
# تنظیمات صفحه و فونت سفارشی
st.set_page_config(page_title="Deribit Trade Analyzer", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
* {font-family: 'Vazirmatn', Arial, Tahoma, sans-serif !important;}
h1, h2, h3, h4, h5, h6 {font-family: 'Vazirmatn', Arial, Tahoma, sans-serif !important;}
.big-title {
    font-size:38px !important;
    color:#1C3879 !important;
    font-weight:800;
    margin-bottom: 5px;
}
.summary-box {
    background: linear-gradient(90deg, #F6F9FF 0%, #E3F0FF 100%);
    border: 1px solid #CDE0F7;
    border-radius: 16px;
    padding: 28px 22px;
    text-align: center;
    margin-bottom: 34px;
    box-shadow: 0 2px 8px #eef3fa;
}
.info-table-title {
    background-color: #256D85;
    color: #fff;
    padding: 8px;
    font-weight: bold;
    border-radius: 6px 6px 0 0;
    margin-top: 20px;
    margin-bottom: 0px;
    font-size: 18px;
}
.st-emotion-cache-1y4p8pa {
    background: #f5fbff !important;
}
.st-emotion-cache-1v0mbdj {
    background: #e3f0ff !important;
}
.st-emotion-cache-11n6jms {
    border-radius: 8px !important;
}
.st-emotion-cache-1jicfl9 {
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# بخش انتخاب نماد و بازه زمانی
assets = ["BTC", "ETH"]
st.markdown("<div class='big-title'>Optihon - Options Viewer</div>", unsafe_allow_html=True)
col_asset, col_start, col_end = st.columns(3)
with col_asset:
    asset = st.selectbox("Asset", assets)
with col_start:
    start_date = st.date_input("Start Date", datetime.date.today())
    start_time = st.time_input("Start Time", datetime.datetime.now().time())
with col_end:
    end_date = st.date_input("End Date", datetime.date.today())
    end_time = st.time_input("End Time", datetime.datetime.now().time())

# ورودی URL یا الگوی endpoint (بدون احراز هویت)
st.markdown("") 
st.markdown("### تنظیم URL آپشن API (بدون احراز هویت)")
st.markdown("مثال قالب‌ها: https://api.example.com/options?asset={asset}  یا  https://api.example.com/options/{asset}")
options_api_template = st.text_input("Options API URL template (use {asset} to inject asset)", "")

# تبدیل تاریخ و ساعت به دیتای مناسب
start_datetime = datetime.datetime.combine(start_date, start_time)
end_datetime = datetime.datetime.combine(end_date, end_time)

# -----------------------------------------------
# تابع کمکی برای ساخت URL نهایی از template
def build_url_from_template(template: str, asset: str) -> str:
    if not template:
        return ""
    if "{asset}" in template:
        return template.format(asset=asset)
    # اگر قالب شامل query است فرض می‌کنیم param اضافه می‌کنیم
    if "?" in template:
        return f"{template}&asset={asset}"
    # اگر انتها اسلش داشت یا نه
    if template.endswith("/"):
        return template + asset
    return template + "/" + asset

@st.cache_data(ttl=60)
def fetch_options(url_template: str, asset: str):
    url = build_url_from_template(url_template, asset)
    if not url:
        return pd.DataFrame()  # خالی یعنی از حالت نمونه استفاده شود
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # نگاشتِ ساختارهای رایج پاسخ به لیست آیتم‌ها
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            # چک کردن کلیدهای رایج
            items = data.get("result") or data.get("data") or data.get("options") or data.get("items") or []
        else:
            items = []
        mapped = []
        for it in items:
            # سعی می‌کنیم فیلدها را از نمونه‌های معمول استخراج کنیم
            symbol = it.get("instrument_name") or it.get("symbol") or it.get("id") or it.get("name")
            option_type = it.get("option_type") or it.get("type") or it.get("side")
            if option_type:
                option_type = option_type.lower()
                if option_type.startswith("c"):
                    option_type = "call"
                elif option_type.startswith("p"):
                    option_type = "put"
            strike = it.get("strike") or it.get("strike_price") or it.get("strikePrice")
            price = it.get("mark_price") or it.get("last_price") or it.get("price") or it.get("mid_price")
            expected_profit = it.get("expected_profit") or it.get("expectedReturn") or it.get("expected")
            risk_index = it.get("risk_index") or it.get("risk") or it.get("iv")
            probability = it.get("probability") or it.get("prob") or it.get("win_chance")
            profit_percent = it.get("profit_percent") or it.get("profitPercent")
            mapped.append({
                "symbol": symbol or "",
                "type": option_type or "",
                "price": price if price is not None else "",
                "strike": strike if strike is not None else "",
                "expected_profit": expected_profit if expected_profit is not None else "",
                "risk_index": risk_index if risk_index is not None else "",
                "probability": probability if probability is not None else "",
                "profit_percent": profit_percent if profit_percent is not None else ""
            })
        return pd.DataFrame(mapped)
    except Exception as e:
        # خطای شبکه یا پردازش
        st.error(f"Failed to fetch options from API: {e}")
        return pd.DataFrame()

# -----------------------------------------------
# دکمه اجرا و نمایش آپشن‌ها
if st.button("Load Options", use_container_width=True):
    df_options = fetch_options(options_api_template, asset)

    # اگر پاسخ API خالی بود از داده نمونه استفاده می‌کنیم تا UI پر باشد
    if df_options.empty:
        st.warning("No data returned from the provided API template — showing sample data.")
        options_data = [
            {
                "symbol": "BTC-29AUG25-12000-C",
                "type": "call",
                "price": 13222,
                "strike": 12000,
                "expected_profit": 5324,
                "risk_index": 0.219,
                "probability": "86%",
                "profit_percent": "27.18%"
            },
            {
                "symbol": "BTC-29AUG25-12500-C",
                "type": "call",
                "price": 13195,
                "strike": 12500,
                "expected_profit": 5316,
                "risk_index": 0.216,
                "probability": "81%",
                "profit_percent": "25.15%"
            },
            {
                "symbol": "BTC-29AUG25-12800-P",
                "type": "put",
                "price": 13007,
                "strike": 12800,
                "expected_profit": 5466,
                "risk_index": 0.388,
                "probability": "81%",
                "profit_percent": "32.39%"
            },
            {
                "symbol": "BTC-29AUG25-13000-P",
                "type": "put",
                "price": 13213,
                "strike": 13000,
                "expected_profit": 5748,
                "risk_index": 0.372,
                "probability": "80%",
                "profit_percent": "30.15%"
            },
        ]
        df_options = pd.DataFrame(options_data)

    # نمایش جدول آپشن‌ها با رنگ و تم زیبا
    st.subheader("Options Contracts (All)")
    st.dataframe(df_options.style.set_properties(**{
        'background-color': '#f5fbff',
        'color': '#1C3879',
        'border-color': '#CDE0F7',
    }), use_container_width=True)

    # بهترین قراردادهای اختیار خرید (call)
    st.markdown("<div class='info-table-title'>به صرفه ترین قراردادهای اختیار خرید (جهت خرید)</div>", unsafe_allow_html=True)
    top_calls = df_options[df_options["type"].str.lower() == "call"].sort_values("expected_profit", ascending=False).head(3)
    st.dataframe(top_calls.style.set_properties(**{
        'background-color': '#e3f0ff',
        'color': '#256D85',
        'border-color': '#CDE0F7',
        'font-weight': 'bold',
    }), use_container_width=True)

    # بهترین قراردادهای اختیار فروش (put)
    st.markdown("<div class='info-table-title'>به صرفه ترین قراردادهای اختیار فروش (جهت فروش)</div>", unsafe_allow_html=True)
    top_puts = df_options[df_options["type"].str.lower() == "put"].sort_values("expected_profit", ascending=False).head(3)
    st.dataframe(top_puts.style.set_properties(**{
        'background-color': '#e3f0ff',
        'color': '#e85a0c',
        'border-color': '#CDE0F7',
        'font-weight': 'bold',
    }), use_container_width=True)

    # نمایش توضیح پایین جدول
    st.info("این بخش صرفاً جهت نمایش برترین آپشن‌هاست و تضمین سوددهی ندارد. تحلیل‌ها بر اساس داده‌های API شما محاسبه می‌شوند.")
else:
    st.warning("برای مشاهده قراردادها، ابتدا URL آپشن API را وارد کرده و سپس دکمه Load Options را بزنید.")

# -------------------------------
# راهنمای جایگزینی API:
st.markdown("""
---
#### <span style='color:#256D85'>راهنمای تنظیم URL:</span>
- اگر API شما قالبی مثل `https://api.example.com/options?asset=BTC` دارد، مقدار `https://api.example.com/options?asset={asset}` را وارد کنید.
- اگر قالبی مثل `https://api.example.com/options/BTC` دارد، مقدار `https://api.example.com/options/{asset}` را وارد کنید.
- اگر endpoint شما پارامترهای متفاوتی نیاز دارد، می‌توانید URL کامل را وارد کنید و پنجره لاگ خطا را برای دیدن ساختار پاسخ بررسی کنید.
""", unsafe_allow_html=True)
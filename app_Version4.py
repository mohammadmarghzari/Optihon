import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

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
st.markdown("<div class='big-title'>Deribit Trade Analyzer</div>", unsafe_allow_html=True)
col_asset, col_start, col_end = st.columns(3)
with col_asset:
    asset = st.selectbox("Asset", assets)
with col_start:
    start_date = st.date_input("Start Date", datetime.date.today())
    start_time = st.time_input("Start Time", datetime.datetime.now().time())
with col_end:
    end_date = st.date_input("End Date", datetime.date.today())
    end_time = st.time_input("End Time", datetime.datetime.now().time())

# تبدیل تاریخ و ساعت به دیتای مناسب
start_datetime = datetime.datetime.combine(start_date, start_time)
end_datetime = datetime.datetime.combine(end_date, end_time)

st.markdown("")

# -------------------------------
# دکمه اجرا و تحلیل داده‌ها
if st.button("Analyze Trades", use_container_width=True):
    # -----------------------------------------------
    # این بخش را با APIهای خودت جایگزین کن!
    # داده‌های نمونه برای نمایش فرمت و ساختار
    # -----------------------------------------------

    # اطلاعات معاملات
    total_positions = 9004
    buy_positions = 4239
    sell_positions = 4765
    trades_chart_data = pd.DataFrame({
        'timestamp': pd.date_range(start=start_datetime, end=end_datetime, periods=10),
        'total': [i*1000 for i in range(10)],
        'buy': [i*500 for i in range(10)],
        'sell': [i*500 for i in range(10,0,-1)],
    })

    # اطلاعات قراردادهای آپشن (جدول کامل)
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

    # -----------------------------------------------
    # نمایش خلاصه اطلاعات معاملات بصورت باکس رنگی و بزرگ
    st.markdown(
        f"""
        <div class='summary-box'>
            <span style='font-size:26px;color:#256D85;font-weight:700;'>{asset}</span><br>
            <span style='font-size:18px;'><b>Total Positions:</b> <span style='color:#1C3879'>{total_positions}</span>
            &nbsp; | &nbsp;
            <b>Buy Positions:</b> <span style='color:#35a79c'>{buy_positions}</span>
            &nbsp; | &nbsp;
            <b>Sell Positions:</b> <span style='color:#e85a0c'>{sell_positions}</span></span><br>
            <span style='font-size:16px;'><b>Date Range:</b> {start_datetime.strftime('%Y/%m/%d %H:%M:%S')} to {end_datetime.strftime('%Y/%m/%d %H:%M:%S')}</span>
        </div>
        """, unsafe_allow_html=True
    )
    st.markdown("")

    # نمایش نمودار معاملات با Plotly واکنش‌گرا
    st.subheader("Positions Over Time")
    fig = px.line(trades_chart_data, x='timestamp', y=['total', 'buy', 'sell'],
                  labels={'value':'Positions', 'variable':'Type', 'timestamp':'Time'},
                  color_discrete_map={'total':'#1C3879', 'buy':'#35a79c', 'sell':'#e85a0c'})
    fig.update_layout(template='plotly_white', legend_title_text='Position Type')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # نمایش جدول آپشن‌ها با رنگ و تم زیبا
    st.subheader("Options Contracts (All)")
    st.dataframe(df_options.style.set_properties(**{
        'background-color': '#f5fbff',
        'color': '#1C3879',
        'border-color': '#CDE0F7',
    }), use_container_width=True)

    # بهترین قراردادهای اختیار خرید (call)
    st.markdown("<div class='info-table-title'>به صرفه ترین قراردادهای اختیار خرید (جهت خرید)</div>", unsafe_allow_html=True)
    top_calls = df_options[df_options["type"] == "call"].sort_values("expected_profit", ascending=False).head(3)
    st.dataframe(top_calls.style.set_properties(**{
        'background-color': '#e3f0ff',
        'color': '#256D85',
        'border-color': '#CDE0F7',
        'font-weight': 'bold',
    }), use_container_width=True)

    # بهترین قراردادهای اختیار فروش (put)
    st.markdown("<div class='info-table-title'>به صرفه ترین قراردادهای اختیار فروش (جهت فروش)</div>", unsafe_allow_html=True)
    top_puts = df_options[df_options["type"] == "put"].sort_values("expected_profit", ascending=False).head(3)
    st.dataframe(top_puts.style.set_properties(**{
        'background-color': '#e3f0ff',
        'color': '#e85a0c',
        'border-color': '#CDE0F7',
        'font-weight': 'bold',
    }), use_container_width=True)

    # نمایش توضیح پایین جدول
    st.info("این بخش صرفاً جهت نمایش برترین آپشن‌هاست و تضمین سوددهی ندارد. تحلیل‌ها بر اساس داده‌های API شما محاسبه می‌شوند.")

else:
    st.warning("برای شروع تحلیل، ابتدا پارامترهای بالا را انتخاب و سپس دکمه Analyze Trades را بزنید.")

# -------------------------------
# راهنمای جایگزینی API:
st.markdown("""
---
#### <span style='color:#256D85'>راهنمای جایگزینی API:</span>
در ابتدای هر بخش داده (معاملات و آپشن)، فقط کافیست به جای داده‌های نمونه، خروجی API خودتان را با همان فرمت و فیلدها جایگزین کنید.
""", unsafe_allow_html=True)
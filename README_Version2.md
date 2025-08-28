# Deribit Trade Analyzer

ابزار تحلیل معاملات و آپشن بیت‌کوین و اتریوم با Streamlit

## نصب و اجرا
ابتدا پکیج‌ها را نصب کنید:
```bash
pip install -r requirements.txt
```

سپس ابزار را اجرا کنید:
```bash
streamlit run app.py
```

## نحوه اتصال به API خودتان
در فایل app.py، داده‌های نمونه معاملات و آپشن را با کد فراخوانی API خودتان جایگزین کنید.  
مثلاً:
```python
# داده نمونه
total_positions = 9004
# جایگزین با:
# total_positions = get_total_positions_from_api(asset, start_datetime, end_datetime)
```
تمام فیلدها را مطابق با خروجی API خودتان تغییر دهید.

## توضیحات بیشتر
- بدون نیاز به احراز هویت
- ظاهر مدرن و واکنش‌گرا
- قابل اجرا روی هر سیستم با Python و Streamlit

اگر سوالی داشتی یا خواستی سفارشی‌سازی کنی، کافیست Issue باز کنی یا پیام بدهی.
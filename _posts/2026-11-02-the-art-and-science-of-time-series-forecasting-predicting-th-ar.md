---
layout: post
title: "فن وعلم التنبؤ بالسلاسل الزمنية: التنبؤ بالمستقبل باستخدام البيانات"
date: 2026-11-02 12:00:00 +0000
categories: [Data Science]
tags:
  - AI
  - Tech
  - Data
lang: ar
excerpt: "التنبؤ بالسلاسل الزمنية هو تقنية حاسمة للتنبؤ بالقيم المستقبلية بناءً على بيانات تاريخية مرتبة زمنيًا. من التنبؤ بأسعار الأسهم إلى أنماط الطقس، يعد فهم مبادئها ونماذجها أمرًا حيويًا لاتخاذ القرارات المستندة إلى البيانات عبر الصناعات. يتعمق هذا المنشور في مفاهيمها الأساسية وتقنياتها الشائعة ومثال عملي باستخدام بايثون."
---

## فن وعلم التنبؤ بالسلاسل الزمنية: التنبؤ بالمستقبل باستخدام البيانات

في عالمنا القائم على البيانات، تعد القدرة على توقع الأحداث المستقبلية قوة خارقة. سواء كان الأمر يتعلق بالتنبؤ بتحركات سوق الأسهم، أو تحسين سلاسل التوريد، أو توقع الطلب على الطاقة، فإن فهم ما قد يحدث بعد ذلك يمكن أن يوفر ميزة تنافسية كبيرة ويمكّن من اتخاذ قرارات أكثر ذكاءً. وهنا يأتي دور **التنبؤ بالسلاسل الزمنية**.

### ما هي السلسلة الزمنية؟

في جوهرها، السلسلة الزمنية هي سلسلة من نقاط البيانات المفهرسة (أو المدرجة) بترتيب زمني. وعادة ما تكون السلسلة الزمنية عبارة عن تسلسل يتم التقاطه عند نقاط متتالية ومتباعدة بالتساوي في الوقت. تشمل الأمثلة أسعار الأسهم اليومية، وقراءات درجة الحرارة بالساعة، وأرقام المبيعات الشهرية، أو نمو الناتج المحلي الإجمالي السنوي.

تشمل الخصائص الرئيسية لبيانات السلاسل الزمنية غالبًا ما يلي:
*   **الاتجاه (Trend):** زيادة أو نقصان طويل الأمد في البيانات.
*   **الموسمية (Seasonality):** أنماط منتظمة يمكن التنبؤ بها تتكرر خلال فترة زمنية محددة (على سبيل المثال، الدورات اليومية، الأسبوعية، الشهرية، السنوية).
*   **الدورية (Cyclical):** تقلبات ليست ذات فترة ثابتة، وغالبًا ما ترتبط بالدورات الاقتصادية أو ظواهر أخرى طويلة الأمد.
*   **غير المنتظمة (أو المتبقية) (Irregular/Residual):** اختلافات عشوائية أو ضوضاء في البيانات لا يمكن تفسيرها بالاتجاه أو الموسمية أو المكونات الدورية.

### لماذا التنبؤ؟

الهدف الأساسي للتنبؤ بالسلاسل الزمنية هو بناء نماذج يمكنها التنبؤ بدقة بالقيم المستقبلية بناءً على الأنماط الملاحظة في البيانات التاريخية. هذه القدرة لا تقدر بثمن عبر العديد من المجالات:
*   **التخطيط الاستراتيجي:** تتوقع الشركات المبيعات لتخطيط المخزون والإنتاج واستراتيجيات التسويق.
*   **تحسين الموارد:** تتوقع شركات الطاقة الطلب لإدارة توليد الطاقة وتوزيعها بكفاءة.
*   **التحليل المالي:** يستخدم المستثمرون التوقعات لاتخاذ قرارات مستنيرة بشأن شراء وبيع الأصول.
*   **السياسة العامة:** تتوقع الحكومات النمو السكاني والمؤشرات الاقتصادية وتفشي الأمراض لتخصيص الموارد ووضع السياسات.
*   **الطقس والمناخ:** يتنبأ خبراء الأرصاد الجوية بأنماط الطقس لإصدار التحذيرات وإبلاغ الأنشطة اليومية.

### المفاهيم الأساسية في السلاسل الزمنية

بالإضافة إلى الاتجاه والموسمية، هناك مفهوم حاسم آخر وهو **الثبات (Stationarity)**. تعتبر السلسلة الزمنية ثابتة إذا لم تتغير خصائصها الإحصائية (المتوسط، التباين، والارتباط الذاتي) بمرور الوقت. تفترض العديد من نماذج التنبؤ الإحصائية الثبات. غالبًا ما تتطلب السلاسل غير الثابتة *التفاضل (differencing)* (حساب الفرق بين الملاحظات المتتالية) لتصبح ثابتة قبل النمذجة.

### نماذج وتقنيات التنبؤ

يستخدم التنبؤ بالسلاسل الزمنية مجموعة متنوعة من النماذج، تتراوح من الأساليب الإحصائية التقليدية إلى تقنيات التعلم الآلي والتعلم العميق المتقدمة.

#### 1. النماذج الإحصائية

تعتبر هذه النماذج غالبًا الأدوات الأساسية لتحليل السلاسل الزمنية نظرًا لقابليتها للتفسير وفعاليتها المثبتة لأنماط بيانات معينة.

*   **الطرق الساذجة (Naive Methods):** خطوط أساس بسيطة، مثل التنبؤ بأن القيمة التالية ستكون هي نفسها آخر قيمة تمت ملاحظتها، أو متوسط جميع القيم السابقة.
*   **التجانس الأسي (Exponential Smoothing - ETS):** تُخصص هذه الطرق أوزانًا تتناقص أسيًا للملاحظات الأقدم. تشمل المتغيرات الرئيسية:
    *   **التجانس الأسي البسيط:** للبيانات التي لا تحتوي على اتجاه أو موسمية.
    *   **طريقة هولت للاتجاه الخطي:** تتضمن مكونًا للاتجاه.
    *   **طريقة هولت-وينترز الموسمية:** توسع طريقة هولت للتعامل مع الاتجاه والموسمية معًا.
*   **أريما (ARIMA - AutoRegressive Integrated Moving Average):** فئة قوية وشائعة الاستخدام من النماذج التي تلتقط الاعتمادات الزمنية المختلفة. تحتوي نماذج أريما على ثلاثة مكونات:
    *   **AR (الانحدار الذاتي) (p):** التنبؤ بالقيم الحالية بناءً على القيم السابقة.
    *   **I (المتكاملة) (d):** عدد مرات تفاضل الملاحظات الخام لجعل السلسلة ثابتة.
    *   **MA (المتوسط المتحرك) (q):** التنبؤ بالقيم الحالية بناءً على أخطاء التنبؤ الماضية.
    *   **ساريما (SARIMA - Seasonal ARIMA):** امتداد لأريما يتعامل صراحة مع المكونات الموسمية باستخدام مصطلحات AR و I و MA موسمية إضافية.

#### 2. نماذج التعلم الآلي

يمكن تكييف نماذج التعلم الآلي للتنبؤ بالسلاسل الزمنية عن طريق تحويل مشكلة السلاسل الزمنية إلى مشكلة تعلم خاضع للإشراف. يتضمن هذا غالبًا **هندسة الميزات (feature engineering)**.

*   **هندسة الميزات:** إنشاء ميزات جديدة من السلسلة الزمنية، مثل:
    *   **القيم المتأخرة (Lagged values):** الملاحظات السابقة للسلسلة نفسها.
    *   **الإحصائيات المتغيرة (Rolling statistics):** المتوسطات المتحركة، الانحرافات المعيارية المتغيرة على أحجام نوافذ مختلفة.
    *   **الميزات المستندة إلى الوقت:** يوم الأسبوع، الشهر، الربع، السنة، العطلات، الوقت منذ آخر حدث.
*   **نماذج الانحدار:** بمجرد هندسة الميزات، يمكن تطبيق خوارزميات الانحدار القياسية:
    *   الانحدار الخطي (Linear Regression)
    *   الغابات العشوائية (Random Forests)
    *   آلات تعزيز التدرج (Gradient Boosting Machines) مثل XGBoost و LightGBM
*   **نماذج التعلم العميق:** لتسلسلات معقدة للغاية ومجموعات بيانات كبيرة، توفر مناهج التعلم العميق أداءً فائقًا:
    *   الشبكات العصبية المتكررة (RNNs) مثل LSTMs (الذاكرة طويلة المدى قصيرة المدى) مناسبة تمامًا للبيانات المتسلسلة.
    *   شبكات المحولات (Transformer networks)، التي نشأت في معالجة اللغة الطبيعية، تكتسب أيضًا زخمًا في السلاسل الزمنية لقدرتها على التقاط الاعتمادات بعيدة المدى.

### الخطوات الرئيسية في سير عمل التنبؤ بالسلاسل الزمنية

1.  **جمع البيانات والمعالجة المسبقة:** جمع بيانات السلسلة الزمنية، والتعامل مع القيم المفقودة (التضمين)، والقيم الشاذة.
2.  **التحليل الاستكشافي للبيانات (EDA):** تصور البيانات لتحديد الاتجاهات والموسمية والدورات. تحليل السلسلة إلى مكوناتها.
3.  **فحص الثبات:** استخدام الاختبارات الإحصائية (مثل اختبار ديكي-فولر المعزز) لتحديد ما إذا كانت السلسلة ثابتة. تطبيق التفاضل إذا لزم الأمر.
4.  **اختيار النموذج:** اختيار نموذج مناسب بناءً على التحليل الاستكشافي للبيانات والثبات وتعقيد الأنماط.
5.  **تدريب النموذج والتحقق من صحته:** تقسيم البيانات إلى مجموعات تدريب واختبار. تدريب النموذج على البيانات التاريخية والتحقق من أدائه على بيانات غير مرئية. غالبًا ما يفضل التحقق المتسلسل (walk-forward validation) للسلاسل الزمنية.
6.  **التنبؤ:** إنشاء تنبؤات للفترات الزمنية المستقبلية.
7.  **التقييم:** تقييم دقة النموذج باستخدام مقاييس مثل متوسط الخطأ المطلق (MAE)، أو الجذر التربيعي لمتوسط الخطأ التربيعي (RMSE)، أو متوسط الخطأ المطلق للنسبة المئوية (MAPE).

### مثال عملي بلغة بايثون: SARIMA على بيانات ركاب الخطوط الجوية

دعنا نلقي نظرة على مثال بسيط باستخدام مكتبة `statsmodels` في بايثون للتنبؤ بأعداد ركاب الخطوط الجوية باستخدام نموذج SARIMA.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA # For SARIMAX (Seasonal ARIMA)
from sklearn.metrics import mean_squared_error
from math import sqrt

# --- 1. Load Data ---
data = pd.read_csv('https://raw.githubusercontent.com/datasets/air-passengers/main/data/air-passengers.csv',
                   index_col='Month', parse_dates=True)
data.index.freq = 'MS' # Set frequency to Month Start
data.rename(columns={'#Passengers': 'Passengers'}, inplace=True)

# --- 2. Exploratory Data Analysis (EDA) ---
plt.figure(figsize=(12, 6))
plt.plot(data['Passengers'])
plt.title('Air Passengers over Time')
plt.xlabel('Date')
plt.ylabel('Number of Passengers')
plt.grid(True)
plt.show()

# Decompose time series to see trend, seasonality, and residuals
decomposition = seasonal_decompose(data['Passengers'], model='additive')
fig = decomposition.plot()
fig.set_size_inches(10, 8)
plt.show()

# --- 3. Check for Stationarity (ADF Test) ---
def check_stationarity(timeseries):
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)
    if dftest[1] <= 0.05:
        print("Series is Stationary")
    else:
        print("Series is Non-Stationary")

print("\n--- Stationarity Test on Original Series ---")
check_stationarity(data['Passengers'])

# --- 4. Differencing to achieve Stationarity ---
# Apply 1st order non-seasonal differencing
data['Passengers_diff'] = data['Passengers'].diff().dropna()

# Apply 1st order seasonal differencing (12 months for Air Passengers data)
data['Passengers_seasonal_diff'] = data['Passengers_diff'].diff(12).dropna()
print("\n--- Stationarity Test on Seasonally Differenced Series ---")
check_stationarity(data['Passengers_seasonal_diff'])

# Plot ACF and PACF for the stationarized series to help identify p, q, P, Q
plt.figure(figsize=(12, 6))
plt.subplot(211)
plot_acf(data['Passengers_seasonal_diff'], ax=plt.gca(), lags=20)
plt.title('Autocorrelation Function (ACF) - Seasonally Differenced')
plt.subplot(212)
plot_pacf(data['Passengers_seasonal_diff'], ax=plt.gca(), lags=20)
plt.title('Partial Autocorrelation Function (PACF) - Seasonally Differenced')
plt.tight_layout()
plt.show()

# Based on common knowledge and visual inspection of ACF/PACF for AirPassengers:
# We'll use non-seasonal order (1,1,1) and seasonal order (1,1,1,12).
# d=1 (non-seasonal differencing), D=1 (seasonal differencing).

# --- 5. Model Training (SARIMA) ---
# Split data into training and testing sets
train_size = int(len(data) * 0.7)
train, test = data['Passengers'][0:train_size], data['Passengers'][train_size:]

# Instantiate and fit the SARIMA model: order(p,d,q), seasonal_order(P,D,Q,s)
model = ARIMA(train, order=(1,1,1), seasonal_order=(1,1,1,12))
model_fit = model.fit()
print(model_fit.summary())

# --- 6. Forecasting ---
# Predict for the test period
forecast_start_index = len(train)
forecast_end_index = len(data) - 1
predictions = model_fit.predict(start=forecast_start_index, end=forecast_end_index, dynamic=False)

# --- 7. Evaluation ---
rmse = sqrt(mean_squared_error(test, predictions))
print(f'Test RMSE: {rmse:.3f}')

# Plot actual vs. predicted values
plt.figure(figsize=(12, 6))
plt.plot(train.index, train, label='Train Data')
plt.plot(test.index, test, label='Actual Test Data')
plt.plot(predictions.index, predictions, label='SARIMA Predictions')
plt.title('Air Passengers SARIMA Forecast vs. Actuals')
plt.xlabel('Date')
plt.ylabel('Number of Passengers')
plt.legend()
plt.grid(True)
plt.show()
```

### التحديات في التنبؤ بالسلاسل الزمنية

على الرغم من قوتها، فإن التنبؤ بالسلاسل الزمنية يأتي بنصيبه من التحديات:
*   **عدم الثبات (Non-Stationarity):** يتطلب التعامل مع الاتجاهات والموسمية المتغيرة تفاضلاً دقيقًا أو تحويلات.
*   **الموسمية المتعددة:** يمكن أن تظهر البيانات أنماطًا يومية وأسبوعية وسنوية في وقت واحد، مما يجعل النمذجة معقدة.
*   **القيم الشاذة والبيانات المفقودة:** يمكن أن تؤدي هذه إلى تحريف كبير في تدريب النموذج والتنبؤات.
*   **الفترات غير المنتظمة:** تفترض معظم النماذج التقليدية بيانات متباعدة بالتساوي.
*   **اختيار النموذج:** يتطلب اختيار أفضل نموذج من بين العديد من الخيارات خبرة واختبارات صارمة.
*   **قابلية التفسير مقابل الدقة:** غالبًا ما توفر نماذج التعلم الآلي/التعلم العميق المتقدمة دقة عالية ولكن قد تكون أقل قابلية للتفسير من النماذج الإحصائية.

### الخلاصة

التنبؤ بالسلاسل الزمنية هو مجال ديناميكي وأساسي يمزج بين الدقة الإحصائية وقوة التعلم الآلي الحديث. من خلال فهم الأنماط الكامنة في البيانات التاريخية وتطبيق تقنيات النمذجة المناسبة، يمكننا الحصول على رؤى قيمة حول المستقبل. مع استمرار نمو البيانات من حيث الحجم والتعقيد، سيظل فن وعلم التنبؤ بما سيأتي في المقدمة في ابتكارات علم البيانات، مما يمكّن الشركات والباحثين من التنقل في عالم غير مؤكد بثقة أكبر.

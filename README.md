# Orders manager

A django project providing an API for customers to order products.

## How to run

To run project in development mode, Just use steps below:

1- Install `python3.5`, `pip3`, `virtualenv` in your system.

2- Make development environment ready using commands below;

```bash
git clone https://github.com/sajadkhosravani1/ && cd canadaHouse
virtualenv -p python3.5 venv # Create virtualenv named venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```
3- Run the server using `python manage.py runserver`

4- Go to [http://localhost:8000](http://localhost:8000) to see the home page.


## Modeling 
![image](https://maktabkhooneh.org/media/uploads/project_phase1_modeling.jpg)

## Products management

### 1- Defining new Product
برای تعریف کالای جدید، یک درخواست POST به آدرس زیر ارسال می‌شود. بدنه درخواست نیز به صورت JSON بوده و حاوی اطلاعات لازم برای تعریف کالا است.

`POST /market/product/insert/`
```json
{
    "code": "1111",
    "name": "Milk",
    "price": 1000,
    "inventory": 10 (optional)
}
```

همان‌طور که مشاهده می‌کنید، ممکن است فیلد inventory ارائه نشود. در این صورت باید مقدار پیش‌فرض (مطابق با تعریف مسئله در فاز اول) برای آن در نظر گرفته شود.

در پاسخ این درخواست، اگر ثبت کالا موفقیت آمیز نبود (به دلیل تکراری‌بودن کد یا هر ممنوعیت دیگری) باید پاسخی با کد 400 و پیامی مناسب به صورت JSON ایجاد شود. اگر هم ثبت کالا موفقیت آمیز بود، کد پاسخ 201 بوده و در متن پاسخ، شناسه کالای ایجاد شده (فیلد id که توسط خود جنگو تنظیم شده و به عنوان کلید اصلی مدل در نظر گرفته می‌شود) قرار می‌گیرد.

`400 Bad Request`
```json
{"message": "Duplicate code (or other messages)"}
```

`201 Created`
```json
{"id": 234}
```

### 2- List of Products, and search them
برای مشاهده فهرست کالاهای موجود یک درخواست GET به آدرس زیر ارسال می‌شود. در صورتی که نیاز به جستجو برای یک اسم در میان کالاها باشد، یک فیلد search به صورت پارامتر در ادامه آدرس می‌آید.

`GET /market/product/list/`

`GET /market/product/list/?search=milk`

در پاسخ این درخواست، فهرستی از کالاها به همراه تمامی فیلدهای آن به صورت JSON با کد پاسخ 200 ارسال می‌شود. اگر کاربر کلمه‌ای برای جستجو ارسال کرده بود، باید تنها کالاهایی در این فهرست نمایش داده شوند که کلمه مذکور در اسم آن‌ها وجود داشته باشد. در مثال زیر، پاسخ به یک درخواست فهرست کامل را مشاهده می‌کنید:

`200 OK`
```json
{
    "products": [
        {
            "id": 101,
            "code": "1111",
            "name": "Milk",
            "price": 1000,
            "inventory": 100
        },
        {
            "id": 102,
            "code": "2222",
            "name": "Rice",
            "price": 2000,
            "inventory": 150
        },
        {
            "id": 103,
            "code": "3333",
            "name": "SoyaMilk",
            "price": 5000,
            "inventory": 30
        }
   ]
}
```

اگر در همین درخواست، فیلد search با مقدار Milk قرار می‌گرفت، همین پاسخ بازگردانده می‌شد؛ با این تفاوت که کالای Rice در لیست نمی‌آمد و تنها کالاهایی که در بخشی از اسم خود، Milk دارند، نمایش داده می‌شدند. بدیهی است که برخی موارد ممکن است جستجو برای کلمه خاصی، منجر به خالی‌شدن فهرست خروجی شود که در این موارد نیز، یک لیست خالی جلوی products قرار می‌گیرد.

### 3- Getting some specific Product's details.
برای مشاهده یک کالای خاص، یک درخواست GET به آدرس زیر ارسال می‌شود. در بخش آخر آدرس، شماره شناسه کالا (در مثال زیر، 233) قرار می‌گیرد.

`GET /market/product/233/`

در پاسخ این درخواست، اگر کالایی با این شناسه وجود نداشت، کد 404 و پیامی مناسب بازگردانده می‌شود. در غیر این صورت کد 200 به همراه جزییات کالا پاسخ داده می‌شود.

`404 Not Found`
```json
{"message": "Product Not Found."}
```
`200 OK`
```json
{
    "id": 233,
    "code": "862345",
    "name": "Shampoo",
    "price": 22000,
    "inventory": 300
}
```

### 4- Changing some specific Product's inventory.
برای تغییر موجودی یک کالای خاص، یک درخواست POST به آدرس زیر ارسال می‌شود (مقدار 233 شبیه بخش قبل، به عنوان مثالی از شناسه کالا قرار گرفته است). در بدنه درخواست مقدار تغییر در موجودی قرار می‌گیرد. مقدار مثبت به منزله افزایش موجودی و مقدار منفی به معنی برداشت از موجودی فروشگاه است.

`POST /market/product/233/edit_inventory/`
```json
{"amount": 200}
```
 
`POST /market/product/233/edit_inventory/`
```json
{"amount": -100}
```

در پاسخ این درخواست، اگر کالایی با این شناسه وجود نداشت، کد 404 و پیامی مناسب بازگردانده می‌شود (مشابه بخش قبل). اگر کالا موجود بود ولی تغییر در موجودی به هر دلیلی ممکن نبود، کد 400 و پیامی مناسب حاوی دلیل ممنوعیت این عملیات بازگردانده می‌شود. در غیر این صورت نیز کد 200 به همراه جزییات جدید کالا پاسخ داده می‌شود.

`404 Not Found`
```json
{"message": "Product Not Found."}
```
 
`400 Bad Request`
```json
{"message": "Not enough inventory. (or other messages)"}
```

`200 OK`
```json
{
    "id": 233,
    "code": "862345",
    "name": "Shampoo",
    "price": 22000,
    "inventory": 500
}
```

## Customers management

### 1- Registering new Customer
برای ثبت‌نام یک مشتری جدید، یک درخواست POST به آدرس زیر ارسال می‌شود. بدنه درخواست نیز به صورت JSON بوده و حاوی اطلاعات لازم برای تعریف مشتری و حساب کاربری او است.

`POST /accounts/customer/register/`
```json
{
    "username": "hamed",
    "password": "123",
    "first_name": "Hamed",
    "last_name": "Moghimi",
    "email": "hamed@example.com",
    "phone": "021-22334455",
    "address": "Tehran, No.1"
}
```

پس از تشکیل حساب کاربری و تعریف مشتری در سامانه، اعتبار هدیه به او اختصاص می‌یابد. در این صورت پاسخ به صورت کد 201 و با بدنه‌ای حاوی شناسه نمونه جدیدی که از کلاس Customer ایجاد شده است، خواهد بود.

`201 Created`
```json
{"id": 12}
```

در صورتی که به هر دلیل، ساخت کاربر ممکن نشد نیز، باید پاسخی با کد 400 و پیامی مناسب ارائه شود.

`400 Bad Request`
```json
{"message": "Username already exists. (or other messages)"}
```
### 2- List of Customers, and search them

برای مشاهده فهرست مشتریان یک درخواست GET به آدرس زیر ارسال می‌شود. در صورتی که نیاز به جستجو برای یک عبارت باشد، یک فیلد search به صورت پارامتر در ادامه آدرس می‌آید.

`GET /accounts/customer/list/`

`GET /accounts/customer/list/?search=hamed`

در پاسخ این درخواست، فهرستی از مشتری‌ها به همراه تمامی فیلدهای آن به صورت JSON با کد پاسخ 200 ارسال می‌شود. دقت کنید که برای هر مشتری، اطلاعات کاربر متصل به آن نیز (شامل نام، نام خانوادگی، نام کاربری و رایانامه) ذکر می‌شود. اگر کاربر کلمه‌ای برای جستجو ارسال کرده بود، باید مشتریانی در این فهرست نمایش داده شوند که کلمه مذکور در نام یا نام خانوادگی یا نام کاربری یا آدرس آن‌ها وجود داشته باشد. در مثال زیر، پاسخ به یک درخواست فهرست کامل را مشاهده می‌کنید:

`200 OK`
```json
{
    "customers": [
        {
            "id": 12,
            "username": "hamed",
            "first_name": "Hamed",
            "last_name": "Moghimi",
            "email": "hamed@example.com",
            "phone": "021-22334455",
            "address": "Tehran, No.1",
            "balance": 20000
        },
        {
            "id": 13,
            "username": "ali",
            "first_name": "Ali",
            "last_name": "Moradi",
            "email": "ali@example.com",
            "phone": "021-22335566",
            "address": "Tehran, No.2",
            "balance": 30000
        },
        {
            "id": 14,
            "username": "reza",
            "first_name": "Reza",
            "last_name": "Maleki",
            "email": "reza@example.com",
            "phone": "081-22335566",
            "address": "Hamedan, No.3",
            "balance": 10000
        }
    ]
}
``` 

### 3- Getting some specific Customer's details

برای مشاهده اطلاعات یک مشتری، یک درخواست GET به آدرس زیر ارسال می‌شود. در بخش آخر آدرس، شماره شناسه مشتری (در مثال زیر، 12) قرار می‌گیرد.

`GET /accounts/customer/12/`

در پاسخ این درخواست، اگر یک مشتری با این شناسه وجود نداشت، کد 404 و پیامی مناسب بازگردانده می‌شود. در غیر این صورت نیز کد 200 به همراه اطلاعات مشتری در پاسخ ارائه می‌شود. دقت کنید که اطلاعات کاربر متصل به مشتری (شامل نام، نام خانوادگی، نام کاربری و رایانامه) نیز در بدنه پاسخ قرار گیرد.

`404 Not Found`
```json
{"message": "Customer Not Found."}
``` 

`200 OK`
```json
{
    "id": 12,
    "username": "hamed",
    "first_name": "Hamed",
    "last_name": "Moghimi",
    "email": "hamed@example.com",
    "phone": "021-22334455",
    "address": "Tehran, No.1",
    "balance": 20000
} 
```
اگر در همین درخواست، فیلد search با مقدار hamed قرار می‌گرفت، همین پاسخ بازگردانده می‌شد؛ با این تفاوت که مشتری شماره ۱۳ در لیست نمی‌آمد. مشتری شماره ۱۲ به دلیل وجود کلمه hamed در نام و نام کاربری خود و کاربر شماره ۱۴ به دلیل وجود کلمه hamed در بخشی از آدرس خود در لیست ظاهر می‌شوند. بدیهی است که برخی موارد ممکن است جستجو برای کلمه خاصی، منجر به خالی‌شدن فهرست خروجی شود که در این موارد نیز، یک لیست خالی جلوی customers قرار می‌گیرد.


## 4- Editing some specific Customer's details
برای ویرایش اطلاعات یک مشتری، یک درخواست POST به آدرس زیر ارسال می‌شود. در بخش آخر آدرس، شماره شناسه مشتری (در مثال زیر، 12) قرار می‌گیرد. در بدنه درخواست نیز، اطلاعات جدید مشتری قرار داده می‌شود.

`POST /accounts/customer/12/edit/`
```json
{
    "first_name": "Ehsan",
    "email": "ehsan@example.com",
    "address": "Tehran, No.2",
    "balance": 120000
}
```
 
در پاسخ این درخواست، اگر یک مشتری با این شناسه وجود نداشت، کد 404 و پیامی مناسب بازگردانده می‌شود. اگر ویرایش اطلاعات مشتری با موفقیت انجام شود، کد 200 به همراه اطلاعات جدید مشتری در پاسخ ارائه می‌شود.

`404 Not Found`
```json
{"message": "Customer Not Found."}
 ```

`200 OK`
```json
{
    "id": 12,
    "username": "hamed",
    "first_name": "Ehsan",
    "last_name": "Moghimi",
    "email": "ehsan@example.com",
    "phone": "021-22334455",
    "address": "Tehran, No.2",
    "balance": 120000
}
```
 
اما دو حالت دیگر نیز برای این درخواست باید در نظر گرفته شود. اول آن‌که اطلاعات احراز هویت مشتری در سامانه (یعنی شناسه مشتری، نام کاربری و گذرواژه) قابل ویرایش نیست. بنابراین اگر درخواست ویرایش هریک از این فیلدها داده شده بود، باید پاسخی با کد 403 مبنی بر غیرمجاز بودن این درخواست به همراه پیام مناسبی نمایش داده شود.

`403 Forbidden`
```json
{"message": "Cannot edit customer's identity and credentials."}
``` 

در نهایت، اگر به هر دلیل دیگری درخواست ویرایش قابل قبول نبود (مثلا داده‌های ورودی اعتبار لازم را نداشتند یا فیلدهای ذکرشده در بدنه درخواست صحیح نبودند)، پاسخی با کد 400 و پیام مناسب ارسال شود.

`400 Bad Request`
```json
{"message": "Balance should be integer. (or other messages)"}

```

## 5- Login
برای ورود یک مشتری به حساب کاربری خود در سامانه، یک درخواست POST به آدرس زیر ارسال می‌شود. در بدنه درخواست، نام کاربری و گذرواژه مشتری قرار داده می‌گیرد.

`POST /accounts/customer/login/`
```json
{
    "username": "hamed",
    "password": "123"
}
```
 
در پاسخ این درخواست، اگر مشخصات نادرست بود، کد 404 و پیامی مناسب بازگردانده می‌شود. اگر اطلاعات صحیح بود، علاوه بر ارسال کد 200 به پیام مناسب، کاربر در سامانه وارد شده و اطلاعات نشست در کوکی برای کاربر ارسال می‌شود. به بیانی دیگر، از مکانیزم پیش‌فرض ورود و خروج کاربران در جنگو استفاده شود.

`404 Not Found`
```json
{"message": "Username or Password is incorrect."}
 ```

`200 OK`
```json
{"message": "You are logged in successfully."}
```

## 6- Logout
برای خروج کاربری که پیش‌تر وارد شده است، یک درخواست POST بدون بدنه به آدرس زیر ارسال می‌شود.

`(after login)`

`POST /accounts/customer/logout/`
```json
{}
 ```

در پاسخ این درخواست، اگر کاربر قبلا وارد نشده بود، کد 403 و پیامی مناسب بازگردانده می‌شود. در غیر این صورت، علاوه بر آن‌که کاربر از سامانه logout می‌شود، کد 200 و پیام مناسبی بازگردانده می‌شود.
`403 Forbidden`
```json
{"message": "You are not logged in."}
```
 
`200 OK`
```json
{"message": "You are logged out successfully."}
```

## 7- Customer's profile
برای مشاهده نمایه کاربری که پیش‌تر وارد سامانه شده است، یک درخواست GET بدون ورودی به آدرس زیر ارسال می‌شود.

`(after login)` 

`GET /accounts/customer/profile/`
 
در پاسخ این درخواست، اگر کاربر قبلا وارد نشده بود، کد 403 و پیامی مناسب بازگردانده می‌شود. در غیر این صورت، کد 200 به همراه اطلاعات هویتی و نمایه کاربر حاضر (مشابه بخش ۳) بازگردانده می‌شود.

`403 Forbidden`
```json
{"message": "You are not logged in."}

 ```
`200 OK`
```json
{
    "id": 12,
    "username": "hamed",
    "first_name": "Hamed",
    "last_name": "Moghimi",
    "email": "hamed@example.com",
    "phone": "021-22334455",
    "address": "Tehran, No.1",
    "balance": 20000
}
```

## Orders management

### 1- Viewing cart
برای مشاهده سبد خرید کاربر حاضر، درخواست GET به آدرس زیر ارسال می‌شود.

`(login required)`

`GET /market/shopping/cart/`

کد پاسخ برابر 200 و بدنه پاسخ حاوی اطلاعات سبد خرید کاربر، شامل فهرستی از کالاهای موجود در سبد (کد کالا، نام کالا، قیمت واحد کالا و مقدار کالا در سبد) و مبلغ کل سبد خرید خواهد بود.


`200 OK`
```json
{
    "total_price": 9000,
    "items": [
        {
            "code": "1111",
            "name": "Milk",
            "price": 1000,
            "amount": 1
        },
        {
            "code": "2222",
            "name": "Rice",
            "price": 2000,
            "amount": 4
        }
    ]
}
```

### 2- Adding to cart

برای افزودن تعدادی کالا به سبد خرید، یک درخواست POST به آدرس زیر ارسال می‌شود. بدنه درخواست شامل فهرستی از اقلام مورد نظر برای افزودن به سبد (شامل کد کالا و مقدار کالا) است. بدیهی است که ممکن است هریک از کالاهای مورد نظر کاربر قبلا هم در سبد موجود باشد یا برای اولین باز به سبد اضافه شود.

`(login required)`

`POST /market/shopping/cart/add_items/`
```json
[
    {
        "code": "1111",
        "amount": 2
    },
    {
        "code": "3333",
        "amount": 1
    }
]
```
 

در زمان پردازش این درخواست، تلاش می‌شود تا هریک از اقلام مدنظر کاربر به سبد خرید اضافه شوند. اگر تمامی اقلام به درستی به سبد اضافه شدند، کد پاسخ 200 خواهد بود و در بدنه نیز، وضعیت جدید سبد خرید گزارش می‌شود.

`200 OK`
```json
{
    "total_price": 16000,
    "items": [
        {
            "code": "1111",
            "name": "Milk",
            "price": 1000,
            "amount": 3
        },
        {
            "code": "2222",
            "name": "Rice",
            "price": 2000,
            "amount": 4
        },
        {
            "code": "3333",
            "name": "SoyaMilk",
            "price": 5000,
            "amount": 1
        }
    ]
}
``` 

در صورتی که به هر دلیل (مثل نبود کالایی با کد مدنظر کاربر یا نبود موجودی کافی برای یک کالا) امکان پردازش برخی از اقلام درخواست وجود نداشت، باید همچنان به اقلام دیگر درخواست که امکان پردازش دارند، رسیدگی شود. در چنین حالتی، کد پاسخ باید 400 باشد. همچنین در بدنه پاسخ، وضعیت جدید سبد خرید درج می‌شود؛ با این تفاوت که یک مقدار errors به خروجی اضافه می‌شود. این مقدار شامل فهرستی از کد کالاهایی که منجر به خطا شده‌اند، به همراه پیام مناسبی در خصوص هریک از آن‌ها خواهد بود. به مثال زیر توجه کنید.

`(login required)`

`POST /market/shopping/cart/add_items/`
```json
[
    {
        "code": "1111",
        "amount": 20
    },
    {
        "code": "3333",
        "amount": 1
    },
    {
        "code": "9999",
        "amount": 2
    }
]
```
 
`400 Bad Request`
```json
{
    "total_price": 14000,
    "errors": [
        {
            "code": "1111",
            "message": "Not enough inventory."
        },
        {
            "code": "9999",
            "message": "Product not found."
        }
    ],
    "items": [
        {
            "code": "1111",
            "name": "Milk",
            "price": 1000,
            "amount": 1
        },
        {
            "code": "2222",
            "name": "Rice",
            "price": 2000,
            "amount": 4
        },
        {
            "code": "3333",
            "name": "SoyaMilk",
            "price": 5000,
            "amount": 1
        }
    ]
}
```

### 3- Deleting from cart

برای حذف تعدادی کالا از سبد خرید، یک درخواست POST به آدرس زیر ارسال می‌شود. بدنه درخواست شامل فهرستی از اقلام مورد نظر برای حذف از سبد (شامل کد کالا و در برخی موارد، مقدار کالا) است. اگر مقداری برای یک کالا درج نشده باشد، منظور آن است که آن کالا به صورت کامل از سبد خرید حذف شود.

`(login required)`

`POST /market/shopping/cart/remove_items/`
```json
[
    {
        "code": "1111"
    },
    {
        "code": "2222",
        "amount": 2
    }
]
```
قالب و قوانین خروجی این درخواست، کاملا مشابه درخواست افزودن کالا (بخش قبل) است. بنابراین اگر تمامی اقلام به درستی از سبد حذف شدند، کد پاسخ 200 خواهد بود و در بدنه نیز، وضعیت جدید سبد خرید گزارش می‌شود.

`200 OK`
```json
{
    "total_price": 4000,
    "items": [
        {
            "code": "2222",
            "name": "Rice",
            "price": 2000,
            "amount": 2
        }
    ]
}
```
 

همچنین در صورتی که به هر دلیل امکان پردازش برخی از اقلام درخواست وجود نداشت، باید به اقلام دیگر درخواست که امکان پردازش دارند، رسیدگی شود. در چنین حالتی، کد پاسخ باید 400 باشد و در بدنه پاسخ، وضعیت جدید سبد خرید به همراه مقدار errors قرار می‌گیرد.

`(login required)`

`POST /market/shopping/cart/remove_items/`
```json
[
    {
        "code": "1111",
        "amount": 20
    },
    {
        "code": "3333",
        "amount": 1
    },
    {
        "code": "4444"
    },
    {
        "code": "9999"
    }
]
```
 
`400 Bad Request`
```json
{
    "total_price": 7000,
    "errors": [
        {
            "code": "1111",
            "message": "Not enough amount in cart."
        },
        {
            "code": "4444",
            "message": "Product not found in cart."
        },
        {
            "code": "9999",
            "message": "Product not found."
        }
    ],
    "items": [
        {
            "code": "1111",
            "name": "Milk",
            "price": 1000,
            "amount": 1
        },
        {
            "code": "2222",
            "name": "Rice",
            "price": 2000,
            "amount": 3
        }
    ]
}
``` 

### 4- Submitting the order
 برای نهایی‌سازی خرید و ثبت سفارش، یک درخواست POST بدون بدنه به آدرس زیر ارسال می‌شود.

`(login required)`
`POST /market/shopping/submit/`
```json
{}
```
پس از دریافت این درخواست، موجودی کالاها از فروشگاه کم شده، مبلغ کل سفارش از اعتبار مشتری کسر شده و سفارشی با وضعیت ثبت‌شده برای مشتری ایجاد می‌شود. پاسخ این درخواست با کد 200 و بدنه‌ای حاوی اطلاعات کامل سفارش خواهد بود.

`200 OK`
```json
{
    "id": 11,
    "order_time": "2019-12-16 14:32:11",
    "status": "submitted",
    "total_price": 7000,
    "rows": [
        {
            "code": "1111",
            "name": "Milk",
            "price": 1000,
            "amount": 1
        },
        {
            "code": "2222",
            "name": "Rice",
            "price": 2000,
            "amount": 3
        }
    ]
}
```
اما در صورتی که به هر دلیلی امکان ثبت سفارش وجود نداشت، پاسخی با کد 400 و پیامی مناسب بازگردانده می‌شود.

`400 Bad Request`
```json
{ "message": "Not enough money." }
```
## TODO
- [x] Modeling
- [x] Products management
    - [x] Defining new Product
    - [x] List of Products, and search them.
    - [x] Getting some specific Product's details.
    - [x] Changing some specific Product's inventory.
- [x] Customers management
    - [x] Registering new Customer
    - [x] List of Customers, and search them
    - [x] Getting some specific Customer's details.
    - [x] Editing some specific Customer's details.
    - [x] Login
    - [x] Logout
    - [x] Customer's profile
- [x] Orders management
    - [x] Viewing cart
    - [x] Adding to cart
    - [x] Deleting from cart
    - [x] Submitting the order

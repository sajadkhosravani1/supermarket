# Orders manager

A django project for customers to order products.
It's actually my final project for a [SUT](http://www.en.sharif.edu/) django course held by [maktabkhooneh](http://maktabkhooneh.org).

## Modeling 
![image](https://maktabkhooneh.org/media/uploads/project_phase1_modeling.jpg)

## Products management

### 1- Defining new Product
برای تعریف کالای جدید، یک درخواست POST به آدرس زیر ارسال می‌شود. بدنه درخواست نیز به صورت JSON بوده و حاوی اطلاعات لازم برای تعریف کالا است.
```json


POST /market/product/insert/
-----------------------------
{
    "code": "1111",
    "name": "Milk",
    "price": 1000,
    "inventory": 10 (optional)
}
```

همان‌طور که مشاهده می‌کنید، ممکن است فیلد inventory ارائه نشود. در این صورت باید مقدار پیش‌فرض (مطابق با تعریف مسئله در فاز اول) برای آن در نظر گرفته شود.

در پاسخ این درخواست، اگر ثبت کالا موفقیت آمیز نبود (به دلیل تکراری‌بودن کد یا هر ممنوعیت دیگری) باید پاسخی با کد 400 و پیامی مناسب به صورت JSON ایجاد شود. اگر هم ثبت کالا موفقیت آمیز بود، کد پاسخ 201 بوده و در متن پاسخ، شناسه کالای ایجاد شده (فیلد id که توسط خود جنگو تنظیم شده و به عنوان کلید اصلی مدل در نظر گرفته می‌شود) قرار می‌گیرد.
```json
400 Bad Request
----------------
{"message": "Duplicate code (or other messages)"}
```
```json
201 Created
----------------
{"id": 234}
```

### 2- List of Products, and search them
برای مشاهده فهرست کالاهای موجود یک درخواست GET به آدرس زیر ارسال می‌شود. در صورتی که نیاز به جستجو برای یک اسم در میان کالاها باشد، یک فیلد search به صورت پارامتر در ادامه آدرس می‌آید.

`GET /market/product/list/`

`GET /market/product/list/?search=milk`

در پاسخ این درخواست، فهرستی از کالاها به همراه تمامی فیلدهای آن به صورت JSON با کد پاسخ 200 ارسال می‌شود. اگر کاربر کلمه‌ای برای جستجو ارسال کرده بود، باید تنها کالاهایی در این فهرست نمایش داده شوند که کلمه مذکور در اسم آن‌ها وجود داشته باشد. در مثال زیر، پاسخ به یک درخواست فهرست کامل را مشاهده می‌کنید:
```json
200 OK
----------------
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
        },        
    ]
}
```

اگر در همین درخواست، فیلد search با مقدار Milk قرار می‌گرفت، همین پاسخ بازگردانده می‌شد؛ با این تفاوت که کالای Rice در لیست نمی‌آمد و تنها کالاهایی که در بخشی از اسم خود، Milk دارند، نمایش داده می‌شدند. بدیهی است که برخی موارد ممکن است جستجو برای کلمه خاصی، منجر به خالی‌شدن فهرست خروجی شود که در این موارد نیز، یک لیست خالی جلوی products قرار می‌گیرد.

### 3- Getting some specific Product's details.
برای مشاهده یک کالای خاص، یک درخواست GET به آدرس زیر ارسال می‌شود. در بخش آخر آدرس، شماره شناسه کالا (در مثال زیر، 233) قرار می‌گیرد.

`GET /market/product/233/`

در پاسخ این درخواست، اگر کالایی با این شناسه وجود نداشت، کد 404 و پیامی مناسب بازگردانده می‌شود. در غیر این صورت کد 200 به همراه جزییات کالا پاسخ داده می‌شود.

```json
404 Not Found
----------------
{"message": "Product Not Found."}
```
```json
200 OK
----------------
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
```json
POST /market/product/233/edit_inventory/
----------------------------------------
{"amount": 200}
```
 
```json
POST /market/product/233/edit_inventory/
----------------------------------------
{"amount": -100}
```

در پاسخ این درخواست، اگر کالایی با این شناسه وجود نداشت، کد 404 و پیامی مناسب بازگردانده می‌شود (مشابه بخش قبل). اگر کالا موجود بود ولی تغییر در موجودی به هر دلیلی ممکن نبود، کد 400 و پیامی مناسب حاوی دلیل ممنوعیت این عملیات بازگردانده می‌شود. در غیر این صورت نیز کد 200 به همراه جزییات جدید کالا پاسخ داده می‌شود.

```json
404 Not Found
----------------
{"message": "Product Not Found."}
```
 
```json
400 Bad Request
----------------
{"message": "Not enough inventory. (or other messages)"}
```

```json
200 OK
----------------
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
```json
POST /accounts/customer/register/
-----------------------------
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

```json
201 Created
----------------
{"id": 12}
```

در صورتی که به هر دلیل، ساخت کاربر ممکن نشد نیز، باید پاسخی با کد 400 و پیامی مناسب ارائه شود.
```json
400 Bad Request
----------------
{"message": "Username already exists. (or other messages)"}
```
### 2- List of Customers, and search them

برای مشاهده فهرست مشتریان یک درخواست GET به آدرس زیر ارسال می‌شود. در صورتی که نیاز به جستجو برای یک عبارت باشد، یک فیلد search به صورت پارامتر در ادامه آدرس می‌آید.

`GET /accounts/customer/list/`

`GET /accounts/customer/list/?search=hamed`

در پاسخ این درخواست، فهرستی از مشتری‌ها به همراه تمامی فیلدهای آن به صورت JSON با کد پاسخ 200 ارسال می‌شود. دقت کنید که برای هر مشتری، اطلاعات کاربر متصل به آن نیز (شامل نام، نام خانوادگی، نام کاربری و رایانامه) ذکر می‌شود. اگر کاربر کلمه‌ای برای جستجو ارسال کرده بود، باید مشتریانی در این فهرست نمایش داده شوند که کلمه مذکور در نام یا نام خانوادگی یا نام کاربری یا آدرس آن‌ها وجود داشته باشد. در مثال زیر، پاسخ به یک درخواست فهرست کامل را مشاهده می‌کنید:

```json
200 OK
----------------
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

```json
404 Not Found
----------------
{"message": "Customer Not Found."}

``` 
```json
200 OK
----------------
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
```json
POST /accounts/customer/12/edit/
-------------------------------
{
    "first_name": "Ehsan",
    "email": "ehsan@example.com",
    "address": "Tehran, No.2",
    "balance": 120000
}
```
 
در پاسخ این درخواست، اگر یک مشتری با این شناسه وجود نداشت، کد 404 و پیامی مناسب بازگردانده می‌شود. اگر ویرایش اطلاعات مشتری با موفقیت انجام شود، کد 200 به همراه اطلاعات جدید مشتری در پاسخ ارائه می‌شود.
```json
404 Not Found
----------------
{"message": "Customer Not Found."}

 ```
```json
200 OK
----------------
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
```json
403 Forbidden
----------------
{"message": "Cannot edit customer's identity and credentials."}

``` 

در نهایت، اگر به هر دلیل دیگری درخواست ویرایش قابل قبول نبود (مثلا داده‌های ورودی اعتبار لازم را نداشتند یا فیلدهای ذکرشده در بدنه درخواست صحیح نبودند)، پاسخی با کد 400 و پیام مناسب ارسال شود.
```json
400 Bad Request
----------------
{"message": "Balance should be integer. (or other messages)"}

```

## Login
برای ورود یک مشتری به حساب کاربری خود در سامانه، یک درخواست POST به آدرس زیر ارسال می‌شود. در بدنه درخواست، نام کاربری و گذرواژه مشتری قرار داده می‌گیرد.
```json
POST /accounts/customer/login/
-------------------------------
{
    "username": "hamed",
    "password": "123"
}
```
 
در پاسخ این درخواست، اگر مشخصات نادرست بود، کد 404 و پیامی مناسب بازگردانده می‌شود. اگر اطلاعات صحیح بود، علاوه بر ارسال کد 200 به پیام مناسب، کاربر در سامانه وارد شده و اطلاعات نشست در کوکی برای کاربر ارسال می‌شود. به بیانی دیگر، از مکانیزم پیش‌فرض ورود و خروج کاربران در جنگو استفاده شود.
```json
404 Not Found
----------------
{"message": "Username or Password is incorrect."}

 ```
```json
200 OK
----------------
{"message": "You are logged in successfully."}

```

##Logout
برای خروج کاربری که پیش‌تر وارد شده است، یک درخواست POST بدون بدنه به آدرس زیر ارسال می‌شود.
```json
(after login)
POST /accounts/customer/logout/
-------------------------------
{}
 ```

در پاسخ این درخواست، اگر کاربر قبلا وارد نشده بود، کد 403 و پیامی مناسب بازگردانده می‌شود. در غیر این صورت، علاوه بر آن‌که کاربر از سامانه logout می‌شود، کد 200 و پیام مناسبی بازگردانده می‌شود.
```json
403 Forbidden
----------------
{"message": "You are not logged in."}
```
 
```json
200 OK
----------------
{"message": "You are logged out successfully."}
```

## Customer's profile
برای مشاهده نمایه کاربری که پیش‌تر وارد سامانه شده است، یک درخواست GET بدون ورودی به آدرس زیر ارسال می‌شود.

`(after login)` 
`GET /accounts/customer/profile/`
 

در پاسخ این درخواست، اگر کاربر قبلا وارد نشده بود، کد 403 و پیامی مناسب بازگردانده می‌شود. در غیر این صورت، کد 200 به همراه اطلاعات هویتی و نمایه کاربر حاضر (مشابه بخش ۳) بازگردانده می‌شود.
```json
403 Forbidden
----------------
{"message": "You are not logged in."}

 ```
```json
200 OK
----------------
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
- [ ] Orders management
    - [ ] Viewing cart
    - [ ] Adding to cart
    - [ ] Deleting from cart
    - [ ] Submitting the order
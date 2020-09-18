# Orders manager

A django project for customers to order products.
It's actually my final project for a [SUT](http://www.en.sharif.edu/) django course held by [maktabkhooneh](maktabkhooneh.org).

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
 


## TODO
- [x] Modeling
- [x] Products management
    - [x] Defining new Product
    - [x] List of Products, and search them.
    - [x] Getting some specific Product's details.
    - [x] Changing some specific Product's inventory.
- [ ] Customers management
    - [x] Registering new Customer
    - [ ] List of Customers, and search them
    - [ ] Getting some specific Customer's details.
    - [ ] Editing some specific Customer's details.
    - [ ] Log in
    - [ ] Log out
    - [ ] Customer's profile
- [ ] Orders management
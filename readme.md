Задание по созданию Rest API в рамках совместной разработки мобильного приложения для Android и IOS от ФСТР (Федерации Спортивного Туризма России).

Описание

На сайте https://pereval.online/ ФСТР ведёт базу горных перевалов, которая пополняется туристами.
После преодоления очередного перевала, турист заполняет отчёт в формате PDF и отправляет его на электронную почту федерации. Экспертная группа ФСТР получает эту информацию, верифицирует, а затем вносит её в базу, которая ведётся в Google-таблице.
ФСТР заказала студентам SkillFactory разработать мобильное приложение для Android и IOS, которое упростило бы туристам задачу по отправке данных о перевале и сократило время обработки запроса до трёх дней.
Пользоваться мобильным приложением будут туристы. В горах они будут вносить данные о перевале в приложение и отправлять их в ФСТР, как только появится доступ в Интернет.
Модератор из федерации будет верифицировать и вносить в базу данных информацию, полученную от пользователей, а те в свою очередь смогут увидеть в мобильном приложении статус модерации и просматривать базу с объектами, внесёнными другими.



Требования:

Для пользователя в мобильном приложении будут доступны следующие действия:
- Внесение информации о новом объекте (перевале) в карточку объекта.
- Редактирование в приложении неотправленных на сервер ФСТР данных об объектах. На перевале не всегда работает Интернет.
- Заполнение ФИО и контактных данных (телефон и электронная почта) с последующим их автозаполнением при внесении данных о новых объектах.
- Отправка данных на сервер ФСТР.
- Получение уведомления о статусе отправки (успешно/неуспешно).
- Согласие пользователя с политикой обработки персональных данных в случае нажатия на кнопку «Отправить» при отправке данных на сервер.

Пользователь с помощью мобильного приложения будет передавать в ФСТР следующие данные о перевале:
- координаты перевала и его высота;
- ФИО пользователя;
- почта и телефон пользователя;
- название перевала;
- несколько фотографий перевала.

Также есть описание CJM пользователя. CJM (customer journey map) — это карта, описывающая путь пользователя при взаимодействии с продуктом.
После этого турист нажмёт кнопку «Отправить» в мобильном приложении. Мобильное приложение вызовет метод submitData REST API.

Метод submitData принимает JSON в теле запроса с информацией о перевале. Ниже находится пример такого JSON-а:

Метод:
```
POST/submitData/
```

```
{
  "beauty_title": "пер. ",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "",
  "add_time": "2021-09-22 13:18:13",
  "user": {
    "email": "qwerty@mail.ru",
    "fam": "Пупкин",
    "name": "Василий",
    "otc": "Иванович",
    "phone": "+7 555 55 55"
  },
  "coords": {
    "latitude": "45.3842",
    "longitude": "7.1525",
    "height": "1200"
  },
  "level": {
    "winter": "",
    "summer": "1А",
    "autumn": "1А",
    "spring": ""
  },
  "images": [
    {"data": "<картинка1>", "title": "Седловина"},
    {"data": "<картинка>", "title": "Подъём"}
  ]
}
```

Результат метода: JSON

status — код HTTP, целое число:
    500 — ошибка при выполнении операции;
    400 — Bad Request (при нехватке полей);
    200 — успех.

message — строка:
    Причина ошибки (если она была);
    Отправлено успешно;
    Если отправка успешна, дополнительно возвращается id вставленной записи;
    id — идентификатор, который был присвоен объекту при добавлении в базу данных.


Примеры oтветов:
`{ "status": 500, "message": "Ошибка подключения к базе данных","id": null}`
`{ "status": 200, "message": null, "id": 42 }`


После того, как турист с помощью мобильного приложения и твоего REST API добавит в БД информацию о новом перевале, сотрудники ФСТР проведут модерацию для каждого нового объекта и поменяют поле *status*.

Допустимые значения поля status
- new;
- pending — модератор взял в работу;
- accepted — модерация прошла успешно;
- rejected — модерация прошла, информация не принята.


Метод:
```
GET /submitData/<id>
```
Получает одну запись (перевала) по её id.
Выводит всю информацию об объекте, в том числе статус модерации.


Метод:
```
PATCH /submitData/<id>
```
Редактирует существующую запись (замена), если она в статусе "new".
Редактировать можно все поля, кроме тех, что содержат в себе ФИО, адрес почты и номер телефона. Метод принимает тот же самый JSON, который принимал уже реализованный тобой метод submitData.

В качестве результата верни два значения:
state:

	1 — если успешно удалось отредактировать запись в базе данных.
	0 — в противном случае.

message — если обновить запись не удалось, напиши почему.

Добавлена возможность удалить фотографии. Для этого в конце JSON запроса нужно добавить поле ("**images_to_delete**": [<id фотографий для удаления>])*


Метод:
```
GET /submitData/?user__email=<email>
```
Список данных обо всех объектах, которые пользователь с почтой <email> отправил на сервер.


Во всех запросах перед /submitData/ нужно указывать: /api/v1*

/*
    Файл конфигурации web-приложения
*/

var createError = require('http-errors');
var express = require('express');
var path = require('path');

// Подключение обработчиков маршрутов
var indexRouter = require('../routes/index');
var contactRouter = require('../routes/contact');
var dataRouter = require('../routes/data');
var contactrequestRouter = require('../routes/contactrequest');

var app = express();

// Подключение шаблонизатора (Pug)
app.set('views', path.join(__dirname, '../views'));
app.set('view engine', 'pug');

app.use(express.json());
app.use(express.urlencoded({ extended: false }));
// Инициализация директории со static-контентом
app.use(express.static(path.join(__dirname, '../public')));

// Привязка обработчиков маршрутов к соответствующим адресам
app.use('/', indexRouter);
app.use('/contact', contactRouter);
app.use('/data', dataRouter);
app.use('/api/contactrequest', contactrequestRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error', err);
});

module.exports = app;
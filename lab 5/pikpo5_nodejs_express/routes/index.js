var express = require('express');
var router = express.Router();

// Подключение контроллера с переменной, содержащей структуру навигационного меню
var webService = require('../services/webService');

/* 
  Обработка запроса к индексной странице.
  Если запрос в БД вернул данные, рендерим шаблон индексной страницы, 
  если возникла ошибка рендерим страницу с ошибкой.
*/
router.get('/', function(req, res, next) {
  webService.getSourceFilesList(req, res)
  .then(data => {
      res.render('index', { 
      title: 'Whitesquare',
      page_name: 'HOME',
      navmenu: webService.navmenu,
      processed_files: data
    });
  })
  .catch(err => {
      console.error(err);
      res.render('error', { 
        error: err
      });
  });
});

module.exports = router;

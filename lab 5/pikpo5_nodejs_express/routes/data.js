var express = require('express');
var router = express.Router();

var webService = require('../services/webService');

/* 
  Обработка запроса по адресу /data/:id (Вывод данных по идентификатору обработанного файла).
  Если запрос в БД вернул данные, рендерим шаблон индексной страницы, 
  если возникла ошибка рендерим страницу с ошибкой.
*/
router.get('/:id', function(req, res, next) {
  webService.getProcessedData(req, res)
  .then(data => {
      res.render('data', {
      title: 'Whitesquare',
      page_name: 'DATA_FILE_' + req.params.id,
      navmenu: webService.navmenu,
      processed_data: data
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
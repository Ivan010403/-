var express = require('express');
var router = express.Router();

var webService = require('../services/webService');

/* Обработка перехода по адресу /contact и
рендеринг соответствующего шаблона */
router.get('/', function(req, res, next) {
  res.render('contact', { 
    title: 'Whitesquare',
    page_name: 'CONTACT',
    navmenu: webService.navmenu
  });
});

module.exports = router;
var express = require('express');
var router = express.Router();

/*
    Обработка POST-запроса (принимаем данные, отправленные c помощью AJAX со страницы /contact)
*/

router.post("/", function (req, res) {
    console.log(req.body);  // выводим в консоль полученные данные
    if (!req.body) return response.sendStatus(400);
    // Читаем поле firstname из полученного json
    try {
      var msg = req.body.firstname + ", ваш запрос получен !";
    } catch(err) {
      console.error(err)
      var msg = err.message;
    }
  
    res.json({ message: msg }); // отправляем ответ
  });

module.exports = router;
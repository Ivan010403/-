/*
    В Service-модулях реализуется бизнес-логика приложения.
*/
const { connector } = require('../config/database');     // подключаем объект модели БД из модуля инициализации sequelize.js

exports.navmenu = [
    {
        name: 'HOME',
        addr: '/'
    },
    {
        name: 'ABOUT',
        addr: '#'
    },
    {
        name: 'CONTACT US',
        addr: '/contact'
    }
];

/*
    ВАЖНО! Результатом выполнения запросов к БД в sequlize является Promise, 
    то обработка результата должна быть реализована через callback-функции в 
    .then() и т.д. (см. реализацию routes).

    Подробнее см.: https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Global_Objects/Promise/then
*/

// Выборка списка обработанных файлов с сортировкой по дате в порядке убывания (DESCENDING)
exports.getSourceFilesList = function(req, res) {
    return connector.query(
        'SELECT * FROM source_files ORDER BY processed DESC', 
        { type: connector.QueryTypes.SELECT }
    )
};
  
/* 
    Выборка строк из таблицы с обработанными данными.
    offset - смещение строк при выборке.
    limit - количество строк в выбоке.
    Например, при запросе: SELECT * FROM processed_data WHERE source_file = {source_file} LIMIT 20,10
    будет выбрано 10 строк, начиная с 21-ой.
*/
exports.getProcessedData = function(req, res) {
    var pageNum = req.query.pageNum;    // получаем значение GET-параметра pageNum из запроса типа: http://127.0.0.1:3000/data/16?pageNum=2
    var pageSize = 10;
    if (pageNum) {
        return connector.query(
            'SELECT * FROM processed_data WHERE source_file = :sourceFileId LIMIT :offset,:limit',
            {
                replacements: { 
                    sourceFileId: req.params.id,
                    offset: pageNum*pageSize,
                    limit: pageSize
                },
                type: connector.QueryTypes.SELECT
            }
        )
    }
    return connector.query(
        'SELECT * FROM processed_data WHERE source_file = :sourceFileId',
        {
            replacements: { sourceFileId: req.params.id },
            type: connector.QueryTypes.SELECT
        }
    )
};

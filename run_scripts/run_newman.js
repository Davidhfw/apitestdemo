const newman = require('newman')

newman.run({
    collection: require('../testcases/ApiTestSamples.postman_collection.json'),
    environment: require('../testcases/env.postman_environment.json'),
    reporters: ['cli','json','junit']

}).on('start', function (err, args) { // on start of run, log to console
    console.log('running a collection...');
}).on('done', function (err, summary) {
    if (err || summary.error) {
        console.error('collection run encountered an error.');
    }
    else {
        console.log('collection run completed.');
    }
});

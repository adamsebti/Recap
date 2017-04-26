var express = require('express');
var bodyParser = require('body-parser');
var path = require('path');
var app = express();
var PythonShell = require('python-shell');

//configure app
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// middleware
app.use(express.static(__dirname + '/views/'));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.listen(8081, function () {
  console.log('listening on port 8081')
})

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Home Page
app.get('/', function(req, res) {
	res.render('index', {
		title: "Recap"});
});

// Summary Page
app.post('/summary', function(req, res) {
	var options = {
	  mode: 'text',
	  args: [req.body.article, req.body.select]
	};

	PythonShell.run('summarize.py', options, function (err, results) {
	  if (err) throw err;
	  var summary = results[0].split('±');
	  var reduced = 100 - parseInt(results[1]) + '%';
	  var keywords = results[2]

	  res.render('summary', {
		title: "Recap", summary:summary, reduced: reduced, keywords: keywords});
	});
	
});



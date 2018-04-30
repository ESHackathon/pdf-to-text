var express = require('express');
var app = express();
var formidable = require('formidable');
var spawn = require('child_process').spawn;
var fs = require('fs');
var path = require('path');

// app.use(express.static(path.join(__dirname, 'static')));

app.use('/static', express.static('static'));
app.use('/js', express.static('js'));

app.get('/', function(req, res){
  res.sendFile(path.join(__dirname, 'index.html'));
});

var process_pdf = function(target_filepath, callback){
  var command = spawn('bash', ['pdf_to_text.sh', target_filepath]);

  var text = "";
  command.stdout.on('data', function (data) {
      text += ('' + data).replace(/\n$/, '').split("\n");
    }
  );
  command.on('exit', function(code, signal) {
    callback(code, text.split("____filename___:")[1]);
  });
};

var process_references = function(txt_processed_filename, callback){
  var command = spawn('python', ['process_references.py', txt_processed_filename]);

  var text = "";
  command.stdout.on('data', function (data) {
      text += ('' + data).replace(/\n$/, '').split("\n");
    }
  );
  command.on('exit', function(code, signal) {
    callback(code, text.split("____filename___:")[1]);
  });
};

function bufferFile(abs_path) {
  return fs.readFileSync(abs_path);
}

app.post('/pdf-to-txt', function(req, res){
  var form = new formidable.IncomingForm();
  form.multiples = false;
  form.uploadDir = path.join(__dirname, '/uploads');
  var target_filepath = null;
  form.on('file', function(field, file) {
    target_filepath = path.join(form.uploadDir, file.name);
    fs.rename(file.path, target_filepath);
  });

  // log any errors that occur
  form.on('error', function(err) {
    console.log('An error has occured: \n' + err);
  });
  form.on('end', function() {
    process_pdf(target_filepath, (err, txt_processed_filename) => {
      // console.log("txt", txt_processed_filename)
      process_references(txt_processed_filename, (err, references_filename) => {
        // console.log("references", references_filename)
        var references_json = JSON.parse(bufferFile(references_filename));
        return res.end(JSON.stringify(
          {
            txt: references_json.no_references,
            references: references_json.references,
          }
        ));
      });
    });
  });
  form.parse(req);
});

var PORT = 80;
if(process.argv.length > 2){
  PORT = parseInt(process.argv[2]);
}

app.listen(PORT, function(){console.log('localhost:' + PORT.toString());});

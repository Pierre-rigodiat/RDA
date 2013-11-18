#!/usr/bin/env node

var program    = require('commander')
  , fs         = require('fs.extra')
  , async      = require('async')
  , path       = require('path')
  , thoonk     = require('thoonk').createClient({port: 6379, host: 'h058084.nist.gov'})
  , Job        = require('thoonk-jobs')
  , shell      = require('shelljs')
  , targz      = require('tar.gz');

var Log = require('log')
  , log = new Log('info');

var msg = {
  NEED_TDIR      : "Target directory must be specified"
};

var localDir
  , queue
  , procesNum = 1;

function assert(condition, message) {
  if (!condition) {
    throw message || "Assertion failed";
  }
}

function setQueue (val) {
  queue = val;
}

function setLocalDir (val) {
  localDir = val;
}

function setProcesNum (val) {
  procesNum = val;
}

try {
  program
    .version('0.0.1')
    .option('-t, --target <dir>'       , 'target directory'    , setLocalDir)
    .option('-q, --queue <queue>'      , 'queue name'          , setQueue)
    .option('-p, --processors <number>', 'number of processors', setProcesNum)
    .parse(process.argv);

  if (process.argv[2] == undefined) {
    program.help();
    process.exit();
  }

  if (queue === undefined) {
    console.log("Must specify queue");
    process.exit();
  }

  if (localDir === undefined) {
    console.log("Must specify a local directory");
    process.exit();
  }

}
catch (e) {
  console.log(e);
}

//Execute the ocropus commands for a target directory.

function executeOcropusCommands(directory, workingDir) {

  var command = [
    "ocropus-sauvola -Q "+procesNum+" "+directory+"/*.png",
    "ocropus-gpageseg -Q "+procesNum+" "+directory+"/*.bin.png",
    "ocropus-rpred -Q "+procesNum+" "+directory+"/*/*.bin.png",
    "ocropus-hocr "+directory+"/*.bin.png -o "+directory+"/"+workingDir+"-hocr.html",
    "ocropus-visualize-results "+directory,
    //"ocropus-gtedit html --debug -o "+directory+"/"+workingDir+"-correction.html "+directory+"/*/*.bin.png"
  ];

  command.forEach(
    function(element, index, array) {
       //Run every command with script to monitor stdout and stderr
       shell.exec("script "+directory+"/typescript-"+workingDir+' -ac "'+element+'"')
    }
  );
}


thoonk.registerObject('Job', Job, function () {
  var jobWorker = thoonk.objects.Job(queue);
  async.forever(function (next) {
    jobWorker.get(0, function (err, item, id) { 
      if (err) return next();
      item = JSON.parse(item);

      //var localDir = "/home/savonitto/Documents/rsync_remote/";
      if (!(/.+\/$/).test(localDir)) {
        localDir = localDir+"/";
      }

      /\/([^/]+)$/.exec(item.file);

      var file = RegExp.$1;

      /(.+)(?:\.tar\.gz|\.zip)$/.exec(file);

      var workingDir = RegExp.$1,
      rsync = {
        PULL : "rsync data@h058084:"+item.file+" "+localDir,
        PUSH : "rsync "+localDir+file+" data@h058084:/home/data/mgi-nlp/ocr-600/"
      };

      //console.log(file);
      //console.log(workingDir);
      //console.log(rsync);

      //Pull the target file
      shell.exec(rsync.PULL);

      //Untar
      /*var untar = new targz().extract(localDir+file, localDir+workingDir,
      function(err) {
        if (err)
            console.log(err);
      });*/

      //Unzip
      shell.exec("unzip -o "+localDir+file+" -d "+localDir);

      //Execute the ocropus commands on the target directory
      executeOcropusCommands(localDir+workingDir, workingDir);

      //Tar the generated files
      /*var tar = new targz().compress(localDir+workingDir, localDir+file,
      function(err) {
        if (err)
          console.log(err);
      });*/

      //Zip
      shell.pushd(localDir);
      shell.exec("zip -ur "+file+" "+workingDir+"/");
      shell.popd();

      //Push the target file
      shell.exec(rsync.PUSH);

      //Delete the files
      rm('-r', localDir+workingDir);

      jobWorker.finish(id, 'the results', function (err) {
      next();  
      });
    });
  });
});


#!/usr/bin/env node

var program = require('commander')
  , fs      = require('fs.extra')
  , path    = require('path')
  , thoonk  = require('thoonk').createClient()
  , Job     = require('thoonk-jobs');

var Log = require('log')
  , log = new Log('info');

function assert(condition, message) {
  if (!condition) {
    throw message || "Assertion failed";
  }
}

var msg = {
  NEXIST_OR_NDIR : " does not exist or is not a directory!"
};

var inputType
  , sourceDir = "."
  , queue;

function setInputType(val) {
  inputType = new RegExp("\\." + val + "$", 'i');
}

function setQueue (val) {
  queue = val;
}

function setSourceDir(val) {
  sourceDir = val;
  fs.stat(sourceDir, function(err, stats) {
    assert(!err && stats.isDirectory(sourceDir), sourceDir + msg.NEXIST_OR_NDIR);
  });
}

try {
  program
    .version('0.0.1')
    .option('-i, --input-type <ext>', 'input file type' , setInputType)
    .option('-q, --queue <queue>'   , 'queue name'      , setQueue)
    .option('-s, --source <dir>'    , 'source directory', setSourceDir)
    .option('-d, --directories'     , 'publish subdirectories')
    .parse(process.argv);

  if (process.argv[2] == undefined) {
    program.help();
    process.exit();
  }

  if (queue === undefined) {
    console.log("Must specify queue");
    process.exit();
  }
}
catch (e) {
  console.log(e);
}

var walker = fs.walk(sourceDir);

function publishFiles(filepath) {
  filepath = path.resolve(filepath);
  thoonk.registerObject('Job', Job, function () {
    var jobPublisher = thoonk.objects.Job(queue);
    jobPublisher.subscribe(function () {
      jobPublisher.publish({"file": filepath}, {
	onFinish: function () {
	  log.info('Completed: ' + filepath); 
	}
      }, function () {
	  log.info('Published: ' + filepath);
      });
    });
  });
}

function visitFile(action) {
  return function(root, stats, next) {
    var filepath = path.join(root, stats.name);
    if (stats.isFile() && stats.name.match(inputType)) {
      try {
	action(filepath);
	log.info("Visited: %s", filepath);
      }
      catch (e) {
	log.error(e);
      }
    }
    next();
  };
}

function visitDir(action) {
  return function(root, stats, next) {
    var filepath = path.join(root, stats.name);
    if (stats.isDirectory()) {
      try {
	action(filepath);
	log.info("Visited: %s", filepath);
      }
      catch (e) {
	log.error(e);
      }
    }
    next();
  };
}

//
// Main
//

if (program.directories)
  walker.on("directory", visitDir(publishFiles));
else
  walker.on("file", visitFile(publishFiles));




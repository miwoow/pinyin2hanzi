    
load data local infile '/home/xud/chinput/start.txt'  into table start CHARACTER  set utf8  FIELDS TERMINATED BY ' '    LINES TERMINATED BY '\n'  (word,prob);
load data local infile '/home/xud/chinput/emission.txt'  into table emission CHARACTER  set utf8  FIELDS TERMINATED BY ' '    LINES TERMINATED BY '\n'  (word,pinyin, prob);
load data local infile '/home/xud/chinput/trans.txt'  into table trans CHARACTER  set utf8  FIELDS TERMINATED BY ' '    LINES TERMINATED BY '\n'  (one, two, prob);

<?php
    ini_set('display_errors', 'On'); // Something useful!
    require __DIR__ . '/../php_util/example.php';
?>

<!DOCTYPE html>
<html>
<head><meta charset="UTF8"></head>
<body>
  <h1>It works!</h1>
  <?php
    echo greeting($_GET['name']);
  ?>
  <h3>Want more tricks?</h3>
  <p>Just remember - If you get a 500 while developing PHP... The syntax of a PHP file can be checked with the command 'php -l some_file.php'</p>
  <p>Now let's do some PHP</p>
</body>
</html>

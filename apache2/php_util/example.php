<?php
  /**
   * Utility function that provides a greeting.
   *
   * @param name; The name of the person to greet.
   * @return: A string with an appropriate greeting for a healthy and happy developer.
   */
  function greeting($name) {
    if (!empty($name)) {
      return "<p>Hello, $name! Did you know that with double quotes, PHP variables will automatically be interpreted withing a string without any need for string concatenation?</p>";
    } else {
      return "<p>You can try to pass your name as a query parameter! Try visiting this page appending ?name=Pepe to the URL!</p>";
    }
  }
?>

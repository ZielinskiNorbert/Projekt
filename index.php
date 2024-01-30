<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Strona próbna</title>
</head>
<body>

    <h1>Strona Próbna</h1>

    <a href="https://www.youtube.com/watch?v=JuYeHPFR3f0">Click me </a>

    <?php
        echo '<?php echo "Infekcja"; ?>';
    ?>

    <a href="https://eportal.pwr.edu.pl/">Click me 2</a>

    <script>
        alert("XSS atakuje");
    </script>

    <h1>Komentarze</h1>

    <form action="#" method="post">
        <label for="comment">Wprowadź komentarz:</label>
        <textarea id="comment" name="comment" rows="4" cols="50"></textarea>
        <br>
        <input type="submit" value="Dodaj komentarz">
    </form>

    <?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        if(isset($_POST['comment']) && !empty($_POST['comment'])) {
            $comment = $_POST['comment']; 


            $file = 'komentarze.txt';
            file_put_contents($file, $comment . PHP_EOL, FILE_APPEND);

            echo "<p><strong>Komentarz:</strong> $comment</p>";
        } else {
            echo "<p><strong>Błąd:</strong> Komentarz nie może być pusty.</p>";
        }
    }
    ?>

    <h2>Historia Komentarzy</h2>

    <?php
    $file = 'komentarze.txt';
    if (file_exists($file)) {
        $comments = file($file, FILE_IGNORE_NEW_LINES);
        foreach ($comments as $comment) {
            echo "<p><strong>Komentarz:</strong> $comment</p>";
        }
    }
    ?>

</body>
</html>

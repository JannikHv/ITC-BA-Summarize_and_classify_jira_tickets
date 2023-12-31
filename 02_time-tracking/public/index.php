<?php

require_once __DIR__ . '/../utils/database.php';

\session_start();

$database = Database::getInstance();
$accessKey = $_SESSION['accessKey'] ?? null;

?>

<!DOCTYPE html>

<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-HwwvtgBNo3bZJJLYd8oVXjrBZt8cqVSpeBNS5n7C8IVInixGAoxmnlMuBnhbgrkm" crossorigin="anonymous"></script>
        <link rel="shortcut icon" href="https://amicaldo.atlassian.net/s/-3o5b4z/b/4/41615a97374969b96da5f96a98098adf/_/favicon-family.ico">
        <title>Jira Timetracker</title>
    </head>

    <body>
        <br>
        <h1 class="text-center">Anmeldung</h1>
        <br>
        <h2 class="text-center">Zeitmessung für Zuweisung von Support-Anfragen</h2>
        <br>
        <div class="text-center">
            Gib Deinen Vor- und Nachnamen ein und drücke anschließend auf "Starten", um Support-Anfragen zuzuweisen.<br>
            Die Support-Anfragen werden zufällig Originaltexte oder Zusammenfassungen beinhalten.<br>
        </div>

        <br>

        <h4 class="text-center">Ablauf</h4>

        <div class="mx-auto" style="max-width: fit-content;">
            <ol>
                <li>Support-Anfrage durchlesen</li>
                <li>Bearbeiter auswählen</li>
                <li>Auf "Weiter" drücken</li>
            </ol>
        </div>

        <div class="text-center">Sobald du fertig bist, kannst du auf "Schließen" drücken.</div>

        <form class="py-4 w-100 mx-auto" style="max-width: 24rem;" method="POST" action="/auth/login.php">
            <div class="form-group">
                <label for="inputFirstname">Zugangsschlüssel</label>
                <input
                    required
                    type="text"
                    class="form-control"
                    id="accessKey"
                    name="accessKey"
                    placeholder="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
                    value="<?= $accessKey ? $accessKey : '' ?>"
                >
            </div>

            <br>

            <div class="text-center">
                <button type="submit" class="btn btn-primary w-25" style="min-width: 20rem;">Starten</button>
            </div>
        </form>
    </body>
</html>
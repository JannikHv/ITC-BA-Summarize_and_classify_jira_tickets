<?php

require_once __DIR__ . '/../../utils/database.php';

\session_start();

$database = Database::getInstance();
$accessKey = $_SESSION['accessKey'] ?? null;
$hasAccess = $database->validateAccessKey($accessKey);

if (!$hasAccess) {
    ?>
    <strong>Ungültiger Zugangsschlüssel</strong><br>
    <a href="/">Zurück zur Startseite</a>
    <?php

    die();
}

$ticket = $database->getNextTicket($accessKey);
$assignees = $database->getAllAssignees();
?>

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-HwwvtgBNo3bZJJLYd8oVXjrBZt8cqVSpeBNS5n7C8IVInixGAoxmnlMuBnhbgrkm" crossorigin="anonymous"></script>
        <link rel="shortcut icon" href="https://amicaldo.atlassian.net/s/-3o5b4z/b/4/41615a97374969b96da5f96a98098adf/_/favicon-family.ico">
        <title>Tracking <?= $ticket['key'] ?></title>

        <style>
            html, body {
                height: 100%;
                width: 100%;
            }

            body {
                display: flex;
                flex-direction: column;
            }

            body main {
                flex: 1;
            }

            form .btn,
            form .dropdown-menu {
                width: 16rem;
            }

            .dropdown-item {
                height: 40px;
            }
        </style>
    </head>

    <body>
        <main class="py-4 mx-auto container">
            <h2 class="text-center">
                <span id="ticket-key"><?= $ticket['key'] ?></span>
            </h2>

            <div class="text-center" id="ticket-reporter">
                Eingereicht von <a href="mailto:<?= $ticket['reporter_email_address'] ?>"><?= $ticket['reporter_email_address'] ?></a>

                <?php
                    if ($database->isControlGroup($accessKey) === false && isset($ticket['spam'])) {
                        ?>
                        <br>
                        <span>Spam-Wahrscheinlichkeit: <?= \round($ticket['spam'], 2) ?> %</span>
                        <?php
                    }
                ?>
            </div>

            <br>
            <hr>
            <br>

            <div id="ticket-content" class="overflow-x-auto">
                <?= $database->isControlGroup($accessKey) ? $ticket['description'] : $ticket['summary'] ?>
            </div>
        </main>

        <div class="container">
            <hr>
        </div>

        <form method="POST" action="/track/finish.php" class="mx-auto py-4 container" style="max-width: fit-content;">
            <input type="hidden" name="access_key" value="<?= $accessKey ?>">
            <input type="hidden" name="issue_id" value="<?= $ticket['id'] ?>">
            <input type="hidden" name="time_start" value="<?= \time() ?>">
            <input type="hidden" name="assignee_id" id="assigneeSelection" required>
            <input type="hidden" name="spam" id="spam" value="0">
            <input type="hidden" name="unassignable" id="unassignable" value="0">

            <div class="text-center">
                <div class="dropdown" id="assignee-dropdown">
                    <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Bearbeiter auswählen
                    </button>
                    <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                        <button type="button" class="dropdown-item text-center">
                            Bearbeiter auswählen
                        </button>

                        <hr>

                        <button type="button" class="dropdown-item text-center" data-value="unassignable">
                            Nicht zuordenbar
                        </button>

                        <button type="button" class="dropdown-item text-center" data-value="spam">
                            Spam
                        </button>

                        <hr>

                        <?php
                        $i = 0;
                        foreach ($assignees as $assignee) {
                            ?>
                            <button type="button" class="dropdown-item" data-value="<?= $assignee['account_id'] ?>">
                            <img class="avatar rounded-circle" src="<?= $assignee['avatar_url'] ?>" height="32" width="32">
                                &nbsp;
                                <?= $assignee['display_name'] ?>
                            </button>
                            <?php
                        }
                        ?>
                    </div>
                </div>
            </div>

            <br>

            <div class="text-center">
                <a class="btn btn-danger" href="/">Schließen</a>
                <button class="btn btn-success" disabled type="submit">Weiter</button>
            </div>
        </form>

        <script>
            document.addEventListener('DOMContentLoaded', () => {
                const dropdown = document.getElementById('assignee-dropdown');
                const dropdownItems = dropdown.querySelectorAll('.dropdown-item');
                const dropdownSelectionInput = document.getElementById('assigneeSelection');
                const submitButtons = document.querySelectorAll('button[type="submit"]')
                const inputSpam = document.getElementById('spam');
                const inputUnassignable = document.getElementById('unassignable');

                dropdownItems.forEach((item) => {
                    item.addEventListener('click', () => {
                        const value = item.getAttribute('data-value');
                        document.getElementById('dropdownMenuButton').innerText = item.innerText;

                        if (value == 'spam') {
                            inputSpam.value = (value == 'spam') ? '1' : '0';
                            dropdownSelectionInput.value = null;
                        } else if (value == 'unassignable') {
                            inputUnassignable.value = (value == 'unassignable') ? '1' : '0';
                            dropdownSelectionInput.value = null;
                        } else {
                            dropdownSelectionInput.value = item.getAttribute('data-value');
                        }

                        submitButtons.forEach((b) => b.toggleAttribute('disabled', !item.getAttribute('data-value')));
                    });
                });
            });
        </script>
    </body>
</html>

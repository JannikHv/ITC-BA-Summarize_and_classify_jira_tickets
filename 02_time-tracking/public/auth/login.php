<?php

require_once __DIR__ . '/../../utils/database.php';

\session_start();

$database = Database::getInstance();
$accessKey = $_POST['accessKey'] ?: null;
$hasAccess = $database->validateAccessKey($accessKey);

if ($hasAccess && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $_SESSION['accessKey'] = $accessKey;
} else {
    $_SESSION['accessKey'] = null;
}

\header('Location: /track');
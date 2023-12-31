<?php

require_once __DIR__ . '/../../utils/database.php';

\session_start();

$database = Database::getInstance();
$accessKey = $_SESSION['accessKey'] ?? null;

if (!isset($_POST['time_start'])) {
    throw new Error('Missing parameter: time_start');
}

if (!isset($_POST['access_key']) || $_POST['access_key'] !== $accessKey) {
    throw new Error('Invalid access key');
}

$database->insertAssignment([
    'access_key' => $accessKey,
    'issue_id' => $_POST['issue_id'],
    'assignee_id' => $_POST['assignee_id'],
    'time_start' => $_POST['time_start'],
    'time_end' => \time(),
    'spam' => \intval($_POST['spam']),
    'unassignable' => \intval($_POST['unassignable'])
]);

\header('Location: /track');
?>

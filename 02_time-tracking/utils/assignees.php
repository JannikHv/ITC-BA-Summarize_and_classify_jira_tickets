<?php

class Assignees {
    public static function all(): array
    {
        $filepath = __DIR__ . '/assignees.json';

        if (\file_exists($filepath) === false) {
            die('File not found: ' . $filepath);
        }

        return \json_decode(\file_get_contents($filepath), true);
    }
}
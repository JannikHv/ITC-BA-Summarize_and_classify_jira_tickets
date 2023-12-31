<?php

class Issues {
    public static function all(): array
    {
        $filepath = __DIR__ . '/issues.json';

        if (\file_exists($filepath) === false) {
            die('File not found: ' . $filepath);
        }

        return \json_decode(\file_get_contents($filepath), true);
    }
}
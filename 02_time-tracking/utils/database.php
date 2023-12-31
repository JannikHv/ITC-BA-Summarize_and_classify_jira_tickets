<?php

require_once __DIR__ . '/issues.php';
require_once __DIR__ . '/assignees.php';

class Database {
    /** @var self */
    private static $instance = null;

    /** @var \SQLite3 */
    private $db;

    private function __construct()
    {
        $dbFilepath = __DIR__ . '/../sqlite3.db';
        $dbInit = !\file_exists($dbFilepath);

        $this->db = new \SQLite3($dbFilepath);

        if ($dbInit) {
            $this->createTables();
            $this->importData();
        }
    }

    public static function getInstance(): self
    {
        return (self::$instance ?? (self::$instance = new self()));
    }

    public function getNextTicket(string $accessKey): ?array
    {
        $stmt = $this->db->prepare('SELECT *
            FROM issues i
            WHERE i.id NOT IN (
                SELECT a.issue_id
                FROM assignments a
                WHERE a.access_key = :access_key
            )
            ORDER BY i.key ASC
            LIMIT 1
        ');

        $stmt->bindValue(':access_key', $accessKey);

        return $stmt->execute()->fetchArray(\SQLITE3_ASSOC) ?: null;
    }

    public function getRandomTicketForUser(string $accessKey): ?array
    {
        $stmt = $this->db->prepare('SELECT *
            FROM issues i
            WHERE i.id NOT IN (
                SELECT a.issue_id
                FROM assignments a
                WHERE a.access_key = :access_key
            )
            ORDER BY RANDOM()
            LIMIT 1
        ');

        $stmt->bindValue(':access_key', $accessKey);

        return $stmt->execute()->fetchArray(\SQLITE3_ASSOC) ?: null;
    }

    public function getAllAssignees(): array {
        $query = $this->db->query('SELECT * FROM `assignees` ORDER BY display_name ASC');

        $rows = [];

        while ($row = $query->fetchArray(\SQLITE3_ASSOC)) {
            $rows[] = $row;
        }

        return $rows;
    }

    public function isControlGroup(string $accessKey): bool
    {
        $stmt = $this->db->prepare('SELECT is_control_group FROM access_keys WHERE `key` = :access_key');

        $stmt->bindValue(':access_key', $accessKey);

        $result = $stmt->execute()->fetchArray(\SQLITE3_ASSOC);

        return $result['is_control_group'];
    }

    public function validateAccessKey(?string $accessKey): bool
    {
        if ($accessKey === false) return false;

        $stmt = $this->db->prepare('SELECT * FROM access_keys WHERE `key` = :access_key');

        $stmt->bindValue(':access_key', $accessKey);

        $result = $stmt->execute()->fetchArray(\SQLITE3_ASSOC);

        return !empty($result);
    }

    public function insertAssignment(array $assignment): bool
    {
        $stmt = $this->db->prepare('INSERT OR IGNORE INTO assignments
        (access_key, issue_id, assignee_id, time_start, time_end, spam, unassignable)
        VALUES (:access_key, :issue_id, :assignee_id, :time_start, :time_end, :spam, :unassignable)');

        $stmt->bindValue(':access_key', $assignment['access_key'] ?? null);
        $stmt->bindValue(':issue_id', $assignment['issue_id'] ?? null);
        $stmt->bindValue(':assignee_id', $assignment['assignee_id'] ?? null);
        $stmt->bindValue(':time_start', $assignment['time_start'] ?? null);
        $stmt->bindValue(':time_end', $assignment['time_end'] ?? null);
        $stmt->bindValue(':spam', $assignment['spam'] ?? 0);
        $stmt->bindValue(':unassignable', $assignment['unassignable'] ?? 0);

        return $stmt->execute() !== false;
    }

    public function insertAccessKey(array $data): bool
    {
        $stmt = $this->db->prepare('INSERT OR IGNORE INTO access_keys VALUES (:key, :is_control_group)');

        $stmt->bindValue(':key', $data['key']);
        $stmt->bindValue(':is_control_group', $data['isControlGroup']);

        return $stmt->execute() !== false;
    }

    public function insertAssignee(array $assignee): bool
    {
        $stmt = $this->db->prepare('INSERT OR IGNORE INTO assignees VALUES (
            :account_id, :display_name, :avatar_url
        )');

        $stmt->bindValue(':account_id', $assignee['accountId'] ?? null);
        $stmt->bindValue(':display_name', $assignee['displayName'] ?? null);
        $stmt->bindValue(':avatar_url', isset($assignee['avatarUrls']) ? $assignee['avatarUrls']['48x48'] : null);

        return $stmt->execute() !== false;
    }

    public function insertTicket(array $ticket): bool
    {
        $stmt = $this->db->prepare('INSERT OR IGNORE INTO issues VALUES (
            :id, :key, :description, :assignee_account_id, :reporter_email_address, :summary, :spam
        )');

        $stmt->bindValue(':id', $ticket['id'] ?? null);
        $stmt->bindValue(':key', $ticket['key'] ?? null);
        $stmt->bindValue(':description', $ticket['description'] ?? null);
        $stmt->bindValue(':assignee_account_id', $ticket['assignee']['accountId'] ?? null);
        $stmt->bindValue(':reporter_email_address', $ticket['reporter']['emailAddress'] ?? null);
        $stmt->bindValue(':summary', $ticket['summary'] ?? null);
        $stmt->bindValue(':spam', $ticket['spam'] ?? null);

        return $stmt->execute() !== false;
    }

    private function createTables(): void
    {
        $this->db->exec('CREATE TABLE IF NOT EXISTS `issues` (
            `id` VARCHAR(256) PRIMARY KEY,
            `key` TEXT,
            `description` TEXT,
            `assignee_account_id` VARCHAR(256),
            `reporter_email_address` VARCHAR(512),
            `summary` TEXT,
            `spam` FLOAT,

            FOREIGN KEY (assignee_account_id) REFERENCES assignees(accountId)
        )');

        $this->db->exec('CREATE TABLE IF NOT EXISTS `assignees` (
            `account_id` VARCHAR(256) PRIMARY KEY,
            `display_name` TEXT,
            `avatar_url` TEXT
        )');

        $this->db->exec('CREATE TABLE IF NOT EXISTS `access_keys` (
            `key` VARCHAR(36) PRIMARY KEY,
            `is_control_group` BOOLEAN
        )');

        $this->db->exec('CREATE TABLE IF NOT EXISTS `assignments` (
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `access_key` VARCHAR(36),
            `issue_id` VARCHAR(256),
            `assignee_id` VARCHAR(256),
            `time_start` TIMESTAMP,
            `time_end` TIMESTAMP,
            `spam` BOOLEAN,
            `unassignable` BOOLEAN,

            FOREIGN KEY (access_key) REFERENCES access_keys(`key`),
            FOREIGN KEY (assignee_id) REFERENCES assignees(`accountId`),
            FOREIGN KEY (issue_id) REFERENCES issues(`id`)
        )');
    }

    private function importData() {
        foreach (Issues::all() as $issue) {
            $this->insertTicket($issue);
        }

        foreach (Assignees::all() as $assignee) {
            $this->insertAssignee($assignee);
        }

        /** Generate 10 codes for amicaldo employees */
        for ($i = 0; $i < 10; $i++) {
            $this->insertAccessKey([
                'key' => $this->generateUuidV4(),
                'isControlGroup' => ($i % 2 === 0)
            ]);
        }
    }

    private function generateUuidV4(): string {
        return \sprintf(
            '%04x%04x-%04x-%04x-%04x-%04x%04x%04x',
            \mt_rand(0, 0xffff),
            \mt_rand(0, 0xffff),
            \mt_rand(0, 0xffff),
            \mt_rand(0, 0x0fff) | 0x4000,
            \mt_rand(0, 0x3fff) | 0x8000,
            \mt_rand(0, 0xffff),
            \mt_rand(0, 0xffff),
            \mt_rand(0, 0xffff)
        );
    }
}
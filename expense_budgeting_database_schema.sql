CREATE TABLE `User` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each user.',
    `username` VARCHAR(255) NOT NULL COMMENT 'User''s login username.',
    `email` VARCHAR(255) NOT NULL COMMENT 'User''s email address.',
    `password` VARCHAR(255) NOT NULL COMMENT 'Hashed password for user authentication.',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp of when the user account was created.',
    `updated_at` DATETIME NULL ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp of when the user account was last updated.',
    CONSTRAINT `user_email_unique` UNIQUE (`email`),
    CONSTRAINT `user_username_unique` UNIQUE (`username`),
    CONSTRAINT `user_email_check` CHECK (REGEXP_LIKE(`email`, '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,}$'))
);

CREATE TABLE `User_Profile` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each user profile.',
    `user_id` INT UNSIGNED NOT NULL COMMENT 'References the User table''s id.',
    `first_name` VARCHAR(255) NOT NULL COMMENT 'User''s first name.',
    `last_name` VARCHAR(255) NOT NULL COMMENT 'User''s last name.',
    `avatar` VARCHAR(255) NULL COMMENT 'URL or file path to user''s profile picture.',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp of when the user profile was created.',
    `updated_at` DATETIME NULL ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp of when the user profile was last updated.',
    CONSTRAINT `user_profile_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE,
    CONSTRAINT `user_profile_user_id_unique` UNIQUE (`user_id`)
);

CREATE TABLE `Category` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each category.',
    `name` VARCHAR(255) NOT NULL COMMENT 'Name of the category.',
    `description` VARCHAR(255) NULL COMMENT 'Description or additional information about the category.',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp of when the category was created.',
    `updated_at` DATETIME NULL ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp of when the category was last updated.',
    CONSTRAINT `category_name_unique` UNIQUE (`name`)
);

CREATE TABLE `Account` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each account.',
    `user_id` INT UNSIGNED NOT NULL COMMENT 'References the User table''s id.',
    `name` VARCHAR(255) NOT NULL COMMENT 'Name of the account.',
    `type` VARCHAR(255) NOT NULL COMMENT 'Type of the account (e.g., bank account, credit card).',
    `balance` DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT 'Current balance of the account.',
    `currency_id` INT UNSIGNED NOT NULL COMMENT 'References the Currency table''s id.',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp of when the account was created.',
    `updated_at` DATETIME NULL ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp of when the account was last updated.',
    CONSTRAINT `account_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE,
    CONSTRAINT `account_currency_id_foreign` FOREIGN KEY (`currency_id`) REFERENCES `Currency` (`id`)
);

CREATE TABLE `Expense` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each expense.',
    `user_id` INT UNSIGNED NOT NULL COMMENT 'References the User table''s id.',
    `category_id` INT UNSIGNED NOT NULL COMMENT 'References the Category table''s id.',
    `account_id` INT UNSIGNED NOT NULL COMMENT 'References the Account table''s id.',
    `amount` DECIMAL(10, 2) NOT NULL COMMENT 'Amount of the expense.',
    `description` VARCHAR(255) NULL COMMENT 'Description or note for the expense.',
    `date` DATE NOT NULL COMMENT 'Date when the expense occurred.',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp of when the expense was created.',
    `updated_at` DATETIME NULL ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp of when the expense was last updated.',
    CONSTRAINT `expense_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE,
    CONSTRAINT `expense_category_id_foreign` FOREIGN KEY (`category_id`) REFERENCES `Category` (`id`),
    CONSTRAINT `expense_account_id_foreign` FOREIGN KEY (`account_id`) REFERENCES `Account` (`id`),
    CONSTRAINT `expense_amount_check` CHECK (`amount` >= 0)
);

CREATE TABLE `Budget` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each budget.',
    `user_id` INT UNSIGNED NOT NULL COMMENT 'References the User table''s id.',
    `category_id` INT UNSIGNED NOT NULL COMMENT 'References the Category table''s id.',
    `amount` DECIMAL(10, 2) NOT NULL COMMENT 'Budgeted amount for the category.',
    `start_date` DATE NOT NULL COMMENT 'Start date of the budget period.',
    `end_date` DATE NOT NULL COMMENT 'End date of the budget period.',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp of when the budget was created.',
    `updated_at` DATETIME NULL ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp of when the budget was last updated.',
    CONSTRAINT `budget_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE,
    CONSTRAINT `budget_category_id_foreign` FOREIGN KEY (`category_id`) REFERENCES `Category` (`id`),
    CONSTRAINT `budget_date_check` CHECK (`end_date` >= `start_date`),
    CONSTRAINT `budget_amount_check` CHECK (`amount` >= 0)
);

CREATE TABLE `Transaction` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each transaction.',
    `account_id` INT UNSIGNED NOT NULL COMMENT 'References the Account table''s id.',
    `category_id` INT UNSIGNED NOT NULL COMMENT 'References the Category table''s id.',
    `amount` DECIMAL(10, 2) NOT NULL COMMENT 'Amount of the transaction.',
    `description` VARCHAR(255) NULL COMMENT 'Description or note for the transaction.',
    `date` DATE NOT NULL COMMENT 'Date when the transaction occurred.',
    `type` ENUM('income', 'expense') NOT NULL COMMENT 'Type of the transaction (income or expense).',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp of when the transaction was created.',
    `updated_at` DATETIME NULL ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp of when the transaction was last updated.',
    CONSTRAINT `transaction_account_id_foreign` FOREIGN KEY (`account_id`) REFERENCES `Account` (`id`),
    CONSTRAINT `transaction_category_id_foreign` FOREIGN KEY (`category_id`) REFERENCES `Category` (`id`)
);

CREATE TABLE `Recurring_Transaction` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each recurring transaction.',
    `account_id` INT UNSIGNED NOT NULL COMMENT 'References the Account table''s id.',
    `category_id` INT UNSIGNED NOT NULL COMMENT 'References the Category table''s id.',
    `amount` DECIMAL(10, 2) NOT NULL COMMENT 'Amount of the recurring transaction.',
    `description` VARCHAR(255) NULL COMMENT 'Description or note for the recurring transaction.',
    `start_date` DATE NOT NULL COMMENT 'Start date of the recurring transaction.',
    `end_date` DATE NULL COMMENT 'End date of the recurring transaction (optional).',
    `frequency` ENUM('daily', 'weekly', 'monthly', 'yearly') NOT NULL COMMENT 'Frequency of the recurring transaction.',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp of when the recurring transaction was created.',
    `updated_at` DATETIME NULL ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp of when the recurring transaction was last updated.',
    CONSTRAINT `recurring_transaction_account_id_foreign` FOREIGN KEY (`account_id`) REFERENCES `Account` (`id`),
    CONSTRAINT `recurring_transaction_category_id_foreign` FOREIGN KEY (`category_id`) REFERENCES `Category` (`id`),
    CONSTRAINT `recurring_transaction_date_check` CHECK (`end_date` IS NULL OR `end_date` >= `start_date`),
    CONSTRAINT `recurring_transaction_amount_check` CHECK (`amount` >= 0)
);

CREATE TABLE `Goal` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each goal.',
    `user_id` INT UNSIGNED NOT NULL COMMENT 'References the User table''s id.',
    `name` VARCHAR(255) NOT NULL COMMENT 'Name or title of the goal.',
    `description` VARCHAR(255) NULL COMMENT 'Description or additional details about the goal.',
    `target_amount` DECIMAL(10, 2) NOT NULL COMMENT 'Target amount to be achieved for the goal.',
    `current_amount` DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT 'Current amount saved or contributed towards the goal.',
    `start_date` DATE NOT NULL COMMENT 'Start date of the goal.',
    `end_date` DATE NOT NULL COMMENT 'Target end date of the goal.',
    `status` ENUM('in_progress', 'achieved', 'abandoned') NOT NULL DEFAULT 'in_progress' COMMENT 'Current status of the goal.',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp of when the goal was created.',
    `updated_at` DATETIME NULL ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp of when the goal was last updated.',
    CONSTRAINT `goal_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE,
    CONSTRAINT `goal_date_check` CHECK (`end_date` >= `start_date`),
    CONSTRAINT `goal_amount_check` CHECK (`current_amount` >= 0 AND `target_amount` >= 0 AND `current_amount` <= `target_amount`)
);

CREATE TABLE `Alert` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each alert.',
    `user_id` INT UNSIGNED NOT NULL COMMENT 'References the User table''s id.',
    `message` VARCHAR(255) NOT NULL COMMENT 'Alert message or notification text.',
    `type` ENUM('budget', 'bill', 'goal') NOT NULL COMMENT 'Type of the alert (budget, bill, or goal).',
    `trigger_date` DATE NOT NULL COMMENT 'Date when the alert should be triggered.',
    `is_read` BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'Indicates whether the alert has been read by the user.',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp of when the alert was created.',
    `updated_at` DATETIME NULL ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp of when the alert was last updated.',
    CONSTRAINT `alert_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE
);

CREATE TABLE `Currency` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each currency.',
    `code` CHAR(3) NOT NULL COMMENT 'ISO 4217 currency code (e.g., USD, EUR).',
    `name` VARCHAR(255) NOT NULL COMMENT 'Full name of the currency.',
    `symbol` VARCHAR(10) NOT NULL COMMENT 'Currency symbol (e.g., $, €).',
    CONSTRAINT `currency_code_unique` UNIQUE (`code`)
);
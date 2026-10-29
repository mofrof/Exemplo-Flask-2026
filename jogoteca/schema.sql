CREATE DATABASE IF NOT EXISTS jogoteca CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE jogoteca;

CREATE TABLE IF NOT EXISTS usuarios (
    uuid VARCHAR(255) NOT NULL,
    login VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    PRIMARY KEY (uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS jogos (
    uuid VARCHAR(255) NOT NULL,
    nome VARCHAR(255) NOT NULL UNIQUE,
    plataforma ENUM('Console', 'PC', 'Portatil') NOT NULL,
    anoLancamento DATE NOT NULL,
    localImagemCapaJogo VARCHAR(255),
    PRIMARY KEY (uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

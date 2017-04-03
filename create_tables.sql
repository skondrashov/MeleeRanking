-- None of these tables, names, architecture is stuck in stone. It will certainly need to be adjusted given what we want to do.
-- Here are a few thing we'd like to do using this database.

-- Store all results from all tournaments given
-- Store all players and their skill levels (Player is a person who has entered a tournament)
-- Store all users on the page (User is a user on the website)
-- Access all results for a single person
-- Access results for a single person limited by opponent, date, type of tournament (UMeMe, Sweet, etc), tournament size, win/loss,
-- Access all tournaments of a given size, skill, date, location, or type (UMeMe, Sweet, etc)
-- Create an elo graph over time for any period of time
-- Track jumps or dips in elo (Store it somewhere maybe? Not sure how to implement this really given our current implementation of ELO changes)
-- Show the possibilities of a future win at a tournament with a known amount of entrants
-- Be able to BACKTRACK a fucked up input or result without it fucking the whole system





-- Feel free to make suggestions for what we could do for the site, as well as structural changes, implementations, redundancies, etc.

-- Most of this stuff aren't things I'm looking to implement right now, but they're all things that I want to keep in mind for the long run
-- Also I didn't put that much thought into the organization, I just wanted a brief format of what we're looking at to begin with,
-- we're waiting on ThugZ to give us his Smash.GG/Challonge parsers rn

CREATE DATABASE IF NOT EXISTS MeleeData;
USE MeleeData

DROP TABLE IF EXISTS
    ratings,
    sets,
    tournaments,
    users,
    players;

CREATE TABLE players(
    id      INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    tag     VARCHAR(50)  NOT NULL,
    sponsor VARCHAR(50)
    /*
    -- tournaments attended:
        SELECT id FROM tournaments t
            JOIN sets s ON t.id = s.tournament_id
            WHERE s.winner_id={player_id} OR s.loser_id={player_id};
    -- data against an opponent:
        SELECT COUNT(*) FROM sets
            WHERE winner_id={player_id} AND loser_id={opponent_id} OR winner_id={opponent_id} AND loser_id={player_id};
    -- all sets in chronological order:
        SELECT * FROM sets s
            JOIN tournaments t ON t.id = s.tournament_id
            WHERE s.winner_id={player_id} OR s.loser_id={player_id}
            ORDER BY t.date, t.id, s.is_losers, s.sets_remaining;
    --
    */
);

CREATE TABLE users(
    id          INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    username    VARCHAR(50)  NOT NULL,
    password    BINARY(64)   NOT NULL,
    player_id   INT UNSIGNED,
    first_name  VARCHAR(50),
    last_name   VARCHAR(50),
    facebook_id VARCHAR(50),
    FOREIGN KEY (player_id)
        REFERENCES players(id)
        ON DELETE SET NULL
    -- add other profile information
);

CREATE TABLE tournaments(
    id       INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    id_string VARCHAR(100) NOT NULL,
    host     VARCHAR(16) NOT NULL,
    name     VARCHAR(100) NOT NULL,
    series   VARCHAR(100),
    location VARCHAR(100) NOT NULL,
    date     TIMESTAMP    NOT NULL
    /*
    -- entrants can be found with (for example):
        SELECT (COUNT(winner_id) + COUNT(loser_id)) AS entrants
            FROM sets
            WHERE tournament_id={tournament_id} AND is_losers = FALSE AND sets_remaining=MAX(sets_remaining);
    */
);

-- bracket can be built using losers_bracket and sets_remaining, and displayed by matching match participants to prior match winner_ids
CREATE TABLE sets(
    id             INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    tournament_id  INT UNSIGNED     NOT NULL,
    winner_id      INT UNSIGNED     NOT NULL,
    loser_id       INT UNSIGNED     NOT NULL,
    best_of        TINYINT UNSIGNED NOT NULL,
    loser_wins     TINYINT UNSIGNED NOT NULL,
    sets_remaining TINYINT UNSIGNED NOT NULL,
    is_losers      BOOLEAN          NOT NULL,
    FOREIGN KEY (tournament_id) REFERENCES tournaments(id)
        ON DELETE CASCADE,
    FOREIGN KEY (winner_id)     REFERENCES players(id),
    FOREIGN KEY (loser_id)      REFERENCES players(id)
);

CREATE TABLE ratings(
    id            INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    player_id     INT UNSIGNED NOT NULL,
    tournament_id INT UNSIGNED NOT NULL,
    set_id        INT UNSIGNED NOT NULL,
    rating        DOUBLE       NOT NULL,
    FOREIGN KEY (player_id)     REFERENCES players(id)     ON DELETE CASCADE,
    FOREIGN KEY (tournament_id) REFERENCES tournaments(id) ON DELETE CASCADE,
    FOREIGN KEY (set_id)        REFERENCES sets(id)        ON DELETE CASCADE
);
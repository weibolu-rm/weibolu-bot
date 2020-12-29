-- DROP TABLE IF EXISTS guilds;
-- DROP TABLE IF EXISTS members;
-- DROP TABLE IF EXISTS member_exp;


CREATE TABLE IF NOT EXISTS guilds (
    guild_id INTEGER PRIMARY KEY,
    name TEXT,
    prefix TEXT  DEFAULT "!",
    log_channel INTEGER,
    welcome_channel INTEGER,
    yoinker_id INTEGER,
    lvl_channel INTEGER,
    lvl_toggle INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS emojis (
    guild_id INTEGER,
    emoji_id INTEGER,
    usage INTEGER,
    FOREIGN KEY (guild_id) REFERENCES guilds (guild_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS members (
    member_id INTEGER,
    guild_id INTEGER,
    username TEXT,
    nickname TEXT,
    discriminator INTEGER,
    joined_date TEXT,
    PRIMARY KEY (guild_id, member_id),
    FOREIGN KEY (guild_id) REFERENCES guilds (guild_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS member_exp (
    member_id INTEGER,
    guild_id INTEGER,
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 0,
    xp_lock TEXT DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (guild_id, member_id),
    FOREIGN KEY (member_id) REFERENCES members (member_id) ON DELETE CASCADE,
    FOREIGN KEY (guild_id) REFERENCES guilds (guild_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS member_points (
    member_id INTEGER,
    guild_id INTEGER,
    points INTEGER DEFAULT 0,
    points_lock TEXT DEFAULT CURRENT_TIMESTAMP,
    daily_cooldown TEXT DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (guild_id, member_id),
    FOREIGN KEY (member_id) REFERENCES members (member_id) ON DELETE CASCADE,
    FOREIGN KEY (guild_id) REFERENCES guilds (guild_id) ON DELETE CASCADE
);
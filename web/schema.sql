-- devashaa accounts.
--
-- WHAT THIS DATABASE DELIBERATELY DOES NOT CONTAIN
-- ------------------------------------------------
-- No name, no email, no birth date, no birth time, no birth place. Not one
-- column here can be read to learn anything about a person. What it holds is:
--   * a self-chosen userid,
--   * a hash of a password verifier that is itself the output of 600 000
--     PBKDF2 iterations, and
--   * ciphertext this server has no key for.
--
-- The encryption key is derived on the client from the password and NEVER
-- transmitted, so the guarantee is architectural rather than a policy.

CREATE TABLE IF NOT EXISTS users (
  -- Normalised to lowercase before storage so 'Ravi' and 'ravi' cannot both be
  -- registered and then be confused for one another.
  userid       TEXT PRIMARY KEY,
  -- sha256(authId). authId is HKDF(master, "auth") and is already high-entropy,
  -- so one fast hash is the right choice: it means a database leak does not
  -- hand an attacker a directly replayable credential, while adding no useful
  -- work for an attacker who is guessing passwords (they must still pay the
  -- 600k PBKDF2 iterations per guess, and the userid salts it per account).
  auth_hash    TEXT NOT NULL,
  created_at   INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS profiles (
  userid       TEXT NOT NULL,
  -- HMAC(idKey, birth-signature) — an opaque, per-account, deterministic id.
  -- It MUST NOT be the birth signature itself: date|time|lat|lon in the clear
  -- would defeat the entire design, since a birth moment and place is close to
  -- a unique identifier on its own.
  profile_id   TEXT NOT NULL,
  blob         TEXT NOT NULL,      -- AES-GCM ciphertext of one profile
  updated_at   INTEGER NOT NULL,
  PRIMARY KEY (userid, profile_id),
  FOREIGN KEY (userid) REFERENCES users(userid) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS profiles_by_user ON profiles(userid);

-- Devashaa Pūjā (created by the Worker on first use — pooja-worker.js ensure()).
-- Unlike the chart store these are readable by design: a pandit's profile is
-- public, and a booking carries a name and a contact so the pandit can reach
-- the family (shown only to the assigned pandit and to admins).
CREATE TABLE IF NOT EXISTS pooja_roles (userid TEXT PRIMARY KEY, role TEXT NOT NULL, created_at INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS pooja_priests (
  userid TEXT PRIMARY KEY, name TEXT NOT NULL, city TEXT, country TEXT, languages TEXT, traditions TEXT,
  rituals TEXT, years INTEGER, bio TEXT, contact TEXT,
  status TEXT NOT NULL,            -- pending | approved | rejected
  vetted_by TEXT, created_at INTEGER NOT NULL, updated_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS pooja_bookings (
  id TEXT PRIMARY KEY,             -- 16 random bytes, hex; the id IS the family's key to the booking and the room
  ritual TEXT NOT NULL, starts_at TEXT NOT NULL, tz TEXT, priest TEXT,
  name TEXT NOT NULL, contact TEXT NOT NULL, city TEXT, family INTEGER, notes TEXT, lang TEXT,
  status TEXT NOT NULL,            -- requested | confirmed | completed | cancelled | self (a family gathering, no pandit)
  created_at INTEGER NOT NULL, updated_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS pooja_bookings_priest ON pooja_bookings(priest, status);

-- A chart shared by link: AES-GCM ciphertext made in the sender's browser;
-- the key lives only in the link's fragment. Created by the Worker on first
-- use (worker.js ensureShares) — kept here so the schema is in one place.
CREATE TABLE IF NOT EXISTS shares (
  id           TEXT PRIMARY KEY,   -- 16 random bytes, hex
  blob         TEXT NOT NULL,      -- "<iv>.<ciphertext>", base64url
  created_at   INTEGER NOT NULL
);

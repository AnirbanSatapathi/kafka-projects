CREATE TABLE events (
    event_id UUID PRIMARY KEY,
    user_id INT NOT NULL,
    event_type TEXT NOT NULL,
    page TEXT,
    event_time TIMESTAMP NOT NULL,
    received_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_events_user_id ON events(user_id);
CREATE INDEX idx_events_event_time ON events(event_time);
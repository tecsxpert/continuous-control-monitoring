CREATE TABLE control_items (
    id                  BIGINT AUTO_INCREMENT PRIMARY KEY,
    title               VARCHAR(255)    NOT NULL,
    description         TEXT,
    category            VARCHAR(100)    NOT NULL,
    status              VARCHAR(50)     NOT NULL DEFAULT 'PENDING',
    priority            VARCHAR(50)     NOT NULL DEFAULT 'MEDIUM',
    risk_score          INT             NOT NULL DEFAULT 0,
    owner               VARCHAR(150),
    due_date            DATE,
    last_reviewed_date  DATE,
    ai_description      TEXT,
    ai_recommendations  TEXT,
    is_deleted          BOOLEAN         NOT NULL DEFAULT FALSE,
    created_at          DATETIME(6)     NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at          DATETIME(6)     NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
                        ON UPDATE CURRENT_TIMESTAMP(6)
);

CREATE INDEX idx_control_status    ON control_items (status);
CREATE INDEX idx_control_category  ON control_items (category);
CREATE INDEX idx_control_priority  ON control_items (priority);
CREATE INDEX idx_control_due_date  ON control_items (due_date);
CREATE INDEX idx_control_owner     ON control_items (owner);
CREATE INDEX idx_control_deleted   ON control_items (is_deleted);
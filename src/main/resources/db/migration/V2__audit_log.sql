CREATE TABLE audit_log (
    id            BIGINT AUTO_INCREMENT PRIMARY KEY,
    entity_type   VARCHAR(100)  NOT NULL,
    entity_id     BIGINT        NOT NULL,
    action        VARCHAR(50)   NOT NULL,
    performed_by  VARCHAR(150),
    old_value     JSON,
    new_value     JSON,
    ip_address    VARCHAR(50),
    created_at    DATETIME(6)   NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
);

CREATE INDEX idx_audit_entity  ON audit_log (entity_type, entity_id);
CREATE INDEX idx_audit_user    ON audit_log (performed_by);
CREATE INDEX idx_audit_action  ON audit_log (action);
CREATE INDEX idx_audit_created ON audit_log (created_at);
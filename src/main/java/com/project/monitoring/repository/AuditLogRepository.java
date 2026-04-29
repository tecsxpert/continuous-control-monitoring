package com.project.monitoring.repository;

import com.project.monitoring.entity.AuditLog;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface AuditLogRepository extends JpaRepository<AuditLog, Long> {

    List<AuditLog> findByEntityTypeAndEntityIdOrderByCreatedAtDesc(
            String entityType, Long entityId);

    Page<AuditLog> findByPerformedByOrderByCreatedAtDesc(
            String performedBy, Pageable pageable);

    Page<AuditLog> findByActionOrderByCreatedAtDesc(
            String action, Pageable pageable);
}
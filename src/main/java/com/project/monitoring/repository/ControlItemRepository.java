package com.project.monitoring.repository;

import com.project.monitoring.entity.ControlItem;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Repository
public interface ControlItemRepository extends JpaRepository<ControlItem, Long> {

    Optional<ControlItem> findByIdAndIsDeletedFalse(Long id);

    Page<ControlItem> findAllByIsDeletedFalse(Pageable pageable);

    Page<ControlItem> findByStatusAndIsDeletedFalse(String status, Pageable pageable);

    List<ControlItem> findByStatusAndIsDeletedFalse(String status);

    Page<ControlItem> findByCategoryAndIsDeletedFalse(String category, Pageable pageable);

    Page<ControlItem> findByPriorityAndIsDeletedFalse(String priority, Pageable pageable);

    @Query("SELECT c FROM ControlItem c WHERE c.isDeleted = false " +
            "AND c.dueDate BETWEEN :start AND :end")
    List<ControlItem> findByDueDateBetween(@Param("start") LocalDate start,
                                           @Param("end") LocalDate end);

    @Query("SELECT c FROM ControlItem c WHERE c.isDeleted = false " +
            "AND c.dueDate < :today AND c.status NOT IN ('COMPLIANT')")
    List<ControlItem> findOverdueControls(@Param("today") LocalDate today);

    @Query("SELECT c FROM ControlItem c WHERE c.isDeleted = false " +
            "AND c.dueDate BETWEEN :today AND :alertDate " +
            "AND c.status NOT IN ('COMPLIANT')")
    List<ControlItem> findDueSoon(@Param("today") LocalDate today,
                                  @Param("alertDate") LocalDate alertDate);

    @Query("SELECT c FROM ControlItem c WHERE c.isDeleted = false AND (" +
            "LOWER(c.title) LIKE LOWER(CONCAT('%',:q,'%')) OR " +
            "LOWER(c.description) LIKE LOWER(CONCAT('%',:q,'%')) OR " +
            "LOWER(c.owner) LIKE LOWER(CONCAT('%',:q,'%')) OR " +
            "LOWER(c.category) LIKE LOWER(CONCAT('%',:q,'%')))")
    Page<ControlItem> search(@Param("q") String query, Pageable pageable);

    long countByIsDeletedFalse();
    long countByStatusAndIsDeletedFalse(String status);
    long countByPriorityAndIsDeletedFalse(String priority);

    @Query("SELECT c.category, COUNT(c) FROM ControlItem c " +
            "WHERE c.isDeleted = false GROUP BY c.category")
    List<Object[]> countByCategory();

    @Query("SELECT AVG(c.riskScore) FROM ControlItem c WHERE c.isDeleted = false")
    Double averageRiskScore();
}
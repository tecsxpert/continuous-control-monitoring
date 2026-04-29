package com.project.monitoring.service;

import com.project.monitoring.dto.ControlItemRequest;
import com.project.monitoring.dto.ControlItemResponse;
import com.project.monitoring.dto.StatsResponse;
import com.project.monitoring.entity.ControlItem;
import com.project.monitoring.exception.ResourceNotFoundException;
import com.project.monitoring.repository.ControlItemRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Slf4j
public class ControlItemService {

    private final ControlItemRepository repo;

    public Page<ControlItemResponse> getAll(Pageable pageable) {
        return repo.findAllByIsDeletedFalse(pageable).map(this::toResponse);
    }

    public ControlItemResponse getById(Long id) {
        return toResponse(findActive(id));
    }

    @Transactional
    public ControlItemResponse create(ControlItemRequest req) {
        ControlItem item = ControlItem.builder()
                .title(req.getTitle())
                .description(req.getDescription())
                .category(req.getCategory())
                .status(req.getStatus() != null ? req.getStatus() : "PENDING")
                .priority(req.getPriority() != null ? req.getPriority() : "MEDIUM")
                .riskScore(req.getRiskScore() != null ? req.getRiskScore() : 0)
                .owner(req.getOwner())
                .dueDate(req.getDueDate())
                .lastReviewedDate(req.getLastReviewedDate())
                .isDeleted(false)
                .build();
        return toResponse(repo.save(item));
    }

    @Transactional
    public ControlItemResponse update(Long id, ControlItemRequest req) {
        ControlItem item = findActive(id);
        if (req.getTitle()            != null) item.setTitle(req.getTitle());
        if (req.getDescription()      != null) item.setDescription(req.getDescription());
        if (req.getCategory()         != null) item.setCategory(req.getCategory());
        if (req.getStatus()           != null) item.setStatus(req.getStatus());
        if (req.getPriority()         != null) item.setPriority(req.getPriority());
        if (req.getRiskScore()        != null) item.setRiskScore(req.getRiskScore());
        if (req.getOwner()            != null) item.setOwner(req.getOwner());
        if (req.getDueDate()          != null) item.setDueDate(req.getDueDate());
        if (req.getLastReviewedDate() != null) item.setLastReviewedDate(req.getLastReviewedDate());
        return toResponse(repo.save(item));
    }

    @Transactional
    public void softDelete(Long id) {
        ControlItem item = findActive(id);
        item.setIsDeleted(true);
        repo.save(item);
        log.info("Control item {} soft-deleted", id);
    }

    public Page<ControlItemResponse> search(String query, Pageable pageable) {
        return repo.search(query, pageable).map(this::toResponse);
    }

    public StatsResponse getStats() {
        Map<String, Long> byCategory = new LinkedHashMap<>();
        repo.countByCategory().forEach(row -> byCategory.put((String) row[0], (Long) row[1]));
        return StatsResponse.builder()
                .totalControls(repo.countByIsDeletedFalse())
                .pendingCount(repo.countByStatusAndIsDeletedFalse("PENDING"))
                .inProgressCount(repo.countByStatusAndIsDeletedFalse("IN_PROGRESS"))
                .compliantCount(repo.countByStatusAndIsDeletedFalse("COMPLIANT"))
                .nonCompliantCount(repo.countByStatusAndIsDeletedFalse("NON_COMPLIANT"))
                .overdueCount(repo.countByStatusAndIsDeletedFalse("OVERDUE"))
                .criticalCount(repo.countByPriorityAndIsDeletedFalse("CRITICAL"))
                .highCount(repo.countByPriorityAndIsDeletedFalse("HIGH"))
                .averageRiskScore(repo.averageRiskScore())
                .byCategory(byCategory)
                .build();
    }

    public byte[] exportCsv() {
        List<ControlItem> all = repo.findAllByIsDeletedFalse(Pageable.unpaged()).getContent();
        StringBuilder sb = new StringBuilder();
        sb.append("ID,Title,Category,Status,Priority,RiskScore,Owner,DueDate,CreatedAt\n");
        for (ControlItem c : all) {
            sb.append(c.getId()).append(",")
                    .append(escape(c.getTitle())).append(",")
                    .append(escape(c.getCategory())).append(",")
                    .append(c.getStatus()).append(",")
                    .append(c.getPriority()).append(",")
                    .append(c.getRiskScore()).append(",")
                    .append(escape(c.getOwner())).append(",")
                    .append(c.getDueDate() != null ? c.getDueDate() : "").append(",")
                    .append(c.getCreatedAt()).append("\n");
        }
        return sb.toString().getBytes();
    }

    private ControlItem findActive(Long id) {
        return repo.findByIdAndIsDeletedFalse(id)
                .orElseThrow(() -> new ResourceNotFoundException("ControlItem", id));
    }

    private ControlItemResponse toResponse(ControlItem c) {
        return ControlItemResponse.builder()
                .id(c.getId())
                .title(c.getTitle())
                .description(c.getDescription())
                .category(c.getCategory())
                .status(c.getStatus())
                .priority(c.getPriority())
                .riskScore(c.getRiskScore())
                .owner(c.getOwner())
                .dueDate(c.getDueDate())
                .lastReviewedDate(c.getLastReviewedDate())
                .aiDescription(c.getAiDescription())
                .aiRecommendations(c.getAiRecommendations())
                .createdAt(c.getCreatedAt())
                .updatedAt(c.getUpdatedAt())
                .build();
    }

    private String escape(String val) {
        if (val == null) return "";
        if (val.contains(",") || val.contains("\"")) {
            return "\"" + val.replace("\"", "\"\"") + "\"";
        }
        return val;
    }
}
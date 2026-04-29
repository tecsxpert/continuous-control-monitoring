package com.project.monitoring.dto;

import lombok.Builder;
import lombok.Data;
import java.util.Map;

@Data
@Builder
public class StatsResponse {
    private long totalControls;
    private long pendingCount;
    private long inProgressCount;
    private long compliantCount;
    private long nonCompliantCount;
    private long overdueCount;
    private long criticalCount;
    private long highCount;
    private Double averageRiskScore;
    private Map<String, Long> byCategory;
}
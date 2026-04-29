package com.project.monitoring.dto;

import lombok.Builder;
import lombok.Data;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@Builder
public class ControlItemResponse {
    private Long id;
    private String title;
    private String description;
    private String category;
    private String status;
    private String priority;
    private Integer riskScore;
    private String owner;
    private LocalDate dueDate;
    private LocalDate lastReviewedDate;
    private String aiDescription;
    private String aiRecommendations;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
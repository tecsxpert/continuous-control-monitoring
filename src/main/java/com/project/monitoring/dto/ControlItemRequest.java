package com.project.monitoring.dto;

import lombok.Data;
import java.time.LocalDate;

@Data
public class ControlItemRequest {
    private String title;
    private String description;
    private String category;
    private String status;
    private String priority;
    private Integer riskScore;
    private String owner;
    private LocalDate dueDate;
    private LocalDate lastReviewedDate;
}
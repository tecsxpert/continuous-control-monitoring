package com.project.monitoring.configuration;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.project.monitoring.entity.AuditLog;
import com.project.monitoring.repository.AuditLogRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

@Aspect
@Component
@RequiredArgsConstructor
@Slf4j
public class AuditAspect {

    private final AuditLogRepository auditLogRepo;
    private final ObjectMapper       objectMapper;

    @Around("execution(* com.project.monitoring.service.ControlItemService.create(..))   || " +
            "execution(* com.project.monitoring.service.ControlItemService.update(..))   || " +
            "execution(* com.project.monitoring.service.ControlItemService.softDelete(..))")
    public Object auditControlOperation(ProceedingJoinPoint pjp) throws Throwable {

        String methodName = pjp.getSignature().getName();
        Object[] args     = pjp.getArgs();

        String action = switch (methodName) {
            case "create"     -> "CREATE";
            case "update"     -> "UPDATE";
            case "softDelete" -> "DELETE";
            default           -> methodName.toUpperCase();
        };

        String oldJson = null;
        if (("UPDATE".equals(action) || "DELETE".equals(action)) && args.length > 0) {
            try {
                oldJson = objectMapper.writeValueAsString(args[0]);
            } catch (Exception ignored) {}
        }

        Object result = pjp.proceed();

        String newJson = null;
        if (result != null) {
            try {
                newJson = objectMapper.writeValueAsString(result);
            } catch (Exception ignored) {}
        }

        Long entityId = null;
        if (args.length > 0 && args[0] instanceof Long l) {
            entityId = l;
        } else if (result != null) {
            try {
                var node = objectMapper.valueToTree(result);
                if (node.has("id")) entityId = node.get("id").asLong();
            } catch (Exception ignored) {}
        }

        try {
            AuditLog auditLog = AuditLog.builder()
                    .entityType("ControlItem")
                    .entityId(entityId)
                    .action(action)
                    .performedBy(currentUser())
                    .oldValue(oldJson)
                    .newValue(newJson)
                    .build();
            auditLogRepo.save(auditLog);
        } catch (Exception e) {
            log.error("Failed to save audit log: {}", e.getMessage());
        }

        return result;
    }

    private String currentUser() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        return (auth != null) ? auth.getName() : "system";
    }
}
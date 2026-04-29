package com.project.monitoring.scheduler;

import com.project.monitoring.entity.ControlItem;
import com.project.monitoring.repository.ControlItemRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.thymeleaf.TemplateEngine;
import org.thymeleaf.context.Context;
import jakarta.mail.internet.MimeMessage;
import java.time.LocalDate;
import java.util.List;

@Component
@RequiredArgsConstructor
@Slf4j
public class ControlScheduler {

    private final ControlItemRepository repo;
    private final JavaMailSender         mailSender;
    private final TemplateEngine         templateEngine;

    @Scheduled(cron = "0 0 8 * * *")
    public void markAndNotifyOverdueControls() {
        log.info("[Scheduler] Running overdue controls check...");
        LocalDate today = LocalDate.now();
        List<ControlItem> overdue = repo.findOverdueControls(today);

        for (ControlItem item : overdue) {
            if (!"OVERDUE".equals(item.getStatus())) {
                item.setStatus("OVERDUE");
                repo.save(item);
                log.info("[Scheduler] Marked control {} as OVERDUE", item.getId());
            }
            if (item.getOwner() != null && item.getOwner().contains("@")) {
                sendOverdueEmail(item);
            }
        }
        log.info("[Scheduler] Overdue check complete — {} items processed", overdue.size());
    }

    @Scheduled(cron = "0 30 8 * * *")
    public void sendDueSoonAlerts() {
        log.info("[Scheduler] Running 7-day advance due alert...");
        LocalDate today     = LocalDate.now();
        LocalDate alertDate = today.plusDays(7);
        List<ControlItem> dueSoon = repo.findDueSoon(today, alertDate);

        for (ControlItem item : dueSoon) {
            if (item.getOwner() != null && item.getOwner().contains("@")) {
                sendDueSoonEmail(item);
            }
        }
        log.info("[Scheduler] Due-soon alerts sent for {} items", dueSoon.size());
    }

    @Scheduled(cron = "0 0 9 * * MON")
    public void sendWeeklySummary() {
        log.info("[Scheduler] Generating weekly compliance summary...");
        long total        = repo.countByIsDeletedFalse();
        long compliant    = repo.countByStatusAndIsDeletedFalse("COMPLIANT");
        long nonCompliant = repo.countByStatusAndIsDeletedFalse("NON_COMPLIANT");
        long overdue      = repo.countByStatusAndIsDeletedFalse("OVERDUE");
        log.info("[Scheduler] Weekly summary — Total: {}, Compliant: {}, Non-Compliant: {}, Overdue: {}",
                total, compliant, nonCompliant, overdue);
        sendWeeklySummaryEmail(total, compliant, nonCompliant, overdue);
    }

    private void sendOverdueEmail(ControlItem item) {
        try {
            Context ctx = new Context();
            ctx.setVariable("item", item);
            String html = templateEngine.process("overdue-notification", ctx);
            sendHtmlEmail(item.getOwner(), "⚠️ Control Overdue: " + item.getTitle(), html);
        } catch (Exception e) {
            log.error("Failed to send overdue email for control {}: {}", item.getId(), e.getMessage());
        }
    }

    private void sendDueSoonEmail(ControlItem item) {
        try {
            Context ctx = new Context();
            ctx.setVariable("item", item);
            String html = templateEngine.process("due-soon-notification", ctx);
            sendHtmlEmail(item.getOwner(), "📅 Control Due Soon: " + item.getTitle(), html);
        } catch (Exception e) {
            log.error("Failed to send due-soon email for control {}: {}", item.getId(), e.getMessage());
        }
    }

    private void sendWeeklySummaryEmail(long total, long compliant,
                                        long nonCompliant, long overdue) {
        try {
            Context ctx = new Context();
            ctx.setVariable("total",        total);
            ctx.setVariable("compliant",    compliant);
            ctx.setVariable("nonCompliant", nonCompliant);
            ctx.setVariable("overdue",      overdue);
            String html = templateEngine.process("weekly-summary", ctx);
            sendHtmlEmail("admin@monitoring.com", "📊 Weekly Compliance Summary", html);
        } catch (Exception e) {
            log.error("Failed to send weekly summary email: {}", e.getMessage());
        }
    }

    private void sendHtmlEmail(String to, String subject, String htmlBody) {
        try {
            MimeMessage msg = mailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(msg, true, "UTF-8");
            helper.setTo(to);
            helper.setSubject(subject);
            helper.setText(htmlBody, true);
            mailSender.send(msg);
            log.debug("Email sent to {} — subject: {}", to, subject);
        } catch (Exception e) {
            log.error("Failed to send email to {}: {}", to, e.getMessage());
        }
    }
}
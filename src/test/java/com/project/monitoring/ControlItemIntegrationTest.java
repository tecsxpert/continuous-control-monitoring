package com.project.monitoring;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.project.monitoring.dto.AuthDto;
import com.project.monitoring.dto.ControlItemRequest;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import java.time.LocalDate;
import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class ControlItemIntegrationTest {

    @Autowired MockMvc mvc;
    @Autowired ObjectMapper mapper;

    private static String adminToken;
    private static Long   createdId;

    @Test @Order(1)
    void loginReturnsJwt() throws Exception {
        AuthDto.LoginRequest req = new AuthDto.LoginRequest();
        req.setUsername("admin");
        req.setPassword("Admin@1234");

        MvcResult result = mvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(mapper.writeValueAsString(req)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.accessToken").isNotEmpty())
                .andReturn();

        adminToken = mapper.readTree(
                        result.getResponse().getContentAsString())
                .get("accessToken").asText();
    }

    @Test @Order(2)
    void noTokenReturns401() throws Exception {
        mvc.perform(get("/api/controls"))
                .andExpect(status().isUnauthorized());
    }

    @Test @Order(3)
    void registerNewUser() throws Exception {
        AuthDto.RegisterRequest req = new AuthDto.RegisterRequest();
        req.setUsername("testviewer");
        req.setEmail("testviewer@monitoring.com");
        req.setPassword("Test@1234");
        req.setFullName("Test Viewer");

        mvc.perform(post("/api/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(mapper.writeValueAsString(req)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.roles", hasItem("VIEWER")));
    }

    @Test @Order(4)
    void createControlItem() throws Exception {
        ControlItemRequest req = new ControlItemRequest();
        req.setTitle("Access Control Review");
        req.setDescription("Review all user access permissions");
        req.setCategory("Access Management");
        req.setStatus("PENDING");
        req.setPriority("HIGH");
        req.setRiskScore(75);
        req.setOwner("security@monitoring.com");
        req.setDueDate(LocalDate.now().plusDays(30));

        MvcResult result = mvc.perform(post("/api/controls")
                        .header("Authorization", "Bearer " + adminToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(mapper.writeValueAsString(req)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").isNumber())
                .andExpect(jsonPath("$.title").value("Access Control Review"))
                .andReturn();

        createdId = mapper.readTree(
                        result.getResponse().getContentAsString())
                .get("id").asLong();
    }

    @Test @Order(5)
    void getAllControlsPaginated() throws Exception {
        mvc.perform(get("/api/controls?page=0&size=10")
                        .header("Authorization", "Bearer " + adminToken))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray())
                .andExpect(jsonPath("$.totalElements").isNumber());
    }

    @Test @Order(6)
    void getControlById() throws Exception {
        mvc.perform(get("/api/controls/" + createdId)
                        .header("Authorization", "Bearer " + adminToken))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(createdId));
    }

    @Test @Order(7)
    void getNonExistentReturns404() throws Exception {
        mvc.perform(get("/api/controls/999999")
                        .header("Authorization", "Bearer " + adminToken))
                .andExpect(status().isNotFound());
    }

    @Test @Order(8)
    void updateControl() throws Exception {
        ControlItemRequest req = new ControlItemRequest();
        req.setStatus("IN_PROGRESS");
        req.setRiskScore(60);

        mvc.perform(put("/api/controls/" + createdId)
                        .header("Authorization", "Bearer " + adminToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(mapper.writeValueAsString(req)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("IN_PROGRESS"));
    }

    @Test @Order(9)
    void searchControls() throws Exception {
        mvc.perform(get("/api/controls/search?q=Access&page=0&size=10")
                        .header("Authorization", "Bearer " + adminToken))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray());
    }

    @Test @Order(10)
    void getStats() throws Exception {
        mvc.perform(get("/api/controls/stats")
                        .header("Authorization", "Bearer " + adminToken))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.totalControls").isNumber());
    }

    @Test @Order(11)
    void softDeleteControl() throws Exception {
        mvc.perform(delete("/api/controls/" + createdId)
                        .header("Authorization", "Bearer " + adminToken))
                .andExpect(status().isNoContent());

        mvc.perform(get("/api/controls/" + createdId)
                        .header("Authorization", "Bearer " + adminToken))
                .andExpect(status().isNotFound());
    }

    @Test @Order(12)
    void exportCsv() throws Exception {
        mvc.perform(get("/api/controls/export")
                        .header("Authorization", "Bearer " + adminToken))
                .andExpect(status().isOk())
                .andExpect(header().string("Content-Disposition",
                        containsString("controls.csv")));
    }
}
# 🔐 SECURITY.md — Continuous Control Monitoring System

**MVP Project | Sprint: Capstone 2026**  
**Security Reviewer:** R Rashmi  

---



## 👥 Team Sign-off

| Role | Name | Sign-off |
|---|---|---|
| Java Developer 1 | Khathija Afreena | Java Developer 1 |
| Java Developer 2 | H.U Varsha | Java Developer 2 |
| Java Developer 3 | Chandana CS | Java Developer 3 |
| AI Developer 1 | Karthik Hugar | AI Developer 1 |
| AI Developer 2 | Shashank S | AI Developer 2|
| AI Developer 3 | Swaroop Patil | AI Developer 3|
| Security Reviewer | R Rashmi | Security Reviewer |
---

## 1. Threat Model

| # | Threat | Risk Level | Mitigation Implemented |
|---|---|---|---|
| 1 | SQL Injection | HIGH | Spring Boot + JPA/Hibernate prevents raw SQL queries |
| 2 | Broken Authentication | HIGH | JWT-based authentication implemented |
| 3 | Unauthorized Access | HIGH | RBAC enforced via Spring Security |
| 4 | Default Credentials | HIGH | ⚠️ Found active (admin/admin) |
| 5 | XSS Attack | MEDIUM | React escapes output (no execution observed) |
| 6 | Data Exposure | HIGH | Export & stats APIs protected by authorization |
| 7 | Invalid Input Handling | MEDIUM | Backend validation applied |

---

## 2. Security Architecture

```
Browser (React - Vite)
    │
    ▼
Spring Boot Backend (Port 8081)
    │  JWT Authentication
    ▼
H2 Database (In-memory)
```

### Public Endpoints
- /api/auth/register  
- /api/auth/login  

### Protected Endpoints
- /api/controls/**  
- /api/controls/export  
- /api/controls/stats  

---

## 3. Security Tests Conducted

### 3.1 Authentication Tests

| Test | Expected | Result |
|---|---|---|
| Login with invalid credentials | Access denied | ✅ PASS |
| Login with default credentials (admin/admin) | Should fail | ❌ FAIL |
| Access API without token | 401/403 | ✅ PASS |

---

### 3.2 JWT Validation Tests

| Test | Expected | Result |
|---|---|---|
| Invalid token | 403 Forbidden | ✅ PASS |
| Missing token | 401 Unauthorized | ✅ PASS |

---

### 3.3 Authorization (RBAC)

| Test | Expected | Result |
|---|---|---|
| VIEWER accessing protected APIs | Access denied | ✅ PASS |
| Admin access to APIs | Allowed | ✅ PASS |

---

### 3.4 Input Validation Tests

| Test | Expected | Result |
|---|---|---|
| Invalid data type | Validation error | ✅ PASS |
| Empty fields | Rejected | ✅ PASS |
| Out-of-range values | Rejected | ✅ PASS |

---

### 3.5 SQL Injection Tests

| Test | Payload | Result |
|---|---|---|
| Login injection | ' OR 1=1 -- | ✅ PASS |
| Search injection | ' OR 1=1 -- | ✅ PASS |

---

### 3.6 XSS Testing (Frontend + Backend)

| Test | Payload | Result |
|---|---|---|
| Input field (Add Control) | `<script>alert("XSS")</script>` | Stored but not executed |
| Image-based XSS | `<img src=x onerror=alert(1)>` | Stored but not executed |

**Observation:**
- Input is stored in database  
- No script execution in UI  

---

### 3.7 Data Exposure Tests

| Test | Expected | Result |
|---|---|---|
| Export API (VIEWER) | Blocked | ✅ PASS |
| Stats API (VIEWER) | Blocked | ✅ PASS |

---

## 4. Findings & Status

| ID | Finding | Severity | Status |
|---|---|---|---|
| F-01 | Default credentials active | HIGH | ❌ OPEN |
| F-02 | XSS payload stored (not executed) | MEDIUM | ⚠️ MONITOR |
| F-03 | No SQL Injection vulnerability | LOW | ✅ SAFE |
| F-04 | Strong RBAC enforcement | LOW | ✅ SAFE |

---

## 5. Residual Risks

| Risk | Detail | Plan |
|---|---|---|
| Default credentials misuse | Unauthorized access possible | Remove before deployment |
| Stored XSS risk | Payload stored in DB | Sanitize inputs |
| Token exposure | JWT usage risk | Use secure storage |

---

## 6. Security Checklist

- [x] Authentication implemented  
- [x] JWT validation enforced  
- [x] RBAC properly configured  
- [x] Input validation applied  
- [x] SQL Injection prevented  
- [x] Data exposure restricted  
- [ ] Default credentials removed ❗  
- [ ] Input sanitization implemented ❗  

---

## 7. Tools & Methods Used

| Tool / Method | Purpose |
|---|---|
| Swagger UI | API testing |
| Frontend UI | Real-world testing |
| Manual payload testing | XSS & SQL injection |
| Browser DevTools | Response analysis |

---

## 8. Final Assessment

The system demonstrates strong backend security controls:

- Authentication & Authorization  
- Role-Based Access Control  
- SQL Injection protection  
- Data exposure prevention  

However:

- 🔴 Default credentials allow unauthorized access  
- 🟡 Stored XSS due to unsanitized input  

---

## 🛡️ Overall Security Status

⚠️ **SECURE WITH MODERATE RISK — REQUIRES FIXES BEFORE PRODUCTION**

---

## 👩‍💻 Reviewer

R Rashmi
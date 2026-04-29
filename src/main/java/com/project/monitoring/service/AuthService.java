package com.project.monitoring.service;

import com.project.monitoring.configuration.JwtUtil;
import com.project.monitoring.dto.AuthDto;
import com.project.monitoring.entity.Role;
import com.project.monitoring.entity.User;
import com.project.monitoring.exception.ResourceNotFoundException;
import com.project.monitoring.repository.RoleRepository;
import com.project.monitoring.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository    userRepo;
    private final RoleRepository    roleRepo;
    private final PasswordEncoder   passwordEncoder;
    private final JwtUtil           jwtUtil;

    public AuthDto.AuthResponse login(AuthDto.LoginRequest req) {
        User user = userRepo.findByUsername(req.getUsername())
                .orElseThrow(() -> new BadCredentialsException("Invalid credentials"));

        if (!passwordEncoder.matches(req.getPassword(), user.getPassword())) {
            throw new BadCredentialsException("Invalid credentials");
        }
        if (!user.getIsActive()) {
            throw new BadCredentialsException("Account is disabled");
        }

        List<String> roles = getRoleNames(user);
        return AuthDto.AuthResponse.builder()
                .accessToken(jwtUtil.generateAccessToken(user.getUsername(), roles))
                .refreshToken(jwtUtil.generateRefreshToken(user.getUsername()))
                .username(user.getUsername())
                .email(user.getEmail())
                .roles(roles)
                .build();
    }

    @Transactional
    public AuthDto.AuthResponse register(AuthDto.RegisterRequest req) {
        if (userRepo.existsByUsername(req.getUsername())) {
            throw new IllegalArgumentException("Username already taken");
        }
        if (userRepo.existsByEmail(req.getEmail())) {
            throw new IllegalArgumentException("Email already registered");
        }

        Role viewerRole = roleRepo.findByName("VIEWER")
                .orElseThrow(() -> new ResourceNotFoundException("Role", "VIEWER"));

        User user = User.builder()
                .username(req.getUsername())
                .email(req.getEmail())
                .password(passwordEncoder.encode(req.getPassword()))
                .fullName(req.getFullName())
                .isActive(true)
                .roles(Set.of(viewerRole))
                .build();

        userRepo.save(user);

        List<String> roles = getRoleNames(user);
        return AuthDto.AuthResponse.builder()
                .accessToken(jwtUtil.generateAccessToken(user.getUsername(), roles))
                .refreshToken(jwtUtil.generateRefreshToken(user.getUsername()))
                .username(user.getUsername())
                .email(user.getEmail())
                .roles(roles)
                .build();
    }

    public AuthDto.AuthResponse refresh(AuthDto.RefreshRequest req) {
        String username = jwtUtil.extractUsername(req.getRefreshToken());
        if (!jwtUtil.validateToken(req.getRefreshToken(), username)) {
            throw new BadCredentialsException("Invalid or expired refresh token");
        }

        User user = userRepo.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User", username));

        List<String> roles = getRoleNames(user);
        return AuthDto.AuthResponse.builder()
                .accessToken(jwtUtil.generateAccessToken(username, roles))
                .refreshToken(jwtUtil.generateRefreshToken(username))
                .username(user.getUsername())
                .email(user.getEmail())
                .roles(roles)
                .build();
    }

    private List<String> getRoleNames(User user) {
        return user.getRoles().stream()
                .map(Role::getName)
                .collect(Collectors.toList());
    }
}
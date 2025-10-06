
# Network Standards (2025)

## Overview

This document defines network standards for AI/ML, LLM, and agentic systems, supporting interoperability, security, and compliance.

---

## 1. Addressing & Naming
- Use clear, consistent naming for all network resources
- Apply environment and agent tags to all resources
- Document all network segments and endpoints

## 2. Protocols & Encryption
- Use HTTPS/TLS 1.3+ for all external and internal traffic
- Prefer gRPC or HTTP/2 for agent-to-agent communication
- Encrypt all sensitive data in transit

## 3. Topology & Segmentation
- Segment networks by environment (dev, test, prod) and workload (LLM, vector DB, API)
- Use private subnets for sensitive workloads
- Document all peering and VPN connections

## 4. Monitoring & Compliance
- Monitor all network traffic and access
- Retain logs for compliance (POPIA, GDPR)
- Regularly review and update network documentation

---

## References
- See `network_security_policy.md`, `cloud_resource_tagging_policy.md`, and `architectural-principles.md` for more details.

Last updated: 2025-10-01

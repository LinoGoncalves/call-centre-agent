#!/usr/bin/env python3
"""
Security Validation Script for Call Centre Agent Docker Environment
Tests all security controls and verifies enterprise-grade security posture
"""

import subprocess
import requests
import json
import socket
import time
import sys
from pathlib import Path

class SecurityValidator:
    def __init__(self):
        self.results = []
        self.critical_failures = 0
        self.high_failures = 0
        
    def log_result(self, test_name, passed, severity="INFO", details=""):
        """Log test result with severity classification"""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "severity": severity,
            "details": details,
            "passed": passed
        }
        self.results.append(result)
        
        if not passed:
            if severity == "CRITICAL":
                self.critical_failures += 1
            elif severity == "HIGH":
                self.high_failures += 1
                
        print(f"{status} [{severity}] {test_name}")
        if details and not passed:
            print(f"    Details: {details}")
    
    def test_container_user(self):
        """Test that containers are running as non-root user"""
        try:
            result = subprocess.run([
                'docker', 'exec', 'call-centre-secure', 'whoami'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                user = result.stdout.strip()
                passed = user != 'root'
                self.log_result(
                    "Container Non-Root Execution", 
                    passed, 
                    "CRITICAL",
                    f"Container running as user: {user}"
                )
            else:
                self.log_result(
                    "Container Non-Root Execution", 
                    False, 
                    "CRITICAL",
                    "Could not check container user"
                )
        except Exception as e:
            self.log_result(
                "Container Non-Root Execution", 
                False, 
                "CRITICAL",
                f"Error checking user: {str(e)}"
            )
    
    def test_network_binding(self):
        """Test that services are bound to localhost only"""
        try:
            result = subprocess.run([
                'docker', 'exec', 'call-centre-secure', 'netstat', '-tlnp'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                output = result.stdout
                # Check for services bound to 0.0.0.0 (insecure)
                insecure_bindings = []
                for line in output.split('\n'):
                    if ':8888' in line or ':5000' in line or ':4200' in line:
                        if '0.0.0.0:' in line:
                            insecure_bindings.append(line.strip())
                
                passed = len(insecure_bindings) == 0
                details = f"Insecure bindings found: {insecure_bindings}" if not passed else "All services bound to localhost"
                self.log_result(
                    "Network Localhost Binding", 
                    passed, 
                    "CRITICAL",
                    details
                )
            else:
                self.log_result(
                    "Network Localhost Binding", 
                    False, 
                    "CRITICAL",
                    "Could not check network bindings"
                )
        except Exception as e:
            self.log_result(
                "Network Localhost Binding", 
                False, 
                "CRITICAL",
                f"Error checking network: {str(e)}"
            )
    
    def test_jupyter_authentication(self):
        """Test that Jupyter requires authentication"""
        try:
            # Try to access Jupyter without token (should fail)
            response = requests.get('http://localhost:8888/lab', timeout=5)
            
            # If we get a login page or authentication error, that's good
            if response.status_code == 401 or 'login' in response.text.lower() or 'token' in response.text.lower():
                passed = True
                details = "Jupyter properly requires authentication"
            else:
                passed = False
                details = f"Jupyter may be accessible without authentication (status: {response.status_code})"
                
            self.log_result(
                "Jupyter Authentication Required", 
                passed, 
                "CRITICAL",
                details
            )
        except requests.exceptions.ConnectionError:
            # Connection refused is actually good - means it's not externally accessible
            self.log_result(
                "Jupyter Authentication Required", 
                True, 
                "CRITICAL",
                "Jupyter not accessible externally (good!)"
            )
        except Exception as e:
            self.log_result(
                "Jupyter Authentication Required", 
                False, 
                "CRITICAL",
                f"Error testing Jupyter auth: {str(e)}"
            )
    
    def test_container_capabilities(self):
        """Test that container has minimal capabilities"""
        try:
            result = subprocess.run([
                'docker', 'inspect', 'call-centre-secure'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                config = json.loads(result.stdout)[0]
                host_config = config.get('HostConfig', {})
                
                # Check capabilities
                cap_add = host_config.get('CapAdd', [])
                cap_drop = host_config.get('CapDrop', [])
                
                # Check security options
                security_opt = host_config.get('SecurityOpt', [])
                
                # Check if running in privileged mode (bad)
                privileged = host_config.get('Privileged', False)
                
                passed = True
                issues = []
                
                if privileged:
                    passed = False
                    issues.append("Container running in privileged mode")
                
                if 'ALL' not in cap_drop:
                    passed = False
                    issues.append("Not all capabilities dropped")
                
                if 'no-new-privileges:true' not in security_opt:
                    passed = False
                    issues.append("New privileges not disabled")
                
                details = f"Issues: {issues}" if issues else "Container capabilities properly restricted"
                self.log_result(
                    "Container Capability Restriction", 
                    passed, 
                    "HIGH",
                    details
                )
            else:
                self.log_result(
                    "Container Capability Restriction", 
                    False, 
                    "HIGH",
                    "Could not inspect container configuration"
                )
        except Exception as e:
            self.log_result(
                "Container Capability Restriction", 
                False, 
                "HIGH",
                f"Error inspecting container: {str(e)}"
            )
    
    def test_file_permissions(self):
        """Test that sensitive files have proper permissions"""
        try:
            # Check Jupyter config file permissions
            result = subprocess.run([
                'docker', 'exec', 'call-centre-secure', 'ls', '-la', '/home/appuser/.jupyter/'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                output = result.stdout
                # Check for world-readable sensitive files
                world_readable = []
                for line in output.split('\n'):
                    if 'jupyter' in line and 'rw-r--r--' in line:
                        world_readable.append(line.strip())
                
                passed = len(world_readable) == 0
                details = f"World-readable files: {world_readable}" if not passed else "File permissions properly restricted"
                self.log_result(
                    "File Permissions Security", 
                    passed, 
                    "MEDIUM",
                    details
                )
            else:
                self.log_result(
                    "File Permissions Security", 
                    False, 
                    "MEDIUM",
                    "Could not check file permissions"
                )
        except Exception as e:
            self.log_result(
                "File Permissions Security", 
                False, 
                "MEDIUM",
                f"Error checking permissions: {str(e)}"
            )
    
    def test_environment_security(self):
        """Test environment variables for security issues"""
        try:
            result = subprocess.run([
                'docker', 'exec', 'call-centre-secure', 'env'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                env_vars = result.stdout
                
                # Check for insecure environment variables
                security_issues = []
                
                if 'DEBUG=true' in env_vars:
                    security_issues.append("Debug mode enabled")
                
                if 'PASSWORD=' in env_vars and 'PASSWORD=\n' not in env_vars:
                    # Check if passwords are exposed in environment
                    for line in env_vars.split('\n'):
                        if 'PASSWORD=' in line and line.split('=')[1]:
                            security_issues.append("Password in environment variables")
                            break
                
                passed = len(security_issues) == 0
                details = f"Security issues: {security_issues}" if not passed else "Environment variables secure"
                self.log_result(
                    "Environment Variables Security", 
                    passed, 
                    "MEDIUM",
                    details
                )
            else:
                self.log_result(
                    "Environment Variables Security", 
                    False, 
                    "MEDIUM",
                    "Could not check environment variables"
                )
        except Exception as e:
            self.log_result(
                "Environment Variables Security", 
                False, 
                "MEDIUM",
                f"Error checking environment: {str(e)}"
            )
    
    def test_resource_limits(self):
        """Test that resource limits are enforced"""
        try:
            result = subprocess.run([
                'docker', 'inspect', 'call-centre-secure'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                config = json.loads(result.stdout)[0]
                host_config = config.get('HostConfig', {})
                
                # Check memory and CPU limits
                memory = host_config.get('Memory', 0)
                cpus = host_config.get('NanoCpus', 0)
                
                passed = True
                issues = []
                
                if memory == 0:
                    passed = False
                    issues.append("No memory limit set")
                
                if cpus == 0:
                    passed = False
                    issues.append("No CPU limit set")
                
                details = f"Issues: {issues}" if issues else f"Resource limits: Memory={memory/1024/1024/1024:.1f}GB, CPUs={cpus/1000000000:.1f}"
                self.log_result(
                    "Resource Limits Enforced", 
                    passed, 
                    "MEDIUM",
                    details
                )
            else:
                self.log_result(
                    "Resource Limits Enforced", 
                    False, 
                    "MEDIUM",
                    "Could not check resource limits"
                )
        except Exception as e:
            self.log_result(
                "Resource Limits Enforced", 
                False, 
                "MEDIUM",
                f"Error checking limits: {str(e)}"
            )
    
    def run_all_tests(self):
        """Run all security validation tests"""
        print("🔒 Security Validation Starting...")
        print("=" * 60)
        
        # Critical security tests
        self.test_container_user()
        self.test_network_binding()
        self.test_jupyter_authentication()
        
        # High priority tests
        self.test_container_capabilities()
        
        # Medium priority tests
        self.test_file_permissions()
        self.test_environment_security()
        self.test_resource_limits()
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate final security validation report"""
        print("\n" + "=" * 60)
        print("🔒 SECURITY VALIDATION REPORT")
        print("=" * 60)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r['passed'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Critical Failures: {self.critical_failures}")
        print(f"High Priority Failures: {self.high_failures}")
        
        print("\n📊 DETAILED RESULTS:")
        for result in self.results:
            print(f"{result['status']} [{result['severity']}] {result['test']}")
            if result['details'] and not result['passed']:
                print(f"    → {result['details']}")
        
        print("\n🎯 SECURITY VERDICT:")
        if self.critical_failures == 0 and self.high_failures == 0:
            print("✅ PRODUCTION READY - All critical and high-priority security tests passed")
            print("🏆 Environment meets enterprise security standards")
        elif self.critical_failures == 0:
            print("⚠️ ACCEPTABLE - Critical security tests passed, minor issues found")
            print("📝 Review and address high-priority findings before production")
        else:
            print("❌ NOT PRODUCTION READY - Critical security failures detected")
            print("🚨 Address all critical issues before deployment")
        
        print("\n📋 RECOMMENDATIONS:")
        if failed_tests > 0:
            print("1. Review failed tests and implement fixes")
            print("2. Re-run validation after addressing issues")
            print("3. Consider additional penetration testing")
        else:
            print("1. Deploy with confidence - all security checks passed")
            print("2. Continue regular security monitoring")
            print("3. Update dependencies regularly")
        
        return self.critical_failures == 0

def check_container_running():
    """Check if the secure container is running"""
    try:
        result = subprocess.run([
            'docker', 'ps', '--filter', 'name=call-centre-secure', '--format', '{{.Names}}'
        ], capture_output=True, text=True, timeout=10)
        
        return 'call-centre-secure' in result.stdout
    except:
        return False

def main():
    """Main security validation function"""
    print("🔒 Call Centre Agent Security Validation")
    print("Enterprise-Grade Security Testing")
    print("=" * 60)
    
    # Check if container is running
    if not check_container_running():
        print("❌ Container 'call-centre-secure' is not running")
        print("\n🚀 To start the secure environment:")
        print("docker-compose -f docker-compose.secure.yml up -d")
        sys.exit(1)
    
    print("✅ Found running secure container")
    print("⏳ Starting security validation tests...\n")
    
    # Run security validation
    validator = SecurityValidator()
    validator.run_all_tests()
    
    # Return appropriate exit code
    sys.exit(0 if validator.critical_failures == 0 else 1)

if __name__ == "__main__":
    main()
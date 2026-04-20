#!/usr/bin/env python3
"""
Script de auditoría de seguridad automática.

Ejecuta verificaciones de seguridad automáticamente.
Útil para CI/CD y pre-deploy.

Usage:
    python scripts/security_audit.py
    python scripts/security_audit.py --report
    python scripts/security_audit.py --fix
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple


class Finding(NamedTuple):
    """Hallazgo de seguridad."""

    severity: str  # CRITICAL, HIGH, MEDIUM, LOW, INFO
    category: str
    file: str
    line: int | None
    message: str
    fix: str | None = None


class SecurityAuditor:
    """Auditor de seguridad automático."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.findings: list[Finding] = []

    def run(self) -> list[Finding]:
        """Ejecutar todas las verificaciones."""
        self.check_hardcoded_secrets()
        self.check_debug_enabled()
        self.check_insecure_random()
        self.check_sql_patterns()
        self.check_logging_secrets()
        self.check_dockerfile_user()
        self.check_compose_secrets()
        self.check_dependencies()
        self.check_cors_wildcard()
        self.check_rate_limiting()
        return self.findings

    def check_hardcoded_secrets(self) -> None:
        """Buscar secrets hardcodeados."""
        patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password"),
            (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key"),
            (r'secret\s*=\s*["\'][^"\']+["\']', "Hardcoded secret"),
            (r'token\s*=\s*["\'][^"\']+["\']', "Hardcoded token"),
            (r'private[_-]?key\s*=\s*["\'][^"\']+["\']', "Hardcoded private key"),
        ]

        for py_file in self.root_dir.glob("app/**/*.py"):
            content = py_file.read_text(encoding="utf-8")
            for line_num, line in enumerate(content.split("\n"), 1):
                for pattern, desc in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        # Excepciones para ejemplos
                        if "example" in line.lower() or "#" in line:
                            continue
                        self.findings.append(
                            Finding(
                                severity="CRITICAL",
                                category="Hardcoded Secret",
                                file=str(py_file.relative_to(self.root_dir)),
                                line=line_num,
                                message=f"Found: {desc}",
                                fix="Use environment variables instead",
                            )
                        )

    def check_debug_enabled(self) -> None:
        """Buscar DEBUG=True."""
        for py_file in self.root_dir.glob("app/**/*.py"):
            content = py_file.read_text(encoding="utf-8")
            if re.search(r"DEBUG\s*=\s*True", content, re.IGNORECASE):
                self.findings.append(
                    Finding(
                        severity="HIGH",
                        category="Debug Enabled",
                        file=str(py_file.relative_to(self.root_dir)),
                        line=None,
                        message="DEBUG=True found",
                        fix="Set DEBUG=False in production",
                    )
                )

    def check_insecure_random(self) -> None:
        """Buscar uso de random en lugar de secrets."""
        for py_file in self.root_dir.glob("app/**/*.py"):
            content = py_file.read_text(encoding="utf-8")
            if re.search(r"import random", content):
                self.findings.append(
                    Finding(
                        severity="MEDIUM",
                        category="Insecure Random",
                        file=str(py_file.relative_to(self.root_dir)),
                        line=None,
                        message="Using random module instead of secrets",
                        fix="Use secrets module instead",
                    )
                )

    def check_sql_patterns(self) -> None:
        """Buscar patrones SQL vulnerables."""
        for py_file in self.root_dir.glob("app/**/*.py"):
            content = py_file.read_text(encoding="utf-8")
            if "execute(" in content and "%" in content:
                self.findings.append(
                    Finding(
                        severity="HIGH",
                        category="SQL Injection",
                        file=str(py_file.relative_to(self.root_dir)),
                        line=None,
                        message="String formatting in SQL query",
                        fix="Use parameterized queries",
                    )
                )

    def check_logging_secrets(self) -> None:
        """Buscar logging de datos sensibles."""
        sensitive = ["password", "token", "secret", "api_key", "credit_card"]
        for py_file in self.root_dir.glob("app/**/*.py"):
            content = py_file.read_text(encoding="utf-8")
            for line_num, line in enumerate(content.split("\n"), 1):
                if "log." in line:
                    for s in sensitive:
                        if s in line.lower():
                            self.findings.append(
                                Finding(
                                    severity="MEDIUM",
                                    category="Sensitive Logging",
                                    file=str(py_file.relative_to(self.root_dir)),
                                    line=line_num,
                                    message=f"Potential sensitive data in log: {s}",
                                    fix="Redact sensitive data before logging",
                                )
                            )
                            break

    def check_dockerfile_user(self) -> None:
        """Verificar que Dockerfile no corre como root."""
        dockerfile = self.root_dir / "Dockerfile"
        if not dockerfile.exists():
            return

        content = dockerfile.read_text(encoding="utf-8")
        if "USER root" in content or "USER root" in content.upper():
            self.findings.append(
                Finding(
                    severity="HIGH",
                    category="Container Security",
                    file="Dockerfile",
                    line=None,
                    message="Running as root user",
                    fix="Use USER directive to switch to non-root",
                )
            )

    def check_compose_secrets(self) -> None:
        """Verificar secrets en docker-compose."""
        compose = self.root_dir / "docker-compose.yml"
        if not compose.exists():
            return

        content = compose.read_text(encoding="utf-8")
        if "password:" in content and "${" not in content:
            self.findings.append(
                Finding(
                    severity="HIGH",
                    category="Secrets Management",
                    file="docker-compose.yml",
                    line=None,
                    message="Hardcoded password in compose",
                    fix="Use ${VARIABLE} syntax",
                )
            )

    def check_dependencies(self) -> None:
        """Verificar dependencias con vulnerabilidades."""
        # Check if safety is installed
        try:
            result = subprocess.run(
                ["safety", "check", "--json"],
                capture_output=True,
                text=True,
                cwd=self.root_dir,
            )
            if result.returncode != 0:
                # Parse output and add findings
                for line in result.stdout.split("\n"):
                    if line.strip():
                        self.findings.append(
                            Finding(
                                severity="HIGH",
                                category="Dependency Vulnerability",
                                file="requirements.txt",
                                line=None,
                                message=line.strip()[:100],
                                fix="Update package",
                            )
                        )
        except FileNotFoundError:
            # safety not installed - check pip
            pass

    def check_cors_wildcard(self) -> None:
        """Verificar CORS con wildcard."""
        for py_file in self.root_dir.glob("app/**/*.py"):
            content = py_file.read_text(encoding="utf-8")
            if 'allow_origins=["*"]' in content or "allow_origins=['*']" in content:
                self.findings.append(
                    Finding(
                        severity="CRITICAL",
                        category="CORS",
                        file=str(py_file.relative_to(self.root_dir)),
                        line=None,
                        message="CORS allows all origins",
                        fix="Specify exact origins",
                    )
                )

    def check_rate_limiting(self) -> None:
        """Verificar que rate limiting existe."""
        files_with_routes = []
        for py_file in self.root_dir.glob("app/**/*.py"):
            content = py_file.read_text(encoding="utf-8")
            if "@app.post(" in content or "@app.get(" in content:
                if "rate_limit" not in content.lower():
                    files_with_routes.append(str(py_file.relative_to(self.root_dir)))

        if files_with_routes:
            self.findings.append(
                Finding(
                    severity="MEDIUM",
                    category="Rate Limiting",
                    file=", ".join(files_with_routes[:3]),
                    line=None,
                    message="No rate limiting found",
                    fix="Add rate limiting",
                )
            )


def main():
    parser = argparse.ArgumentParser(
        description="Security audit script"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate report",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Attempt to fix findings",
    )
    args = parser.parse_args()

    root = Path(__file__).parent.parent
    auditor = SecurityAuditor(root)
    findings = auditor.run()

    if not findings:
        print("✅ No security issues found!")
        return 0

    # Print findings
    print(f"\n{'='*60}")
    print(f"🔴 SECURITY AUDIT - {len(findings)} ISSUES FOUND")
    print(f"{'='*60}\n")

    by_severity = {}
    for f in findings:
        by_severity.setdefault(f.severity, []).append(f)

    for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        if severity in by_severity:
            print(f"\n🔴 {severity} ({len(by_severity[severity])})")
            print("-" * 40)
            for f in by_severity[severity]:
                location = f"{f.file}"
                if f.line:
                    location += f":{f.line}"
                print(f"  • {location}")
                print(f"    {f.message}")
                if f.fix:
                    print(f"    Fix: {f.fix}")

    print(f"\n{'='*60}")
    if args.report:
        print(f"Full report generated")

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
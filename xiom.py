#!/usr/bin/env python3
"""
Xiom — Website & Server Fingerprinting OSINT Tool

Comprehensive fingerprinting tool that identifies web server types, frameworks,
SSL certificates, DNS records, and other reconnaissance data from target URLs.
"""

import argparse
import json
import logging
import os
import re
import socket
import ssl
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
from urllib.request import urlopen, Request

import dns.resolver
import requests
from colorama import Fore, Style, init
from cryptography import x509
from cryptography.hazmat.backends import default_backend

init(autoreset=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class XiomConfig:
    """Configuration manager for Xiom."""

    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.data = self._load_config()

    def _load_config(self) -> Dict:
        """Load configuration from file or use defaults."""
        defaults = {
            "timeout": 10,
            "verify_ssl": True,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "ports_to_scan": [80, 443, 22, 21, 25, 8080, 8443, 3306, 5432],
            "api_keys": {},
            "max_retries": 3,
            "retry_delay": 2
        }

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    defaults.update(loaded)
                    logger.info(f"Loaded config from {self.config_file}")
            except Exception as e:
                logger.warning(f"Failed to load config: {e}. Using defaults.")

        return defaults

    def get(self, key: str, default=None):
        """Get config value."""
        return self.data.get(key, default)


class ServerFingerprint:
    """Core fingerprinting engine."""

    def __init__(self, config: XiomConfig):
        self.config = config
        self.results = {}

    def fingerprint(self, url: str) -> Dict:
        """Run full fingerprinting on target URL."""
        self.results = {"url": url, "timestamp": datetime.now().isoformat()}

        try:
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                url = f"https://{url}"
                parsed_url = urlparse(url)

            self.results["domain"] = parsed_url.netloc

            print(f"\n{Fore.CYAN}[*] Fingerprinting {url}...{Style.RESET_ALL}\n")

            self._get_http_info(url)
            self._get_ssl_info(parsed_url.netloc)
            self._get_dns_info(parsed_url.netloc)
            self._get_whois_info(parsed_url.netloc)

        except Exception as e:
            logger.error(f"Fingerprinting failed: {e}")
            self.results["error"] = str(e)

        return self.results

    def _get_http_info(self, url: str) -> None:
        """Extract HTTP headers and server information."""
        try:
            print(f"{Fore.YELLOW}[*] Analyzing HTTP headers...{Style.RESET_ALL}")

            headers = {
                "User-Agent": self.config.get("user_agent"),
            }

            response = requests.head(
                url,
                headers=headers,
                timeout=self.config.get("timeout"),
                verify=self.config.get("verify_ssl"),
                allow_redirects=True
            )

            http_data = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "redirects": response.url if response.url != url else None
            }

            # Detect server
            server_header = response.headers.get("Server", "Unknown")
            http_data["server"] = server_header

            # Detect frameworks and tech
            tech_stack = self._detect_technologies(response.headers)
            http_data["technologies"] = tech_stack

            # Detect CMS
            cms = self._detect_cms(response.headers)
            if cms:
                http_data["cms"] = cms

            self.results["http"] = http_data
            print(f"{Fore.GREEN}[✓] HTTP Info: {server_header}{Style.RESET_ALL}")

        except Exception as e:
            logger.error(f"HTTP analysis failed: {e}")
            self.results["http"] = {"error": str(e)}

    def _detect_technologies(self, headers: Dict) -> List[str]:
        """Identify web frameworks and technologies from headers."""
        technologies = []

        tech_signatures = {
            "X-Powered-By": ["PHP", "Express", "ASP.NET"],
            "X-AspNet-Version": ["ASP.NET"],
            "X-Runtime": ["Ruby"],
            "Server": ["Apache", "Nginx", "IIS", "Tomcat", "Node.js"],
        }

        for header, values in tech_signatures.items():
            if header in headers:
                technologies.append(headers[header])

        return list(set(technologies))

    def _detect_cms(self, headers: Dict) -> Optional[str]:
        """Detect CMS from headers and common indicators."""
        cms_indicators = {
            "Wordpress": "wp-content",
            "Drupal": "drupal",
            "Joomla": "joomla",
            "Magento": "magento",
        }

        for cms, indicator in cms_indicators.items():
            if any(indicator in str(v).lower() for v in headers.values()):
                return cms

        return None

    def _get_ssl_info(self, domain: str) -> None:
        """Extract SSL/TLS certificate information."""
        try:
            print(f"{Fore.YELLOW}[*] Analyzing SSL/TLS certificate...{Style.RESET_ALL}")

            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            with socket.create_connection((domain, 443), timeout=self.config.get("timeout")) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    der_cert = ssock.getpeercert(binary_form=True)
                    cert = x509.load_der_x509_certificate(der_cert, default_backend())

                    # Parse subject and issuer
                    subject_dict = {}
                    for attr in cert.subject:
                        subject_dict[attr.oid._name] = attr.value

                    issuer_dict = {}
                    for attr in cert.issuer:
                        issuer_dict[attr.oid._name] = attr.value

                    ssl_data = {
                        "subject": subject_dict,
                        "issuer": issuer_dict,
                        "valid_from": str(cert.not_valid_before),
                        "valid_until": str(cert.not_valid_after),
                        "version": cert.version.name,
                    }

                    self.results["ssl"] = ssl_data
                    print(f"{Fore.GREEN}[✓] SSL Info: Valid until {cert.not_valid_after}{Style.RESET_ALL}")

        except Exception as e:
            logger.warning(f"SSL analysis failed: {e}")
            self.results["ssl"] = {"error": str(e)}

    def _get_dns_info(self, domain: str) -> None:
        """Query DNS records."""
        try:
            print(f"{Fore.YELLOW}[*] Querying DNS records...{Style.RESET_ALL}")

            dns_data = {}
            record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]

            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    dns_data[record_type] = [str(rdata) for rdata in answers]
                except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, Exception):
                    pass

            self.results["dns"] = dns_data
            print(f"{Fore.GREEN}[✓] DNS Info: Found {len(dns_data)} record types{Style.RESET_ALL}")

        except Exception as e:
            logger.warning(f"DNS queries failed: {e}")
            self.results["dns"] = {"error": str(e)}

    def _get_whois_info(self, domain: str) -> None:
        """Basic whois lookup (simplified version)."""
        try:
            print(f"{Fore.YELLOW}[*] Retrieving WHOIS info...{Style.RESET_ALL}")

            # Try to resolve domain IP
            try:
                ip = socket.gethostbyname(domain)
                self.results["ip"] = ip
                print(f"{Fore.GREEN}[✓] IP Address: {ip}{Style.RESET_ALL}")
            except socket.gaierror as e:
                logger.warning(f"DNS resolution failed: {e}")

        except Exception as e:
            logger.warning(f"WHOIS lookup failed: {e}")


def print_report(results: Dict) -> None:
    """Print formatted fingerprint report."""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'XIOM FINGERPRINT REPORT':^60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

    print(f"{Fore.YELLOW}[*] Target:{Style.RESET_ALL} {results.get('url', 'Unknown')}")
    print(f"{Fore.YELLOW}[*] Time:{Style.RESET_ALL} {results.get('timestamp', 'Unknown')}\n")

    # HTTP Info
    if "http" in results and "error" not in results["http"]:
        http = results["http"]
        print(f"{Fore.GREEN}[✓] SERVER INFORMATION{Style.RESET_ALL}")
        print(f"    Server:        {http.get('server', 'Unknown')}")
        print(f"    Status Code:   {http.get('status_code', 'Unknown')}")
        if http.get('technologies'):
            print(f"    Technologies:  {', '.join(http['technologies'])}")
        if http.get('cms'):
            print(f"    CMS:           {http['cms']}")
        print()

    # SSL Info
    if "ssl" in results and "error" not in results["ssl"]:
        ssl_info = results["ssl"]
        print(f"{Fore.GREEN}[✓] SSL/TLS CERTIFICATE{Style.RESET_ALL}")
        
        # Get issuer common name if available
        issuer = ssl_info.get('issuer', {})
        issuer_str = issuer.get('commonName', 'Unknown') if isinstance(issuer, dict) else str(issuer)[:50]
        
        print(f"    Issuer:        {issuer_str}")
        print(f"    Valid From:    {ssl_info.get('valid_from', 'Unknown')}")
        print(f"    Valid Until:   {ssl_info.get('valid_until', 'Unknown')}")
        print(f"    Version:       {ssl_info.get('version', 'Unknown')}")
        print()

    # DNS Info
    if "dns" in results:
        dns_data = results["dns"]
        if dns_data and "error" not in dns_data:
            print(f"{Fore.GREEN}[✓] DNS RECORDS{Style.RESET_ALL}")
            for record_type, values in dns_data.items():
                if values:
                    print(f"    {record_type}:     {', '.join(values[:2])}")
            print()

    # IP Address
    if "ip" in results:
        print(f"{Fore.GREEN}[✓] NETWORK INFORMATION{Style.RESET_ALL}")
        print(f"    IP Address:    {results['ip']}")
        print()

    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Xiom - Website & Server Fingerprinting OSINT Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python xiom.py https://example.com
  python xiom.py example.com --json
  python xiom.py example.com --verbose
        """
    )

    parser.add_argument("url", help="Target URL to fingerprint")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--config", default="config.json", help="Path to config file")

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    config = XiomConfig(args.config)
    fingerprinter = ServerFingerprint(config)

    results = fingerprinter.fingerprint(args.url)

    if args.json:
        print(json.dumps(results, indent=2, default=str))
    else:
        print_report(results)


if __name__ == "__main__":
    main()

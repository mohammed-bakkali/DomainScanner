import requests
import re
import dns.resolver
import argparse

def search_domains_by_extension(extension):
    if not extension.startswith("."):
        print("❌ Invalid extension! It must start with a dot (e.g., .com or .net).")
        return []

    url = f"https://crt.sh/?q=%{extension}&output=json"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        domains = set()
        email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

        for entry in data:
            name = entry.get("name_value", "")
            found_domains = name.split("\n")
            for domain in found_domains:
                clean_domain = domain.replace("www.", "").strip()
                if not email_pattern.search(clean_domain) and not clean_domain.startswith("*.") and clean_domain.endswith(extension):
                    domains.add(clean_domain)

        if not domains:
            print(f"❌ No domains found for the extension: {extension}")
            return []
        
        with open("found_domains.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(sorted(domains)))

        print(f"✅ Found {len(domains)} domains and saved them in found_domains.txt")
        return list(domains)

    except requests.RequestException as e:
        print(f"❌ Error fetching data: {e}")
        return []

def check_dns(domain):
    records = {}
    
    def fetch_record(record_type):
        try:
            answers = dns.resolver.resolve(domain, record_type)
            return [rdata.to_text() for rdata in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            return []
        except Exception as e:
            return [f"Error: {e}"]

    records["SPF"] = fetch_record("TXT")
    records["MX"] = fetch_record("MX")
    records["AAAA"] = fetch_record("AAAA")
    records["CNAME"] = fetch_record("CNAME")
    records["NS"] = fetch_record("NS")

    return records

def check_group(domains):
    dns_results = []

    for domain in domains:
        print(f"\n🔍 Searching for DNS records of the domain: {domain}")
        records = check_dns(domain)
        dns_results.append(f"🔹 {domain}")
        for record, values in records.items():
            dns_results.append(f"{record}: {', '.join(values) if values else 'None'}")
        dns_results.append("\n" + "-"*50 + "\n")

    with open("dns_results.txt", "w") as file:
        file.write("\n".join(dns_results))

    print("\n✅ All results saved in dns_results.txt")

def fetch_subdomains(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        subdomains = set()
        for entry in data:
            name = entry.get("name_value", "")
            found_subdomains = name.split("\n")
            for sub in found_subdomains:
                clean_sub = sub.strip().replace("www.", "")
                if clean_sub.endswith(domain):
                    subdomains.add(clean_sub)

        return sorted(subdomains)

    except requests.RequestException as e:
        print(f"❌ Error fetching subdomains for {domain}: {e}")
        return []

def extract_subdomains(domains):
    with open("all_subdomains.txt", "w", encoding="utf-8") as file:
        for domain in domains:
            subdomains = fetch_subdomains(domain)
            if subdomains:
                file.write(f"🔹 {domain}\n")
                file.write("\n".join(subdomains))
                file.write("\n" + "="*40 + "\n")
                print(f"✅ Found {len(subdomains)} subdomains for {domain}.")
            else:
                print(f"❌ No subdomains found for {domain}.")

    print(f"✅ All subdomains saved in all_subdomains.txt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🔍 Comprehensive tool for domain and DNS record searches")
    parser.add_argument("--search", type=str, help="🔹 Search for domains by extension (e.g., .com)")
    parser.add_argument("--all", action="store_true", help="🔹 Automatically run DNS analysis and subdomain search after domain search")
    parser.add_argument("--dns", type=str, help="🔹 Check DNS records for a specific domain")

    # Parsing the arguments
    args = parser.parse_args()

    if args.dns:
        print(f"\n🔍 Checking DNS records for {args.dns}...\n")
        records = check_dns(args.dns)
        for record, values in records.items():
            print(f"{record}: {', '.join(values) if values else 'None'}")

    if args.search:
        found_domains = search_domains_by_extension(args.search)
        if args.all and found_domains:
            check_group(found_domains)
            extract_subdomains(found_domains)
    else:
        parser.print_help()

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import ast
import requests
from .fetch_courses import fetch_courses
import google.generativeai as genai
import os
import re
from .fetch_courses import fetch_course_structure

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# # from .models import QuestionAnswer
# # from .serializers import QuestionAnswerSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .models import QuestionAnswer
# from .serializers import QuestionAnswerSerializer

@csrf_exempt
def score_answers(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            file = request.FILES['file']
            print("File received:", file.name)
            print("File content type:", file.content_type)
            print("File size:", file.size)
            if file.size == 0:
                return JsonResponse({'error': 'Empty file'}, status=400)
            file_content = file.read().decode('utf-8')
            print("File content:", file_content)
            data = json.loads(file_content)
            print("Data loaded:", data)
            questions_and_answers = data.get('questions_and_answers', [])
            for item in questions_and_answers:
                # Simulate AI model scoring
                item['score'] = 0.8  # Assign a default score of 0.8 to each answer
            return JsonResponse({'questions_and_answers': questions_and_answers}, status=200)
        except json.JSONDecodeError as e:
            print("JSON Decode Error:", str(e))
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print("Exception:", str(e))
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method or missing file'}, status=405)

@csrf_exempt 
def generate_roadmap(request):
  if request.method == "GET":
    skill = request.GET.get('skill', None)
    current_skill_level = request.GET.get('current_skill_level', None)
    target_skill_level = request.GET.get('target_skill_level', None)
    price = request.GET.get('price', None)
    if skill is None:
      return JsonResponse({'error': 'Skill not provided'}, status=400)
    if current_skill_level is None:
      return JsonResponse({'error': 'Current skill level not provided'}, status=400)
    if target_skill_level is None:
      return JsonResponse({'error': 'Target skill level not provided'}, status=400)

    genai.configure(api_key="AIzaSyBzjohOuPQSaNZ9hTJBYCiKLwpC_8_PSMo")

    model = genai.GenerativeModel('gemini-1.5-flash')
    
    roadmap_prompt = f"""
    Create a comprehensive roadmap for mastering the topic {skill}, I am currently at {current_skill_level} level and want to get to the level of {target_skill_level}. Provide the output in different levels of increasing difficulty starting from ("Level 1") to maximum ("Level 6") and give the output in a JSON file: Keep the topics as concise as possible, topics should be the main things to learn. A level should no contain more than 5 topics within itself. Ensure the topics are completely technical to help me optimally prepare for my job. Do not include any other text or explanations as well as do not include any text formatting.
    """

    roadmap = model.generate_content(roadmap_prompt).text.replace("`", "").replace("json", "")
    # roadmap = json.loads(roadmap)
    roadmap_dict = ast.literal_eval(roadmap)

    courses = {}
 
    # fetch_coures
    for level, topics in roadmap_dict.items():
      courses[level] = {}
      for topic in topics:
        courses[level][topic] = fetch_courses(topic, price)

    # def convert_to_bullet_points(data):
    #   result = []
    #   for level, topics in data.items():
    #     result.append(f"$$$ {level}")
    #     for topic, courses in topics.items():
    #       result.append(f"  !!! {topic}")
    #       for course in courses:
    #         result.append(f"   ### {course['title']}")
    #         result.append(f"    URL: {course['url']}")
    #         result.append(f"    Description: {course['description']}")
    #   return "\n".join(result)

    # list_courses = convert_to_bullet_points(courses)

    select_courses_prompt = f"""
    You have a list of courses with levels and topics {courses}. For each topic, you have a list of courses. The list contains levels, topics, and then courses for each topic. Don't change topic, or the level. Only choose between the courses available for it. Choose the most relevant course for each topic based on title and description. Choose only one course per topic. Give the output in a JSON file.
    Include the best course for each topic as specified, and make sure to cover all topics listed. Only provide the formatted data without additional explanations. Don't include any text other than the list.
    """

    select_courses_response = model.generate_content(select_courses_prompt).text.replace("`", "").replace("json", "")
    select_courses_response_dict = ast.literal_eval(select_courses_response)

    # # TODO: Change this to id of courses
    # # Assuming select_courses_response is defined elsewhere
    # urls = re.findall(r'https://www\.udemy\.com/course/[^\s/]+/', select_courses_response)

    # # Assuming courses is already a dictionary
    # courses_data = courses

    # # Step 3: Filter courses based on matching URLs
    # filtered_courses = {
    #   level: {
    #     course_name: [
    #       course for course in course_list if course['url'] in urls
    #     ]
    #     for course_name, course_list in level_courses.items()
    #   }
    #   for level, level_courses in courses_data.items()
    # }

    # # Step 4: Output the filtered JSON
    # filtered_courses_json = json.dumps(filtered_courses, indent=2)
    # for level, topics, chapters in filtered_courses_json.items():
    #   level[topics][chapters] = {}
    #   for topic in topics:
    #     courses[level][topic] = fetch_courses(topic, price)
    # print(filtered_courses_json)

    # # Load the JSON file
    # with open('courses.json', 'r') as file:
    #     courses_data = json.load(file)

    # Extract IDs and fetch course structures
    # course_structures = {}
    for level, courses in select_courses_response_dict.items():
        for course_name, course_info in courses.items():
            course_id = course_info["id"]
            select_courses_response_dict[level][course_name]["structure"] = fetch_course_structure(course_id)

    # Write output to file
    # with open('roadmap_output.txt', 'w') as file:
    #   file.write("### Roadmap Response\n")
    #   file.write(roadmap_response + "\n\n")
    #   file.write("### Roadmap JSON\n")
    #   file.write(json.dumps(roadmap, indent=2) + "\n\n")
    #   file.write("### Courses JSON\n")
    #   file.write(json.dumps(courses, indent=2) + "\n\n")
    #   file.write("### List of Courses\n")
    #   file.write(list_courses + "\n\n")
    #   file.write("### Selected Courses Response\n")
    #   file.write(select_courses_response + "\n")

    return HttpResponse(
      # filtered_courses_json,
      json.dumps(select_courses_response_dict),
      content_type="application/json"
    )

@csrf_exempt
def test_roadmap(request):
  roadmap = {
    "roadmap": {
      "Level 1": {
          "Basic Networking Concepts": {
              "id": 4606674,
              "title": "Introduction to Computer Networking - Crash Course",
              "url": "https://www.udemy.com/course/networkingbasics/",
              "description": "Learn the basics of IP, Ethernet, VPNs, WANs, DHCP, DNS, with no prior knowledge required.   Bonus IP addressing course!",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/4606674_aa40.jpg",
              "price": "₹2,499",
              "structure": [
                  "Introduction",
                  "IP Addressing and Subnetting"
              ]
          },
          "Operating System Fundamentals": {
              "id": 1555228,
              "title": "Operating Systems from scratch - Part 1",
              "url": "https://www.udemy.com/course/operating-systems-from-scratch-part1/",
              "description": "Learn the concepts of Operating Systems from scratch as Operating System forms the core of Computer Science",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/1555228_0997_12.jpg",
              "price": "₹3,099",
              "structure": [
                  "Introduction",
                  "Introduction to Operating Systems",
                  "Operating System Concepts",
                  "CPU Scheduling Algorithms - SJF, SRTF, FCFS",
                  "Comparision of FCFS, SJF and SRTF - Advantages and Disadvantages",
                  "CPU Scheduling Algorithms - LJF, LRTF, Priority-based, HRRN",
                  "Basics of Number System",
                  "Memory Allocation Techniques",
                  "Bonus : How to proceed further"
              ]
          },
          "Cybersecurity Concepts & Terminology": {
              "id": 4639504,
              "title": "Want a Job in Cybersecurity - Foundation Concepts To Know",
              "url": "https://www.udemy.com/course/want-a-job-in-cybersecurity/",
              "description": "Master The Foundation Concepts For A Career In Cybersecurity",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/4639504_a74d.jpg",
              "price": "₹799",
              "structure": [
                  "Course Introduction",
                  "Part 1:  Introduction",
                  "Part 1:  Foundations of Cybersecurity",
                  "Part 1:  Identifying and Handling Risk",
                  "Part 1:  Business Continuity, Disaster Recovery, and Incident Response",
                  "Part 1:  Access Controls",
                  "Part 1:  Cryptography",
                  "Part 1:  Network and Communications Security",
                  "Part 1:  Security in the Cloud",
                  "Part 1:  System and Application Security",
                  "Part 1:  Governance, Risk, and Compliance",
                  "Part 1:  Conclusion",
                  "Part 2:  Certification Exam Prep",
                  "Part 2:  Exam Strategy",
                  "Part 2: Identifying Memorization Testing Questions",
                  "Part 2:  Essential Diagrams",
                  "Part 2:  Information Lists",
                  "Part 2:  Essential Facts",
                  "Part 3: Exam Practice",
                  "Part 4:  Navigating the Interview",
                  "Course Conclusion and Thank You"
              ]
          },
          "Common Threats & Vulnerabilities": {
              "id": 3002858,
              "title": "Threat Modeling",
              "url": "https://www.udemy.com/course/the-threat-modeling/",
              "description": "Terminology, Tools, Processes, Supplementary, Techniques, Applied Examples, Threat, and Countermeasure Catalogues",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/3002858_6608_2.jpg",
              "price": "₹2,799",
              "structure": [
                  "Summary and Wrap Up",
                  "Basics and Terminology",
                  "Threat Modeling Tools and Techniques",
                  "Microsoft Threat Modeling Tool In-Depth",
                  "Microsoft SDL",
                  "Standards, Dictionaries and Other Useful Information",
                  "Countermeasures",
                  "Conclusion"
              ]
          },
          "Security Awareness & Best Practices": {
              "id": 1361726,
              "title": "Security Awareness Training, Internet Security for Employees",
              "url": "https://www.udemy.com/course/security-awareness-training-internet-security-for-everyone/",
              "description": "Basic security awareness guide on Internet security and privacy to help keep you, your home, and your employer safe.",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/1361726_508a_2.jpg",
              "price": "₹3,299",
              "structure": [
                  "Introduction",
                  "User and Device Accountability",
                  "Phishing and Other Malicious Emails",
                  "Social Engineering",
                  "Handling of Data (Data Leakage)",
                  "Passwords and Security Questions",
                  "Safe Browsing",
                  "Mobile Devices and Traveling",
                  "Ransomware",
                  "Conclusion"
              ]
          }
      },
      "Level 2": {
          "Linux Fundamentals": {
              "id": 3945922,
              "title": "Linux for Beginners: Linux Basics",
              "url": "https://www.udemy.com/course/linux-for-beginners-2021/",
              "description": "Linux For Beginners covers Linux basics. You will learn Linux fundamental skills; Command line, Linux Administration",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/3945922_0e43_2.jpg",
              "price": "₹3,299",
              "structure": [
                  "Introduction to Linux Course",
                  "Setting Up the Laboratory for linux",
                  "Introduction to Linux",
                  "Basic Commands - 1 in Linux",
                  "Linux File Systems",
                  "Basic Commands - 2 in Linux",
                  "Network Settings",
                  "Services",
                  "User Management Linux",
                  "Process Management",
                  "Package Management",
                  "System Monitoring",
                  "Extra"
              ]
          },
          "Windows Security Hardening": {
              "id": 755984,
              "title": "Linux Security and Hardening, The Practical Security Guide.",
              "url": "https://www.udemy.com/course/linux-security/",
              "description": "Secure any Linux server from hackers & protect it against hacking. The practical Linux Administration security guide.",
              "thumbnail": "https://img-b.udemycdn.com/course/480x270/755984_6223_3.jpg",
              "price": "₹3,099",
              "structure": [
                  "Course Overview and Downloads",
                  "General Security",
                  "Physical Security",
                  "Account Security",
                  "Network Security",
                  "File System Security",
                  "Additional Security Resources",
                  "Bonus Section"
              ]
          },
          "Network Security Tools (Wireshark, Nmap)": {
              "id": 5773538,
              "title": "Wireshark | Wireshark Packet Analysis for Network Security",
              "url": "https://www.udemy.com/course/wireshark-wireshark-packet-analysis-for-network-security/",
              "description": "Wireshark- Learn TCP/IP, Network Protocols' Packet Capture ; Network Analysis to troubleshoot network for cyber security",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/5773538_b4fd.jpg",
              "price": "₹799",
              "structure": [
                  "Network Fundamentals",
                  "Packet Captures in Wireshark",
                  "Analyse Protocols in Wireshark",
                  "Packet Operations in Wireshark",
                  "Wireshark - ICMP Analysis",
                  "Wireshark - ARP Analysis",
                  "Wireshark - TCP Analysis",
                  "Wireshark - UDP Analysis",
                  "Wireshark - DHCP Analysis",
                  "Wireshark - DNS Analysis",
                  "Wireshark - HTTP Analysis",
                  "Wireshark - HTTPS Analysis",
                  "Extra"
              ]
          },
          "Cryptography Basics (Symmetric & Asymmetric)": {
              "id": 1694794,
              "title": "Cryptography and Hashing Fundamentals in Python and Java",
              "url": "https://www.udemy.com/course/learn-cryptography-basics-in-python/",
              "description": "Private and Public Key Cryptosystems, DES, AES, Cryptoanalysis, RSA, Elliptic Curve Cryptography and Hashing",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/1694794_f387_2.jpg",
              "price": "₹3,099",
              "structure": [
                  "Introduction",
                  "Cryptography Fundamentals",
                  "### SYMMETRIC (PRIVATE KEY) CRYPTOGRAPHY ###",
                  "Caesar Cipher Theory",
                  "Caesar Cipher Implementation (Python)",
                  "Caesar Cipher Implementation (Java)",
                  "Cracking Caesar Cipher",
                  "Detecting Languages",
                  "Vigenere Cipher Theory",
                  "Vigenere Cipher Implementation (Python)",
                  "Vigenere Cipher Implementation (Java)",
                  "Cracking the Vigenere Cipher (Kasiski Algorithm)",
                  "One Time Pad (Vernam Cipher)",
                  "Randomness in Cryptography",
                  "One Time Pad Implementation (Python)",
                  "One Time Pad Implementation (Java)",
                  "Cracking One Time Pad",
                  "Data Encryption Standard (DES)",
                  "Data Encryption Standard (DES) Implementation (Python)",
                  "Data Encryption Standard (DES) Implementation (Java)",
                  "Cracking Data Encryption Standard (DES)",
                  "Advanced Encryption Standard (AES)",
                  "Advanced Encryption Standard (AES) Implementation (Python)",
                  "Advanced Encryption Standard (AES) Implementation (Java)",
                  "Cracking Advanced Encryption Standard (AES)",
                  "### ASYMMETRIC (PUBLIC KEY) CRYPTOGRAPHY ###",
                  "Asymmetric Cryptosystems",
                  "Modular Arithmetic",
                  "Diffie-Hellman Key Exchange",
                  "Diffie-Hellman Cryptosystem Implementation (Python)",
                  "Diffie-Hellman Cryptosystem Implementation (Java)",
                  "Cracking Diffie-Hellman Cryptosystem",
                  "RSA",
                  "Advanced Modular Arithmetic",
                  "RSA Implementation (Python)",
                  "RSA Implementation (Java)",
                  "Cracking RSA",
                  "Elliptic Curve Cryptography (ECC)",
                  "Elliptic Curve Cryptography (ECC) Implementation (Python)",
                  "Elliptic Curve Digital Signature Algorithms (ECDSA) Implementation (Python)",
                  "Elliptic Curve Cryptography (ECC) Implementation (Java)",
                  "Elliptic Curve Digital Signature Algorithms (ECDSA) Implementation (Java)",
                  "Cracking the Elliptic Curve Cryptosystem (ECC)",
                  "### HASHING ###",
                  "Hashing Algorithms Implementation (Python)",
                  "Hashing Algorithms Implementation (Java)",
                  "### APPLICATIONS OF CRYPTOGRAPHY###",
                  "Course Materials (DOWNLOADS)"
              ]
          },
          "Vulnerability Scanning & Penetration Testing Fundamentals": {
              "id": 4576350,
              "title": "Nessus Scanner: Network Scanning from Beginner to Advanced!",
              "url": "https://www.udemy.com/course/nessus-scanner-network-scanning-from-beginner-to-advanced/",
              "description": "After this ONE course, you will be able to configure and use Nessus for vulnerability assessments like a PRO!",
              "thumbnail": "https://img-b.udemycdn.com/course/480x270/4576350_0212_8.jpg",
              "price": "₹3,099",
              "structure": [
                  "Welcome to the Course",
                  "Setting up the Laboratory",
                  "Basics of Vulnerability Analysis",
                  "Each Tab of Nessus in Deep",
                  "Nessus For Real Life Scenarios",
                  "Writing Fully Custom Reports",
                  "BONUS Section"
              ]
          }
      },
      "Level 3": {
          "Ethical Hacking & Penetration Testing Methodology": {
              "id": 857010,
              "title": "Learn Ethical Hacking From Scratch 2024",
              "url": "https://www.udemy.com/course/learn-ethical-hacking-from-scratch/",
              "description": "Become an ethical hacker that can hack like black hat hackers and secure systems like cybersecurity experts",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/857010_8239_5.jpg",
              "price": "₹4,099",
              "structure": [
                  "Course Introduction",
                  "Setting up a Hacking Lab",
                  "Linux Basics",
                  "Network Hacking",
                  "Network Hacking - Pre Connection Attacks",
                  "Network Hacking - Gaining Access - WEP Cracking",
                  "Network Hacking - Gaining Access - WPA / WPA2 Cracking",
                  "Network Hacking - Gaining Access - Security",
                  "Network Hacking - Post Connection Attacks",
                  "Network Hacking - Post-Connection Attacks - Information Gathering",
                  "Network Hacking - Post Connection Attacks - MITM Attacks",
                  "Network Hacking - Detection & Security",
                  "Gaining Access To Computers",
                  "Gaining Access - Server Side Attacks",
                  "Gaining Access - Client Side Attacks",
                  "Gaining Access - Client Side Attacks - Social Engineering",
                  "Gaining Access - Hacking Outside The Local Network",
                  "Post Exploitation",
                  "Website Hacking",
                  "Website Hacking - Information Gathering",
                  "Website Hacking - File Upload, Code Execution & File Inclusion Vulns",
                  "Website Hacking - SQL Injection Vulnerabilities",
                  "Website Hacking -  Cross Site Scripting (XSS) Vulnerabilities",
                  "Website Hacking - Discovering Vulnerabilities Automatically",
                  "Bonus Section"
              ]
          },
          "Web Application Security (OWASP Top 10)": {
              "id": 1331472,
              "title": "OWASP top 10 Web Application Security for Absolute Beginners",
              "url": "https://www.udemy.com/course/web-application-security-for-absolute-beginners-no-coding/",
              "description": "Learn OWASP top 10 risks! Jumpstart your cyber security career; increase earnings! Cyber Security | CISO | Ransomware",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/1331472_6b6a_5.jpg",
              "price": "₹3,999",
              "structure": [
                  "OWASP Top 10 Most Critical Web Application Security Risks",
                  "Finalised top 10 in 2017",
                  "New in 2021",
                  "Extra tips!",
                  "Even more additional videos!"
              ]
          },
          "Security Information and Event Management (SIEM)": {
              "id": 2741966,
              "title": "A Guide to Security Information and Event Management - SIEM",
              "url": "https://www.udemy.com/course/a-guide-to-security-information-and-event-management-siem/",
              "description": "Gain hands-on Tool insights using Splunk Enterprise and FortiSIEM. Interview preparation case study, hints and tips",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/2741966_b866_7.jpg",
              "price": "₹2,299",
              "structure": [
                  "Introduction to SIEM",
                  "Key Objectives of SIEM",
                  "Defence in Depth",
                  "Corporate environment",
                  "Log Management",
                  "Why is SIEM necessary?",
                  "Use Cases for SIEM",
                  "Elements of SIEM",
                  "SIEM Deployment Options",
                  "Quiz Time",
                  "Security Operations Center - SOC with Splunk & FortiSIEM",
                  "Network Concepts Refresher, OSI, TCPIP Protocol Suite",
                  "Cyber Security Attacks, Ethical Hacking, DoS, DDoS, SYN Flooding, Metasploit",
                  "Maltego, Cyber Killchain methodology, Information security vectors, Ransomware",
                  "Introduction to Splunk's  UI - User Interface",
                  "Splunk: Using basic transforming commands",
                  "Splunk: Creating Reports and Dashboards",
                  "Splunk: Saving and sharing reports",
                  "Splunk: Dashboards",
                  "Splunk: Creating alerts",
                  "Splunk Enterprise Security",
                  "FortiSIEM: A Case Study on a powerful SIEM",
                  "Types of Viruses",
                  "Security Devices",
                  "Email: SMTP, Email system, webmail architecture - IMAP4 based",
                  "Cyber security incidence response",
                  "Vulnerability Management",
                  "Interview Preparation for Cyber Security Roles & SOC Roles!"
              ]
          },
          "Incident Response & Forensics Fundamentals": {
              "id": 1585012,
              "title": "Build Security Incident Response for GDPR data protection",
              "url": "https://www.udemy.com/course/build-security-incident-response-for-eu-gdpr-compliance/",
              "description": "CIPT, CIPM_FREE GDPR and Incident Response Templates & Documentation - Practical GDPR and Incident Response Blueprint",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/1585012_7514_5.jpg",
              "price": "₹3,099",
              "structure": [
                  "Introduction",
                  "Incident Response in CyberSecurity",
                  "Building a Security Operations Center (SOC)",
                  "GDPR and Incident Response",
                  "GDPR Incident Response Methodologies (IRM)",
                  "Incident Response Tools for GDPR compliance - free vs enterprise",
                  "Banking challenges related to cyber risk",
                  "Financial Malware history with examples",
                  "Making a business case for Financial Malware",
                  "Some simple hacking attempts - demo",
                  "Conclusion"
              ]
          },
          "Security Auditing & Compliance": {
              "id": 5534152,
              "title": "IT Audit: Cybersecurity Audit Project",
              "url": "https://www.udemy.com/course/cybersecurity-audit-fundamentals/",
              "description": "Perform Cybersecurity Audit | Information Security Audit | IT Audit",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/5534152_3694_4.jpg",
              "price": "₹2,299",
              "structure": [
                  "Introduction",
                  "Cybersecurity Audit",
                  "IT Controls",
                  "Cybersecurity Frameworks & Standards",
                  "Cybersecurity Audit Process",
                  "Performing Cybersecurity Audit",
                  "Next Steps"
              ]
          }
      },
      "Level 4": {
          "Advanced Cryptography (Digital Signatures, PKI)": {
              "id": 2624084,
              "title": "Cryptography: A Hands-on Approach",
              "url": "https://www.udemy.com/course/du-cryptography/",
              "description": "Secret-key encryption, one-way hash, public-key cryptography, digital signature, PKI, TLS, cryptocurrency and blockchain",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/2624084_6878_3.jpg",
              "price": "₹2,799",
              "structure": [
                  "Course Overview",
                  "Secret-Key Encryption",
                  "One-Way Hash Function",
                  "Public-Key Cryptography",
                  "Public-Key Infrastructure",
                  "Transport Layer Security",
                  "Bitcoin and Blockchain"
              ]
          },
          "Network Security Protocols (SSL/TLS, VPNs)": {
              "id": 3504366,
              "title": "Computer Network Security Protocols And Techniques",
              "url": "https://www.udemy.com/course/computer-network-security-protocols-cryptography-tls-ssl-ipsec-rsa/",
              "description": "Public-Private Key Cryptography, Hash Functions, End Point Authentication, TLS/SSL, IPsec in VPNs, Integrity Protection",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/3504366_5958_2.jpg",
              "price": "₹1,299",
              "structure": [
                  "Introduction",
                  "Principles Of Cryptography",
                  "The Modern Ciphers",
                  "Asymmetric key cryptography",
                  "Message Authentication/Integrity Protection",
                  "End Point Authentication",
                  "Securing The E-mail",
                  "Transport Layer Security Using TLS/SSL",
                  "Virtual Private Networks",
                  "Firewalls"
              ]
          },
          "Cloud Security (AWS, Azure, GCP)": {
              "id": 2414030,
              "title": "Introduction to Cloud Computing with AWS, Azure and GCP",
              "url": "https://www.udemy.com/course/the-complete-introduction-to-cloud-with-aws-azure-and-gcp/",
              "description": "Understanding cloud computing concepts and introduction to Amazon Web Services,Microsoft Azure and Google Cloud Platform",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/2414030_c422.jpg",
              "price": "₹2,299",
              "structure": [
                  "Overview of Cloud Computing",
                  "Amazon Web Service (AWS)",
                  "Microsoft Azure",
                  "Google Cloud Platform (GCP)",
                  "Comparing Cloud Providers"
              ]
          },
          "Security Automation & Orchestration": {
              "id": 2745980,
              "title": "AWS Advanced Security: SecOps Automation for the cloud",
              "url": "https://www.udemy.com/course/aws-cloud-security-proactive-way/",
              "description": "100% Hands-On | Learn to secure applications on AWS. Defend against threats DDoS Intrusions Vulnerabilities",
              "thumbnail": "https://img-b.udemycdn.com/course/480x270/2745980_ed8b_5.jpg",
              "price": "₹3,099",
              "structure": [
                  "Course Introduction",
                  "Detective Controls: Introduction",
                  "Reactive Controls: Automatically Remediate Non Compliant Resources",
                  "Proactive Security Controls",
                  "Proactive Security Controls: Taking it to the next level",
                  "Next Steps: Assignment",
                  "Resources",
                  "Additional Reading"
              ]
          },
          "Threat Intelligence & Analysis": {
              "id": 5766826,
              "title": "Cyber Threat Intelligence",
              "url": "https://www.udemy.com/course/cyber-threat-intelligence/",
              "description": "Learn Cyber Threat Intelligence | Hands-on experience | Elevate your career to the next level",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/5766826_67b6_2.jpg",
              "price": "₹1,499",
              "structure": [
                  "Introduction",
                  "Basics - SOC",
                  "Basics - Azure",
                  "Basics - Zero Trust & Microsoft Security",
                  "Intelligence",
                  "Cyber Threat Intelligence (CTI)",
                  "CTI-Related Frameworks",
                  "MITRE ATT&CK",
                  "Threat Actors and APTs",
                  "CTI Tools",
                  "CTI Platforms",
                  "Artificial Intelligence (AI) & CTI",
                  "Case Study I - MISP on Azure",
                  "Case Study II - Researching APT41 with ATT&CK",
                  "Case Study III - Leveraging CTI in Microsoft Sentinel",
                  "Case Study IV - Building a CTI Program",
                  "Bonus Section"
              ]
          }
      },
      "Level 5": {
          "Security Architecture & Design": {
              "id": 3081656,
              "title": "Software Architecture Security - The Complete Guide",
              "url": "https://www.udemy.com/course/software-architecture-security-the-complete-guide/",
              "description": "Become a better Software Architect by designing secure systems",
              "thumbnail": "https://img-b.udemycdn.com/course/480x270/3081656_606f.jpg",
              "price": "₹3,299",
              "structure": [
                  "Welcome",
                  "Introduction to Software Security",
                  "Secure Architecture Process",
                  "Threat Modeling",
                  "Secure Architecture",
                  "Application and Data Security",
                  "SDLC",
                  "Testing",
                  "Production",
                  "Case Study",
                  "Conclusion"
              ]
          },
          "DevSecOps & Secure Software Development": {
              "id": 4489006,
              "title": "DevSecOps Fundamentals - Including Hands-On Demos",
              "url": "https://www.udemy.com/course/devsecops-fundamentals/",
              "description": "The complete course covering what you need to know to get started in DevSecOps and exactly how to do it!",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/4489006_9ef6_8.jpg",
              "price": "₹3,099",
              "structure": [
                  "Introduction",
                  "Testing, Tooling and Principles",
                  "Organisations & Projects",
                  "Linux  Security Fundamentals",
                  "Docker",
                  "Terraform",
                  "Jenkins",
                  "Kubernetes",
                  "Pipelines",
                  "Course Summary"
              ]
          },
          "Advanced Penetration Testing & Red Teaming": {
              "id": 984734,
              "title": "Website Hacking / Penetration Testing",
              "url": "https://www.udemy.com/course/learn-website-hacking-penetration-testing-from-scratch/",
              "description": "Hack websites and web applications like black hat hackers and secure them like experts.",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/984734_90be_6.jpg",
              "price": "₹4,099",
              "structure": [
                  "Course Introduction",
                  "Preparation - Creating a Hacking Lab",
                  "Preparation - Linux Basics",
                  "Website Basics",
                  "Information Gathering",
                  "File Upload Vulnerabilities",
                  "Code Execution Vulnerabilities",
                  "Local File Inclusion Vulnerabilities (LFI)",
                  "Remote File Inclusion Vulnerabilities (RFI)",
                  "SQL Injection Vulnerabilities",
                  "SQL Injection Vulnerabilities - SQLi In Login Pages",
                  "SQL injection Vulnerabilities - Extracting Data From The Database",
                  "SQL injection Vulnerabilities - Advanced Exploitation",
                  "XSS Vulnerabilities",
                  "XSS Vulnerabilities - Exploitation",
                  "Insecure Session Management",
                  "Brute Force & Dictionary Attacks",
                  "Discovering Vulnerabilities Automatically Using Owasp ZAP",
                  "Post Exploitation",
                  "Bonus Section"
              ]
          },
          "Cybersecurity Governance, Risk, and Compliance (GRC)": {
              "id": 5559024,
              "title": "The Ultimate GRC Course - Governance, Risk & Compliance 2024",
              "url": "https://www.udemy.com/course/cgrc-training-isc2/",
              "description": "The Ultimate GRC Bootcamp for all GRC folks - Governance, Risk, Compliance Master Course to make you a REAL GRC Expert!",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/5559024_1298_7.jpg",
              "price": "₹1,499",
              "structure": [
                  "Course Introduction - Become a GRC Consultant",
                  "New to the Career?",
                  "Part 1 - Security Essentials for GRC Candidates",
                  "Part 2 - Security Program and Information Security Function",
                  "Part 3 - Regulations and Standards and its influence",
                  "Part 4 - Enterprise Risk Management - ERM",
                  "Part 5 - Security Controls",
                  "Part 6 - Security Governance Tools",
                  "Part 7 - Personnel and Third-Party Risk Management - TRPM",
                  "Part 8 - Information System Auditing and Control Validation",
                  "Part 9 - Guide to Information Systems and Basics of Information Technology",
                  "Part 10 - Endpoint and Data and Physical Security Overview",
                  "Part 11 - Software Development and Security Aspects",
                  "Part 12 - Release Management and Change Management",
                  "Part 13 - The Incident Management and Business Continuity",
                  "What is Next?"
              ]
          },
          "Security Operations Center (SOC) Management": {
              "id": 5266716,
              "title": "The Modern SOC (Security Operations Center)",
              "url": "https://www.udemy.com/course/the-modern-soc-security-operations-center/",
              "description": "Learning critical skills for future SOC success.",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/5266716_5f8b_2.jpg",
              "price": "₹799",
              "structure": [
                  "Introduction",
                  "Final Exam"
              ]
          }
      },
      "Level 6": {
          "Cybersecurity Research & Innovation": {
              "id": 4672448,
              "title": "The Complete Certified in Cybersecurity CC course ISC2 2024",
              "url": "https://www.udemy.com/course/certifiedincybersecurity/",
              "description": "Start your Cyber security career today! Take the Complete Certified in Cybersecurity (CC) beginners course ISC2 - 2024",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/4672448_5ec9_4.jpg",
              "price": "₹3,499",
              "structure": [
                  "Introduction",
                  "Domain 1: Security Principles",
                  "Domain 2: Business Continuity, Disaster Recovery, and Incident Response",
                  "Domain 3: Access Controls Concepts",
                  "Domain 4: Network Security",
                  "Domain 5: Security Operations",
                  "Domain recaps",
                  "The study process, material, tips, tricks and practice tests!"
              ]
          },
          "Advanced Malware Analysis": {
              "id": 1947808,
              "title": "Advanced Malware Analysis",
              "url": "https://www.udemy.com/course/advanced-malware-analysis/",
              "description": "Evade malware using IDA Pro, OllyDbg, and WINDBG",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/1947808_260c_2.jpg",
              "price": "₹1,999",
              "structure": [
                  "Exploring Malware Functionalities",
                  "Malware Advanced Techniques",
                  "Advanced Dynamic Malware Analysis",
                  "Advanced Static Malware Analysis",
                  "How to Detect and Defend against Malware in a Network",
                  "How to Deal with Evasive Malware"
              ]
          },
          "Data Security & Privacy (GDPR, CCPA)": {
              "id": 4584410,
              "title": "4x1 Data Management/Governance/Security/Ethics Masterclass",
              "url": "https://www.udemy.com/course/data-management-and-governance/",
              "description": "You'll learn about data literacy, Data Quality operations, Data Governance policies and Data Security/Privacy controls.",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/4584410_4847.jpg",
              "price": "₹3,099",
              "structure": [
                  "Course Introduction",
                  "Data Literacy and Considerations",
                  "Data and Data Quality (DQ)",
                  "Data Governance",
                  "Data Ethics, Security and Privacy",
                  "Additional Module: Extra Security Controls",
                  "Additional Module: Pitching Technical Projects",
                  "Bonus Lecture"
              ]
          },
          "Cyberwarfare & National Security": {
              "id": 5945312,
              "title": "Master Cyber Security Without Even Prior Experience",
              "url": "https://www.udemy.com/course/master-cyber-security-without-even-prior-experience/",
              "description": "Accelerate Your Cybersecurity Career",
              "thumbnail": "https://img-b.udemycdn.com/course/480x270/5945312_ab6c.jpg",
              "price": "₹1,499",
              "structure": [
                  "Introduction",
                  "The Need for Cybersecurity",
                  "Attacks, Concepts and Techniques",
                  "Protecting your data and privacy",
                  "Protecting The organization",
                  "Will Your Future Be In Cybersecurity ?",
                  "Next Steps"
              ]
          },
          "Emerging Cybersecurity Trends & Technologies": {
              "id": 5539304,
              "title": "Advanced Cybersecurity and Ethical Hacking with ChatGPT",
              "url": "https://www.udemy.com/course/advanced-cybersecurity-and-ethical-hacking-with-chatgpt/",
              "description": "Master Cybersecurity with ChatGPT Ethical Hacking & AI-Powered Threat Analysis - Explore Networking, Cloud, & Compliance",
              "thumbnail": "https://img-c.udemycdn.com/course/480x270/5539304_cdbe_2.jpg",
              "price": "₹799",
              "structure": [
                  "Section 1: Introduction to Cybersecurity and Ethical Hacking",
                  "Foundations of Cybersecurity and Hacking",
                  "Getting Started with ChatGPT",
                  "Information Gathering with ChatGPT",
                  "Vulnerability Identification and Assessment",
                  "Exploitation and Penetration Testing",
                  "Advanced Ethical Hacking Techniques",
                  "Protecting Against Cyber Attacks",
                  "ChatGPT for Security Innovation",
                  "Emerging Trends and Future of Cybersecurity",
                  "Case Studies and Real-World Scenarios",
                  "Secure Development and DevSecOps",
                  "Cybersecurity Regulations and Compliance",
                  "Ethical Hacking in Cloud Environments",
                  "CTF Challenges and Capture The Flag Events",
                  "Final Projects and Practical Assessments",
                  "Professional Development and Career Insights",
                  "Additional Insights: Cyber / GPT Landscape, Data Collection, NLP & Architecture",
                  "ChatGPT & Cyber Security: Fraud, Insiders, Phishing, Malware, Threats",
                  "ChatGPT & Cyber Security: Vulnerabilities, Access Control. Monitoring, Threats",
                  "ChatGPT & Cyber Security: Networks, Testings, IAM, Data Privacy, Encryption",
                  "ChatGPT & Cyber Security: Cloud, Web, Social Engineering, Incidents & Compliance",
                  "ChatGPT & Cyber Security: Training, Machine Learning, Mobile, Ops & The Future"
              ]
          }
      }
    }
  }

  return HttpResponse(
    json.dumps(roadmap),
    content_type="application/json"
  )
    
@csrf_exempt
def generate_mcqs(request):
    if request.method == "GET":
        topic_name = request.GET.get('name', None)
        
        if not topic_name:
            return JsonResponse({'error': 'Topic name is required'}, status=400)
        
        genai.configure(api_key="AIzaSyBzjohOuPQSaNZ9hTJBYCiKLwpC_8_PSMo")
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        You have the following topic {topic_name}. Give me 10 questions, 5 of which are objective and contain 4 options, the remaining 5 are subjective questions ensure that you do NOT give me answers for them. The questions should cover essentials in that topic. The questions are required for a preparatory quiz for a job interview, so keep the questions at industry level difficulty only, do not keep the questions of easy difficulty. Ensure there are no redundant questions and that you give exact 10 MCQs with only 1 correct answer. Ensure that you only give the questions and the answer key as the response with no extra text. Do not include any bolded letters or any sort of font formatting. Give the output in JSON format.
        """
        
        response = model.generate_content(prompt).text
        
        return HttpResponse(response, content_type = "application/json")


def generate_interview_questions(request):
  if request.method == "GET":
    skill = request.GET.get('skill', None)
    skill_level = request.GET.get('skill_level', None)

    genai.configure(api_key="AIzaSyBzjohOuPQSaNZ9hTJBYCiKLwpC_8_PSMo")
        
    model = genai.GenerativeModel('gemini-1.5-flash')

    if skill is None:
      return JsonResponse({'error': 'Skill not provided'}, status=400)

    if skill_level is None:
      return JsonResponse({'error': 'Skill level not provided'}, status=400)

    interview_prompt = f"""
    Create a comprehensive set of 5 subjective questions for {skill}, for someone with a skill of {skill_level}. The questions are required for a preparatory quiz for a job interview, so keep the questions at industry level difficulty only, do not keep the questions of easy difficulty. Ensure there are no redundant questions. The questions should only include things one can be asked in an interview. Ensure that you only give the questions and there should be NO answer key as the response with no extra text. Do not include any bolded letters or any sort of font formatting. Give the output in JSON format.
    """
    response = model.generate_content(interview_prompt).text
        
    return HttpResponse(response, content_type = "application/json")

    # return HttpResponse(
    #   interview_response,
    #   content_type="application/json"
    # )
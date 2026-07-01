
import os
import sys
import socket
import subprocess
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000
SERVER_LOG = "server.log"

SYSTEM_PROMPT = """
Esti Profesor AI, un asistent educational integrat intr-un proiect GNS3 de rete.
Raspunzi in romana, clar, practic si pe pasi.

Context proiect:
- Site A: VLAN 10, VLAN 20, VLAN 99 management.
- Site B: VLAN 30, VLAN 40, VLAN 99 management.
- Customer Office: EtherChannel PAgP/LACP.
- Core/WAN: RIPv2, rute default, rute statice.
- Admin: SSH, Telnet pe SW5, SCP backup, NetworkAutomation.
- DMZ: 192.168.100.0/24, ACL DMZ_IN, Snort/Darkstat.
- Security Edge: FortiGate intre BORDER si ISP.
- Site Profesor: 172.16.50.0/24, separat de topologia principala.

Reguli:
- Nu inventa topologie noua.
- Daca nu esti sigur, cere comenzi de verificare precum show ip interface brief.
- Explica output-urile Cisco pe intelesul unui student.
- Pune accent pe troubleshooting.
"""

app = Flask(__name__)


def ask_openai(question):
    if not OPENAI_API_KEY or OPENAI_API_KEY == "PASTE_OPENAI_KEY_HERE":
        return "Cheia OpenAI nu este configurata. Editeaza fisierul .env si pun"

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=data, timeout=60)

    if response.status_code != 200:
        return f"Eroare API OpenAI {response.status_code}: {response.text}"

    result = response.json()
    return result["choices"][0]["message"]["content"]


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Profesor AI API",
        "status": "running",
        "usage": "POST /ask cu JSON: {\"question\": \"intrebarea ta\"}"
    })


@app.route("/ask", methods=["POST"])
def ask_api():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Lipseste campul question."}), 400

    answer = ask_openai(question)
    return jsonify({"question": question, "answer": answer})


def run_api_server():
    app.run(host="0.0.0.0", port=5000)


def is_server_running():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((SERVER_HOST, SERVER_PORT))
    sock.close()
    return result == 0


def start_api_server():
    if is_server_running():
        print("\nServerul API ruleaza deja pe portul 5000.")
        return

    log_file = open(SERVER_LOG, "a")

    subprocess.Popen(
        [sys.executable, "main.py", "--server"],
        stdout=log_file,
        stderr=log_file,
        start_new_session=True
    )

    print("\nServerul API a fost pornit in background.")
    print("Adresa locala: http://127.0.0.1:5000")
    print("Endpoint intrebari: http://127.0.0.1:5000/ask")


def stop_api_server():
    subprocess.run(
        ["pkill", "-f", "main.py --server"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print("\nServerul API a fost oprit.")


def show_server_log():
    print("\n--- Ultimele linii din server.log ---\n")

    if not os.path.exists(SERVER_LOG):
        print("server.log nu exista inca.")
        return

    subprocess.run(["tail", "-n", "20", SERVER_LOG])


def chat_local():
    print("\n--- Chat local cu Profesor AI ---")
    print("Scrie exit pentru revenire la meniu.\n")

    while True:
        question = input("Student: ").strip()

        if question.lower() in ["exit", "quit", "0"]:
            print("Revenire la meniu...")
            break

        if not question:
            continue

        print("\nProfesor AI:")
        print(ask_openai(question))
        print()


def test_openai_connection():
    print("\n--- Test conexiune OpenAI ---\n")
    print(ask_openai("Raspunde doar cu: Conexiunea OpenAI functioneaza."))


def menu():
    while True:
        print("\n========================================")
        print("       Profesor AI - Meniu principal")
        print("========================================")
        print("1. Porneste serverul API in background")
        print("2. Chat local cu Profesor AI")
        print("3. Testeaza conexiunea OpenAI")
        print("4. Afiseaza ultimele linii din server.log")
        print("5. Opreste serverul API")
        print("0. Iesire")
        print("========================================")

        choice = input("Alege optiunea: ").strip()

        if choice == "1":
            start_api_server()
        elif choice == "2":
            chat_local()
        elif choice == "3":
            test_openai_connection()
        elif choice == "4":
            show_server_log()
        elif choice == "5":
            stop_api_server()
        elif choice == "0":
            print("Iesire...")
            break
        else:
            print("Optiune invalida.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--server":
        run_api_server()
    else:
        menu()

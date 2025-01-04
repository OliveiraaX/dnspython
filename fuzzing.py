import requests
import sys
import threading

# Função para escanear uma parte da wordlist
def scanner(url, wordlist):
    for nome in wordlist:
        try:
            site = "{}/{}".format(url, nome.strip())
            resposta = requests.get(site)
            code = resposta.status_code
            if code != 404:
                print("{} == {}".format(nome.strip(), code))
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as error:
            print(f"Erro: {error}")
            pass

# Função principal para dividir a wordlist entre threads
def start_scanner(url, wordlist, num_threads=10):
    # Dividindo a wordlist em partes iguais para cada thread
    chunk_size = len(wordlist) // num_threads
    threads = []

    for i in range(num_threads):
        # Divisão da lista de palavras para cada thread
        start = i * chunk_size
        # Se for a última thread, pega o resto da lista
        end = None if i == num_threads - 1 else (i + 1) * chunk_size
        thread_wordlist = wordlist[start:end]

        # Criando e iniciando a thread
        thread = threading.Thread(target=scanner, args=(url, thread_wordlist))
        threads.append(thread)
        thread.start()

    # Aguardando todas as threads terminarem
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python script.py <url> <wordlist> [num_threads]")
        sys.exit(1)

    url = sys.argv[1]
    wordlist_path = sys.argv[2]
    num_threads = int(sys.argv[3]) if len(sys.argv) > 3 else 10  # Número de threads (default: 10)

    # Lendo a wordlist do arquivo
    with open(wordlist_path, "r") as file:
        wordlist = file.readlines()

    # Iniciando o scanner com threads
    start_scanner(url, wordlist, num_threads)

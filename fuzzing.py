import requests 
import sys
import threading

def scanner (url, wordlist):
    for nome in wordlist:
        try:
            site = "{}/{}".format(url, nome.strip()) 
            resposta = requests.get(site)
            code = resposta.status_code
            if code != 404:
                print("{} == {}".format(nome, code))
        except KeyboardInterrupt: 
            sys.exit(0)
        except Exception as error:
            print(error)
            pass

def start_scanner(url, wordlist, num_threads=10):
    chunk_size = len(wordlist) // num_threads
    threads = []

    for i in range(num_threads):
        start = i * chunk_size

        end = None if i == num_threads - 1 else (i + 1) * chunk_size
        thread_wordlist = wordlist[start:end]

        thread = threading.Thread(target=scanner, args=(url, thread_wordlist))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python script.py <url> <wordlist> [num_threads]")
        sys.exit(1)

    url = sys.argv[1]
    wordlist_path = sys.argv[2]
    num_threads = int(sys.argv[3]) if len(sys.argv) > 3 else 10 

    with open(wordlist_path, "r") as file:
        wordlist = file.readlines()

    start_scanner(url, wordlist, num_threads)

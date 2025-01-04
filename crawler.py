import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urlparse, urljoin
import threading
from queue import Queue, Empty

# Função para buscar e analisar links de uma página
def fetch_links(url, visited_urls, to_visit, lock, level=0):
    if url in visited_urls:
        return
    
    with lock:
        visited_urls.add(url)
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return  # Ignora erros de acesso
    
    print(" " * level * 2 + url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(url, href)
        if urlparse(full_url).netloc == urlparse(url).netloc:
            with lock:
                if full_url not in visited_urls:
                    to_visit.put((full_url, level + 1))

# Worker para processar URLs na fila
def worker(to_visit, visited_urls, lock, stop_event):
    while not stop_event.is_set():
        try:
            current_url, level = to_visit.get(timeout=1)
            fetch_links(current_url, visited_urls, to_visit, lock, level)
            to_visit.task_done()
        except Empty:
            continue
        except KeyboardInterrupt:
            stop_event.set()
            break

# Função principal para iniciar o crawler
def crawl(url):
    visited_urls = set()
    to_visit = Queue()
    lock = threading.Lock()
    stop_event = threading.Event()

    to_visit.put((url, 0))
    
    threads = []
    for _ in range(10):
        thread = threading.Thread(target=worker, args=(to_visit, visited_urls, lock, stop_event))
        thread.daemon = True
        thread.start()
        threads.append(thread)

    to_visit.join()
    stop_event.set()
    for thread in threads:
        thread.join()

# Ponto de entrada
if __name__ == "__main__":
    if len(sys.argv) > 1:
        start_url = sys.argv[1]
        crawl(start_url)
    else:
        print("Por favor, forneça uma URL para rastrear.")

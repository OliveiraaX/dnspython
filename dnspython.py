import sys
import dns.resolver

# Verificar se o número correto de argumentos foi passado
if len(sys.argv) != 3:
    print("Uso: python3 dnspython.py dominio wordlist.txt")
    sys.exit(1)

alvo = sys.argv[1]  # Domínio alvo
wordlist = sys.argv[2]  # Caminho para o arquivo da wordlist

# Tentar abrir o arquivo de wordlist
try:
    with open(wordlist, "r") as arq:
        subdominios = arq.read().splitlines()
except FileNotFoundError:
    print(f"Erro: Arquivo '{wordlist}' não encontrado.")
    sys.exit(1)
except Exception as e:
    print(f"Erro ao abrir o arquivo: {e}")
    sys.exit(1)

# Resolver subdomínios
resolver = dns.resolver.Resolver()

for subdominio in subdominios:
    sub_alvo = "{}.{}".format(subdominio, alvo)
    try:
        # Tenta resolver o registro A do subdomínio
        resultados = resolver.resolve(sub_alvo, "A")
        for resultado in resultados:
            print(f"{sub_alvo} -> {resultado}")
    except dns.resolver.NoAnswer:
        # Caso não tenha resposta para o subdomínio
        pass
    except dns.resolver.NXDOMAIN:
        # Caso o subdomínio não exista
        pass
    except Exception as e:
        # Captura outras exceções e imprime
        print(f"Erro ao tentar resolver {sub_alvo}: {e}")

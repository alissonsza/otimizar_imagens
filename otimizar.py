from PIL import Image
import os

def get_tamanho_kb(caminho):
    try:
        return os.path.getsize(caminho) / 1024
    except:
        return 0

def otimizar_imagem(caminho_original, caminho_destino, qualidade=70):
    try:
        tamanho_original = get_tamanho_kb(caminho_original)

        with Image.open(caminho_original) as img:
            img.convert("RGB").save(caminho_destino, optimize=True, quality=qualidade)

        tamanho_final = get_tamanho_kb(caminho_destino)
        return True, tamanho_original, tamanho_final
    except Exception as e:
        print(f"Erro ao otimizar {caminho_original}: {e}")
        return False, 0, 0

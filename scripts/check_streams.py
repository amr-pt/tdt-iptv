#!/usr/bin/env python3
"""
Script para verificar a disponibilidade dos streams IPTV
"""

import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import json
import sys
import os


def parse_m3u(file_path):
    """Ler ficheiro M3U e extrair informação dos canais"""
    channels = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    current_channel = None
    
    for line in lines:
        line = line.strip()
        
        # Verificar linha EXTINF
        if line.startswith('#EXTINF:'):
            # Extrair nome do canal do EXTINF
            match = re.search(r',(.+)$', line)
            if match:
                channel_name = match.group(1).strip()
                # Extrair URL do logo
                logo_match = re.search(r'tvg-logo="([^"]+)"', line)
                logo_url = logo_match.group(1) if logo_match else None
                
                current_channel = {
                    'name': channel_name,
                    'extinf': line,
                    'url': None,
                    'logo_url': logo_url,
                    'headers': {},
                    'status': None,
                    'logo_status': None,
                    'error': None,
                    'logo_error': None
                }
        
        # Verificar linhas EXTVLCOPT (headers e opções)
        elif line.startswith('#EXTVLCOPT:') and current_channel:
            # Analisar opções EXTVLCOPT
            option = line.replace('#EXTVLCOPT:', '')
            
            # Analisar http-user-agent
            if option.startswith('http-user-agent='):
                current_channel['headers']['User-Agent'] = option.split('=', 1)[1]
            
            # Analisar http-origin
            elif option.startswith('http-origin='):
                current_channel['headers']['Origin'] = option.split('=', 1)[1]
            
            # Analisar http-referrer
            elif option.startswith('http-referrer='):
                current_channel['headers']['Referer'] = option.split('=', 1)[1]
        
        # Verificar linha de URL (não começa com #)
        elif line and not line.startswith('#') and current_channel:
            current_channel['url'] = line
            channels.append(current_channel)
            current_channel = None
    
    return channels


def check_stream(channel, timeout=10):
    """Verificar se um stream está acessível"""
    url = channel['url']
    
    # Ignorar URLs placeholder
    if url == '#':
        channel['status'] = 'placeholder'
        return channel
    
    # Preparar headers
    headers = channel.get('headers', {}).copy()
    
    # Adicionar User-Agent predefinido se não especificado
    if 'User-Agent' not in headers:
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    
    try:
        # Tentar pedido HEAD primeiro (mais rápido)
        response = requests.head(
            url,
            timeout=timeout,
            allow_redirects=True,
            headers=headers
        )
        
        if response.status_code in [200, 206, 302, 301]:
            channel['status'] = 'working'
            channel['http_status'] = response.status_code
            channel['method'] = 'HEAD'
        else:
            # Se o HEAD falhar, tentar pedido GET (alguns servidores não suportam HEAD)
            response = requests.get(
                url,
                timeout=timeout,
                allow_redirects=True,
                headers=headers,
                stream=True  # Não descarregar o conteúdo completo
            )
            
            # Ler apenas os primeiros bytes para verificar se é um stream válido
            try:
                content = next(response.iter_content(chunk_size=1024))
                response.close()
                
                if response.status_code in [200, 206, 302, 301]:
                    channel['status'] = 'working'
                    channel['http_status'] = response.status_code
                    channel['method'] = 'GET'
                else:
                    channel['status'] = 'not_working'
                    channel['http_status'] = response.status_code
                    channel['error'] = f'HTTP {response.status_code}'
            except:
                # Se não conseguirmos ler o conteúdo, mas tivermos um bom código de estado, marcar como a funcionar
                if response.status_code in [200, 206, 302, 301]:
                    channel['status'] = 'working'
                    channel['http_status'] = response.status_code
                    channel['method'] = 'GET'
                else:
                    channel['status'] = 'not_working'
                    channel['http_status'] = response.status_code
                    channel['error'] = f'HTTP {response.status_code}'
    
    except requests.exceptions.Timeout:
        channel['status'] = 'timeout'
        channel['error'] = 'Pedido excedeu o tempo limite'
    
    except requests.exceptions.RequestException as e:
        channel['status'] = 'error'
        channel['error'] = str(e)
    
    return channel


def check_logo(channel, timeout=5):
    """Verificar se o logo de um canal está acessível"""
    logo_url = channel.get('logo_url')
    
    if not logo_url:
        channel['logo_status'] = 'no_logo'
        return channel
    
    try:
        response = requests.head(
            logo_url,
            timeout=timeout,
            allow_redirects=True,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        
        if response.status_code in [200, 206, 302, 301]:
            channel['logo_status'] = 'working'
            channel['logo_http_status'] = response.status_code
        else:
            channel['logo_status'] = 'not_working'
            channel['logo_http_status'] = response.status_code
            channel['logo_error'] = f'HTTP {response.status_code}'
    
    except requests.exceptions.Timeout:
        channel['logo_status'] = 'timeout'
        channel['logo_error'] = 'Pedido excedeu o tempo limite'
    
    except requests.exceptions.RequestException as e:
        channel['logo_status'] = 'error'
        channel['logo_error'] = str(e)
    
    return channel


def generate_report(channels, output_file=None):
    """Gerar um relatório do estado dos streams e logos"""
    total = len(channels)
    working = sum(1 for c in channels if c['status'] == 'working')
    placeholder = sum(1 for c in channels if c['status'] == 'placeholder')
    not_working = sum(1 for c in channels if c['status'] in ['not_working', 'error', 'timeout'])
    
    # Estatísticas de logos
    logos_with = sum(1 for c in channels if c.get('logo_url'))
    logos_working = sum(1 for c in channels if c.get('logo_status') == 'working')
    logos_not_working = sum(1 for c in channels if c.get('logo_status') in ['not_working', 'error', 'timeout'])
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total': total,
            'streams': {
                'working': working,
                'placeholder': placeholder,
                'not_working': not_working,
                'percentage_working': round((working / total * 100) if total > 0 else 0, 2)
            },
            'logos': {
                'with_logo': logos_with,
                'working': logos_working,
                'not_working': logos_not_working,
                'percentage_working': round((logos_working / logos_with * 100) if logos_with > 0 else 0, 2)
            }
        },
        'channels': channels
    }
    
    # Imprimir resumo
    print("\n" + "="*60)
    print("📊 RELATÓRIO DE STREAMS E LOGOS")
    print("="*60)
    print(f"Total de canais: {total}")
    print("\n📺 Streams:")
    print(f"  ✅ A funcionar: {working} ({report['summary']['streams']['percentage_working']}%)")
    print(f"  ⚪ Placeholders: {placeholder}")
    print(f"  ❌ A não funcionar: {not_working}")
    print(f"\n🖼️  Logos:")
    print(f"  📊 Com logo: {logos_with}")
    print(f"  ✅ A funcionar: {logos_working} ({report['summary']['logos']['percentage_working']}%)")
    print(f"  ❌ A não funcionar: {logos_not_working}")
    print("="*60 + "\n")
    
    # Imprimir canais a não funcionar
    if not_working > 0:
        print("📋 Canais a não funcionar:")
        print("-" * 60)
        for channel in channels:
            if channel['status'] in ['not_working', 'error', 'timeout']:
                status_icon = '⏱️' if channel['status'] == 'timeout' else '❌'
                print(f"{status_icon} {channel['name']}")
                print(f"   URL: {channel['url']}")
                print(f"   Erro: {channel.get('error', 'N/A')}")
                print()
    
    # Imprimir logos a não funcionar
    if logos_not_working > 0:
        print("🖼️  Logos a não funcionar:")
        print("-" * 60)
        for channel in channels:
            if channel.get('logo_status') in ['not_working', 'error', 'timeout']:
                status_icon = '⏱️' if channel.get('logo_status') == 'timeout' else '❌'
                print(f"{status_icon} {channel['name']}")
                print(f"   Logo URL: {channel.get('logo_url', 'N/A')}")
                print(f"   Erro: {channel.get('logo_error', 'N/A')}")
                print()
    
    # Guardar em ficheiro se especificado
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"📄 Relatório guardado em: {output_file}")
    
    return report


def main():
    # Obter o diretório onde o script está localizado
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    m3u_file = os.path.join(project_dir, 'playlists', 'tdt.m3u')
    output_file = os.path.join(project_dir, 'output', 'stream_status_report.json')
    
    print("🔍 A analisar ficheiro M3U...")
    channels = parse_m3u(m3u_file)
    print(f"📺 Encontrados {len(channels)} canais")
    
    print("\n🔄 A verificar streams (isto pode demorar alguns minutos)...")
    
    # Verificar streams em paralelo
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_stream, channel): channel for channel in channels}
        
        for i, future in enumerate(as_completed(futures), 1):
            channel = future.result()
            print(f"  [{i}/{len(channels)}] {channel['name']}: {channel['status']}")
    
    print("\n🖼️  A verificar logos...")
    
    # Verificar logos em paralelo
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_logo, channel): channel for channel in channels}
        
        for i, future in enumerate(as_completed(futures), 1):
            channel = future.result()
        print(f"  Verificados {len(channels)} logos")
    
    # Gerar relatório
    generate_report(channels, output_file)
    
    print("\n✅ Verificação concluída!")


if __name__ == '__main__':
    main()

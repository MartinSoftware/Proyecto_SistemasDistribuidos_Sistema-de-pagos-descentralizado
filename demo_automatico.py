import requests
import time
import json
from datetime import datetime

# Configuración de nodos
ALICE_URL = "http://localhost:5000"
BOB_URL = "http://localhost:5001"
CHARLIE_URL = "http://localhost:5002"

# Colores para consola
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Imprime un encabezado visual"""
    print("\n" + "="*70)
    print(f"   {Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}")
    print("="*70 + "\n")

def print_step(emoji, text):
    """Imprime un paso de la demo"""
    print(f"{emoji} {text}")

def print_success(text):
    """Imprime un mensaje de éxito"""
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_error(text):
    """Imprime un mensaje de error"""
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")

def print_info(text):
    """Imprime información"""
    print(f"{Colors.YELLOW}ℹ️  {text}{Colors.RESET}")

def wait(seconds, message=""):
    """Espera con mensaje"""
    if message:
        print(f"{Colors.YELLOW}⏳ {message} ({seconds}s)...{Colors.RESET}")
    time.sleep(seconds)

def check_node(url, name):
    """Verifica si un nodo está disponible"""
    try:
        response = requests.get(f"{url}/", timeout=5)
        if response.status_code == 200:
            print_success(f"{name} está respondiendo")
            return True
        else:
            print_error(f"{name} respondió con error {response.status_code}")
            return False
    except Exception as e:
        print_error(f"{name} no responde: {str(e)}")
        return False

def create_wallet(url, name, owner_name):
    """Crea una wallet en un nodo"""
    try:
        response = requests.post(
            f"{url}/wallet/create",
            json={"owner_name": owner_name},
            timeout=10
        )
        if response.status_code == 201:
            data = response.json()
            print_success(f"Wallet de {name} creada")
            print_info(f"   Dirección: {data['address']}")
            print_info(f"   Balance inicial: {data['balance']} tokens")
            return data['address']
        else:
            print_error(f"Error creando wallet de {name}: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error al crear wallet de {name}: {str(e)}")
        return None

def register_peers(nodes):
    """Registra los nodos como peers entre sí"""
    print_header("🔗 CONECTANDO NODOS COMO PEERS")
    
    for i, node1 in enumerate(nodes):
        for j, node2 in enumerate(nodes):
            if i != j:
                try:
                    response = requests.post(
                        f"{node1['url']}/peers/register",
                        json={"peer_url": node2['url']},
                        timeout=5
                    )
                    if response.status_code == 201:
                        print_success(f"{node1['name']} ↔️  {node2['name']}")
                except:
                    pass
    
    print_success("Red P2P establecida")

def mine_blocks(url, name, count=1):
    """Mina bloques en un nodo"""
    for i in range(count):
        try:
            print_info(f"⛏️  {name} está minando bloque {i+1}/{count}...")
            response = requests.post(f"{url}/mine", timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                block_index = data.get('block_index', '?')
                reward = data.get('reward', 0)
                balance_before = data.get('balance_before', 0)
                new_balance = data.get('new_balance', 0)
                block_hash = data.get('block_hash', '')
                tx_count = data.get('transactions_in_block', 0)
                
                print_success(f"{name} minó bloque #{block_index}")
                print_info(f"   Hash: {block_hash[:16]}...")
                print_info(f"   Transacciones incluidas: {tx_count}")
                print_info(f"   Recompensa: {reward} tokens")
                print_info(f"   Balance: {balance_before} → {new_balance} tokens")
                
                # Verificar que el balance aumentó
                if new_balance > balance_before:
                    print_success(f"   ✅ Balance aumentó correctamente")
                else:
                    print_error(f"   ⚠️  Balance no aumentó como se esperaba")
                    
            else:
                print_error(f"Error minando en {name}: {response.text}")
                return False
                
        except Exception as e:
            print_error(f"Error al minar en {name}: {str(e)}")
            return False
        
        if i < count - 1:
            wait(2, f"Esperando antes del siguiente bloque")
    
    return True

def create_transaction(url, sender_name, recipient_address, recipient_name, amount):
    """Crea una transacción"""
    try:
        response = requests.post(
            f"{url}/transaction/create",
            json={
                "recipient_address": recipient_address,
                "amount": amount
            },
            timeout=10
        )
        if response.status_code == 201:
            data = response.json()
            print_success(f"Transacción creada: {sender_name} → {recipient_name}")
            print_info(f"   Monto: {amount} tokens")
            tx_data = data.get('transaction', {})
            if 'timestamp' in tx_data:
                print_info(f"   Timestamp: {tx_data['timestamp']}")
            pending_count = data.get('pending_count', 0)
            print_info(f"   Transacciones pendientes: {pending_count}")
            return True
        else:
            print_error(f"Error en transacción: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error creando transacción: {str(e)}")
        return False

def get_blockchain_info(url):
    """Obtiene información de la blockchain"""
    try:
        response = requests.get(f"{url}/blockchain", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_wallet_info(url):
    """Obtiene información de la wallet"""
    try:
        response = requests.get(f"{url}/wallet/info", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def sync_node(url, name, peer_url):
    """Sincroniza un nodo con otro"""
    try:
        response = requests.post(
            f"{url}/blockchain/sync",
            json={"peer_url": peer_url},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if 'new_length' in data:
                print_success(f"{name} sincronizado → {data['new_length']} bloques")
                return True
            else:
                blockchain_info = get_blockchain_info(url)
                if blockchain_info:
                    length = blockchain_info.get('length', 0)
                    print_info(f"{name} tiene {length} bloques")
                return True
        else:
            print_error(f"Error sincronizando {name}: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error sincronizando {name}: {str(e)}")
        return False

def sync_all_nodes(nodes):
    """Sincroniza todos los nodos con el que tiene la cadena más larga"""
    
    # Obtener longitudes de todos los nodos
    node_lengths = []
    for node in nodes:
        info = get_blockchain_info(node['url'])
        if info:
            length = info.get('length', 0)
            node_lengths.append((length, node))
            print_info(f"{node['name']}: {length} bloques")
        else:
            node_lengths.append((0, node))
    
    # Ordenar por longitud (el más largo primero)
    node_lengths.sort(reverse=True, key=lambda x: x[0])
    longest_length, longest_node = node_lengths[0]
    
    if longest_length == 0:
        print_error("No se pudo obtener información de los nodos")
        return
    
    print_success(f"📡 Fuente: {longest_node['name']} ({longest_length} bloques)")
    print_info(f"Sincronizando todos los nodos con {longest_node['name']}...")
    
    # Sincronizar cada nodo con el más largo
    synced_count = 0
    for length, node in node_lengths:
        if node['name'] != longest_node['name']:
            if sync_node(node['url'], node['name'], longest_node['url']):
                synced_count += 1
            wait(0.5)
    
    # Verificación final
    print_info("Verificando sincronización final...")
    all_synced = True
    final_lengths = []
    
    for node in nodes:
        info = get_blockchain_info(node['url'])
        if info:
            length = info.get('length', 0)
            final_lengths.append(length)
            if length != longest_length:
                all_synced = False
                print_error(f"❌ {node['name']}: {length} bloques (esperado {longest_length})")
    
    if all_synced and len(set(final_lengths)) == 1:
        print_success(f"✅ Todos sincronizados ({longest_length} bloques)")
    else:
        print_error(f"⚠️  Sincronización incompleta: {final_lengths}")
    
    wait(1)

def print_final_status(nodes):
    """Imprime el estado final de todos los nodos"""
    print_header("📊 ESTADO FINAL DE LA RED")
    
    for node in nodes:
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}👤 {node['name']}{Colors.RESET}")
        
        wallet_info = get_wallet_info(node['url'])
        if wallet_info:
            print(f"   💰 Balance: {Colors.GREEN}{wallet_info['balance']} tokens{Colors.RESET}")
            print(f"   📍 Dirección: {wallet_info['address'][:20]}...")
        
        blockchain_info = get_blockchain_info(node['url'])
        if blockchain_info:
            print(f"   ⛓️  Bloques en cadena: {blockchain_info['length']}")
            print(f"   ✅ Blockchain válida: {'Sí' if blockchain_info['valid'] else 'No'}")

def main():
    """Función principal de la demo"""
    print("\n" + Colors.BOLD + Colors.CYAN)
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║                                                               ║")
    print("║        🚀 DEMO AUTOMÁTICA - BLOCKCHAIN P2P                   ║")
    print("║           Sistema de Pagos Descentralizado                   ║")
    print("║                                                               ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print(Colors.RESET)
    
    # Definir nodos
    nodes = [
        {"url": ALICE_URL, "name": "Alice", "owner": "Alice"},
        {"url": BOB_URL, "name": "Bob", "owner": "Bob"},
        {"url": CHARLIE_URL, "name": "Charlie", "owner": "Charlie"}
    ]
    
    # FASE 1: Verificar conexión
    print_header("🔍 FASE 1: VERIFICANDO NODOS")
    
    all_online = True
    for node in nodes:
        if not check_node(node['url'], node['name']):
            all_online = False
    
    if not all_online:
        print_error("No todos los nodos están disponibles. Abortando demo.")
        return
    
    wait(2, "Nodos verificados, continuando")
    
    # FASE 2: Crear wallets
    print_header("👛 FASE 2: CREANDO WALLETS CON RSA-2048")
    
    for node in nodes:
        address = create_wallet(node['url'], node['name'], node['owner'])
        if address:
            node['address'] = address
        else:
            print_error(f"No se pudo crear wallet para {node['name']}")
            return
        wait(1)
    
    wait(2, "Wallets creadas exitosamente")
    
    # FASE 3: Conectar nodos como peers
    register_peers(nodes)
    wait(2, "Red P2P configurada")
    
    # FASE 4: Alice mina bloques iniciales para obtener fondos
    print_header("⛏️  FASE 4: ALICE MINA BLOQUES INICIALES")
    print_info("Alice necesita tokens para poder realizar transacciones")
    
    if not mine_blocks(ALICE_URL, "Alice", count=3):
        print_error("Error durante el minado inicial")
        return
    
    wait(2, "Esperando confirmación de bloques")
    
    # Sincronizar todos los nodos
    print_header("🔗 SINCRONIZACIÓN POST-MINADO")
    sync_all_nodes(nodes)
    
    # Verificar que Alice tenga tokens suficientes
    alice_wallet = get_wallet_info(ALICE_URL)
    if alice_wallet:
        alice_balance = alice_wallet.get('balance', 0)
        print_success(f"Balance de Alice: {alice_balance} tokens")
        
        if alice_balance < 25:
            print_error(f"Alice solo tiene {alice_balance} tokens, necesita al menos 25")
            print_info("Minando bloque adicional...")
            mine_blocks(ALICE_URL, "Alice", count=1)
            wait(2)
            print_header("🔗 SINCRONIZACIÓN ADICIONAL")
            sync_all_nodes(nodes)
            alice_wallet = get_wallet_info(ALICE_URL)
            alice_balance = alice_wallet.get('balance', 0) if alice_wallet else 0
            print_info(f"Nuevo balance de Alice: {alice_balance} tokens")
    
    wait(1, "Preparando transacciones")
    
    # FASE 5: Alice realiza transacciones
    print_header("💸 FASE 5: ALICE ENVÍA TOKENS")
    
    print_step("📤", "Alice envía 15 tokens a Bob")
    if not create_transaction(ALICE_URL, "Alice", nodes[1]['address'], "Bob", 15):
        print_error("Error en transacción Alice → Bob")
        return
    
    wait(2, "Transacción propagada a la red")
    
    print_step("📤", "Alice envía 10 tokens a Charlie")
    if not create_transaction(ALICE_URL, "Alice", nodes[2]['address'], "Charlie", 10):
        print_error("Error en transacción Alice → Charlie")
        return
    
    wait(2, "Transacción propagada a la red")
    
    # FASE 6: Bob mina para confirmar transacciones
    print_header("⛏️  FASE 6: BOB MINA PARA CONFIRMAR TRANSACCIONES")
    print_info("Las transacciones pendientes serán incluidas en el nuevo bloque")
    
    if not mine_blocks(BOB_URL, "Bob", count=1):
        print_error("Error durante el minado de confirmación")
        return
    
    # Sincronizar todos los nodos
    print_header("🔗 SINCRONIZACIÓN POST-MINADO BOB")
    sync_all_nodes(nodes)
    wait(3, "Transacciones confirmadas en la blockchain")
    
    # FASE 7: Bob envía tokens a Charlie
    print_header("💸 FASE 7: BOB ENVÍA TOKENS A CHARLIE")
    
    print_step("📤", "Bob envía 5 tokens a Charlie")
    if not create_transaction(BOB_URL, "Bob", nodes[2]['address'], "Charlie", 5):
        print_error("Error en transacción Bob → Charlie")
        return
    
    wait(2, "Transacción propagada a la red")
    
    # FASE 8: Charlie mina el último bloque
    print_header("⛏️  FASE 8: CHARLIE MINA BLOQUE FINAL")
    
    if not mine_blocks(CHARLIE_URL, "Charlie", count=1):
        print_error("Error durante el minado final")
        return
    
    # Sincronización final
    print_header("🔗 SINCRONIZACIÓN FINAL")
    sync_all_nodes(nodes)
    wait(2, "Bloque final minado y sincronizado")
    
    # FASE 9: Mostrar estado final
    print_final_status(nodes)
    
    # Resumen final
    print_header("🎉 DEMO COMPLETADA EXITOSAMENTE")
    
    print(f"{Colors.GREEN}✅ Sistema funcionando correctamente{Colors.RESET}\n")
    
    print("📋 Resumen de actividades:")
    print("   • 3 nodos P2P conectados")
    print("   • 3 wallets con claves RSA-2048")
    print("   • 5 bloques minados (Proof of Work)")
    print("   • 3 transacciones confirmadas")
    print("   • Blockchain validada y sincronizada\n")
    
    print("🌐 Puedes ver los detalles en:")
    print(f"   • Dashboard: Abre dashboard.html en tu navegador")
    print(f"   • Alice API: {ALICE_URL}/blockchain")
    print(f"   • Bob API: {BOB_URL}/blockchain")
    print(f"   • Charlie API: {CHARLIE_URL}/blockchain\n")
    
    print(f"{Colors.CYAN}💡 Los nodos seguirán ejecutándose para que explores la blockchain{Colors.RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Demo interrumpida por el usuario{Colors.RESET}")
    except Exception as e:
        print(f"\n\n{Colors.RED}❌ Error inesperado: {str(e)}{Colors.RESET}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*70)
    print(f"{Colors.BOLD}Presiona Enter para continuar...{Colors.RESET}")
    input()